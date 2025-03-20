# 工具模块 API 文档

`utils` 模块提供了一组通用的工具函数，用于简化常见的开发任务。

## JSON 操作

### load_json()

从JSON文件加载数据。

```python
from typing import Any, Dict

def load_json(file_path: str) -> Dict[str, Any]:
    """从JSON文件加载数据。

    Args:
        file_path (str): JSON文件路径

    Returns:
        Dict[str, Any]: 加载的JSON数据

    Raises:
        FileNotFoundError: 文件不存在时抛出
        json.JSONDecodeError: JSON格式错误时抛出
    """
```

#### 示例

```python
from your_package.utils import load_json

try:
    # 加载配置文件
    config = load_json('config.json')
    print(f"加载的配置: {config}")
except FileNotFoundError:
    print("配置文件不存在")
except json.JSONDecodeError:
    print("配置文件格式错误")
```

### save_json()

保存数据到JSON文件。

```python
from typing import Any, Dict

def save_json(data: Dict[str, Any], file_path: str) -> None:
    """保存数据到JSON文件。

    Args:
        data (Dict[str, Any]): 要保存的数据
        file_path (str): 目标文件路径

    Raises:
        OSError: 写入文件失败时抛出
    """
```

#### 示例

```python
from your_package.utils import save_json

config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "settings": {
        "debug": True,
        "log_level": "INFO"
    }
}

try:
    save_json(config, 'config.json')
    print("配置已保存")
except OSError as e:
    print(f"保存配置失败: {e}")
```

## 日志配置

### setup_logging()

配置日志系统。

```python
from typing import Optional
import logging

def setup_logging(
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> None:
    """设置日志配置。

    Args:
        log_file (Optional[str]): 日志文件路径，如果为None则只输出到控制台
        level (int): 日志级别
        format_str (str): 日志格式字符串
    """
```

#### 示例

```python
from your_package.utils import setup_logging
import logging

# 基本配置
setup_logging()
logging.info("使用默认配置的日志")

# 输出到文件
setup_logging(
    log_file='app.log',
    level=logging.DEBUG,
    format_str='%(asctime)s [%(levelname)s] %(message)s'
)
logging.debug("调试信息会被写入文件")
```

## 最佳实践

### JSON 操作

1. **错误处理**
   ```python
   from your_package.utils import load_json, save_json
   
   def safe_load_config(path: str) -> Dict[str, Any]:
       try:
           return load_json(path)
       except FileNotFoundError:
           # 文件不存在时使用默认配置
           default_config = {"setting": "default"}
           save_json(default_config, path)
           return default_config
       except json.JSONDecodeError:
           # JSON格式错误时备份原文件并使用默认配置
           import shutil
           shutil.copy2(path, f"{path}.backup")
           default_config = {"setting": "default"}
           save_json(default_config, path)
           return default_config
   ```

2. **路径处理**
   ```python
   from pathlib import Path
   from your_package.utils import load_json
   
   def load_project_config():
       config_dir = Path.home() / ".myapp"
       config_dir.mkdir(exist_ok=True)
       config_file = config_dir / "config.json"
       return load_json(str(config_file))
   ```

### 日志配置

1. **模块级日志器**
   ```python
   from your_package.utils import setup_logging
   import logging
   
   # 创建模块级日志器
   logger = logging.getLogger(__name__)
   
   def setup_module():
       setup_logging(
           log_file='module.log',
           level=logging.INFO
       )
       logger.info("模块初始化完成")
   ```

2. **分级日志**
   ```python
   from your_package.utils import setup_logging
   import logging
   import os
   
   def setup_app_logging(app_name: str):
       # 创建日志目录
       log_dir = f"logs/{app_name}"
       os.makedirs(log_dir, exist_ok=True)
       
       # 错误日志
       setup_logging(
           log_file=f"{log_dir}/error.log",
           level=logging.ERROR
       )
       
       # 信息日志
       setup_logging(
           log_file=f"{log_dir}/info.log",
           level=logging.INFO
       )
   ```

## 开发指南

### 添加新工具函数

添加新的工具函数时，请遵循以下原则：

1. **通用性**
   - 函数应该解决常见问题
   - 避免特定业务逻辑
   - 保持简单和直观

2. **文档完整性**
   - 详细的文档字符串
   - 参数和返回值说明
   - 异常说明
   - 使用示例

3. **错误处理**
   - 明确定义可能的异常
   - 提供有意义的错误信息
   - 考虑恢复策略

4. **类型注解**
   - 使用类型提示
   - 支持静态类型检查
   - 文档中包含类型信息

### 示例模板

```python
from typing import TypeVar, Optional, Callable
import logging

T = TypeVar('T')

def retry_operation(
    operation: Callable[[], T],
    max_attempts: int = 3,
    delay: float = 1.0,
    logger: Optional[logging.Logger] = None
) -> Optional[T]:
    """重试执行操作直到成功或达到最大尝试次数。

    Args:
        operation: 要执行的操作函数
        max_attempts: 最大尝试次数
        delay: 重试之间的延迟（秒）
        logger: 可选的日志记录器

    Returns:
        操作的结果，如果所有尝试都失败则返回None

    Example:
        >>> def unstable_operation():
        ...     import random
        ...     if random.random() < 0.5:
        ...         raise ValueError("操作失败")
        ...     return "成功"
        ...
        >>> result = retry_operation(unstable_operation)
        >>> print(result)
    """
    import time
    
    log = logger or logging.getLogger(__name__)
    
    for attempt in range(max_attempts):
        try:
            return operation()
        except Exception as e:
            log.warning(f"第{attempt + 1}次尝试失败: {e}")
            if attempt < max_attempts - 1:
                time.sleep(delay)
    
    return None
``` 