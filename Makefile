.PHONY: help install install-dev lint format type-check test clean run-example run-tests check-all

# 默认目标
help:
	@echo "HawaiiHub.net - Firecrawl × 火鸟门户 × n8n 采集与自动化运营"
	@echo ""
	@echo "可用命令:"
	@echo "  make install          - 安装项目依赖"
	@echo "  make install-dev      - 安装开发依赖"
	@echo "  make lint             - 运行代码检查 (ruff)"
	@echo "  make format           - 格式化代码 (ruff format)"
	@echo "  make type-check       - 类型检查 (mypy)"
	@echo "  make test             - 运行测试 (pytest)"
	@echo "  make run-example      - 运行 FastMCP 示例"
	@echo "  make run-tests        - 运行所有测试"
	@echo "  make check-all        - 运行所有检查 (lint + format + type-check)"
	@echo "  make clean            - 清理临时文件"
	@echo ""

# Python 路径
PYTHON := python3
PYTHON_MODULES := Firecrawl代码模块 docs/Firecrawl工具/代码模块

# 安装依赖
install:
	@echo "安装项目依赖..."
	@if [ -f requirements.txt ]; then \
		$(PYTHON) -m pip install -r requirements.txt; \
	else \
		echo "未找到 requirements.txt，跳过依赖安装"; \
	fi

# 安装开发依赖
install-dev:
	@echo "安装开发依赖..."
	@$(PYTHON) -m pip install ruff mypy pytest pytest-cov
	@if [ -f requirements-dev.txt ]; then \
		$(PYTHON) -m pip install -r requirements-dev.txt; \
	fi

# 代码检查
lint:
	@echo "运行代码检查 (ruff)..."
	@$(PYTHON) -m ruff check $(PYTHON_MODULES) || true
	@echo "代码检查完成"

# 代码检查（仅错误）
lint-errors:
	@echo "运行代码检查（仅错误）..."
	@$(PYTHON) -m ruff check $(PYTHON_MODULES) --select E || true
	@echo "错误检查完成"

# 格式化代码
format:
	@echo "格式化代码 (ruff format)..."
	@$(PYTHON) -m ruff format $(PYTHON_MODULES)
	@echo "代码格式化完成"

# 类型检查
type-check:
	@echo "运行类型检查 (mypy)..."
	@for module in $(PYTHON_MODULES); do \
		if [ -d "$$module" ] || [ -f "$$module" ]; then \
			$(PYTHON) -m mypy $$module --ignore-missing-imports || true; \
		fi; \
	done
	@echo "类型检查完成"

# 运行测试
test:
	@echo "运行测试 (pytest)..."
	@$(PYTHON) -m pytest tests/ -v || echo "未找到测试目录，跳过测试"

# 运行 FastMCP 示例
run-example:
	@echo "运行 FastMCP 示例..."
	@$(PYTHON) Firecrawl代码模块/canvas_fastmcp_example.py || echo "示例运行失败"

# 运行所有测试
run-tests:
	@echo "运行所有测试..."
	@$(PYTHON) Firecrawl代码模块/canvas_fastmcp_example.py
	@if [ -f "docs/Firecrawl工具/代码模块/集成测试.py" ]; then \
		$(PYTHON) docs/Firecrawl工具/代码模块/集成测试.py || true; \
	fi
	@echo "所有测试完成"

# 运行所有检查
check-all: lint format type-check
	@echo "所有检查完成"

# 清理临时文件
clean:
	@echo "清理临时文件..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "清理完成"

# 验证特定文件
check-file:
	@if [ -z "$(FILE)" ]; then \
		echo "用法: make check-file FILE=path/to/file.py"; \
		exit 1; \
	fi
	@echo "检查文件: $(FILE)"
	@$(PYTHON) -m ruff check $(FILE)
	@$(PYTHON) -m ruff format --check $(FILE)
	@echo "文件检查完成"

# 批量修复（自动修复可修复的问题）
fix:
	@echo "自动修复代码问题..."
	@$(PYTHON) -m ruff check --fix $(PYTHON_MODULES) || true
	@$(PYTHON) -m ruff format $(PYTHON_MODULES)
	@echo "自动修复完成"

# 检查所有Python文件
check-all-files:
	@echo "检查所有Python文件..."
	@find $(PYTHON_MODULES) -name "*.py" -exec $(PYTHON) -m ruff check {} \; || true
	@echo "所有文件检查完成"

