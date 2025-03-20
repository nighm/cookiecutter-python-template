"""自动更新 README 演示模块.

这个模块用于演示当添加新的 Python 文件时，
README.md 会自动更新模块文档。

Example:
    ```python
    calculator = Calculator()
    result = calculator.add(1, 2)
    print(result)  # 输出: 3
    ```
"""


class Calculator:
    """一个简单的计算器类.

    这个类提供基本的数学运算功能，包括加法、减法等。
    每个方法都有详细的文档说明。

    Attributes:
        history (list): 保存计算历史记录
    """

    def __init__(self):
        """初始化计算器实例."""
        self.history = []

    def add(self, a: float, b: float) -> float:
        """执行加法运算.

        Args:
            a (float): 第一个数
            b (float): 第二个数

        Returns:
            float: 两个数的和

        Example:
            ```python
            calc = Calculator()
            result = calc.add(1.5, 2.5)  # 返回 4.0
            ```
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """执行减法运算.

        Args:
            a (float): 被减数
            b (float): 减数

        Returns:
            float: 两个数的差

        Example:
            ```python
            calc = Calculator()
            result = calc.subtract(5, 3)  # 返回 2
            ```
        """
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def get_history(self) -> list:
        """获取计算历史记录.

        Returns:
            list: 包含所有计算历史的列表
        """
        return self.history
