"""
FastMCP 快速开始示例(带兼容处理与简单测试).

在真实环境中(已安装 `mcp` 包)，本文件示例一个 FastMCP 服务器:
- 注册一个加法工具 `add`
- 注册一个动态资源 `greeting://{name}`
- 注册一个用于生成问候 Prompt 的函数 `greet_user`

在不支持 `mcp` 的环境（比如当前沙箱）中：
- 会自动使用一个“假的 FastMCP”实现，只是让代码能跑通、能调试函数逻辑
- 不会真的启动 MCP 服务器
"""

# 尝试导入 FastMCP，如果当前环境没有 `mcp` 模块，则使用一个简易占位实现
try:
    from mcp.server.fastmcp import FastMCP  # 真实环境下的导入
except ModuleNotFoundError:
    # 兼容：在没有安装 mcp 的环境中，定义一个简单的占位类
    class FastMCP:  # type: ignore
        """兼容用的简易 FastMCP，占位实现。

        目的：
        - 让示例代码在没有安装 `mcp` 的环境中也能正常运行、调试业务逻辑
        - 所有装饰器（tool/resource/prompt）都只是原样返回函数，不做注册
        """

        def __init__(self, name: str) -> None:
            self.name = name

        def tool(self):
            """用作装饰器的假实现，直接返回原函数。"""

            def decorator(func):
                return func

            return decorator

        def resource(self, pattern: str):  # noqa: ARG002
            """用作装饰器的假实现，直接返回原函数。"""

            def decorator(func):
                return func

            return decorator

        def prompt(self):
            """用作装饰器的假实现，直接返回原函数。"""

            def decorator(func):
                return func

            return decorator


# 创建一个 MCP 服务器实例，名称为 "Demo"
mcp = FastMCP("Demo")


# 定义一个加法工具，通过装饰器注册为 MCP 工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """将两个数字相加。"""
    return a + b


# 定义一个动态资源，通过 URL 模式生成个性化问候
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """返回个性化问候语，例如: "Hello, 张三!"."""
    return f"Hello, {name}!"


# 定义一个 Prompt，可根据不同风格生成问候文本
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """根据名字和风格生成问候提示词，返回一段英文说明文本.

    Args:
        name: 用户名字，会出现在提示词中
        style: 风格，可选: "friendly" / "formal" / "casual"
    """

    styles = {
        "friendly": "Please write a warm, friendly greeting",  # 友好风格
        "formal": "Please write a formal, professional greeting",  # 正式风格
        "casual": "Please write a casual, relaxed greeting",  # 轻松风格
    }

    # 根据用户指定风格选择提示，不存在则默认友好风格
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# =====================
# 简单“测试用例”区域
# =====================


def _run_tests() -> None:
    """简单测试当前文件中的核心函数逻辑.

    注意:
    - 这里只测试 Python 逻辑，不测试真实 MCP 通信
    """

    # 测试 add
    assert add(1, 2) == 3
    assert add(-1, 5) == 4

    # 测试 get_greeting
    assert get_greeting("Alice") == "Hello, Alice!"
    assert get_greeting("乐哥") == "Hello, 乐哥!"

    # 测试 greet_user：只检查是否包含关键字段
    msg = greet_user("Alice")
    assert "warm, friendly greeting" in msg
    assert "Alice" in msg

    msg_formal = greet_user("Bob", style="formal")
    assert "formal, professional greeting" in msg_formal
    assert "Bob" in msg_formal

    msg_unknown_style = greet_user("Charlie", style="??")
    # 未知风格应回退到 friendly
    assert "warm, friendly greeting" in msg_unknown_style
    assert "Charlie" in msg_unknown_style


if __name__ == "__main__":
    # 在当前环境直接运行本文件时，执行简单测试
    _run_tests()
    print("所有测试通过, 核心逻辑正常运行.")
