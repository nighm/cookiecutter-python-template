"""示例模块

这个模块展示了如何正确编写Python代码的中文文档。
包含了类、函数、方法等各种代码元素的标准文档格式。

使用方法:
    from examples.documentation_example import DataProcessor
    
    processor = DataProcessor()
    result = processor.process_data({"name": "张三"})
"""

from typing import Dict, List, Optional
from datetime import datetime


class DataProcessor:
    """数据处理器
    
    这个类用于展示如何编写类的文档字符串，包括类的整体说明、
    属性说明、方法说明等。
    
    属性:
        cache_enabled (bool): 是否启用缓存
        max_items (int): 最大处理条目数
        
    示例:
        ```python
        processor = DataProcessor(cache_enabled=True)
        result = processor.process_data({"name": "张三"})
        ```
    """
    
    def __init__(self, cache_enabled: bool = True, max_items: int = 1000):
        """初始化数据处理器
        
        参数:
            cache_enabled: 是否启用缓存，默认为True
            max_items: 最大处理条目数，默认为1000
            
        示例:
            ```python
            processor = DataProcessor(cache_enabled=True, max_items=500)
            ```
        """
        self.cache_enabled = cache_enabled
        self.max_items = max_items
        self._cache = {}
    
    def process_data(self, data: Dict) -> Dict:
        """处理输入的数据
        
        这个方法展示了如何编写方法的详细文档，包括参数说明、
        返回值说明、异常说明等。
        
        参数:
            data: 要处理的数据字典
            
        返回:
            处理后的数据字典
            
        异常:
            ValueError: 当输入数据格式不正确时抛出
            
        示例:
            ```python
            data = {"name": "张三", "age": 30}
            result = processor.process_data(data)
            print(result)  # 输出处理后的数据
            ```
        """
        if not isinstance(data, dict):
            raise ValueError("输入数据必须是字典类型")
            
        # 处理逻辑...
        return data
    
    def batch_process(self, items: List[Dict]) -> List[Dict]:
        """批量处理多条数据
        
        参数:
            items: 数据字典列表
            
        返回:
            处理后的数据字典列表
            
        示例:
            ```python
            items = [
                {"name": "张三", "age": 30},
                {"name": "李四", "age": 25}
            ]
            results = processor.batch_process(items)
            ```
        """
        return [self.process_data(item) for item in items]


def format_date(date: datetime, format_str: str = "%Y-%m-%d") -> str:
    """格式化日期
    
    这个函数展示了如何编写独立函数的文档字符串。
    
    参数:
        date: 要格式化的日期
        format_str: 日期格式字符串，默认为 %Y-%m-%d
        
    返回:
        格式化后的日期字符串
        
    示例:
        ```python
        from datetime import datetime
        
        now = datetime.now()
        formatted = format_date(now, "%Y年%m月%d日")
        print(formatted)  # 输出: 2024年03月10日
        ```
    """
    return date.strftime(format_str)


class ConfigManager:
    """配置管理器
    
    用于管理应用程序的配置信息。
    
    属性:
        config_path (str): 配置文件路径
        auto_reload (bool): 是否自动重新加载
        
    示例:
        ```python
        config = ConfigManager("config.yml")
        db_url = config.get("database.url")
        ```
    """
    
    def __init__(self, config_path: str):
        """初始化配置管理器
        
        参数:
            config_path: 配置文件的路径
        """
        self.config_path = config_path
        self._config = {}
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """获取配置值
        
        参数:
            key: 配置键名
            default: 默认值，当键不存在时返回
            
        返回:
            配置值或默认值
            
        示例:
            ```python
            db_url = config.get("database.url", "sqlite:///db.sqlite3")
            ```
        """
        return self._config.get(key, default)


if __name__ == "__main__":
    # 使用示例
    processor = DataProcessor(cache_enabled=True)
    data = {"name": "张三", "age": 30}
    result = processor.process_data(data)
    print(f"处理结果: {result}")
    
    # 日期格式化示例
    current_time = datetime.now()
    formatted_date = format_date(current_time, "%Y年%m月%d日")
    print(f"当前日期: {formatted_date}")
    
    # 配置管理示例
    config = ConfigManager("config.yml")
    db_url = config.get("database.url", "默认数据库地址")
    print(f"数据库地址: {db_url}") 