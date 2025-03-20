开发指南
========

开发流程
-------

1. 分支管理
^^^^^^^^^

我们使用Git Flow作为分支管理策略：

* `main`: 生产环境分支
* `develop`: 开发环境分支
* `feature/*`: 功能分支
* `release/*`: 发布分支
* `hotfix/*`: 热修复分支

2. 提交规范
^^^^^^^^^

使用约定式提交（Conventional Commits）规范：

* `feat`: 新功能
* `fix`: 修复bug
* `docs`: 文档更新
* `style`: 代码格式调整
* `refactor`: 代码重构
* `test`: 测试相关
* `chore`: 构建过程或辅助工具的变动

示例::

    feat(auth): 添加用户认证功能
    fix(db): 修复数据库连接泄露问题
    docs(api): 更新API文档

3. 代码审查
^^^^^^^^^

所有代码变更必须通过代码审查：

1. 创建Pull Request
2. 运行自动化测试
3. 代码审查者审查
4. 解决反馈意见
5. 合并到目标分支

编码规范
-------

Python规范
^^^^^^^^

1. 代码风格遵循PEP 8
2. 使用类型注解
3. 编写文档字符串
4. 保持函数简单明了

示例代码::

    def calculate_average(numbers: list[float]) -> float:
        """计算数字列表的平均值.

        Args:
            numbers: 要计算平均值的数字列表

        Returns:
            数字列表的平均值

        Raises:
            ValueError: 如果列表为空
        """
        if not numbers:
            raise ValueError("数字列表不能为空")
        return sum(numbers) / len(numbers)

文档规范
^^^^^^^

1. 所有公共API必须有文档字符串
2. 使用reStructuredText格式
3. 包含参数和返回值说明
4. 提供使用示例

测试规范
^^^^^^^

1. 单元测试覆盖率要求80%以上
2. 每个功能模块都要有测试
3. 测试代码要简洁清晰
4. 使用pytest作为测试框架

示例测试::

    def test_calculate_average():
        """测试计算平均值函数."""
        numbers = [1.0, 2.0, 3.0]
        assert calculate_average(numbers) == 2.0

        with pytest.raises(ValueError):
            calculate_average([])

发布流程
-------

1. 版本管理
^^^^^^^^^

使用语义化版本（Semantic Versioning）:

* 主版本号：不兼容的API修改
* 次版本号：向下兼容的功能性新增
* 修订号：向下兼容的问题修正

2. 发布步骤
^^^^^^^^^

1. 更新版本号
2. 更新CHANGELOG
3. 创建发布分支
4. 运行测试套件
5. 生成文档
6. 创建发布标签
7. 发布到PyPI

3. 发布检查清单
^^^^^^^^^^^^

* [ ] 所有测试通过
* [ ] 文档已更新
* [ ] CHANGELOG已更新
* [ ] 版本号已更新
* [ ] 依赖已更新
* [ ] 性能测试通过
* [ ] 安全检查通过
