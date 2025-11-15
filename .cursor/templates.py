"""
AI Agent代码模板库
提供标准化的代码模板，确保代码质量和一致性
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import logging
import asyncio
import json
from enum import Enum

# 配置日志
logger = logging.getLogger(__name__)

# ============================================================================
# 基础数据模型模板
# ============================================================================

@dataclass
class BaseResponse:
    """基础响应模型"""
    success: bool
    message: str = ""
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class CollectionRequest:
    """数据采集请求模型"""
    url: str
    options: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    retry_count: int = 0
    max_retries: int = 3
    
    def validate(self) -> bool:
        """验证请求参数"""
        if not self.url or not isinstance(self.url, str):
            return False
        if self.priority < 0 or self.priority > 10:
            return False
        if self.retry_count < 0 or self.retry_count > self.max_retries:
            return False
        return True

@dataclass
class CollectionResult:
    """数据采集结果模型"""
    url: str
    success: bool
    content: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    processing_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

# ============================================================================
# 服务基类模板
# ============================================================================

class BaseService:
    """服务基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化服务
        
        Args:
            config: 服务配置
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._validate_config()
        self.logger.info(f"{self.__class__.__name__} initialized")
    
    def _validate_config(self) -> None:
        """验证配置"""
        required_fields = self.get_required_config_fields()
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required config field: {field}")
    
    def get_required_config_fields(self) -> List[str]:
        """获取必需的配置字段"""
        return []
    
    async def health_check(self) -> BaseResponse:
        """健康检查"""
        try:
            # 实现健康检查逻辑
            return BaseResponse(success=True, message="Service is healthy")
        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return BaseResponse(success=False, error=str(e))

# ============================================================================
# 数据采集器模板
# ============================================================================

class BaseCollector(BaseService):
    """基础数据采集器"""
    
    def get_required_config_fields(self) -> List[str]:
        """获取必需的配置字段"""
        return ["api_key", "base_url", "timeout"]
    
    async def collect(self, request: CollectionRequest) -> CollectionResult:
        """采集数据
        
        Args:
            request: 采集请求
            
        Returns:
            CollectionResult: 采集结果
        """
        start_time = datetime.utcnow()
        
        try:
            # 验证请求
            if not request.validate():
                raise ValueError("Invalid request parameters")
            
            self.logger.info(f"Starting collection for URL: {request.url}")
            
            # 执行采集
            content, metadata = await self._execute_collection(request)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return CollectionResult(
                url=request.url,
                success=True,
                content=content,
                metadata=metadata,
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self.logger.error(f"Collection failed for {request.url}: {e}")
            
            return CollectionResult(
                url=request.url,
                success=False,
                error_message=str(e),
                processing_time=processing_time
            )
    
    async def _execute_collection(self, request: CollectionRequest) -> tuple[str, Dict[str, Any]]:
        """执行采集逻辑（子类实现）"""
        raise NotImplementedError("Subclasses must implement _execute_collection")

# ============================================================================
# 数据处理器模板
# ============================================================================

class BaseProcessor(BaseService):
    """基础数据处理器"""
    
    def get_required_config_fields(self) -> List[str]:
        """获取必需的配置字段"""
        return ["processing_options"]
    
    async def process(self, data: CollectionResult) -> BaseResponse:
        """处理数据
        
        Args:
            data: 采集结果数据
            
        Returns:
            BaseResponse: 处理结果
        """
        try:
            self.logger.info(f"Starting processing for URL: {data.url}")
            
            # 数据验证
            if not self._validate_data(data):
                raise ValueError("Invalid input data")
            
            # 执行处理
            processed_data = await self._execute_processing(data)
            
            return BaseResponse(
                success=True,
                data=processed_data,
                message="Data processed successfully"
            )
            
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return BaseResponse(success=False, error=str(e))
    
    def _validate_data(self, data: CollectionResult) -> bool:
        """验证输入数据"""
        return data.success and data.content is not None
    
    async def _execute_processing(self, data: CollectionResult) -> Dict[str, Any]:
        """执行处理逻辑（子类实现）"""
        raise NotImplementedError("Subclasses must implement _execute_processing")

# ============================================================================
# API接口模板
# ============================================================================

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

class BaseAPIServer:
    """基础API服务器"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化API服务器"""
        self.config = config
        self.app = FastAPI(
            title=config.get("title", "API Server"),
            version=config.get("version", "1.0.0"),
            description=config.get("description", "")
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_middleware()
        self._setup_routes()
    
    def _setup_middleware(self):
        """设置中间件"""
        # CORS中间件
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.get("cors_origins", ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 请求日志中间件
        @self.app.middleware("http")
        async def log_requests(request, call_next):
            start_time = datetime.utcnow()
            response = await call_next(request)
            process_time = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.3f}s")
            return response
    
    def _setup_routes(self):
        """设置路由"""
        @self.app.get("/health")
        async def health_check():
            """健康检查端点"""
            return BaseResponse(success=True, message="API is healthy")
        
        @self.app.get("/")
        async def root():
            """根端点"""
            return {
                "message": "Welcome to Firecrawl Data Collector API",
                "version": self.config.get("version", "1.0.0"),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def run(self, host: str = "0.0.0.0", port: int = 8000):
        """运行服务器"""
        self.logger.info(f"Starting API server on {host}:{port}")
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

# ============================================================================
# 数据库操作模板
# ============================================================================

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import JSONB

Base = declarative_base()

class CollectionRecord(Base):
    """采集记录模型"""
    __tablename__ = "collection_records"
    
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="pending")
    content = Column(Text, nullable=True)
    metadata = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class BaseDatabaseService:
    """基础数据库服务"""
    
    def __init__(self, database_url: str):
        """初始化数据库服务"""
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.logger = logging.getLogger(self.__class__.__name__)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()
    
    async def create_record(self, url: str, content: str, metadata: Dict[str, Any]) -> CollectionRecord:
        """创建记录"""
        with self.get_session() as session:
            record = CollectionRecord(
                url=url,
                content=content,
                metadata=metadata,
                status="completed"
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            self.logger.info(f"Created record for URL: {url}")
            return record
    
    async def get_records(self, limit: int = 100, offset: int = 0) -> List[CollectionRecord]:
        """获取记录列表"""
        with self.get_session() as session:
            records = session.query(CollectionRecord)\
                           .filter(CollectionRecord.is_active == True)\
                           .offset(offset)\
                           .limit(limit)\
                           .all()
            return records

# ============================================================================
# 任务调度器模板
# ============================================================================

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """任务模型"""
    id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None
    error: Optional[str] = None

class BaseTaskScheduler(BaseService):
    """基础任务调度器"""
    
    def __init__(self, config: Dict[str, Any]):
        """初始化任务调度器"""
        super().__init__(config)
        self.tasks: Dict[str, Task] = {}
        self.max_concurrent_tasks = config.get("max_concurrent_tasks", 5)
        self.running_tasks: Dict[str, asyncio.Task] = {}
    
    async def submit_task(self, task: Task) -> str:
        """提交任务"""
        self.tasks[task.id] = task
        self.logger.info(f"Task {task.id} submitted: {task.name}")
        
        # 如果当前运行任务数未达到上限，立即执行
        if len(self.running_tasks) < self.max_concurrent_tasks:
            await self._execute_task(task)
        
        return task.id
    
    async def _execute_task(self, task: Task):
        """执行任务"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        
        try:
            # 创建异步任务
            async_task = asyncio.create_task(self._run_task(task))
            self.running_tasks[task.id] = async_task
            
            # 等待任务完成
            result = await async_task
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            task.result = result
            
            self.logger.info(f"Task {task.id} completed successfully")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.utcnow()
            task.error = str(e)
            
            self.logger.error(f"Task {task.id} failed: {e}")
            
        finally:
            # 清理运行中的任务记录
            if task.id in self.running_tasks:
                del self.running_tasks[task.id]
    
    async def _run_task(self, task: Task) -> Any:
        """运行任务（子类实现）"""
        raise NotImplementedError("Subclasses must implement _run_task")
    
    async def get_task_status(self, task_id: str) -> Optional[Task]:
        """获取任务状态"""
        return self.tasks.get(task_id)

# ============================================================================
# 配置管理模板
# ============================================================================

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        """初始化配置管理器"""
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            self.logger.info(f"Configuration loaded from {self.config_file}")
        except FileNotFoundError:
            self.logger.warning(f"Config file {self.config_file} not found, using defaults")
            self.config = self._get_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            raise
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "firecrawl": {
                "api_key": "",
                "base_url": "https://api.firecrawl.dev",
                "timeout": 30,
                "max_retries": 3
            },
            "database": {
                "url": "sqlite:///data/firecrawl.db"
            },
            "redis": {
                "url": "redis://localhost:6379/0"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/app.log"
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Configuration saved to {self.config_file}")

# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 示例：创建配置管理器
    config_manager = ConfigManager()
    
    # 示例：创建基础服务
    config = config_manager.config
    service = BaseService(config)
    
    # 示例：运行健康检查
    async def main():
        health_result = await service.health_check()
        print(f"Health check result: {health_result.to_dict()}")
    
    asyncio.run(main())
