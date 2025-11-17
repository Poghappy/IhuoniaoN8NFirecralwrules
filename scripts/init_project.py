#!/usr/bin/env python3
"""
HawaiiHub.net 项目初始化脚本

用于初始化项目环境，包括：
- 创建必要的目录结构
- 复制配置文件模板
- 验证环境配置
- 安装依赖

作者: HawaiiHub Team
创建时间: 2025-01-27
版本: 1.0.0
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class ProjectInitializer:
    """项目初始化器"""

    def __init__(self, project_root: Optional[Path] = None):
        """初始化项目初始化器

        Args:
            project_root: 项目根目录，默认为脚本所在目录的父目录
        """
        if project_root is None:
            # 获取脚本所在目录的父目录（项目根目录）
            self.project_root = Path(__file__).parent.parent.resolve()
        else:
            self.project_root = Path(project_root).resolve()

        self.required_dirs = [
            "Firecrawl代码模块",
            "docs",
            "logs",
            "data",
            "tasks",
            ".cursor/logs",
        ]

        self.required_files = {
            ".env.example": ".env",
        }

    def create_directories(self) -> List[str]:
        """创建必要的目录结构

        Returns:
            List[str]: 创建的目录列表
        """
        created_dirs = []
        for dir_path in self.required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(str(dir_path))
                print(f"✅ 创建目录: {dir_path}")
            else:
                print(f"ℹ️  目录已存在: {dir_path}")

        return created_dirs

    def copy_config_files(self) -> List[str]:
        """复制配置文件模板

        Returns:
            List[str]: 复制的文件列表
        """
        copied_files = []
        for src, dst in self.required_files.items():
            src_path = self.project_root / src
            dst_path = self.project_root / dst

            if not src_path.exists():
                print(f"⚠️  源文件不存在: {src}")
                continue

            if dst_path.exists():
                print(f"ℹ️  目标文件已存在: {dst}，跳过复制")
                continue

            try:
                shutil.copy2(src_path, dst_path)
                copied_files.append(dst)
                print(f"✅ 复制配置文件: {src} -> {dst}")
            except Exception as e:
                print(f"❌ 复制文件失败 {src} -> {dst}: {e}")

        return copied_files

    def check_python_version(self) -> bool:
        """检查 Python 版本

        Returns:
            bool: 版本是否符合要求
        """
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 9):
            print(f"❌ Python 版本过低: {version.major}.{version.minor}")
            print("   需要 Python 3.9 或更高版本")
            return False

        print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
        return True

    def check_dependencies(self) -> dict:
        """检查依赖是否已安装

        Returns:
            dict: 依赖检查结果
        """
        required_packages = [
            "firecrawl",
            "requests",
            "flask",
            "pandas",
            "beautifulsoup4",
        ]

        results = {}
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                results[package] = True
                print(f"✅ {package} 已安装")
            except ImportError:
                results[package] = False
                print(f"⚠️  {package} 未安装")

        return results

    def install_dependencies(self, dev: bool = False) -> bool:
        """安装项目依赖

        Args:
            dev: 是否安装开发依赖

        Returns:
            bool: 安装是否成功
        """
        requirements_file = "requirements-dev.txt" if dev else "requirements.txt"
        req_path = self.project_root / requirements_file

        if not req_path.exists():
            print(f"⚠️  依赖文件不存在: {requirements_file}")
            return False

        print(f"📦 安装依赖: {requirements_file}")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(req_path)],
                check=True,
                cwd=self.project_root,
            )
            print("✅ 依赖安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败: {e}")
            return False

    def verify_env_file(self) -> bool:
        """验证 .env 文件配置

        Returns:
            bool: 配置是否完整
        """
        env_path = self.project_root / ".env"
        if not env_path.exists():
            print("⚠️  .env 文件不存在，请从 .env.example 复制并配置")
            return False

        # 读取 .env 文件
        required_vars = [
            "FIRECRAWL_API_KEY",
            "HUONIAO_API_BASE_URL",
            "HUONIAO_API_KEY",
        ]

        missing_vars = []
        with open(env_path, encoding="utf-8") as f:
            content = f.read()
            for var in required_vars:
                if f"{var}=" not in content or f"{var}=your_" in content:
                    missing_vars.append(var)

        if missing_vars:
            print(f"⚠️  以下环境变量未配置: {', '.join(missing_vars)}")
            return False

        print("✅ .env 文件配置完整")
        return True

    def run_initialization(self, install_deps: bool = False, dev: bool = False) -> bool:
        """运行完整的初始化流程

        Args:
            install_deps: 是否安装依赖
            dev: 是否安装开发依赖

        Returns:
            bool: 初始化是否成功
        """
        print("=" * 60)
        print("HawaiiHub.net 项目初始化")
        print("=" * 60)
        print()

        # 1. 检查 Python 版本
        print("📋 步骤 1: 检查 Python 版本")
        if not self.check_python_version():
            return False
        print()

        # 2. 创建目录结构
        print("📋 步骤 2: 创建目录结构")
        created_dirs = self.create_directories()
        print(f"   创建了 {len(created_dirs)} 个目录")
        print()

        # 3. 复制配置文件
        print("📋 步骤 3: 复制配置文件")
        copied_files = self.copy_config_files()
        if copied_files:
            print(f"   复制了 {len(copied_files)} 个配置文件")
            print("   ⚠️  请编辑 .env 文件并填入实际配置值")
        print()

        # 4. 检查依赖
        print("📋 步骤 4: 检查依赖")
        dep_results = self.check_dependencies()
        missing_deps = [pkg for pkg, installed in dep_results.items() if not installed]
        if missing_deps:
            print(f"   发现 {len(missing_deps)} 个未安装的依赖")
        print()

        # 5. 安装依赖（可选）
        if install_deps:
            print("📋 步骤 5: 安装依赖")
            if not self.install_dependencies(dev=dev):
                print("   ⚠️  依赖安装失败，请手动安装")
            print()

        # 6. 验证配置
        print("📋 步骤 6: 验证配置")
        env_ok = self.verify_env_file()
        print()

        # 总结
        print("=" * 60)
        print("初始化完成！")
        print("=" * 60)
        print()
        print("📝 下一步:")
        print("   1. 编辑 .env 文件，填入实际配置值")
        if missing_deps and not install_deps:
            print(f"   2. 安装依赖: pip install -r requirements.txt")
        if not env_ok:
            print("   3. 配置环境变量后重新运行此脚本验证")
        print("   4. 运行测试: make test")
        print("   5. 查看文档: README.md")
        print()

        return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="HawaiiHub.net 项目初始化脚本")
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="安装项目依赖",
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="安装开发依赖（需要 --install-deps）",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        help="项目根目录路径",
    )

    args = parser.parse_args()

    initializer = ProjectInitializer(project_root=args.project_root)
    success = initializer.run_initialization(
        install_deps=args.install_deps, dev=args.dev
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

