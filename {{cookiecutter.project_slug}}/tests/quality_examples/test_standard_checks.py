"""标准级别检查的测试示例。

这个模块展示了标准级别检查会关注的代码质量问题，包括：
1. 完整的文档字符串
2. 异常处理
3. 代码复杂度控制
4. 安全性检查
"""
import logging
from typing import List, Optional, Union
from unittest.mock import patch

logger = logging.getLogger(__name__)


class DataProcessor:
    """数据处理类，展示标准级别的代码质量要求。

    这个类展示了：
    1. 完整的类文档
    2. 方法级别的文档
    3. 异常处理
    4. 日志记录
    """

    def __init__(self, max_items: int = 100):
        """初始化数据处理器。

        Args:
            max_items: 最大处理项数，默认为100

        Raises:
            ValueError: 如果max_items小于等于0
        """
        if max_items <= 0:
            raise ValueError("max_items must be positive")
        self.max_items = max_items
        self._processed_count = 0

    def process_data(
        self, data: List[Union[int, float]], scale_factor: float = 1.0
    ) -> List[float]:
        """处理数值数据列表。

        Args:
            data: 要处理的数值列表
            scale_factor: 缩放因子，默认为1.0

        Returns:
            处理后的数值列表

        Raises:
            ValueError: 如果输入数据超过最大项数限制
            TypeError: 如果输入包含非数值类型
        """
        if len(data) > self.max_items:
            logger.error(
                f"Input data exceeds max items: {len(data)} > {self.max_items}"
            )
            raise ValueError(f"Too many items: {len(data)} > {self.max_items}")

        try:
            result = [float(x) * scale_factor for x in data]
            self._processed_count += len(result)
            logger.info(f"Successfully processed {len(result)} items")
            return result
        except (TypeError, ValueError) as e:
            logger.error(f"Error processing data: {str(e)}")
            raise TypeError("All items must be numeric") from e

    @property
    def processed_count(self) -> int:
        """获取已处理的数据项总数。

        Returns:
            已处理的数据项总数
        """
        return self._processed_count


def test_data_processor():
    """测试DataProcessor类的功能。"""
    processor = DataProcessor(max_items=5)

    # 测试正常处理
    input_data = [1, 2, 3]
    expected = [2.0, 4.0, 6.0]
    assert processor.process_data(input_data, scale_factor=2.0) == expected

    # 测试异常处理
    with patch.object(logger, "error") as mock_logger:
        try:
            processor.process_data([1, 2, 3, 4, 5, 6])
            assert False, "Should raise ValueError"
        except ValueError:
            mock_logger.assert_called_once()

    # 测试属性访问
    assert processor.processed_count == 3

    # 测试类型错误
    with patch.object(logger, "error") as mock_logger:
        try:
            processor.process_data([1, "2", 3])
            assert False, "Should raise TypeError"
        except TypeError:
            mock_logger.assert_called_once()
