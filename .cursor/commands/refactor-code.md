# 代码重构

帮我重构当前代码，提升代码质量和可维护性。

## 重构目标

### 1. 提升可读性

- 使用有意义的变量和函数名
- 添加必要的注释
- 简化复杂的表达式
- 遵循编码规范

### 2. 减少重复

- 提取公共代码
- 创建可复用的函数
- 使用设计模式
- 消除代码重复

### 3. 改善结构

- 单一职责原则
- 合理的函数长度
- 清晰的模块划分
- 降低耦合度

### 4. 提升性能

- 优化算法复杂度
- 减少不必要的计算
- 使用更高效的数据结构
- 优化数据库查询

## 重构技巧

### 提取函数

将复杂的代码块提取为独立函数

**重构前**:
```python
# 复杂的内联代码
result = []
for item in data:
    if item['status'] == 'active':
        processed = item['value'] * 2 + 10
        if processed > 100:
            result.append(processed)
```

**重构后**:
```python
def is_active(item):
    return item['status'] == 'active'

def process_value(value):
    return value * 2 + 10

def is_valid_result(value):
    return value > 100

result = [
    process_value(item['value'])
    for item in data
    if is_active(item) and is_valid_result(process_value(item['value']))
]
```

### 提取变量

使用有意义的变量名替代复杂表达式

**重构前**:
```python
if user.age >= 18 and user.country == 'US' and user.verified:
    # 处理
```

**重构后**:
```python
is_adult = user.age >= 18
is_us_user = user.country == 'US'
is_verified = user.verified
can_proceed = is_adult and is_us_user and is_verified

if can_proceed:
    # 处理
```

### 使用早期返回

减少嵌套层级

**重构前**:
```python
def process_user(user):
    if user is not None:
        if user.is_active:
            if user.has_permission:
                return do_something(user)
            else:
                return None
        else:
            return None
    else:
        return None
```

**重构后**:
```python
def process_user(user):
    if user is None:
        return None
    if not user.is_active:
        return None
    if not user.has_permission:
        return None
    return do_something(user)
```

### 使用数据类/接口

替代字典或元组

**重构前**:
```python
user = {
    'name': 'John',
    'age': 30,
    'email': 'john@example.com'
}
```

**重构后**:
```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

user = User(name='John', age=30, email='john@example.com')
```

## 重构检查清单

### 代码质量

- [ ] 函数长度合理（< 50 行）
- [ ] 参数数量合理（< 5 个）
- [ ] 嵌套层级合理（< 4 层）
- [ ] 循环复杂度合理

### 命名规范

- [ ] 变量名清晰有意义
- [ ] 函数名动词开头
- [ ] 类名名词开头
- [ ] 常量全大写

### 代码组织

- [ ] 相关代码放在一起
- [ ] 公共代码已提取
- [ ] 模块职责单一
- [ ] 依赖关系清晰

### 测试覆盖

- [ ] 保持测试通过
- [ ] 添加新的测试
- [ ] 测试覆盖率不降低

## 输出格式

### 📋 重构计划

列出需要重构的地方和优先级

### 🔧 重构实施

提供重构后的代码

### 📊 改进对比

对比重构前后的改进：
- 代码行数变化
- 复杂度变化
- 性能变化
- 可读性提升

### ✅ 验证结果

确认重构后：
- 功能正常
- 测试通过
- 性能未降低


