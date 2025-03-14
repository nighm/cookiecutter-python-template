# 文档编写指南

本指南提供了项目文档编写的规范和建议，帮助维护高质量的项目文档。

## 文档结构

### 1. 项目文档结构

```
docs/
├── index.md              # 主页
├── quick_start/         # 快速开始指南
├── development_guide/   # 开发指南
├── api/                # API文档
├── examples/           # 使用示例
└── best_practices/     # 最佳实践
```

### 2. 文档类型

1. **用户文档**
   - 安装指南
   - 快速开始
   - 使用教程
   - 配置说明

2. **开发者文档**
   - API参考
   - 架构说明
   - 贡献指南
   - 测试文档

3. **运维文档**
   - 部署指南
   - 监控配置
   - 故障处理
   - 性能优化

## Markdown 规范

### 1. 基本格式

```markdown
# 一级标题

## 二级标题

### 三级标题

正文内容使用清晰的段落划分。

- 列表项1
- 列表项2
  - 子列表项

1. 有序列表1
2. 有序列表2

> 引用内容
```

### 2. 代码块

````markdown
```python
def example_function():
    """函数示例。"""
    return True
```
````

### 3. 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 内容1 | 内容2 | 内容3 |
```

### 4. 链接和图片

```markdown
[链接文字](URL)
![图片描述](图片URL)
```

## Python文档字符串

### 1. 模块文档

```python
"""
模块名称

模块描述，包括主要功能和用途。

典型用法:
    >>> from module import Class
    >>> instance = Class()
    >>> instance.method()

依赖:
    - dependency1
    - dependency2
"""
```

### 2. 类文档

```python
class ExampleClass:
    """类的简要描述。

    详细描述，包括类的主要功能和使用场景。

    Attributes:
        attr1 (type): 属性1的描述
        attr2 (type): 属性2的描述

    Example:
        >>> obj = ExampleClass()
        >>> obj.method()
    """
```

### 3. 函数文档

```python
def example_function(param1: str, param2: int = 0) -> bool:
    """函数的简要描述。

    详细描述函数的功能和使用方法。

    Args:
        param1 (str): 参数1的描述
        param2 (int, optional): 参数2的描述。默认为0

    Returns:
        bool: 返回值的描述

    Raises:
        ValueError: 异常情况的描述

    Example:
        >>> result = example_function("test", 42)
        >>> print(result)
        True
    """
```

## MkDocs 使用指南

### 1. 安装和配置

```bash
# 安装MkDocs
poetry add mkdocs mkdocs-material

# 创建新文档
mkdocs new .

# 本地预览
mkdocs serve

# 构建文档
mkdocs build
```

### 2. mkdocs.yml配置

```yaml
site_name: 项目名称
site_description: 项目描述
repo_url: https://github.com/username/project

theme:
  name: material
  language: zh
  features:
    - navigation.tabs
    - search.highlight

plugins:
  - search
  - mkdocstrings

markdown_extensions:
  - admonition
  - codehilite
  - toc:
      permalink: true
```

### 3. 使用提示框

```markdown
!!! note "注意"
    这是一个注意事项。

!!! warning "警告"
    这是一个警告信息。

!!! tip "提示"
    这是一个提示信息。
```

## API文档生成

### 1. 使用mkdocstrings

```yaml
# mkdocs.yml
plugins:
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          selection:
            docstring_style: google
          rendering:
            show_source: true
```

### 2. 在文档中引用代码

```markdown
::: your_package.module.Class
    handler: python
    selection:
      members:
        - method1
        - method2
```

## 文档最佳实践

### 1. 内容组织

- 使用清晰的层次结构
- 保持导航简单直观
- 相关内容放在一起
- 使用描述性的标题

### 2. 写作风格

- 使用简洁明了的语言
- 避免专业术语，必要时解释
- 提供具体的示例
- 使用主动语态

### 3. 代码示例

- 提供可运行的示例
- 包含输入和预期输出
- 解释关键步骤
- 使用真实场景

### 4. 文档维护

- 定期审查和更新
- 删除过时内容
- 修复损坏的链接
- 响应用户反馈

## 常见问题

### 1. 文档不同步

- 在代码审查中包含文档更新
- 使用自动化工具检查文档
- 定期审查文档准确性

### 2. 示例过时

- 使用自动化测试验证示例
- 在CI中运行文档测试
- 使用文档测试工具

### 3. 导航混乱

- 保持结构简单
- 使用描述性的文件名
- 提供清晰的导航路径
- 添加搜索功能

## 文档检查清单

### 新功能文档
- [ ] API文档完整
- [ ] 包含使用示例
- [ ] 解释配置选项
- [ ] 更新相关指南

### 文档更新
- [ ] 检查文档准确性
- [ ] 更新代码示例
- [ ] 检查格式一致性
- [ ] 验证所有链接

### 发布文档
- [ ] 更新版本号
- [ ] 更新更新日志
- [ ] 检查构建结果
- [ ] 验证部署状态 