# 核心模块 API 文档

`core` 模块提供了项目的核心功能实现。

## 版本信息

### get_version()

获取当前项目和Python环境的版本信息。

```python
from typing import Any, Dict

def get_version() -> Dict[str, Any]:
    """获取当前版本信息。

    Returns:
        Dict[str, Any]: 包含版本信息的字典，具有以下键：
            - version (str): 项目版本号
            - python_version (str): Python解释器版本
    """
```

#### 示例

```python
from your_package.core import get_version

# 获取版本信息
version_info = get_version()
print(f"项目版本: {version_info['version']}")
print(f"Python版本: {version_info['python_version']}")
```

#### 返回值说明

返回的字典包含以下信息：

| 键名 | 类型 | 说明 |
|------|------|------|
| version | str | 项目的版本号，遵循语义化版本规范 |
| python_version | str | Python解释器的版本号，格式为 "major.minor.micro" |

#### 注意事项

- 版本号遵循[语义化版本 2.0.0](https://semver.org/lang/zh-CN/) 规范
- Python版本信息从 `sys.version_info` 获取，确保准确性
- 该函数不会抛出异常

## 最佳实践

### 版本号管理

1. 在发布新版本时更新 `__version__` 变量
2. 遵循语义化版本规范：
   - 主版本号：不兼容的API修改
   - 次版本号：向下兼容的功能性新增
   - 修订号：向下兼容的问题修正

### 使用示例

```python
from your_package.core import get_version

def check_compatibility():
    version_info = get_version()
    
    # 检查项目版本
    if version_info['version'].startswith('0.'):
        print('警告：当前使用的是开发版本')
    
    # 检查Python版本
    python_version = version_info['python_version']
    major, minor, _ = map(int, python_version.split('.'))
    if (major, minor) < (3, 11):
        raise RuntimeError(f'需要Python 3.11+，当前版本为 {python_version}')
```

## 开发指南

### 扩展核心模块

如果需要向核心模块添加新功能，请遵循以下原则：

1. **保持简单性**
   - 核心模块应该只包含最基础、最重要的功能
   - 复杂功能应该放在专门的子模块中

2. **向后兼容**
   - 新功能不应该破坏现有的API
   - 如果需要进行破坏性更改，请在新的主版本中进行

3. **完善文档**
   - 为新功能添加详细的文档字符串
   - 更新本API文档
   - 提供使用示例

4. **添加测试**
   - 编写单元测试覆盖新功能
   - 确保测试覆盖率维持在高水平

### 代码示例

```python
from typing import Any, Dict
import sys

def get_extended_version() -> Dict[str, Any]:
    """获取扩展的版本信息。
    
    除了基本版本信息外，还包括更多系统信息。
    """
    base_info = get_version()
    return {
        **base_info,
        "platform": sys.platform,
        "implementation": sys.implementation.name,
        "build_date": "2024-03-20"  # 应该从实际构建信息中获取
    }
``` 