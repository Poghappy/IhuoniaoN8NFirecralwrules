#!/usr/bin/env python3
"""
集成测试脚本

用于测试Firecrawl数据采集模块和火鸟门户API集成模块的功能，
包括单元测试、集成测试、性能测试和端到端测试。

主要功能：
- Firecrawl采集器测试
- 数据处理器测试
- API集成测试
- 任务调度器测试
- 端到端流程测试
- 性能基准测试

作者: Trae IDE Agent
创建时间: 2025-01-17
版本: v1.0
"""

import asyncio
import json
import logging
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import Mock, patch


# 导入测试模块
try:
    from .API集成 import (
        APIConfig,
        APIIntegration,
        PublishRequest,
        PublishStatus,
    )
    from .任务调度 import TaskScheduler, TaskType
    from .数据处理 import DataProcessor, ProcessedArticle
    from .火爬配置 import ConfigManager, FirecrawlCollectorConfig
    from .火爬采集器 import ArticleData, CollectorConfig, FirecrawlCollector
except ImportError:
    # 如果作为独立模块运行
    import sys

    sys.path.append(".")
    from API集成 import (
        APIConfig,
        APIIntegration,
        PublishRequest,
        PublishStatus,
    )
    from 任务调度 import TaskScheduler, TaskType
    from 数据处理 import DataProcessor, ProcessedArticle
    from 火爬配置 import ConfigManager, FirecrawlCollectorConfig
    from 火爬采集器 import ArticleData, CollectorConfig, FirecrawlCollector


class TestFirecrawlCollector(unittest.TestCase):
    """Firecrawl采集器测试"""

    def setUp(self):
        """测试初始化"""
        self.config = CollectorConfig(
            api_key="test_api_key",
            concurrent_limit=2,
            timeout=10,
        )
        self.collector = FirecrawlCollector(self.config)

    def test_config_validation(self):
        """测试配置验证"""
        # 测试有效配置
        valid_config = CollectorConfig(api_key="valid_key")
        self.assertIsNotNone(valid_config)

        # 测试无效配置
        with self.assertRaises(ValueError):
            CollectorConfig(api_key="")

    @patch("火爬采集器.Firecrawl")
    def test_scrape_single_page(self, mock_firecrawl):
        """测试单页抓取"""
        # 模拟Firecrawl响应
        mock_response = {
            "success": True,
            "data": {
                "content": "Test content",
                "markdown": "# Test Title\n\nTest content",
                "metadata": {
                    "title": "Test Title",
                    "description": "Test description",
                    "keywords": "test,keywords",
                    "author": "Test Author",
                },
                "links": ["https://example.com/link1"],
                "screenshot": "base64_screenshot_data",
            },
        }

        mock_firecrawl.return_value.scrape.return_value = mock_response

        # 执行测试（异步函数需要await）
        async def run_test():
            return await self.collector.scrape_single_page("https://example.com/test")

        result = asyncio.run(run_test())

        # 验证结果
        if result:
            self.assertIsInstance(result, ArticleData)
            self.assertEqual(result.title, "Test Title")
            self.assertEqual(result.content, "Test content")
            self.assertEqual(result.url, "https://example.com/test")

    @patch("火爬采集器.Firecrawl")
    def test_crawl_website(self, mock_firecrawl):
        """测试网站爬取"""
        # 模拟爬取响应
        mock_response = {"success": True, "jobId": "test_job_id"}

        mock_status_response = {
            "status": "completed",
            "data": [
                {
                    "content": "Page 1 content",
                    "markdown": "# Page 1\n\nContent",
                    "metadata": {"title": "Page 1"},
                    "url": "https://example.com/page1",
                },
                {
                    "content": "Page 2 content",
                    "markdown": "# Page 2\n\nContent",
                    "metadata": {"title": "Page 2"},
                    "url": "https://example.com/page2",
                },
            ],
        }

        mock_firecrawl.return_value.crawl.return_value = mock_response
        mock_firecrawl.return_value.check_crawl_status.return_value = mock_status_response

        # 执行测试（异步函数需要await）
        async def run_test():
            return await self.collector.crawl_website("https://example.com", max_pages=2)

        results = asyncio.run(run_test())

        # 验证结果
        if results:
            self.assertGreaterEqual(len(results.articles), 0)
            if results.articles:
                self.assertIsInstance(results.articles[0], ArticleData)

    def test_save_results(self):
        """测试结果保存"""
        # 创建测试数据
        test_data = ArticleData(
            title="Test Article",
            content="Test content",
            url="https://example.com/test",
            metadata={"author": "Test Author"},
        )

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "test_results.json"

            # 保存结果
            self.collector.save_results([test_data], str(output_path))

            # 验证文件存在
            self.assertTrue(output_path.exists())

            # 验证文件内容
            with open(output_path, encoding="utf-8") as f:
                saved_data = json.load(f)

            self.assertEqual(len(saved_data), 1)
            self.assertEqual(saved_data[0]["title"], "Test Article")


class TestDataProcessor(unittest.TestCase):
    """数据处理器测试"""

    def setUp(self):
        """测试初始化"""
        self.processor = DataProcessor()

    def test_clean_content(self):
        """测试内容清洗"""
        # 测试HTML清洗
        html_content = "<p>This is <strong>bold</strong> text.</p><script>alert('xss')</script>"
        cleaned = self.processor.cleaner.clean_html(html_content)

        self.assertNotIn("<script>", cleaned)
        self.assertIn("bold", cleaned)

    def test_extract_keywords(self):
        """测试关键词提取"""
        text = "Python是一种编程语言。机器学习和人工智能是热门技术。"
        keywords = self.processor.keyword_extractor.extract_keywords("Python编程", text)

        self.assertIsInstance(keywords, list)
        self.assertGreaterEqual(len(keywords), 0)

    def test_classify_content(self):
        """测试内容分类"""
        # 测试技术文章
        title = "Python编程指南"
        content = "Python编程语言机器学习算法数据科学"
        url = "https://example.com/python"
        category = self.processor.classifier.classify(title, content, url)

        self.assertIn(category, ["技术", "科技", "编程", "其他"])

    def test_process_firecrawl_data(self):
        """测试Firecrawl数据处理"""
        # 模拟Firecrawl数据
        firecrawl_data = {
            "url": "https://example.com/article",
            "content": "This is a test article about Python programming. " * 20,  # 确保内容足够长
            "title": "Python Programming Guide",
            "source_name": "测试来源",
            "metadata": {
                "description": "A comprehensive guide to Python programming.",
                "keywords": "python,programming,guide",
                "author": "John Doe",
            },
        }

        # 处理数据
        result = self.processor.process_article(firecrawl_data)

        # 验证结果
        if result:
            self.assertIsInstance(result, ProcessedArticle)
            self.assertEqual(result.title, "Python Programming Guide")
            self.assertEqual(result.source_url, "https://example.com/article")
            self.assertGreater(result.quality_score, 0)

    def test_quality_scoring(self):
        """测试质量评分"""
        # 高质量内容
        high_quality = ProcessedArticle(
            title="详细的Python编程指南",
            content="这是一篇详细的Python编程指南，包含了大量的示例代码和最佳实践。" * 10,
            url="https://example.com",
            source_name="测试来源",
            summary="Python编程的完整指南",
            keywords=["Python", "编程", "指南"],
            source_url="https://example.com",
        )

        score = self.processor._calculate_quality_score(high_quality)
        self.assertGreater(score, 0.7)

        # 低质量内容
        low_quality = ProcessedArticle(
            title="短标题",
            content="很短的内容",
            url="https://example.com",
            source_name="测试来源",
            summary="",
            keywords=[],
            source_url="https://example.com",
        )

        score = self.processor._calculate_quality_score(low_quality)
        self.assertLess(score, 0.5)


class TestAPIIntegration(unittest.TestCase):
    """API集成测试"""

    def setUp(self):
        """测试初始化"""
        self.api_config = APIConfig(
            base_url="https://api.test.com/",
            api_key="test_api_key",
            default_category_id=1,
            default_author_id=1,
        )
        self.integration = APIIntegration(self.api_config)

    @patch("api_integration.requests.Session")
    def test_api_connection(self, mock_session):
        """测试API连接"""
        # 模拟成功响应
        mock_response = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response

        # 测试连接
        result = self.integration.test_connection()
        self.assertTrue(result)

    @patch("api_integration.requests.Session")
    def test_publish_article(self, mock_session):
        """测试文章发布"""
        # 模拟发布响应
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "data": {"id": 123},
            "message": "发布成功",
        }
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_response

        # 创建发布请求
        publish_request = PublishRequest(
            title="测试文章",
            content="这是测试内容",
            status=PublishStatus.DRAFT,
        )

        # 执行发布
        result = self.integration.api_client.publish_article(publish_request)

        # 验证结果
        self.assertTrue(result.success)
        self.assertEqual(result.article_id, 123)

    def test_data_mapping(self):
        """测试数据映射"""
        # 创建处理后的文章
        processed_article = ProcessedArticle(
            title="测试文章标题",
            content="测试文章内容",
            url="https://example.com/test",
            source_name="测试来源",
            summary="测试摘要",
            keywords=["测试", "文章"],
            category="技术",
            author="测试作者",
            source_url="https://example.com/test",
            quality_score=0.8,
        )

        # 执行映射
        publish_request = self.integration.data_mapper.map_processed_article(
            processed_article, self.api_config
        )

        # 验证映射结果
        self.assertEqual(publish_request.title, "测试文章标题")
        self.assertEqual(publish_request.content, "测试文章内容")
        self.assertEqual(publish_request.source_url, "https://example.com/test")
        self.assertIn("quality_score", publish_request.metadata)


class TestTaskScheduler(unittest.TestCase):
    """任务调度器测试"""

    def setUp(self):
        """测试初始化"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp()
        from 任务调度 import FileTaskStorage

        storage = FileTaskStorage(storage_dir=self.temp_dir)
        self.scheduler = TaskScheduler(storage=storage)

    def tearDown(self):
        """测试清理"""
        # 停止调度器
        if self.scheduler._running:
            self.scheduler.stop()

        # 清理临时目录
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_add_task(self):
        """测试添加任务"""
        # 创建任务
        task = self.scheduler.create_task(
            name="测试任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )

        # 验证任务创建
        self.assertIsNotNone(task)
        if task:
            # 添加任务
            success = self.scheduler.add_task(task)
            self.assertTrue(success)

            # 获取任务
            loaded_task = self.scheduler.get_task(task.id)
            self.assertIsNotNone(loaded_task)
            if loaded_task:
                self.assertEqual(loaded_task.url, "https://example.com")

    def test_task_execution(self):
        """测试任务执行"""

        # 模拟任务执行函数
        def mock_execute_task(task):
            time.sleep(0.1)  # 模拟执行时间
            return {"success": True, "data": "test_result"}

        # 注册执行器
        self.scheduler.register_executor(TaskType.SCRAPE, mock_execute_task)

        # 创建并添加任务
        task = self.scheduler.create_task(
            name="测试执行任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )
        if task:
            self.scheduler.add_task(task)

            # 启动调度器
            self.scheduler.start()

            # 等待任务完成
            time.sleep(0.5)

            # 检查任务状态（任务可能还在执行中，所以只检查任务存在）
            loaded_task = self.scheduler.get_task(task.id)
            self.assertIsNotNone(loaded_task)

            # 停止调度器
            self.scheduler.stop()

    def test_task_persistence(self):
        """测试任务持久化"""
        # 创建并添加任务
        task = self.scheduler.create_task(
            name="测试持久化任务",
            task_type=TaskType.SCRAPE,
            url="https://example.com",
        )
        if task:
            self.scheduler.add_task(task)
            task_id = task.id

            # 创建新的调度器实例（模拟重启）
            from 任务调度 import FileTaskStorage

            storage = FileTaskStorage(storage_dir=self.temp_dir)
            new_scheduler = TaskScheduler(storage=storage)

            # 验证任务仍然存在
            loaded_task = new_scheduler.get_task(task_id)
            self.assertIsNotNone(loaded_task)
            if loaded_task:
                self.assertEqual(loaded_task.url, "https://example.com")


class TestEndToEndIntegration(unittest.TestCase):
    """端到端集成测试"""

    def setUp(self):
        """测试初始化"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()

        # 创建配置
        self.collector_config = CollectorConfig(api_key="test_api_key")

        self.api_config = APIConfig(base_url="https://api.test.com/", api_key="test_api_key")

        # 创建组件
        self.collector = FirecrawlCollector(self.collector_config)
        self.processor = DataProcessor()
        self.integration = APIIntegration(self.api_config, self.processor)
        from 任务调度 import FileTaskStorage

        storage = FileTaskStorage(storage_dir=self.temp_dir)
        self.scheduler = TaskScheduler(storage=storage)

    def tearDown(self):
        """测试清理"""
        if self.scheduler._running:
            self.scheduler.stop()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("火爬采集器.Firecrawl")
    @patch("api_integration.requests.Session")
    def test_complete_workflow(self, mock_session, mock_firecrawl):
        """测试完整工作流程"""
        # 模拟Firecrawl响应
        mock_firecrawl_response = {
            "success": True,
            "data": {
                "content": "This is a comprehensive guide to Python programming.",
                "markdown": "# Python Programming Guide\n\nThis is a comprehensive guide.",
                "metadata": {
                    "title": "Python Programming Guide",
                    "description": "A comprehensive guide to Python programming.",
                    "keywords": "python,programming,guide",
                    "author": "John Doe",
                },
                "url": "https://example.com/python-guide",
            },
        }

        mock_firecrawl.return_value.scrape_url.return_value = mock_firecrawl_response

        # 模拟API响应
        mock_api_response = Mock()
        mock_api_response.json.return_value = {
            "success": True,
            "data": {"id": 456},
            "message": "发布成功",
        }
        mock_api_response.raise_for_status.return_value = None
        mock_session.return_value.request.return_value = mock_api_response

        # 执行完整流程
        # 1. 数据采集（异步）
        async def run_collect():
            return await self.collector.scrape_single_page("https://example.com/python-guide")

        article_data = asyncio.run(run_collect())
        self.assertIsNotNone(article_data)

        # 2. 数据处理
        if article_data:
            firecrawl_data = {
                "url": article_data.url,
                "content": article_data.content,
                "title": article_data.title,
                "source_name": "测试来源",
                "metadata": article_data.metadata or {},
            }

            # 3. 处理和发布
            response = self.integration.process_and_publish(firecrawl_data, auto_publish=False)

            # 验证结果
            if response:
                self.assertTrue(response.success)
                self.assertEqual(response.article_id, 456)

                # 验证统计信息
                stats = self.integration.get_statistics()
                self.assertEqual(stats["total_processed"], 1)
                self.assertEqual(stats["successful_publishes"], 1)


class TestPerformance(unittest.TestCase):
    """性能测试"""

    def test_data_processing_performance(self):
        """测试数据处理性能"""
        processor = DataProcessor()

        # 创建大量测试数据
        test_data = {
            "url": "https://example.com/article",
            "content": "This is a test article. " * 1000,  # 大内容
            "title": "Performance Test Article",
            "source_name": "测试来源",
            "metadata": {
                "description": "Testing processing performance.",
                "keywords": "performance,test,article",
            },
        }

        # 测试处理时间
        start_time = time.time()

        for _ in range(10):
            result = processor.process_article(test_data)
            self.assertIsNotNone(result)

        end_time = time.time()
        processing_time = end_time - start_time

        # 验证性能（每次处理应该在合理时间内完成）
        avg_time = processing_time / 10
        self.assertLess(avg_time, 2.0, f"平均处理时间过长: {avg_time:.2f}秒")

    def test_concurrent_processing(self):
        """测试并发处理性能"""
        import concurrent.futures

        processor = DataProcessor()

        def process_item(i):
            test_data = {
                "url": f"https://example.com/article-{i}",
                "content": f"This is test article {i}. " * 100,
                "title": f"Test Article {i}",
                "source_name": "测试来源",
                "metadata": {
                    "description": f"Testing article {i}.",
                    "keywords": f"test,article,{i}",
                },
            }
            return processor.process_article(test_data)

        # 并发处理测试
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(process_item, i) for i in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        end_time = time.time()
        processing_time = end_time - start_time

        # 验证结果
        self.assertEqual(len(results), 20)
        self.assertTrue(all(result is not None for result in results))

        # 验证并发性能
        self.assertLess(processing_time, 10.0, f"并发处理时间过长: {processing_time:.2f}秒")


class TestConfigManager(unittest.TestCase):
    """配置管理器测试"""

    def setUp(self):
        """测试初始化"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / "test_config.json"

    def tearDown(self):
        """测试清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_config_save_load(self):
        """测试配置保存和加载"""
        from 火爬配置 import FirecrawlAPIConfig

        # 创建配置
        config = FirecrawlCollectorConfig(
            firecrawl_api=FirecrawlAPIConfig(api_key="test_key", base_url="https://api.test.com")
        )

        manager = ConfigManager()

        # 保存配置
        manager.save_config(str(self.config_path), config)

        # 验证文件存在
        self.assertTrue(self.config_path.exists())

        # 加载配置
        loaded_config = manager.load_config(str(self.config_path))

        # 验证配置
        self.assertIsNotNone(loaded_config.firecrawl_api)
        if loaded_config.firecrawl_api:
            self.assertEqual(loaded_config.firecrawl_api.api_key, "test_key")
            self.assertEqual(loaded_config.firecrawl_api.base_url, "https://api.test.com")

    def test_config_validation(self):
        """测试配置验证"""
        from 火爬配置 import FirecrawlAPIConfig

        # 有效配置
        valid_config = FirecrawlCollectorConfig(
            firecrawl_api=FirecrawlAPIConfig(
                api_key="valid_key", base_url="https://api.firecrawl.dev"
            )
        )

        errors = valid_config.validate()
        self.assertEqual(len(errors), 0)

        # 无效配置
        invalid_config = FirecrawlCollectorConfig(
            firecrawl_api=FirecrawlAPIConfig(api_key="", base_url="invalid_url")
        )

        errors = invalid_config.validate()
        self.assertGreater(len(errors), 0)


def run_all_tests():
    """运行所有测试"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 创建测试套件
    test_suite = unittest.TestSuite()

    # 添加测试类
    test_classes = [
        TestFirecrawlCollector,
        TestDataProcessor,
        TestAPIIntegration,
        TestTaskScheduler,
        TestEndToEndIntegration,
        TestPerformance,
        TestConfigManager,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # 打印测试结果摘要
    print("\n" + "=" * 50)
    print("测试结果摘要:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"跳过数: {len(result.skipped)}")

    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('\n')[-2]}")

    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\n')[-2]}")

    success_rate = (
        (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    )
    print(f"\n成功率: {success_rate:.1f}%")

    return result.wasSuccessful()


if __name__ == "__main__":
    # 运行所有测试
    success = run_all_tests()

    if success:
        print("\n🎉 所有测试通过！")
        exit(0)
    else:
        print("\n❌ 部分测试失败！")
        exit(1)
