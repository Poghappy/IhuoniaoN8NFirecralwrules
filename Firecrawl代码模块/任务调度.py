#!/usr/bin/env python3
"""
任务调度器模块

负责管理和调度Firecrawl数据采集任务，支持定时任务、优先级队列、
并发控制、任务重试、状态监控等功能。

主要功能：
- 定时任务调度
- 任务队列管理
- 并发控制
- 任务重试机制
- 状态监控和日志
- 任务持久化

作者: Trae IDE Agent
创建时间: 2025-01-17
版本: v1.0
"""

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
import json
import logging
from pathlib import Path
from queue import Empty, PriorityQueue
import threading
import time
from typing import Any, Callable, Dict, List, Optional
import uuid


# 自定义异常类
class TaskStorageError(Exception):
    """任务存储相关异常基类"""

    pass


class TaskNotFoundError(TaskStorageError):
    """任务未找到异常"""

    pass


class TaskValidationError(ValueError):
    """任务验证错误"""

    pass


# 第三方库
try:
    from croniter import croniter
except ImportError:
    croniter = None

try:
    import redis
except ImportError:
    redis = None


class TaskStatus(Enum):
    """任务状态枚举"""

    PENDING = "pending"  # 等待执行
    RUNNING = "running"  # 正在执行
    COMPLETED = "completed"  # 执行完成
    FAILED = "failed"  # 执行失败
    CANCELLED = "cancelled"  # 已取消
    RETRYING = "retrying"  # 重试中
    PAUSED = "paused"  # 已暂停


class TaskPriority(Enum):
    """任务优先级枚举"""

    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


class TaskType(Enum):
    """任务类型枚举"""

    SCRAPE = "scrape"  # 单页抓取
    CRAWL = "crawl"  # 网站爬取
    EXTRACT = "extract"  # 结构化提取
    BATCH = "batch"  # 批量处理
    SCHEDULED = "scheduled"  # 定时任务


@dataclass
class TaskConfig:
    """任务配置"""

    # 基础配置
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: int = 300

    # Firecrawl配置
    firecrawl_params: Dict[str, Any] = field(default_factory=dict)

    # 处理配置
    enable_processing: bool = True
    processing_params: Dict[str, Any] = field(default_factory=dict)

    # 输出配置
    save_results: bool = True
    output_format: str = "json"
    output_path: Optional[str] = None

    # 通知配置
    notify_on_completion: bool = False
    notify_on_failure: bool = True
    notification_webhook: Optional[str] = None


@dataclass
class Task:
    """任务对象"""

    # 基础信息
    id: str
    name: str
    task_type: TaskType
    url: str

    # 调度信息
    priority: TaskPriority = TaskPriority.NORMAL
    scheduled_time: Optional[datetime] = None
    cron_expression: Optional[str] = None

    # 状态信息
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # 执行信息
    retry_count: int = 0
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    # 配置
    config: TaskConfig = field(default_factory=TaskConfig)

    # 元数据
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: "Task") -> bool:
        """用于优先级队列排序。

        Args:
            other: 另一个任务对象

        Returns:
            bool: 如果当前任务优先级更高（值更小）或创建时间更早，返回True
        """
        if not isinstance(other, Task):
            return NotImplemented
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典。

        Returns:
            Dict[str, Any]: 任务的字典表示，枚举和日期时间已序列化
        """
        data = asdict(self)
        # 处理枚举类型
        data["task_type"] = self.task_type.value
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        # 处理日期时间
        for field_name in ["created_at", "started_at", "completed_at", "scheduled_time"]:
            if data[field_name]:
                data[field_name] = data[field_name].isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """从字典创建任务。

        Args:
            data: 包含任务数据的字典

        Returns:
            Task: 任务对象

        Raises:
            ValueError: 数据格式错误或缺少必需字段
            KeyError: 缺少必需的键
        """
        try:
            # 创建数据副本以避免修改原始数据
            task_data = data.copy()

            # 处理枚举类型
            task_data["task_type"] = TaskType(task_data["task_type"])
            task_data["priority"] = TaskPriority(task_data["priority"])
            task_data["status"] = TaskStatus(task_data["status"])

            # 处理日期时间
            for field_name in ["created_at", "started_at", "completed_at", "scheduled_time"]:
                if task_data.get(field_name):
                    task_data[field_name] = datetime.fromisoformat(task_data[field_name])

            # 处理配置对象
            if "config" in task_data and isinstance(task_data["config"], dict):
                task_data["config"] = TaskConfig(**task_data["config"])

            return cls(**task_data)
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"无法从字典创建任务: {e}") from e


class TaskStorage:
    """任务存储接口。

    定义任务存储的抽象接口，子类需要实现所有方法。
    """

    def save_task(self, task: Task) -> bool:
        """保存任务。

        Args:
            task: 要保存的任务对象

        Returns:
            bool: 保存是否成功

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError

    def load_task(self, task_id: str) -> Optional[Task]:
        """加载任务。

        Args:
            task_id: 任务ID

        Returns:
            Optional[Task]: 任务对象，如果不存在则返回None

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError

    def update_task(self, task: Task) -> bool:
        """更新任务。

        Args:
            task: 要更新的任务对象

        Returns:
            bool: 更新是否成功

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError

    def delete_task(self, task_id: str) -> bool:
        """删除任务。

        Args:
            task_id: 任务ID

        Returns:
            bool: 删除是否成功

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError

    def list_tasks(self, status: Optional[TaskStatus] = None, limit: int = 100) -> List[Task]:
        """列出任务。

        Args:
            status: 任务状态过滤，None表示不过滤
            limit: 最大返回数量

        Returns:
            List[Task]: 任务列表

        Raises:
            NotImplementedError: 子类必须实现此方法
        """
        raise NotImplementedError


class FileTaskStorage(TaskStorage):
    """文件任务存储"""

    def __init__(self, storage_dir: str = "./tasks"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save_task(self, task: Task) -> bool:
        """保存任务到文件。

        Args:
            task: 要保存的任务对象

        Returns:
            bool: 保存是否成功

        Raises:
            OSError: 文件系统操作失败
            ValueError: 任务数据无效
        """
        try:
            task_file = self.storage_dir / f"{task.id}.json"
            with open(task_file, "w", encoding="utf-8") as f:
                json.dump(task.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except (OSError, IOError) as e:
            self.logger.error("保存任务失败（文件系统错误）: %s", e)
            return False
        except (ValueError, TypeError) as e:
            self.logger.error("保存任务失败（数据序列化错误）: %s", e)
            return False

    def load_task(self, task_id: str) -> Optional[Task]:
        """从文件加载任务。

        Args:
            task_id: 任务ID

        Returns:
            Optional[Task]: 任务对象，如果不存在或加载失败则返回None

        Raises:
            OSError: 文件系统操作失败
            ValueError: JSON解析失败或数据格式错误
        """
        try:
            task_file = self.storage_dir / f"{task_id}.json"
            if not task_file.exists():
                return None

            with open(task_file, encoding="utf-8") as f:
                data = json.load(f)

            return Task.from_dict(data)
        except (OSError, IOError) as e:
            self.logger.error("加载任务失败（文件系统错误）: %s", e)
            return None
        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
            self.logger.error("加载任务失败（数据解析错误）: %s", e)
            return None

    def update_task(self, task: Task) -> bool:
        """更新任务。

        Args:
            task: 要更新的任务对象

        Returns:
            bool: 更新是否成功

        Raises:
            OSError: 文件系统操作失败
            ValueError: 任务数据无效
        """
        return self.save_task(task)

    def delete_task(self, task_id: str) -> bool:
        """删除任务文件。

        Args:
            task_id: 任务ID

        Returns:
            bool: 删除是否成功

        Raises:
            OSError: 文件系统操作失败
        """
        try:
            task_file = self.storage_dir / f"{task_id}.json"
            if task_file.exists():
                task_file.unlink()
            return True
        except OSError as e:
            self.logger.error("删除任务失败（文件系统错误）: %s", e)
            return False

    def list_tasks(self, status: Optional[TaskStatus] = None, limit: int = 100) -> List[Task]:
        """列出任务。

        Args:
            status: 任务状态过滤，None表示不过滤
            limit: 最大返回数量

        Returns:
            List[Task]: 任务列表，按创建时间倒序排列

        Raises:
            OSError: 文件系统操作失败
        """
        tasks = []
        try:
            for task_file in self.storage_dir.glob("*.json"):
                task = self.load_task(task_file.stem)
                if task and (status is None or task.status == status):
                    tasks.append(task)

                if len(tasks) >= limit:
                    break
        except OSError as e:
            self.logger.error("列出任务失败（文件系统错误）: %s", e)

        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


class RedisTaskStorage(TaskStorage):
    """Redis任务存储。

    使用Redis存储任务，支持状态索引和快速查询。
    """

    def __init__(
        self, redis_url: str = "redis://localhost:6379/0", key_prefix: str = "firecrawl:task:"
    ) -> None:
        """初始化Redis任务存储。

        Args:
            redis_url: Redis连接URL
            key_prefix: 键前缀

        Raises:
            ImportError: redis库未安装
            ConnectionError: 无法连接到Redis服务器
        """
        if not redis:
            raise ImportError("需要安装redis库")

        try:
            self.redis_client = redis.from_url(redis_url)
            # 测试连接
            self.redis_client.ping()
        except Exception as e:
            raise ConnectionError(f"无法连接到Redis服务器: {e}") from e

        self.key_prefix = key_prefix
        self.logger = logging.getLogger(__name__)

    def _get_key(self, task_id: str) -> str:
        """生成Redis键。

        Args:
            task_id: 任务ID

        Returns:
            str: Redis键
        """
        return f"{self.key_prefix}{task_id}"

    def save_task(self, task: Task) -> bool:
        """保存任务到Redis。

        Args:
            task: 要保存的任务对象

        Returns:
            bool: 保存是否成功

        Raises:
            TaskStorageError: Redis操作失败
            ValueError: 任务数据序列化失败
        """
        try:
            key = self._get_key(task.id)
            data = json.dumps(task.to_dict(), ensure_ascii=False)
            self.redis_client.set(key, data)

            # 添加到状态索引
            status_key = f"{self.key_prefix}status:{task.status.value}"
            self.redis_client.sadd(status_key, task.id)

            return True
        except (ConnectionError, TimeoutError) as e:
            self.logger.error("保存任务失败（Redis连接错误）: %s", e)
            return False
        except (ValueError, TypeError) as e:
            self.logger.error("保存任务失败（数据序列化错误）: %s", e)
            return False
        except Exception as e:
            self.logger.error("保存任务失败（未知错误）: %s", e)
            return False

    def load_task(self, task_id: str) -> Optional[Task]:
        """从Redis加载任务。

        Args:
            task_id: 任务ID

        Returns:
            Optional[Task]: 任务对象，如果不存在或加载失败则返回None

        Raises:
            TaskStorageError: Redis操作失败
            ValueError: JSON解析失败或数据格式错误
        """
        try:
            key = self._get_key(task_id)
            data = self.redis_client.get(key)

            if not data:
                return None

            if isinstance(data, bytes):
                data = data.decode("utf-8")

            task_data = json.loads(data)
            return Task.from_dict(task_data)
        except (ConnectionError, TimeoutError) as e:
            self.logger.error("加载任务失败（Redis连接错误）: %s", e)
            return None
        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
            self.logger.error("加载任务失败（数据解析错误）: %s", e)
            return None
        except Exception as e:
            self.logger.error("加载任务失败（未知错误）: %s", e)
            return None

    def update_task(self, task: Task) -> bool:
        """更新任务。

        Args:
            task: 要更新的任务对象

        Returns:
            bool: 更新是否成功

        Raises:
            TaskStorageError: Redis操作失败
            ValueError: 任务数据序列化失败
        """
        # 先删除旧的状态索引
        old_task = self.load_task(task.id)
        if old_task and old_task.status != task.status:
            old_status_key = f"{self.key_prefix}status:{old_task.status.value}"
            self.redis_client.srem(old_status_key, task.id)

        return self.save_task(task)

    def delete_task(self, task_id: str) -> bool:
        """从Redis删除任务。

        Args:
            task_id: 任务ID

        Returns:
            bool: 删除是否成功

        Raises:
            TaskStorageError: Redis操作失败
        """
        try:
            # 删除任务数据
            key = self._get_key(task_id)
            self.redis_client.delete(key)

            # 从所有状态索引中删除
            for status in TaskStatus:
                status_key = f"{self.key_prefix}status:{status.value}"
                self.redis_client.srem(status_key, task_id)

            return True
        except (ConnectionError, TimeoutError) as e:
            self.logger.error("删除任务失败（Redis连接错误）: %s", e)
            return False
        except Exception as e:
            self.logger.error("删除任务失败（未知错误）: %s", e)
            return False

    def list_tasks(self, status: Optional[TaskStatus] = None, limit: int = 100) -> List[Task]:
        """列出任务。

        Args:
            status: 任务状态过滤，None表示不过滤
            limit: 最大返回数量

        Returns:
            List[Task]: 任务列表，按创建时间倒序排列

        Raises:
            TaskStorageError: Redis操作失败
        """
        tasks = []
        try:
            if status:
                # 从状态索引获取任务ID
                status_key = f"{self.key_prefix}status:{status.value}"
                task_ids = self.redis_client.smembers(status_key)
            else:
                # 获取所有任务ID
                pattern = f"{self.key_prefix}*"
                keys = self.redis_client.keys(pattern)
                task_ids = [
                    key.decode().replace(self.key_prefix, "")
                    for key in keys
                    if ":status:" not in key.decode()
                ]

            for task_id in list(task_ids)[:limit]:
                if isinstance(task_id, bytes):
                    task_id = task_id.decode()

                task = self.load_task(task_id)
                if task:
                    tasks.append(task)
        except (ConnectionError, TimeoutError) as e:
            self.logger.error("列出任务失败（Redis连接错误）: %s", e)
        except Exception as e:
            self.logger.error("列出任务失败（未知错误）: %s", e)

        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


class TaskScheduler:
    """任务调度器"""

    def __init__(
        self,
        storage: Optional[TaskStorage] = None,
        max_workers: int = 5,
        check_interval: float = 1.0,
    ):
        """初始化任务调度器

        Args:
            storage: 任务存储后端
            max_workers: 最大工作线程数
            check_interval: 检查间隔（秒）
        """
        self.storage = storage or FileTaskStorage()
        self.max_workers = max_workers
        self.check_interval = check_interval

        self.logger = logging.getLogger(__name__)

        # 任务队列
        self.task_queue = PriorityQueue()
        self.running_tasks: Dict[str, Future] = {}

        # 线程池
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        # 控制标志
        self._running = False
        self._scheduler_thread: Optional[threading.Thread] = None

        # 任务执行器映射
        self.task_executors: Dict[TaskType, Callable] = {}

        # 统计信息
        self.stats = {"total_tasks": 0, "completed_tasks": 0, "failed_tasks": 0, "running_tasks": 0}

    def register_executor(
        self, task_type: TaskType, executor: Callable[[Task], Dict[str, Any]]
    ) -> None:
        """注册任务执行器。

        Args:
            task_type: 任务类型
            executor: 执行器函数，接受Task对象，返回执行结果字典

        Raises:
            ValueError: 执行器函数签名不正确
        """
        if not callable(executor):
            raise ValueError(f"执行器必须是可调用对象，当前类型: {type(executor)}")
        self.task_executors[task_type] = executor
        self.logger.info("注册任务执行器: %s", task_type.value)

    def add_task(self, task: Task) -> bool:
        """添加任务

        Args:
            task: 任务对象

        Returns:
            bool: 是否添加成功
        """
        try:
            # 保存任务到存储
            if not self.storage.save_task(task):
                return False

            # 添加到队列
            if task.scheduled_time and task.scheduled_time > datetime.now(timezone.utc):
                # 定时任务，暂不加入队列
                self.logger.info("定时任务已添加: %s, 执行时间: %s", task.id, task.scheduled_time)
            else:
                # 立即执行的任务
                self.task_queue.put(task)
                self.logger.info("任务已添加到队列: %s", task.id)

            self.stats["total_tasks"] += 1
            return True

        except (TaskStorageError, ValueError) as e:
            self.logger.error("添加任务失败（存储或验证错误）: %s", e)
            return False
        except Exception as e:
            self.logger.error("添加任务失败（未知错误）: %s", e)
            return False

    def create_task(
        self,
        name: str,
        task_type: TaskType,
        url: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        scheduled_time: Optional[datetime] = None,
        cron_expression: Optional[str] = None,
        config: Optional[TaskConfig] = None,
        **metadata,
    ) -> Optional[Task]:
        """创建任务

        Args:
            name: 任务名称
            task_type: 任务类型
            url: 目标URL
            priority: 优先级
            scheduled_time: 计划执行时间
            cron_expression: Cron表达式
            config: 任务配置
            **metadata: 元数据

        Returns:
            Optional[Task]: 创建的任务对象
        """
        try:
            task = Task(
                id=str(uuid.uuid4()),
                name=name,
                task_type=task_type,
                url=url,
                priority=priority,
                scheduled_time=scheduled_time,
                cron_expression=cron_expression,
                config=config or TaskConfig(),
                metadata=metadata,
            )

            if self.add_task(task):
                return task
            return None

        except (TaskValidationError, ValueError) as e:
            self.logger.error("创建任务失败（验证错误）: %s", e)
            return None
        except Exception as e:
            self.logger.error("创建任务失败（未知错误）: %s", e)
            return None

    def cancel_task(self, task_id: str) -> bool:
        """取消任务

        Args:
            task_id: 任务ID

        Returns:
            bool: 是否取消成功
        """
        try:
            # 如果任务正在运行，取消执行
            if task_id in self.running_tasks:
                future = self.running_tasks[task_id]
                future.cancel()
                del self.running_tasks[task_id]

            # 更新任务状态
            task = self.storage.load_task(task_id)
            if task:
                task.status = TaskStatus.CANCELLED
                task.completed_at = datetime.now(timezone.utc)
                self.storage.update_task(task)

                self.logger.info("任务已取消: %s", task_id)
                return True

            return False

        except (TaskStorageError, TaskNotFoundError) as e:
            self.logger.error("取消任务失败（存储错误）: %s", e)
            return False
        except Exception as e:
            self.logger.error("取消任务失败（未知错误）: %s", e)
            return False

    def pause_task(self, task_id: str) -> bool:
        """暂停任务

        Args:
            task_id: 任务ID

        Returns:
            bool: 是否暂停成功
        """
        try:
            task = self.storage.load_task(task_id)
            if task and task.status == TaskStatus.PENDING:
                task.status = TaskStatus.PAUSED
                self.storage.update_task(task)

                self.logger.info("任务已暂停: %s", task_id)
                return True

            return False

        except (TaskStorageError, TaskNotFoundError) as e:
            self.logger.error("暂停任务失败（存储错误）: %s", e)
            return False
        except Exception as e:
            self.logger.error("暂停任务失败（未知错误）: %s", e)
            return False

    def resume_task(self, task_id: str) -> bool:
        """恢复任务

        Args:
            task_id: 任务ID

        Returns:
            bool: 是否恢复成功
        """
        try:
            task = self.storage.load_task(task_id)
            if task and task.status == TaskStatus.PAUSED:
                task.status = TaskStatus.PENDING
                self.storage.update_task(task)
                self.task_queue.put(task)

                self.logger.info("任务已恢复: %s", task_id)
                return True

            return False

        except (TaskStorageError, TaskNotFoundError) as e:
            self.logger.error("恢复任务失败（存储错误）: %s", e)
            return False
        except Exception as e:
            self.logger.error("恢复任务失败（未知错误）: %s", e)
            return False

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """获取任务状态

        Args:
            task_id: 任务ID

        Returns:
            Optional[TaskStatus]: 任务状态
        """
        task = self.storage.load_task(task_id)
        return task.status if task else None

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务详情

        Args:
            task_id: 任务ID

        Returns:
            Optional[Task]: 任务对象
        """
        return self.storage.load_task(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None, limit: int = 100) -> List[Task]:
        """列出任务

        Args:
            status: 过滤状态
            limit: 限制数量

        Returns:
            List[Task]: 任务列表
        """
        return self.storage.list_tasks(status, limit)

    def start(self) -> None:
        """启动调度器。

        Raises:
            RuntimeError: 如果调度器已经在运行
        """
        if self._running:
            self.logger.warning("调度器已在运行")
            return

        self._running = True
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self._scheduler_thread.start()

        self.logger.info("任务调度器已启动")

    def stop(self) -> None:
        """停止调度器。"""
        if not self._running:
            return

        self._running = False

        # 等待调度线程结束
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)

        # 取消所有运行中的任务
        for task_id, future in self.running_tasks.items():
            future.cancel()

        # 关闭线程池
        self.executor.shutdown(wait=True)

        self.logger.info("任务调度器已停止")

    def _scheduler_loop(self) -> None:
        """调度器主循环。

        持续检查定时任务、处理队列、监控运行中的任务。
        捕获所有异常以确保循环不会中断。
        """
        while self._running:
            try:
                # 检查定时任务
                self._check_scheduled_tasks()

                # 处理队列中的任务
                self._process_task_queue()

                # 检查运行中的任务
                self._check_running_tasks()

                # 清理完成的任务
                self._cleanup_completed_tasks()

                time.sleep(self.check_interval)

            except (TaskStorageError, ValueError) as e:
                self.logger.error("调度器循环错误（存储或验证错误）: %s", e)
                time.sleep(self.check_interval)
            except Exception as e:
                self.logger.error("调度器循环错误（未知错误）: %s", e)
                time.sleep(self.check_interval)

    def _check_scheduled_tasks(self) -> None:
        """检查定时任务。

        检查所有待执行的定时任务，如果执行时间已到或Cron表达式匹配，则加入执行队列。
        """
        try:
            # 获取所有待执行的定时任务
            pending_tasks = self.storage.list_tasks(TaskStatus.PENDING)
            current_time = datetime.now(timezone.utc)

            for task in pending_tasks:
                if task.scheduled_time and task.scheduled_time <= current_time:
                    # 时间到了，添加到执行队列
                    self.task_queue.put(task)
                    self.logger.info("定时任务已加入执行队列: %s", task.id)

                elif task.cron_expression and croniter:
                    # 检查Cron表达式
                    try:
                        cron = croniter(task.cron_expression, current_time)
                        # cron.get_next() 默认返回 float (timestamp)
                        # 使用 ret_type=datetime 参数返回 datetime 对象
                        next_run_timestamp = cron.get_next()
                        next_run = datetime.fromtimestamp(next_run_timestamp, tz=timezone.utc)

                        # 如果下次执行时间在1分钟内，添加到队列
                        if next_run <= current_time + timedelta(minutes=1):
                            # 创建新的任务实例（保持原任务为模板）
                            new_task = Task(
                                id=str(uuid.uuid4()),
                                name=f"{task.name} (定时执行)",
                                task_type=task.task_type,
                                url=task.url,
                                priority=task.priority,
                                config=task.config,
                                metadata=task.metadata.copy(),
                            )

                            self.task_queue.put(new_task)
                            self.storage.save_task(new_task)

                            self.logger.info("Cron任务已创建并加入队列: %s", new_task.id)

                    except (ValueError, TypeError) as e:
                        self.logger.error(
                            "Cron表达式解析失败（格式错误）: %s, %s", task.cron_expression, e
                        )
                    except Exception as e:
                        self.logger.error(
                            "Cron表达式解析失败（未知错误）: %s, %s", task.cron_expression, e
                        )

        except TaskStorageError as e:
            self.logger.error("检查定时任务失败（存储错误）: %s", e)
        except Exception as e:
            self.logger.error("检查定时任务失败（未知错误）: %s", e)

    def _process_task_queue(self) -> None:
        """处理任务队列。

        从队列中取出任务并提交到线程池执行。
        """
        try:
            # 检查是否有可用的工作线程
            if len(self.running_tasks) >= self.max_workers:
                return

            # 从队列中获取任务
            try:
                task = self.task_queue.get_nowait()
            except Empty:
                return

            # 检查任务是否已被取消或暂停
            current_task = self.storage.load_task(task.id)
            if not current_task or current_task.status in [TaskStatus.CANCELLED, TaskStatus.PAUSED]:
                return

            # 提交任务执行
            future = self.executor.submit(self._execute_task, task)
            self.running_tasks[task.id] = future

            # 更新任务状态
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now(timezone.utc)
            self.storage.update_task(task)

            self.stats["running_tasks"] += 1
            self.logger.info("任务开始执行: %s", task.id)

        except TaskStorageError as e:
            self.logger.error("处理任务队列失败（存储错误）: %s", e)
        except Exception as e:
            self.logger.error("处理任务队列失败（未知错误）: %s", e)

    def _check_running_tasks(self) -> None:
        """检查运行中的任务。

        检查所有正在执行的任务，处理已完成的任务。
        """
        try:
            completed_tasks = []

            for task_id, future in self.running_tasks.items():
                if future.done():
                    completed_tasks.append(task_id)

                    try:
                        result = future.result()
                        self._handle_task_completion(task_id, result, None)
                    except ValueError as e:
                        self._handle_task_completion(task_id, None, f"验证错误: {e}")
                    except Exception as e:
                        self._handle_task_completion(task_id, None, f"执行错误: {e}")

            # 清理已完成的任务
            for task_id in completed_tasks:
                del self.running_tasks[task_id]
                self.stats["running_tasks"] -= 1

        except Exception as e:
            self.logger.error("检查运行任务失败: %s", e)

    def _cleanup_completed_tasks(self) -> None:
        """清理完成的任务。

        清理过期的已完成任务（当前为空实现，可根据需要扩展）。
        """
        try:
            # 这里可以实现任务清理逻辑，比如删除过期的已完成任务
            pass
        except Exception as e:
            self.logger.error("清理任务失败: %s", e)

    def _execute_task(self, task: Task) -> Dict[str, Any]:
        """执行任务。

        Args:
            task: 任务对象

        Returns:
            Dict[str, Any]: 执行结果

        Raises:
            ValueError: 未找到对应的任务执行器
            RuntimeError: 任务执行失败
        """
        # 获取任务执行器
        executor = self.task_executors.get(task.task_type)
        if not executor:
            raise ValueError(f"未找到任务类型 {task.task_type.value} 的执行器")

        # 执行任务
        try:
            return executor(task)
        except Exception as e:
            # 将执行器抛出的异常包装为 RuntimeError
            raise RuntimeError(f"任务执行失败: {e}") from e

    def _handle_task_completion(
        self, task_id: str, result: Optional[Dict[str, Any]], error: Optional[str]
    ) -> None:
        """处理任务完成。

        Args:
            task_id: 任务ID
            result: 执行结果，成功时提供
            error: 错误信息，失败时提供

        Raises:
            TaskStorageError: 存储操作失败
        """
        try:
            task = self.storage.load_task(task_id)
            if not task:
                return

            task.completed_at = datetime.now(timezone.utc)

            if error:
                # 任务失败
                task.error_message = error

                # 检查是否需要重试
                if task.retry_count < task.config.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.RETRYING

                    # 延迟后重新加入队列
                    retry_delay = task.config.retry_delay * (
                        2 ** (task.retry_count - 1)
                    )  # 指数退避

                    def retry_task() -> None:
                        time.sleep(retry_delay)
                        task.status = TaskStatus.PENDING
                        self.storage.update_task(task)
                        self.task_queue.put(task)

                    threading.Thread(target=retry_task, daemon=True).start()

                    self.logger.info(
                        "任务将在 %s 秒后重试: %s (第 %s 次重试)",
                        retry_delay,
                        task_id,
                        task.retry_count,
                    )
                else:
                    # 重试次数用完，标记为失败
                    task.status = TaskStatus.FAILED
                    self.stats["failed_tasks"] += 1
                    self.logger.error("任务执行失败: %s, 错误: %s", task_id, error)
            else:
                # 任务成功
                task.status = TaskStatus.COMPLETED
                task.result = result
                self.stats["completed_tasks"] += 1
                self.logger.info("任务执行成功: %s", task_id)

            # 更新任务状态
            self.storage.update_task(task)

        except TaskStorageError as e:
            self.logger.error("处理任务完成失败（存储错误）: %s", e)
        except Exception as e:
            self.logger.error("处理任务完成失败（未知错误）: %s", e)

    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息

        Returns:
            Dict[str, Any]: 统计信息
        """
        stats = self.stats.copy()
        stats.update(
            {
                "queue_size": self.task_queue.qsize(),
                "max_workers": self.max_workers,
                "is_running": self._running,
            }
        )
        return stats


# 使用示例
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 创建调度器
    scheduler = TaskScheduler(max_workers=3)

    # 模拟任务执行器
    def mock_scrape_executor(task: Task) -> Dict[str, Any]:
        """模拟抓取执行器"""
        time.sleep(2)  # 模拟执行时间
        return {
            "url": task.url,
            "title": f"页面标题 - {task.name}",
            "content": "页面内容...",
            "timestamp": datetime.now().isoformat(),
        }

    def mock_crawl_executor(task: Task) -> Dict[str, Any]:
        """模拟爬取执行器"""
        time.sleep(5)  # 模拟执行时间
        return {
            "url": task.url,
            "pages": [
                {"title": "页面1", "url": f"{task.url}/page1"},
                {"title": "页面2", "url": f"{task.url}/page2"},
            ],
            "timestamp": datetime.now().isoformat(),
        }

    # 注册执行器
    scheduler.register_executor(TaskType.SCRAPE, mock_scrape_executor)
    scheduler.register_executor(TaskType.CRAWL, mock_crawl_executor)

    # 启动调度器
    scheduler.start()

    try:
        # 创建测试任务
        task1 = scheduler.create_task(
            name="抓取Firecrawl博客",
            task_type=TaskType.SCRAPE,
            url="https://firecrawl.dev/blog",
            priority=TaskPriority.HIGH,
        )

        task2 = scheduler.create_task(
            name="爬取Firecrawl文档",
            task_type=TaskType.CRAWL,
            url="https://docs.firecrawl.dev",
            priority=TaskPriority.NORMAL,
        )

        # 创建定时任务
        scheduled_time = datetime.now(timezone.utc) + timedelta(seconds=10)
        task3 = scheduler.create_task(
            name="定时抓取任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
            scheduled_time=scheduled_time,
        )

        print("创建了 3 个任务")
        print(f"任务1 ID: {task1.id if task1 else 'None'}")
        print(f"任务2 ID: {task2.id if task2 else 'None'}")
        print(f"任务3 ID: {task3.id if task3 else 'None'} (定时任务)")

        # 等待任务执行
        time.sleep(15)

        # 打印统计信息
        stats = scheduler.get_statistics()
        print("\n调度器统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        # 列出所有任务
        all_tasks = scheduler.list_tasks()
        print(f"\n总任务数: {len(all_tasks)}")
        for task in all_tasks:
            print(f"  {task.name}: {task.status.value}")

    finally:
        # 停止调度器
        scheduler.stop()
        print("\n调度器已停止")
