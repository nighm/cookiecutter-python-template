# 测试指南

本文档提供了项目测试相关的详细指南，包括测试策略、编写测试、运行测试等内容。

## 测试策略

### 测试类型

1. **单元测试**
   - 测试单个函数/方法的功能
   - 模拟外部依赖
   - 快速执行
   - 位于 `tests/unit/` 目录

2. **集成测试**
   - 测试多个组件的交互
   - 可能需要外部资源（数据库等）
   - 位于 `tests/integration/` 目录

3. **端到端测试**
   - 测试完整的功能流程
   - 模拟真实用户操作
   - 位于 `tests/e2e/` 目录

### 测试覆盖率目标

- 单元测试覆盖率 > 80%
- 集成测试覆盖关键路径
- 端到端测试覆盖主要用户场景

## 测试环境

### 1. 安装依赖

```bash
# 安装所有依赖（包括测试依赖）
poetry install

# 仅安装测试依赖
poetry install --with test
```

### 2. 测试配置

在 `pyproject.toml` 中配置pytest：

```toml
[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --cov=src --cov-report=html"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "e2e: marks tests as end-to-end tests",
]
```

## 编写测试

### 1. 测试文件组织

```
tests/
├── conftest.py           # 共享fixtures
├── unit/                # 单元测试
│   ├── test_core.py
│   └── test_utils.py
├── integration/         # 集成测试
│   └── test_database.py
└── e2e/                # 端到端测试
    └── test_api.py
```

### 2. 编写单元测试

```python
import pytest
from your_package.calculator import Calculator

def test_add():
    """测试加法功能。"""
    calc = Calculator()
    assert calc.add(1, 2) == 3
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0

def test_divide():
    """测试除法功能。"""
    calc = Calculator()
    assert calc.divide(6, 2) == 3
    assert calc.divide(5, 2) == 2.5
    
    with pytest.raises(ValueError):
        calc.divide(1, 0)
```

### 3. 使用Fixtures

```python
# conftest.py
import pytest
from your_package.database import Database

@pytest.fixture
async def db():
    """数据库连接fixture。"""
    db = Database()
    await db.connect()
    yield db
    await db.disconnect()

@pytest.fixture
def sample_data():
    """测试数据fixture。"""
    return {
        "id": 1,
        "name": "test",
        "value": 100
    }

# test_database.py
async def test_save_data(db, sample_data):
    """测试数据保存功能。"""
    # 使用fixtures
    result = await db.save(sample_data)
    assert result.id == sample_data["id"]
```

### 4. 模拟外部依赖

```python
from unittest.mock import Mock, patch
from your_package.client import APIClient

def test_api_call():
    """测试API调用。"""
    with patch("your_package.client.requests.get") as mock_get:
        # 设置模拟响应
        mock_get.return_value.json.return_value = {"data": "test"}
        mock_get.return_value.status_code = 200
        
        # 执行测试
        client = APIClient()
        result = client.get_data()
        
        # 验证结果
        assert result == {"data": "test"}
        mock_get.assert_called_once()
```

### 5. 参数化测试

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, True),
    (3, True),
    (4, False),
    (5, True)
])
def test_is_prime(input, expected):
    """测试素数判断功能。"""
    from your_package.math import is_prime
    assert is_prime(input) == expected
```

## 运行测试

### 1. 运行所有测试

```bash
# 运行所有测试
pytest

# 显示详细输出
pytest -v

# 显示额外测试摘要
pytest -ra
```

### 2. 运行特定测试

```bash
# 运行特定文件
pytest tests/test_specific.py

# 运行特定测试函数
pytest tests/test_file.py::test_function

# 运行特定测试类
pytest tests/test_file.py::TestClass
```

### 3. 使用标记

```bash
# 运行标记的测试
pytest -m slow
pytest -m "not slow"
pytest -m "integration or e2e"
```

### 4. 生成覆盖率报告

```bash
# 生成覆盖率报告
pytest --cov=src

# 生成HTML报告
pytest --cov=src --cov-report=html

# 生成XML报告（用于CI）
pytest --cov=src --cov-report=xml
```

## 持续集成

### 1. GitHub Actions配置

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11"]

    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
    
    - name: Run tests
      run: |
        poetry run pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## 测试最佳实践

### 1. 测试设计

- 每个测试只测试一个功能点
- 测试函数命名清晰明确
- 使用有意义的测试数据
- 测试边界条件和错误情况

### 2. 测试原则

- 测试应该是可重复的
- 测试应该是独立的
- 测试应该是简单的
- 测试应该是快速的

### 3. 测试数据管理

- 使用fixtures管理测试数据
- 避免测试间数据依赖
- 测试后清理数据
- 使用工厂模式创建测试数据

### 4. 异步测试

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """测试异步函数。"""
    result = await your_async_function()
    assert result == expected_value
```

### 5. 性能测试

```python
import pytest
import time

@pytest.mark.benchmark
def test_performance(benchmark):
    """测试函数性能。"""
    # 使用benchmark装饰器测量性能
    result = benchmark(your_function)
    assert result == expected_value
```

## 常见问题

### 1. 测试失败调试

```bash
# 显示完整回溯
pytest -vv

# 在失败时进入PDB
pytest --pdb

# 显示最慢的测试
pytest --durations=10
```

### 2. 测试数据清理

```python
@pytest.fixture(autouse=True)
async def cleanup_database():
    """测试后自动清理数据库。"""
    yield
    await cleanup_data()
```

### 3. 并发测试

```python
# conftest.py
def pytest_configure(config):
    """配置pytest-xdist以并行运行测试。"""
    config.option.numprocesses = 4
```

### 4. 测试超时处理

```python
@pytest.mark.timeout(5)
def test_with_timeout():
    """超时测试示例。"""
    result = long_running_function()
    assert result == expected_value
```

## 测试检查清单

### 新功能测试
- [ ] 单元测试覆盖主要功能
- [ ] 测试边界条件
- [ ] 测试错误处理
- [ ] 文档字符串完整
- [ ] 测试覆盖率达标

### 错误修复测试
- [ ] 添加重现问题的测试
- [ ] 验证修复后测试通过
- [ ] 确保未引入新问题
- [ ] 更新相关文档

### 重构测试
- [ ] 确保现有测试全部通过
- [ ] 更新过时的测试
- [ ] 添加新的测试场景
- [ ] 维持或提高覆盖率 