#!/usr/bin/env python3
"""
配置验证脚本
验证 GitHub 认证和 Python 语言服务器配置
"""

import sys
import subprocess
from pathlib import Path


def check_github_auth() -> bool:
    """检查 GitHub 认证状态"""
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and "Logged in" in result.stdout:
            print("✅ GitHub CLI 已认证")
            return True
        else:
            print("❌ GitHub CLI 未认证")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  GitHub CLI 未安装或无法访问")
        return False


def check_git_config() -> bool:
    """检查 Git 配置"""
    try:
        result = subprocess.run(
            ["git", "config", "--global", "credential.helper"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Git 凭据助手已配置: {result.stdout.strip()}")
            return True
        else:
            print("⚠️  Git 凭据助手未配置")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Git 未安装或无法访问")
        return False


def check_python_language_server() -> bool:
    """检查 Python 语言服务器配置"""
    settings_file = Path(".vscode/settings.json")
    if not settings_file.exists():
        print("❌ .vscode/settings.json 不存在")
        return False

    content = settings_file.read_text(encoding="utf-8")

    # 检查 Pylance 配置
    if '"python.languageServer": "Pylance"' in content:
        print("✅ Python 语言服务器已设置为 Pylance")
    else:
        print("❌ Python 语言服务器未正确配置")
        return False

    # 检查 Cursor Pyright 是否已禁用
    if '"cursorpyright.enable": false' in content:
        print("✅ Cursor Pyright 已禁用")
    else:
        print("⚠️  Cursor Pyright 可能未禁用")

    return True


def main() -> int:
    """主函数"""
    print("🔍 开始验证配置...\n")

    results = []

    print("1. 检查 GitHub 认证:")
    results.append(check_github_auth())
    print()

    print("2. 检查 Git 配置:")
    results.append(check_git_config())
    print()

    print("3. 检查 Python 语言服务器配置:")
    results.append(check_python_language_server())
    print()

    # 总结
    print("=" * 50)
    if all(results):
        print("✅ 所有配置验证通过！")
        return 0
    else:
        print("⚠️  部分配置需要检查")
        return 1


if __name__ == "__main__":
    sys.exit(main())
