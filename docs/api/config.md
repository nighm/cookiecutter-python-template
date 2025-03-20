# 配置模块 API 文档

`config` 模块提供了项目配置的管理功能。

## Config 类

### 基本用法

```python
from your_package.config import Config

# 使用默认配置路径
config = Config()

# 使用自定义配置路径
config = Config("/path/to/config.json")

# 获取配置项
log_level = config.get("log_level", "INFO")

# 设置配置项
config.set("debug", True)

# 保存配置
config.save()
```

### 构造函数

```python
def __init__(self, config_path: Optional[str] = None):
    """初始化配置管理器。

    Args:
        config_path: 配置文件路径，如果为None则使用默认路径
            默认路径为：~/.your_package/config.json
    """
```

### 方法

#### get()

获取配置项的值。

```python
def get(self, key: str, default: Any = None) -> Any:
    """获取配置项。

    Args:
        key: 配置项键名
        default: 默认值，当配置项不存在时返回

    Returns:
        配置项的值
    """
```

示例：
```python
config = Config()

# 获取日志级别，默认为 "INFO"
log_level = config.get("log_level", "INFO")

# 获取调试模式，默认为 False
debug = config.get("debug", False)
```

#### set()

设置配置项的值。

```python
def set(self, key: str, value: Any) -> None:
    """设置配置项。

    Args:
        key: 配置项键名
        value: 配置项的值
    """
```

示例：
```python
config = Config()

# 设置日志级别
config.set("log_level", "DEBUG")

# 设置调试模式
config.set("debug", True)

# 保存更改
config.save()
```

#### update()

批量更新配置项。

```python
def update(self, config_dict: Dict[str, Any]) -> None:
    """更新多个配置项。

    Args:
        config_dict: 包含配置项的字典
    """
```

示例：
```python
config = Config()

# 批量更新配置
config.update({
    "app_name": "MyApp",
    "version": "1.0.0",
    "settings": {
        "debug": True,
        "log_level": "INFO"
    }
})

# 保存更改
config.save()
```

#### save()

保存当前配置到文件。

```python
def save(self) -> None:
    """保存当前配置到文件。"""
```

#### all

获取所有配置项的属性。

```python
@property
def all(self) -> Dict[str, Any]:
    """获取所有配置项。

    Returns:
        包含所有配置项的字典
    """
```

示例：
```python
config = Config()

# 获取所有配置
all_config = config.all
print("当前配置:", all_config)
```

## 最佳实践

### 1. 配置初始化

```python
from your_package.config import Config

def initialize_app():
    # 创建配置实例
    config = Config()
    
    # 设置默认值
    if not config.get("initialized"):
        config.update({
            "initialized": True,
            "app_name": "MyApp",
            "version": "1.0.0",
            "log_level": "INFO",
            "debug": False
        })
        config.save()
    
    return config
```

### 2. 配置验证

```python
from typing import Dict, Any
from your_package.config import Config

def validate_config(config: Dict[str, Any]) -> bool:
    """验证配置是否有效。"""
    required_fields = {"app_name", "version", "log_level"}
    return all(field in config for field in required_fields)

def get_validated_config() -> Config:
    config = Config()
    
    if not validate_config(config.all):
        raise ValueError("配置无效：缺少必要字段")
    
    return config
```

### 3. 环境特定配置

```python
import os
from your_package.config import Config

def load_environment_config() -> Config:
    """根据环境加载不同的配置。"""
    env = os.getenv("APP_ENV", "development")
    
    config = Config(f"config/{env}.json")
    
    # 添加环境特定的配置
    config.update({
        "environment": env,
        "debug": env == "development"
    })
    
    return config
```

### 4. 配置监听

```python
from typing import Callable, Dict, Any
from your_package.config import Config

class ConfigManager:
    def __init__(self):
        self.config = Config()
        self._listeners: Dict[str, list[Callable]] = {}
    
    def add_listener(self, key: str, callback: Callable[[Any], None]):
        """添加配置变更监听器。"""
        if key not in self._listeners:
            self._listeners[key] = []
        self._listeners[key].append(callback)
    
    def set(self, key: str, value: Any):
        """设置配置并通知监听器。"""
        old_value = self.config.get(key)
        self.config.set(key, value)
        
        if key in self._listeners and old_value != value:
            for callback in self._listeners[key]:
                callback(value)
```

## 开发指南

### 扩展配置功能

1. **添加配置验证**
   ```python
   from dataclasses import dataclass
   from typing import Optional
   
   @dataclass
   class AppConfig:
       app_name: str
       version: str
       log_level: str
       debug: bool = False
       
   class ValidatedConfig(Config):
       def __init__(self, config_path: Optional[str] = None):
           super().__init__(config_path)
           self.validate()
       
       def validate(self):
           """验证配置并转换为强类型。"""
           config_data = self.all
           try:
               self.app_config = AppConfig(**config_data)
           except TypeError as e:
               raise ValueError(f"配置验证失败: {e}")
   ```

2. **添加配置加密**
   ```python
   from cryptography.fernet import Fernet
   import base64
   
   class EncryptedConfig(Config):
       def __init__(self, config_path: Optional[str] = None, key: Optional[str] = None):
           self._key = key or os.getenv("CONFIG_KEY")
           if not self._key:
               raise ValueError("需要加密密钥")
           
           self._fernet = Fernet(base64.b64encode(self._key.encode()))
           super().__init__(config_path)
       
       def _load_config(self) -> None:
           """加载并解密配置。"""
           with open(self.config_path, 'rb') as f:
               encrypted_data = f.read()
           decrypted_data = self._fernet.decrypt(encrypted_data)
           self._config = json.loads(decrypted_data)
       
       def save(self) -> None:
           """加密并保存配置。"""
           data = json.dumps(self._config).encode()
           encrypted_data = self._fernet.encrypt(data)
           with open(self.config_path, 'wb') as f:
               f.write(encrypted_data)
   ```

### 配置最佳实践

1. **使用环境变量覆盖**
   ```python
   import os
   
   class EnvAwareConfig(Config):
       def get(self, key: str, default: Any = None) -> Any:
           # 检查环境变量
           env_key = f"APP_{key.upper()}"
           if env_key in os.environ:
               return os.environ[env_key]
           
           return super().get(key, default)
   ```

2. **配置版本控制**
   ```python
   class VersionedConfig(Config):
       def __init__(self, config_path: Optional[str] = None):
           super().__init__(config_path)
           self._upgrade_if_needed()
       
       def _upgrade_if_needed(self):
           current_version = self.get("config_version", 0)
           if current_version < 1:
               self._upgrade_to_v1()
           if current_version < 2:
               self._upgrade_to_v2()
           
       def _upgrade_to_v1(self):
           # 执行版本1的升级
           self.set("config_version", 1)
           self.save()
   ```

3. **配置备份**
   ```python
   import shutil
   from datetime import datetime
   
   class BackupConfig(Config):
       def save(self) -> None:
           # 创建备份
           if os.path.exists(self.config_path):
               timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
               backup_path = f"{self.config_path}.{timestamp}.bak"
               shutil.copy2(self.config_path, backup_path)
           
           super().save()
   ``` 