"""命令行工具示例."""
import asyncio
import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from src.core.cache import cache
from src.core.database import db
from src.monitoring import health
from src.utils.logging import configure_logging, get_logger

logger = get_logger(__name__)
console = Console()


@click.group()
def cli() -> None:
    """项目管理CLI工具."""
    configure_logging()


@cli.command()
def status() -> None:
    """检查系统状态."""
    # 创建状态表格
    table = Table(title="系统状态")
    table.add_column("服务", style="cyan")
    table.add_column("状态", style="green")

    # 获取健康状态
    health_status = health.check_health()
    table.add_row("系统", "✓ 正常" if health_status.status == "healthy" else "✗ 异常")

    # 检查数据库连接
    try:
        asyncio.run(db.check_connection())
        table.add_row("数据库", "✓ 已连接")
    except Exception as e:
        logger.error("数据库连接失败", exc_info=e)
        table.add_row("数据库", "✗ 未连接")

    # 检查缓存连接
    try:
        asyncio.run(cache.check_connection())
        table.add_row("缓存", "✓ 已连接")
    except Exception as e:
        logger.error("缓存连接失败", exc_info=e)
        table.add_row("缓存", "✗ 未连接")

    console.print(table)


@cli.command()
@click.argument("key")
@click.argument("value", required=False)
@click.option("--ttl", type=int, help="缓存过期时间（秒）")
def cache_op(key: str, value: Optional[str], ttl: Optional[int]) -> None:
    """缓存操作.

    Args:
        key: 缓存键
        value: 缓存值（如果不提供则为获取操作）
        ttl: 过期时间
    """
    async def _cache_op() -> None:
        if value is None:
            # 获取缓存
            result = await cache.get(key)
            if result is None:
                console.print(f"键 [cyan]{key}[/cyan] 不存在")
            else:
                console.print(f"键 [cyan]{key}[/cyan] 的值为: [green]{result}[/green]")
        else:
            # 设置缓存
            await cache.set(key, value, expire=ttl)
            console.print(
                f"已设置键 [cyan]{key}[/cyan] 的值为: [green]{value}[/green]"
                f"{f'，过期时间为 {ttl} 秒' if ttl else ''}"
            )

    try:
        asyncio.run(_cache_op())
    except Exception as e:
        logger.error("缓存操作失败", exc_info=e)
        sys.exit(1)


@cli.command()
def clear_cache() -> None:
    """清除所有缓存."""
    async def _clear_cache() -> None:
        if cache._redis is None:
            await cache.connect()
        await cache._redis.flushall()  # type: ignore

    try:
        asyncio.run(_clear_cache())
        console.print("[green]缓存已清除[/green]")
    except Exception as e:
        logger.error("清除缓存失败", exc_info=e)
        sys.exit(1)


if __name__ == "__main__":
    cli()
