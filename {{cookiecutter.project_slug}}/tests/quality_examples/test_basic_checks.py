"""基础级别检查的测试示例。

这个模块展示了基础级别检查会关注的代码质量问题。
"""
from typing import List, Optional


def example_function(input_list: Optional[List[int]] = None) -> int:
    """计算列表中所有数字的和。

    Args:
        input_list: 输入的整数列表，默认为None

    Returns:
        列表中所有数字的和，如果列表为空或None则返回0
    """
    if input_list is None:
        return 0

    return sum(input_list)


def test_example_function():
    """测试示例函数的基本功能。"""
    # 基本功能测试
    assert example_function([1, 2, 3]) == 6

    # 边界条件测试
    assert example_function([]) == 0
    assert example_function(None) == 0

    # 类型提示检查
    numbers: List[int] = [1, 2, 3]
    result: int = example_function(numbers)
    assert result == 6
