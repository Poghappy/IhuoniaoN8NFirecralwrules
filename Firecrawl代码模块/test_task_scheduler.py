#!/usr/bin/env python3
"""
任务调度器测试模块

使用 pytest 进行测试，覆盖任务调度器的核心功能。

运行测试:
    pytest test_task_scheduler.py -v
"""

import pytest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import shutil
from typing import Dict, Any

from 任务调度 import (
    TaskScheduler,
    Task,
    TaskType,
    TaskPriority,
    TaskStatus,
    TaskConfig,
    FileTaskStorage,
    TaskStorageError,
    TaskValidationError,
)


class TestFileTaskStorage:
    """文件任务存储测试"""

    def setup_method(self) -> None:
        """每个测试方法执行前的设置。"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = FileTaskStorage(self.temp_dir)

    def teardown_method(self) -> None:
        """每个测试方法执行后的清理。"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_task(self) -> None:
        """测试保存和加载任务。"""
        task = Task(
            id="test-1",
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        # 保存任务
        assert self.storage.save_task(task) is True

        # 加载任务
        loaded_task = self.storage.load_task("test-1")
        assert loaded_task is not None
        assert loaded_task.id == task.id
        assert loaded_task.name == task.name
        assert loaded_task.url == task.url

    def test_load_nonexistent_task(self) -> None:
        """测试加载不存在的任务。"""
        task = self.storage.load_task("nonexistent")
        assert task is None

    def test_delete_task(self) -> None:
        """测试删除任务。"""
        task = Task(
            id="test-2",
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        self.storage.save_task(task)
        assert self.storage.delete_task("test-2") is True
        assert self.storage.load_task("test-2") is None

    def test_list_tasks(self) -> None:
        """测试列出任务。"""
        # 创建多个任务
        for i in range(3):
            task = Task(
                id=f"test-{i}",
                name=f"任务 {i}",
                task_type=TaskType.SCRAPE,
                url=f"https://example.com/{i}",
            )
            self.storage.save_task(task)

        # 列出所有任务
        tasks = self.storage.list_tasks()
        assert len(tasks) == 3

        # 按状态过滤
        tasks = self.storage.list_tasks(TaskStatus.PENDING)
        assert len(tasks) == 3

    def test_save_task_handles_io_error(self) -> None:
        """测试保存任务时处理IO错误。"""
        # 使用只读目录模拟IO错误
        read_only_dir = Path(self.temp_dir) / "readonly"
        read_only_dir.mkdir()
        read_only_dir.chmod(0o444)

        storage = FileTaskStorage(str(read_only_dir))
        task = Task(
            id="test-io-error",
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        # 应该返回False而不是抛出异常
        result = storage.save_task(task)
        assert result is False


class TestTaskScheduler:
    """任务调度器测试"""

    def setup_method(self) -> None:
        """每个测试方法执行前的设置。"""
        self.temp_dir = tempfile.mkdtemp()
        storage = FileTaskStorage(self.temp_dir)
        self.scheduler = TaskScheduler(storage=storage, max_workers=2)

        # 注册测试执行器
        def mock_executor(task: Task) -> Dict[str, Any]:
            return {"status": "success", "task_id": task.id}

        self.scheduler.register_executor(TaskType.SCRAPE, mock_executor)

    def teardown_method(self) -> None:
        """每个测试方法执行后的清理。"""
        if self.scheduler._running:
            self.scheduler.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_task(self) -> None:
        """测试创建任务。"""
        task = self.scheduler.create_task(
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        assert task is not None
        assert task.name == "测试任务"
        assert task.task_type == TaskType.SCRAPE
        assert task.url == "https://example.com"
        assert task.status == TaskStatus.PENDING

    def test_add_task(self) -> None:
        """测试添加任务。"""
        task = Task(
            id="test-add",
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        result = self.scheduler.add_task(task)
        assert result is True

        # 验证任务已保存
        loaded_task = self.scheduler.get_task("test-add")
        assert loaded_task is not None
        assert loaded_task.id == task.id

    def test_cancel_task(self) -> None:
        """测试取消任务。"""
        task = self.scheduler.create_task(
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        assert task is not None
        task_id = task.id

        result = self.scheduler.cancel_task(task_id)
        assert result is True

        # 验证任务状态已更新
        status = self.scheduler.get_task_status(task_id)
        assert status == TaskStatus.CANCELLED

    def test_pause_and_resume_task(self) -> None:
        """测试暂停和恢复任务。"""
        task = self.scheduler.create_task(
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        assert task is not None
        task_id = task.id

        # 暂停任务
        assert self.scheduler.pause_task(task_id) is True
        assert self.scheduler.get_task_status(task_id) == TaskStatus.PAUSED

        # 恢复任务
        assert self.scheduler.resume_task(task_id) is True
        assert self.scheduler.get_task_status(task_id) == TaskStatus.PENDING

    def test_get_statistics(self) -> None:
        """测试获取统计信息。"""
        # 创建几个任务
        for i in range(3):
            self.scheduler.create_task(
                name=f"任务 {i}",
                task_type=TaskType.SCRAPE,
                url=f"https://example.com/{i}",
            )

        stats = self.scheduler.get_statistics()
        assert stats["total_tasks"] == 3
        assert stats["queue_size"] >= 0
        assert stats["max_workers"] == 2
        assert stats["is_running"] is False

    def test_register_executor_validation(self) -> None:
        """测试注册执行器的验证。"""
        # 测试非可调用对象
        with pytest.raises(ValueError, match="执行器必须是可调用对象"):
            # type: ignore[arg-type]
            self.scheduler.register_executor(TaskType.CRAWL, "not_callable")

    def test_start_and_stop(self) -> None:
        """测试启动和停止调度器。"""
        # 启动调度器
        self.scheduler.start()
        assert self.scheduler._running is True

        # 停止调度器
        self.scheduler.stop()
        assert self.scheduler._running is False

    def test_scheduled_task(self) -> None:
        """测试定时任务。"""
        scheduled_time = datetime.now(timezone.utc) + timedelta(seconds=5)

        task = self.scheduler.create_task(
            name="定时任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
            scheduled_time=scheduled_time,
        )

        assert task is not None
        assert task.scheduled_time == scheduled_time
        assert task.status == TaskStatus.PENDING


class TestTaskValidation:
    """任务验证测试"""

    def test_task_priority_comparison(self) -> None:
        """测试任务优先级比较。"""
        task1 = Task(
            id="task-1",
            name="高优先级任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
            priority=TaskPriority.HIGH,
        )

        task2 = Task(
            id="task-2",
            name="低优先级任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
            priority=TaskPriority.LOW,
        )

        # 高优先级应该小于低优先级（用于优先级队列）
        assert task1 < task2

    def test_task_to_dict(self) -> None:
        """测试任务序列化。"""
        task = Task(
            id="test-serialize",
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
            priority=TaskPriority.NORMAL,
        )

        task_dict = task.to_dict()
        assert task_dict["id"] == "test-serialize"
        assert task_dict["name"] == "测试任务"
        assert task_dict["task_type"] == TaskType.SCRAPE.value
        assert task_dict["priority"] == TaskPriority.NORMAL.value

    def test_task_from_dict(self) -> None:
        """测试任务反序列化。"""
        from dataclasses import asdict

        task_dict = {
            "id": "test-deserialize",
            "name": "测试任务",
            "task_type": TaskType.SCRAPE.value,
            "url": "https://example.com",
            "priority": TaskPriority.NORMAL.value,
            "status": TaskStatus.PENDING.value,
            "config": asdict(TaskConfig()),
            "metadata": {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        task = Task.from_dict(task_dict)
        assert task.id == "test-deserialize"
        assert task.name == "测试任务"
        assert task.task_type == TaskType.SCRAPE
        assert task.priority == TaskPriority.NORMAL


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
