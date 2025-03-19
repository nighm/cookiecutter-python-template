# 代码质量检查示例

本文档通过具体的代码示例展示了不同级别的代码质量检查要求和实践。

## 基础级别检查

基础级别的检查主要关注：
1. 代码格式规范
2. 基本类型提示
3. 简单文档字符串
4. 基本测试覆盖

### 示例代码
```python
def example_function(input_list: Optional[List[int]] = None) -> int:
    """计算列表中所有数字的和。"""
    if input_list is None:
        return 0
    return sum(input_list)
```

### 检查重点
- 使用类型提示
- 函数有基本文档
- 代码格式符合PEP 8
- 包含基本测试

### 运行检查
```bash
# 格式检查
poetry run black .
poetry run isort .

# 类型检查
poetry run mypy src

# 运行测试
poetry run pytest
```

## 标准级别检查

标准级别的检查增加了：
1. 完整的文档字符串
2. 异常处理
3. 日志记录
4. 代码复杂度控制
5. 基本安全检查

### 示例代码
```python
class DataProcessor:
    """数据处理类，展示标准级别的代码质量要求。"""

    def process_data(
        self, 
        data: List[Union[int, float]], 
        scale_factor: float = 1.0
    ) -> List[float]:
        """处理数值数据列表。

        Args:
            data: 要处理的数值列表
            scale_factor: 缩放因子

        Raises:
            ValueError: 如果输入数据超过限制
        """
        try:
            result = [float(x) * scale_factor for x in data]
            logger.info(f"Processed {len(result)} items")
            return result
        except (TypeError, ValueError) as e:
            logger.error(f"Error: {str(e)}")
            raise
```

### 检查重点
- 完整的文档（包含参数和异常说明）
- 异常处理和日志记录
- 代码复杂度控制
- 安全漏洞扫描
- 测试覆盖率要求（>80%）

### 运行检查
```bash
# 代码质量检查
poetry run pylint src tests
poetry run bandit -r .

# 测试覆盖率
poetry run pytest --cov=src --cov-fail-under=80
```

## 高级级别检查

高级级别的检查进一步要求：
1. 高级类型检查
2. 性能优化
3. 并发安全
4. 资源管理
5. 深度安全分析

### 示例代码
```python
class ResourceManager(Generic[T]):
    """资源管理器，展示高级级别的代码质量要求。"""

    async def __aenter__(self) -> T:
        """异步上下文管理器入口。"""
        async with self._lock:
            if self._resource is not None:
                raise RuntimeError("Resource already in use")
            self._resource = self._factory()
            return self._resource

    async def process_batch(
        self, 
        items: List[Union[int, float]]
    ) -> AsyncIterator[List[float]]:
        """异步批处理数据。"""
        with self.performance_logging("Processing batch"):
            results = await asyncio.get_event_loop().run_in_executor(
                self._executor,
                lambda: [float(x) * 2 for x in items]
            )
            yield results
```

### 检查重点
- 泛型和高级类型
- 并发安全性
- 性能监控
- 资源管理
- 深度安全分析
- 高测试覆盖率（>95%）

### 运行检查
```bash
# 高级安全检查
poetry run bandit -r . -c bandit.yaml
poetry run safety check

# 性能分析
poetry run scalene src/

# 复杂度检查
poetry run radon cc src/

# 完整测试套件
poetry run pytest --cov=src --cov-fail-under=95
```

## 检查工具配置

### 基础级别
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### 标准级别
```yaml
# 在基础级别基础上添加
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.0
    hooks:
      - id: bandit
  - repo: https://github.com/PyCQA/pylint
    rev: v2.17.0
    hooks:
      - id: pylint
```

### 高级级别
```yaml
# 在标准级别基础上添加
  - repo: local
    hooks:
      - id: security-checks
        name: Security Checks
        entry: bash -c 'poetry run bandit -r . && poetry run safety check'
      - id: performance-checks
        name: Performance Checks
        entry: bash -c 'poetry run scalene src/'
```

## 最佳实践建议

1. **渐进式采用**
   - 从基础级别开始
   - 随项目发展提高要求
   - 根据团队反馈调整

2. **自动化集成**
   - 配置 pre-commit 钩子
   - 设置 CI/CD 流程
   - 自动化报告生成

3. **团队协作**
   - 统一代码规范
   - 定期代码审查
   - 持续改进流程 