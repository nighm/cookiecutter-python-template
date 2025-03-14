"""数据处理模块。

此模块提供了数据加载和处理的基本功能。
"""

import json
import os.path
from datetime import datetime
from typing import Any, Dict, List, cast


def load_data(filepath: str) -> Dict[str, Any]:
    """从JSON文件加载数据。

    Args:
        filepath: 要加载的JSON文件路径

    Returns:
        加载的数据字典

    Raises:
        FileNotFoundError: 如果文件不存在
        json.JSONDecodeError: 如果文件不是有效的JSON
    """
    with open(filepath, encoding="utf-8") as f:
        return cast(Dict[str, Any], json.load(f))


class DataProcessor:
    """数据处理器类。

    用于处理和转换数据的主类。

    Attributes:
        data_dir: 数据目录的路径
    """

    def __init__(self, data_dir: str) -> None:
        """初始化数据处理器。

        Args:
            data_dir: 数据目录的路径
        """
        self.data_dir = data_dir

    def process_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """处理项目列表。

        Args:
            items: 要处理的项目列表

        Returns:
            处理后的项目列表
        """
        processed = []
        for item in items:
            if (
                isinstance(item, dict)
                and item.get("value", 0) > 0
                and item.get("name", "").strip()
            ):
                processed.append(self._process_item(item))
        return processed

    def _process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """处理单个项目。

        Args:
            item: 要处理的项目

        Returns:
            处理后的项目，包含processed_value和name字段
        """
        return {
            "processed_value": f"Processed: {item['value']}",
            "name": item["name"]
        }

    def save_results(self, results: List[Dict[str, Any]], filename: str) -> None:
        """保存处理结果到文件。

        Args:
            results: 要保存的结果
            filename: 输出文件名
        """
        filepath = os.path.join(self.data_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(results, f)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Saved at {current_time}")

    def load_and_process(self, input_file: str) -> None:
        """加载并处理数据。

        Args:
            input_file: 输入文件路径

        Raises:
            FileNotFoundError: 如果输入文件不存在
            json.JSONDecodeError: 如果输入文件不是有效的JSON
            ValueError: 如果输入数据不是列表格式
        """
        try:
            data = load_data(input_file)
            if not isinstance(data, list):
                raise ValueError("Input data must be a list")
            results = self.process_items(data)
            self.save_results(results, "output.json")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error processing file: {e}")
            raise
