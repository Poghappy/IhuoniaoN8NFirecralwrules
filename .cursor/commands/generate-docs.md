# 生成文档

帮我为当前代码生成完整的文档。

## 文档类型

### API 文档

为 API 接口生成文档，包括：
- 接口路径和方法
- 请求参数说明
- 响应格式说明
- 示例请求和响应
- 错误码说明

### 函数文档

为函数生成文档字符串，包括：
- 函数功能描述
- 参数说明（类型、默认值、说明）
- 返回值说明
- 异常说明
- 使用示例

### 类文档

为类生成文档，包括：
- 类的功能描述
- 属性说明
- 方法说明
- 使用示例
- 继承关系

### 模块文档

为模块生成文档，包括：
- 模块功能概述
- 主要功能列表
- 使用指南
- 配置说明
- 示例代码

## 文档格式

### Python (Google Style)

```python
def function_name(param1: str, param2: int = 0) -> dict:
    """
    函数功能的简短描述

    详细描述函数的功能、用途和注意事项

    Args:
        param1 (str): 参数1的说明
        param2 (int, optional): 参数2的说明. Defaults to 0.

    Returns:
        dict: 返回值的说明，包括字典的结构
            {
                'key1': str,  # 键1的说明
                'key2': int   # 键2的说明
            }

    Raises:
        ValueError: 什么情况下抛出此异常
        TypeError: 什么情况下抛出此异常

    Example:
        >>> result = function_name("test", 10)
        >>> print(result)
        {'key1': 'value', 'key2': 10}

    Note:
        特别需要注意的事项
    """
    pass
```

### TypeScript (JSDoc)

```typescript
/**
 * 函数功能的简短描述
 *
 * 详细描述函数的功能、用途和注意事项
 *
 * @param param1 - 参数1的说明
 * @param param2 - 参数2的说明
 * @returns 返回值的说明
 * @throws {Error} 什么情况下抛出错误
 *
 * @example
 * ```typescript
 * const result = functionName("test", 10);
 * console.log(result);
 * ```
 */
function functionName(param1: string, param2: number = 0): object {
    // 实现
}
```

### Markdown 文档

```markdown
# 模块名称

模块功能的简短描述

## 功能特性

- 特性1
- 特性2
- 特性3

## 安装

\`\`\`bash
pip install module-name
\`\`\`

## 快速开始

\`\`\`python
from module import function
result = function()
\`\`\`

## API 参考

### function_name

功能描述

**参数**:
- `param1` (str): 参数说明
- `param2` (int): 参数说明

**返回**:
- dict: 返回值说明

**示例**:
\`\`\`python
result = function_name("test")
\`\`\`
```

## 文档要求

### 必须包含

- [ ] 清晰的功能描述
- [ ] 完整的参数说明
- [ ] 返回值说明
- [ ] 使用示例
- [ ] 类型注解

### 建议包含

- [ ] 异常说明
- [ ] 注意事项
- [ ] 相关链接
- [ ] 版本信息
- [ ] 作者信息

### 质量标准

- 描述清晰、准确
- 示例代码可运行
- 格式规范统一
- 信息完整充分

## 输出格式

请为选中的代码生成符合规范的文档，并确保：
1. 文档格式正确
2. 内容完整准确
3. 示例代码可用
4. 符合项目规范


