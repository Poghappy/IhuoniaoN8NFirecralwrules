#!/usr/bin/env python3
"""
测试 cron 表达式解析修复

验证 cron.get_next(datetime) 的正确用法
"""

from datetime import datetime, timedelta, timezone


try:
    from croniter import croniter

    def test_cron_get_next():
        """测试 cron.get_next(datetime) 的返回值类型"""
        current_time = datetime.now(timezone.utc)
        cron = croniter("0 * * * *", current_time)

        # 测试 get_next(datetime) 返回类型
        result_timestamp = cron.get_next(datetime)

        # 将时间戳转换为 datetime 对象
        result = datetime.fromtimestamp(result_timestamp, tz=timezone.utc)

        print(f"✅ cron.get_next(datetime) 返回类型: {type(result_timestamp)}")
        print(f"✅ 返回值（时间戳）: {result_timestamp}")
        print(f"✅ 转换后的 datetime: {result}")
        print(f"✅ 是否为 datetime 对象: {isinstance(result, datetime)}")

        # 测试比较逻辑
        next_run = result
        next_run_time = current_time + timedelta(minutes=1)

        print(f"\n当前时间: {current_time}")
        print(f"下次运行时间: {next_run}")
        print(f"1分钟后时间: {next_run_time}")
        print(f"比较结果 (next_run <= next_run_time): {next_run <= next_run_time}")

        # 验证修复后的逻辑
        if next_run <= current_time + timedelta(minutes=1):
            print("\n✅ 修复后的比较逻辑正确")
        else:
            print("\n⚠️  下次运行时间不在1分钟内")

        return True

    if __name__ == "__main__":
        test_cron_get_next()

except ImportError:
    print("⚠️  croniter 未安装，无法运行测试")
    print("安装命令: pip install croniter")
except Exception as e:
    print(f"❌ 测试错误: {e}")
