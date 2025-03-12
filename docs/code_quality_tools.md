# 代码质量工具指南

## 工具级别分类

### 1. 基础级别 (Basic Level)

| 工具 | 版本 | 用途 | 配置文件 | 说明 |
|------|------|------|----------|------|
| black | ^24.0 | 代码格式化 | pyproject.toml | 自动格式化Python代码，统一代码风格 |
| isort | ^5.13.0 | 导入排序 | pyproject.toml | 自动整理和分类导入语句 |
| ruff | ^0.3.0 | 代码检查 | pyproject.toml | 快速的Python代码检查工具 |
| mypy | ^1.8.0 | 类型检查 | pyproject.toml | 静态类型检查，验证类型注解 |
| pytest | ^8.0 | 测试框架 | pyproject.toml | 单元测试和功能测试框架 |

### 2. 标准级别 (Standard Level)
（包含基础级别所有工具）

| 工具 | 版本 | 用途 | 配置文件 | 说明 |
|------|------|------|----------|------|
| pytest-cov | ^4.1.0 | 测试覆盖率 | pyproject.toml | 测试覆盖率报告生成 |
| pylint | ^3.0.0 | 代码分析 | pyproject.toml | 深度代码分析，查找代码问题 |
| bandit | ^1.7.7 | 安全检查 | pyproject.toml | Python代码安全漏洞检查 |
| vulture | ^2.14 | 死代码检查 | pyproject.toml | 检测未使用的代码 |

### 3. 高级级别 (Advanced Level)
（包含基础和标准级别所有工具）

| 工具 | 版本 | 用途 | 配置文件 | 说明 |
|------|------|------|----------|------|
| safety | ^2.3.0 | 依赖安全检查 | - | 检查依赖包的已知安全漏洞 |
| xenon | ^0.9.1 | 代码复杂度检查 | - | 检查代码复杂度指标 |
| radon | ^6.0.1 | 代码质量度量 | - | 计算代码质量指标 |
| pytype | ^2024.2.27 | 类型检查 | pyproject.toml | Google的静态类型检查器 |
| scalene | ^1.5.37 | 性能分析 | - | CPU和内存分析工具 |

## 检查标准

### 1. 代码风格标准

- 行长度限制：88字符
- 缩进：4个空格
- 导入排序：按标准库、第三方库、本地模块分组
- 类型注解：要求所有函数和方法都有类型注解
- 文档字符串：使用Google风格

### 2. 代码质量标准

- 测试覆盖率要求：
  - 基础级别：>= 60%
  - 标准级别：>= 80%
  - 高级级别：>= 90%

- 代码复杂度限制：
  - 圈复杂度：<= 10
  - 认知复杂度：<= 15
  - 函数行数：<= 50

### 3. 安全标准

- 禁止使用不安全的函数和模块
- 所有依赖包必须无已知安全漏洞
- 敏感信息必须通过环境变量或安全存储管理
- 定期更新依赖包版本

## 自动化检查

项目使用pre-commit钩子自动运行以下检查：

```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 24.0.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
    -   id: isort

-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
    -   id: ruff
        args: [--fix]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]
```

## 最佳实践

1. **渐进式采用**
   - 从基础级别开始
   - 逐步添加更多检查
   - 根据项目需求调整配置

2. **自动化集成**
   - 使用pre-commit钩子
   - 配置CI/CD流程
   - 定期运行完整检查

3. **持续改进**
   - 定期更新工具版本
   - 根据团队反馈调整规则
   - 保持文档更新

## 常见问题解决

1. **工具冲突处理**
   - black和pylint的格式化冲突：使用black兼容配置
   - isort和black的冲突：设置isort profile = "black"
   - ruff和其他工具的重叠：适当禁用重复规则

2. **性能优化**
   - 使用pre-commit的缓存功能
   - 只检查修改的文件
   - 并行运行检查

3. **误报处理**
   - 使用行内注释禁用特定警告
   - 在配置文件中全局禁用特定规则
   - 记录禁用原因

更多详细配置示例和使用说明，请参考[配置示例]({{cookiecutter.project_slug}}/docs/code_quality_config.md)文档。 