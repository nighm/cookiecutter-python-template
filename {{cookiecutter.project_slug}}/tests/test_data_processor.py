"""数据处理器测试模块。"""

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from {{cookiecutter.package_name}}.data_processor import DataProcessor
from {{cookiecutter.package_name}}.data_processor import load_data


def test_load_data(tmp_path: Path) -> None:
    """测试数据加载功能。"""
    # 创建测试数据
    data_file = tmp_path / "test.json"
    test_data: Dict[str, str] = {"test": "data"}
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    # 测试加载
    data = load_data(str(data_file))
    assert data == test_data


def test_process_items() -> None:
    """测试项目处理功能。"""
    processor = DataProcessor("./data")
    items: List[Dict[str, Any]] = [
        {"value": 1, "name": "test1"},
        {"value": 2, "name": "test2"},
        {"value": 0, "name": "test3"},  # 应该被过滤掉
        {"value": 3, "name": ""},  # 应该被过滤掉
        {"value": 4},  # 应该被过滤掉
    ]
    results = processor.process_items(items)
    assert len(results) == 2
    assert all("processed_value" in result for result in results)


def test_save_results(tmp_path: Path) -> None:
    """测试结果保存功能。"""
    processor = DataProcessor(str(tmp_path))
    results: List[Dict[str, str]] = [{"processed_value": "test"}]
    filename = "output.json"

    processor.save_results(results, filename)

    output_file = tmp_path / filename
    assert output_file.exists()
    with open(output_file, encoding="utf-8") as f:
        saved_data = json.load(f)
    assert saved_data == results


def test_load_and_process_invalid_file(tmp_path: Path) -> None:
    """测试处理无效文件时的错误处理。"""
    processor = DataProcessor(str(tmp_path))
    invalid_file = tmp_path / "invalid.json"

    # 测试文件不存在的情况
    with pytest.raises(FileNotFoundError):
        processor.load_and_process(str(invalid_file))

    # 测试无效JSON的情况
    invalid_file.write_text("invalid json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        processor.load_and_process(str(invalid_file))


def test_load_and_process_invalid_data(tmp_path: Path) -> None:
    """测试处理无效数据格式时的错误处理。"""
    processor = DataProcessor(str(tmp_path))
    invalid_file = tmp_path / "invalid_format.json"
    
    # 测试非列表数据的情况
    with open(invalid_file, "w", encoding="utf-8") as f:
        json.dump({"not": "a list"}, f)
    
    with pytest.raises(ValueError, match="Input data must be a list"):
        processor.load_and_process(str(invalid_file)) 