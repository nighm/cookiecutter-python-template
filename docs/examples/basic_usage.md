# 基础使用示例

本文档提供了项目的基本使用示例，帮助您快速上手。

## 1. 数据处理示例

### 1.1 基本数据处理

```python
from your_package.data_processor import DataProcessor
from your_package.models import DataModel
from typing import List

def process_data(raw_data: List[dict]) -> List[DataModel]:
    """处理原始数据并返回处理后的数据模型列表。"""
    processor = DataProcessor()
    
    # 数据验证和转换
    validated_data = [
        DataModel(**item)
        for item in raw_data
    ]
    
    # 数据处理
    processed_data = processor.process_batch(validated_data)
    
    return processed_data

# 使用示例
raw_data = [
    {"id": 1, "name": "示例1", "value": 100},
    {"id": 2, "name": "示例2", "value": 200}
]

results = process_data(raw_data)
```

### 1.2 异步数据处理

```python
import asyncio
from your_package.async_processor import AsyncDataProcessor

async def process_data_async(raw_data: List[dict]) -> List[DataModel]:
    """异步处理数据。"""
    processor = AsyncDataProcessor()
    
    # 并行处理数据
    tasks = [
        processor.process_item(item)
        for item in raw_data
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# 使用示例
async def main():
    raw_data = [
        {"id": 1, "name": "示例1", "value": 100},
        {"id": 2, "name": "示例2", "value": 200}
    ]
    
    results = await process_data_async(raw_data)
    print(results)

asyncio.run(main())
```

## 2. 配置管理示例

### 2.1 基本配置

```python
from your_package.config import Settings
from pydantic import BaseModel

class AppSettings(BaseModel):
    """应用配置模型。"""
    debug: bool = False
    api_key: str
    max_workers: int = 4

# 从环境变量加载配置
settings = Settings()
app_settings = AppSettings(**settings.dict())
```

### 2.2 环境变量配置

```bash
# .env 文件示例
DEBUG=true
API_KEY=your-api-key
MAX_WORKERS=8
```

```python
from your_package.config import load_env_config

# 加载环境变量
config = load_env_config()
print(f"Debug模式: {config.debug}")
print(f"API密钥: {config.api_key}")
```

## 3. 日志记录示例

### 3.1 基本日志记录

```python
from your_package.logger import get_logger

logger = get_logger(__name__)

def some_function():
    logger.info("开始处理", extra={"process_id": 123})
    try:
        # 业务逻辑
        result = process_data()
        logger.info("处理完成", extra={"result": result})
    except Exception as e:
        logger.error("处理失败", exc_info=True)
```

### 3.2 结构化日志

```python
from your_package.logger import StructuredLogger

logger = StructuredLogger(__name__)

def process_order(order_id: str):
    with logger.context(order_id=order_id):
        logger.info("开始处理订单")
        # 处理逻辑
        logger.info("订单处理完成")
```

## 4. 数据库操作示例

### 4.1 基本数据库操作

```python
from your_package.database import Database
from your_package.models import User

async def get_user(user_id: int) -> User:
    """获取用户信息。"""
    async with Database() as db:
        query = """
            SELECT id, name, email
            FROM users
            WHERE id = :user_id
        """
        result = await db.fetch_one(
            query=query,
            values={"user_id": user_id}
        )
        return User(**result)

# 使用示例
user = await get_user(123)
print(f"用户名: {user.name}")
```

### 4.2 事务处理

```python
from your_package.database import transaction

async def transfer_money(
    from_account: int,
    to_account: int,
    amount: float
):
    """转账操作示例。"""
    async with transaction() as tx:
        # 扣款
        await tx.execute(
            "UPDATE accounts SET balance = balance - :amount "
            "WHERE id = :account_id",
            {"amount": amount, "account_id": from_account}
        )
        
        # 入账
        await tx.execute(
            "UPDATE accounts SET balance = balance + :amount "
            "WHERE id = :account_id",
            {"amount": amount, "account_id": to_account}
        )
```

## 5. API集成示例

### 5.1 REST API客户端

```python
from your_package.client import APIClient

async def get_data_from_api():
    """从外部API获取数据。"""
    client = APIClient(
        base_url="https://api.example.com",
        api_key="your-api-key"
    )
    
    # GET请求
    response = await client.get("/data")
    
    # POST请求
    data = {"name": "test", "value": 100}
    response = await client.post("/data", json=data)
    
    return response.json()
```

### 5.2 WebSocket客户端

```python
from your_package.client import WSClient

async def listen_to_updates():
    """监听WebSocket更新。"""
    async with WSClient("wss://api.example.com/ws") as ws:
        while True:
            msg = await ws.receive_json()
            print(f"收到更新: {msg}")
```

## 6. 测试示例

### 6.1 单元测试

```python
import pytest
from your_package.data_processor import DataProcessor

def test_data_processing():
    """测试数据处理功能。"""
    # 准备测试数据
    test_data = [
        {"id": 1, "value": 100},
        {"id": 2, "value": 200}
    ]
    
    # 初始化处理器
    processor = DataProcessor()
    
    # 执行处理
    result = processor.process_batch(test_data)
    
    # 验证结果
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].value == 100
```

### 6.2 异步测试

```python
import pytest
from your_package.async_processor import AsyncProcessor

@pytest.mark.asyncio
async def test_async_processing():
    """测试异步处理功能。"""
    processor = AsyncProcessor()
    
    # 执行异步操作
    result = await processor.process_item({"id": 1})
    
    # 验证结果
    assert result.id == 1
```

## 7. 命令行工具示例

### 7.1 基本CLI命令

```python
import click
from your_package.cli import cli

@cli.command()
@click.option("--input", "-i", required=True, help="输入文件路径")
@click.option("--output", "-o", required=True, help="输出文件路径")
def process(input: str, output: str):
    """处理输入文件并保存结果。"""
    click.echo(f"处理文件: {input}")
    # 处理逻辑
    click.echo(f"结果已保存至: {output}")

if __name__ == "__main__":
    cli()
```

### 7.2 进度显示

```python
import click
from your_package.processor import process_items

def process_with_progress(items):
    """带进度显示的处理函数。"""
    with click.progressbar(items) as bar:
        for item in bar:
            process_items(item)
```

## 8. 错误处理示例

### 8.1 自定义异常

```python
from your_package.exceptions import AppError

class ValidationError(AppError):
    """数据验证错误。"""
    pass

class ProcessingError(AppError):
    """处理过程错误。"""
    pass

def validate_data(data: dict):
    """数据验证示例。"""
    if not data.get("id"):
        raise ValidationError("缺少ID字段")
    if data.get("value") < 0:
        raise ValidationError("值不能为负数")
```

### 8.2 错误处理

```python
from your_package.exceptions import AppError
from your_package.logger import get_logger

logger = get_logger(__name__)

def process_with_error_handling(data: dict):
    """带错误处理的处理函数。"""
    try:
        validate_data(data)
        # 处理逻辑
    except ValidationError as e:
        logger.error("数据验证失败", exc_info=True)
        raise
    except ProcessingError as e:
        logger.error("处理失败", exc_info=True)
        raise
    except Exception as e:
        logger.error("未知错误", exc_info=True)
        raise AppError("处理过程中发生未知错误") from e
``` 