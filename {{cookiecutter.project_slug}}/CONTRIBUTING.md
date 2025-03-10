# 贡献指南

感谢你考虑为Python项目模板做出贡献！

## 如何贡献

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 开发流程

### 1. 设置开发环境

```bash
# 克隆项目
git clone <your-fork-url>
cd python-project-template

# 安装依赖
poetry install

# 安装pre-commit钩子
poetry run pre-commit install
```

### 2. 开发规范

#### 代码风格

- 遵循PEP 8规范
- 使用Black格式化代码
- 添加类型注解
- 编写详细的文档字符串

#### 提交信息规范

使用约定式提交规范：

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码风格调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(core): 添加异步任务支持
fix(db): 修复连接池泄露问题
docs(api): 更新API文档
```

### 3. 测试

- 为新功能添加测试
- 确保所有测试通过
- 保持测试覆盖率

```bash
# 运行测试
poetry run pytest

# 检查覆盖率
poetry run pytest --cov=src
```

### 4. 文档

- 更新相关文档
- 添加新功能的使用示例
- 确保文档构建成功

```bash
# 构建文档
cd docs/zh && poetry run make html
cd docs/en && poetry run make html
```

## 提交问题和拉取请求

### 提交问题

1. 在GitHub上查看现有问题，确保您的问题尚未被报告。
2. 如果没有，点击“New Issue”按钮，填写问题描述。

### 提交拉取请求

1. Fork此仓库。
2. 创建一个新的分支：`git checkout -b my-feature-branch`
3. 在新分支上进行您的更改。
4. 提交更改：`git commit -m 'Add some feature'`
5. 推送到您的分支：`git push origin my-feature-branch`
6. 在GitHub上创建拉取请求。

## Pull Request 检查清单

提交PR前，请确保：

- [ ] 代码已格式化
- [ ] 添加了测试
- [ ] 所有测试通过
- [ ] 更新了文档
- [ ] 遵循提交信息规范
- [ ] 更新了CHANGELOG（如果适用）

## 功能建议

提出新功能建议时，请说明：

- 功能描述
- 使用场景
- 实现建议（可选）

## 行为准则

请保持专业和友善。我们欢迎所有建设性的贡献！

## 如何贡献

感谢您对本项目的兴趣！以下是如何贡献的步骤：

### 提交问题
1. 在GitHub上查看现有问题，确保您的问题尚未被报告。
2. 如果没有，点击“New Issue”按钮，填写问题描述。

### 提交拉取请求
1. Fork此仓库。
2. 创建一个新的分支：`git checkout -b my-feature-branch`
3. 在新分支上进行您的更改。
4. 提交更改：`git commit -m 'Add some feature'`
5. 推送到您的分支：`git push origin my-feature-branch`
6. 在GitHub上创建拉取请求。
