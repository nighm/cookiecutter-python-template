# 开发指南

## 开发环境设置

### 1. 基础环境

确保你的系统已安装：
- Python 3.11+
- Poetry
- Git

### 2. 开发工具推荐

- VS Code 或 PyCharm
- 推荐的VS Code插件：
  - Python
  - Pylance
  - Python Test Explorer
  - Python Docstring Generator
  - GitLens

### 3. 环境初始化

```bash
# 克隆项目
git clone <project-url>
cd <project-name>

# 安装依赖
poetry install

# 激活环境
poetry shell

# 安装pre-commit hooks
pre-commit install
```

## 开发工作流

### 1. 功能开发流程

1. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 编写代码：
   - 遵循项目代码风格
   - 添加必要的测试
   - 更新相关文档

3. 本地验证：
   ```bash
   # 运行测试
   pytest
   
   # 代码质量检查
   python scripts/run_quality_checks.py
   ```

4. 提交代码：
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

5. 创建Pull Request

### 2. 测试开发

#### 测试文件组织
```
tests/
├── conftest.py          # 共享fixtures
├── unit/               # 单元测试
├── integration/        # 集成测试
└── data/              # 测试数据
```

#### 编写测试
```python
import pytest
from your_package import YourClass

def test_your_function():
    # Arrange
    input_data = ...
    
    # Act
    result = YourClass().your_function(input_data)
    
    # Assert
    assert result == expected_result
```

#### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_specific.py

# 运行带标记的测试
pytest -m "slow"

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

### 3. 文档开发

#### 文档结构
```
docs/
├── index.md           # 主页
├── api/              # API文档
├── guides/           # 使用指南
└── examples/         # 示例代码
```

#### 编写文档
- 使用Markdown格式
- 包含代码示例
- 添加适当的链接
- 保持文档最新

#### 本地预览
```bash
# 启动文档服务
mkdocs serve

# 构建文档
mkdocs build
```

## 依赖管理

### 1. 添加依赖

```bash
# 添加生产依赖
poetry add package_name

# 添加开发依赖
poetry add -D package_name
```

### 2. 更新依赖

```bash
# 更新所有依赖
poetry update

# 更新特定依赖
poetry update package_name
```

### 3. 依赖管理最佳实践

- 明确指定依赖版本范围
- 定期更新依赖
- 使用依赖锁定文件
- 分离生产和开发依赖

## 版本发布流程

### 1. 版本号规范

遵循语义化版本 (SemVer)：
- MAJOR.MINOR.PATCH
- MAJOR: 不兼容的API修改
- MINOR: 向后兼容的功能性新增
- PATCH: 向后兼容的问题修正

### 2. 发布步骤

1. 更新版本号：
   ```bash
   poetry version patch  # 或 minor 或 major
   ```

2. 更新CHANGELOG.md

3. 创建发布分支：
   ```bash
   git checkout -b release/v1.0.0
   ```

4. 运行完整测试：
   ```bash
   python scripts/run_quality_checks.py
   pytest
   ```

5. 构建包：
   ```bash
   poetry build
   ```

6. 创建发布标签：
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   ```

## 最佳实践

### 1. 代码组织

- 使用清晰的模块结构
- 遵循单一职责原则
- 保持函数和类的简单性
- 使用有意义的命名

### 2. 错误处理

- 使用自定义异常类
- 提供有意义的错误信息
- 适当的日志记录
- 优雅的错误恢复

### 3. 配置管理

- 使用环境变量
- 配置文件分离
- 敏感信息保护
- 配置验证

### 4. 性能优化

- 编写高效的代码
- 使用性能分析工具
- 实现缓存机制
- 优化数据库查询

## 故障排除

### 1. 常见问题

#### 依赖安装失败
```bash
# 清理缓存
poetry cache clear . --all
# 重新安装
poetry install
```

#### 测试失败
- 检查测试环境
- 验证测试数据
- 查看详细日志
- 使用调试器

#### pre-commit检查失败
```bash
# 手动运行检查
pre-commit run --all-files
# 跳过检查（紧急情况）
git commit -m "message" --no-verify
```

### 2. 调试技巧

- 使用断点调试
- 添加日志输出
- 使用性能分析器
- 代码审查 