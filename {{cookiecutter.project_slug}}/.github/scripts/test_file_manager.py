#!/usr/bin/env python3
"""
文件管理器测试
"""

import os
import pytest
from pathlib import Path
from file_manager import get_file_manager


@pytest.fixture
def file_manager():
    """创建文件管理器实例"""
    return get_file_manager()


def test_find_similar_files(file_manager, tmp_path):
    """测试查找相似文件"""
    # 创建测试文件
    test_content = "test content"
    test_file = tmp_path / "test.yml"
    test_file.write_text(test_content)

    # 查找文件（在临时目录中）
    similar_files = file_manager.find_similar_files("test.yml", str(tmp_path))
    assert len(similar_files) >= 1
    assert similar_files[0].content == test_content


def test_suggest_directory(file_manager):
    """测试目录建议"""
    # 测试配置文件
    config_dir = file_manager.suggest_directory("test.yml")
    assert "config" in config_dir.lower()

    # 测试Python脚本
    script_dir = file_manager.suggest_directory("test.py")
    assert "script" in script_dir.lower()


def test_create_or_update_file(file_manager, tmp_path):
    """测试文件创建和更新"""
    test_content = "test content"
    test_file = "test.yml"

    # 创建新文件
    success, message = file_manager.create_or_update_file(
        test_file, test_content, str(tmp_path)
    )
    assert success
    assert "创建新文件" in message

    # 尝试创建相同内容的文件
    success, message = file_manager.create_or_update_file(
        test_file, test_content, str(tmp_path)
    )
    assert success
    assert "已存在" in message

    # 尝试更新文件（内容相似度高）
    new_content = test_content + "\n# Add comment"  # 使用英文注释
    success, message = file_manager.create_or_update_file(
        test_file, new_content, str(tmp_path)
    )
    assert success
    assert "更新文件" in message

    # 验证文件内容已更新
    with open(tmp_path / test_file, "r", encoding=file_manager.encoding) as f:
        content = f.read()
    assert content == new_content


def test_move_file(file_manager, tmp_path):
    """测试文件移动"""
    # 创建源文件
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    source_file = source_dir / "test.yml"
    source_file.write_text("test content")

    # 创建目标目录
    target_dir = tmp_path / "target"
    target_dir.mkdir()

    # 移动文件
    success, message = file_manager.move_file(
        str(source_file), str(target_dir / "test.yml")
    )
    assert success
    assert "已移动到" in message

    # 验证文件已移动
    assert not source_file.exists()
    assert (target_dir / "test.yml").exists()


if __name__ == "__main__":
    pytest.main([__file__])
