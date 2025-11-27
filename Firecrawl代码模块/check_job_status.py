#!/usr/bin/env python3
"""
检查 Firecrawl 任务状态

使用方法:
    python3 check_job_status.py <job_id>
    python3 check_job_status.py fc-31ebbe4647b84fdc975318d372eebea8
"""

import json
import os
import sys
from typing import Any, Dict, Optional

try:
    from firecrawl import Firecrawl  # type: ignore
except ImportError:
    print("❌ 请安装 Firecrawl SDK: pip install firecrawl-py")
    sys.exit(1)


def load_api_key() -> Optional[str]:
    """从环境变量或配置文件加载 API 密钥"""
    # 1. 检查环境变量
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if api_key:
        return api_key

    # 2. 检查 .env 文件
    try:
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if api_key:
            return api_key
    except ImportError:
        pass

    # 3. 检查 settings.json
    try:
        settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
        if os.path.exists(settings_path):
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                if "firecrawl" in settings and "api_key" in settings["firecrawl"]:
                    api_key = settings["firecrawl"]["api_key"]
                    if api_key and api_key != "your_firecrawl_api_key_here":
                        return api_key
    except Exception:
        pass

    return None


def check_crawl_status(firecrawl: Firecrawl, job_id: str) -> Dict[str, Any]:
    """检查爬取任务状态

    Args:
        firecrawl: Firecrawl 客户端实例
        job_id: 任务 ID

    Returns:
        任务状态信息
    """
    try:
        # 尝试使用 get_crawl_status 方法
        if hasattr(firecrawl, "get_crawl_status"):
            status = firecrawl.get_crawl_status(job_id)
            return status
        # 尝试使用 check_crawl_status 方法（某些版本可能使用此方法名）
        elif hasattr(firecrawl, "check_crawl_status"):
            status = firecrawl.check_crawl_status(job_id)
            return status
        else:
            # 列出所有可用方法用于调试
            methods = [m for m in dir(firecrawl) if "crawl" in m.lower() and not m.startswith("_")]
            print(f"⚠️  SDK 版本可能不支持 get_crawl_status")
            print(f"   可用的 crawl 相关方法: {', '.join(methods)}")
            return {"error": "SDK 方法不可用", "available_methods": methods}
    except Exception as e:
        error_msg = str(e)
        # 如果是 404 错误，提供更详细的提示
        if "404" in error_msg or "not found" in error_msg.lower():
            return {"error": error_msg, "hint": "任务可能已过期（超过24小时）或任务ID不正确"}
        return {"error": error_msg}


def check_extract_status(firecrawl: Firecrawl, job_id: str) -> Dict[str, Any]:
    """检查提取任务状态

    Args:
        firecrawl: Firecrawl 客户端实例
        job_id: 任务 ID

    Returns:
        任务状态信息
    """
    try:
        # 尝试使用 get_extract_status 方法
        if hasattr(firecrawl, "get_extract_status"):
            status = firecrawl.get_extract_status(job_id)
            return status
        else:
            return {"error": "SDK 方法不可用"}
    except Exception as e:
        return {"error": str(e)}


def format_status(status: Dict[str, Any]) -> str:
    """格式化状态输出

    Args:
        status: 状态字典

    Returns:
        格式化后的字符串
    """
    if "error" in status:
        return f"❌ 错误: {status['error']}"

    output = []
    output.append("=" * 60)
    output.append("📊 Firecrawl 任务状态")
    output.append("=" * 60)

    # 基本信息
    if "status" in status:
        status_emoji = {
            "scraping": "🔄",
            "completed": "✅",
            "failed": "❌",
            "pending": "⏳",
        }
        emoji = status_emoji.get(status["status"], "❓")
        output.append(f"{emoji} 状态: {status['status']}")

    if "total" in status:
        output.append(f"📄 总页数: {status.get('total', 'N/A')}")
    if "completed" in status:
        output.append(f"✅ 已完成: {status.get('completed', 'N/A')}")

    if "creditsUsed" in status:
        output.append(f"💰 已使用积分: {status.get('creditsUsed', 'N/A')}")

    if "expiresAt" in status:
        output.append(f"⏰ 过期时间: {status.get('expiresAt', 'N/A')}")

    # 数据预览
    if "data" in status and status["data"]:
        data_count = len(status["data"])
        output.append(f"\n📦 数据项数量: {data_count}")
        if data_count > 0:
            output.append("\n📝 数据预览（前3项）:")
            for i, item in enumerate(status["data"][:3], 1):
                if isinstance(item, dict):
                    if "metadata" in item and "sourceURL" in item["metadata"]:
                        output.append(f"  {i}. {item['metadata']['sourceURL']}")
                    elif "url" in item:
                        output.append(f"  {i}. {item['url']}")
                    else:
                        output.append(f"  {i}. {json.dumps(item, ensure_ascii=False)[:100]}...")

    # 分页信息
    if "next" in status:
        output.append(f"\n➡️  下一页: {status['next']}")

    output.append("=" * 60)
    return "\n".join(output)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("❌ 请提供任务 ID")
        print(f"使用方法: {sys.argv[0]} <job_id>")
        print(f"示例: {sys.argv[0]} fc-31ebbe4647b84fdc975318d372eebea8")
        sys.exit(1)

    job_id = sys.argv[1].strip()

    # 加载 API 密钥
    api_key = load_api_key()
    if not api_key:
        print("❌ 未找到 Firecrawl API 密钥")
        print("请设置环境变量 FIRECRAWL_API_KEY 或在 settings.json 中配置")
        sys.exit(1)

    # 初始化 Firecrawl 客户端
    try:
        firecrawl = Firecrawl(api_key=api_key)
    except Exception as e:
        print(f"❌ 初始化 Firecrawl 客户端失败: {e}")
        sys.exit(1)

    print(f"🔍 正在检查任务状态: {job_id}\n")
    print(
        f"📋 任务 ID 格式: {'✅ 正确（fc- 开头）' if job_id.startswith('fc-') else '⚠️  非标准格式'}\n"
    )

    # 尝试检查爬取任务状态
    print("1️⃣  尝试检查爬取任务状态...")
    status = check_crawl_status(firecrawl, job_id)

    # 如果失败，尝试检查提取任务状态
    if "error" in status:
        print("\n2️⃣  爬取任务检查失败，尝试检查提取任务...")
        status = check_extract_status(firecrawl, job_id)

    # 输出结果
    if "error" in status:
        print(f"\n❌ 无法获取任务状态: {status['error']}")
        if "hint" in status:
            print(f"\n💡 {status['hint']}")
        if "available_methods" in status:
            print(f"\n📚 可用的方法: {', '.join(status['available_methods'])}")
        print("\n💡 其他可能的原因:")
        print("  - 确认任务 ID 是否正确（格式: fc-xxxxxxxxxxxxx）")
        print("  - 确认 API 密钥是否有效")
        print("  - 确认任务是否在 24 小时内完成（过期任务无法查询）")
        print("  - 确认任务是否属于当前 API 密钥的账户")
        sys.exit(1)
    else:
        print(format_status(status))

        # 如果任务已完成且有数据，询问是否保存
        if status.get("status") == "completed" and "data" in status and status["data"]:
            print("\n💾 任务已完成，是否保存结果到文件？(y/n): ", end="")
            try:
                response = input().strip().lower()
                if response == "y":
                    output_file = f"firecrawl_result_{job_id}.json"
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(status, f, ensure_ascii=False, indent=2)
                    print(f"✅ 结果已保存到: {output_file}")
            except KeyboardInterrupt:
                print("\n\n👋 已取消")


if __name__ == "__main__":
    main()
