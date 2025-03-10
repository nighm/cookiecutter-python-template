# 更新日志

本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范，并使用 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/) 的格式记录所有重要变更。

每个版本的变更按以下类别组织：
- `新增`: 新功能和特性
  - 影响范围：新功能对现有系统的影响程度
  - 依赖要求：新功能所需的外部依赖
  - 性能影响：对系统性能的潜在影响
- `变更`: 对现有功能的修改
  - ⚠️ Breaking Changes：不向后兼容的变更
  - 迁移说明：如何从旧版本迁移到新版本
  - 性能影响：变更对性能的影响评估
- `弃用`: 即将被移除的功能
  - 替代方案：推荐的替代功能或方法
  - 时间计划：预计在哪个版本完全移除
- `移除`: 已经移除的功能
  - 影响评估：对现有系统的影响
  - 迁移指南：如何适应功能移除
- `修复`: Bug修复
  - 问题描述：详细的问题描述和复现步骤
  - 修复方案：采用的修复方法
  - 影响范围：修复可能带来的副作用
- `安全`: 安全性相关的变更
  - 漏洞等级：安全漏洞的严重程度
  - CVE编号：关联的CVE编号（如有）
  - 修复方案：安全问题的解决方案
  - 影响评估：对系统安全的整体影响
- `性能`: 性能优化相关的变更
  - 优化指标：具体的性能提升数据
  - 测试环境：性能测试的环境配置
  - 影响范围：优化对其他模块的影响
- `文档`: 文档更新
  - 更新范围：文档更新的具体内容
  - 相关模块：受影响的代码模块
- `依赖`: 依赖项更新
  - 版本变化：依赖版本的具体变化
  - 兼容性：与其他依赖的兼容性评估
  - 安全影响：依赖更新带来的安全改进
- `工程`: 工程化相关变更
  - 工具链：工程工具的变更说明
  - 流程优化：开发流程的改进
  - 规范调整：开发规范的更新
- `测试`: 测试相关变更
  - 测试范围：新增或优化的测试类型
  - 覆盖率：测试覆盖率的变化
  - 自动化：测试自动化的改进

## [未发布]

### 工程
- 改进CHANGELOG格式，增加更详细的变更分类 ([#123](https://github.com/nighm/python-project-template/issues/123))
  - 工具链：新增变更日志格式检查工具，支持自动化验证 ([#123](https://github.com/nighm/python-project-template/issues/123))
  - 流程优化：引入自动化验证流程，确保变更日志格式一致性 ([#123](https://github.com/nighm/python-project-template/issues/123))
  - 规范调整：采用更细粒度的变更分类，提高文档可读性 ([#123](https://github.com/nighm/python-project-template/issues/123))
- 添加变更日志格式验证工具 ([#124](https://github.com/nighm/python-project-template/issues/124))
  - 工具链：集成自动化验证工具，提高开发效率 ([#124](https://github.com/nighm/python-project-template/issues/124))
  - 流程优化：在CI/CD流程中增加格式验证，保证质量 ([#124](https://github.com/nighm/python-project-template/issues/124))
  - 规范调整：强制执行统一的变更日志格式规范 ([#124](https://github.com/nighm/python-project-template/issues/124))

## [0.2.0] - 2024-01-10

### 新增
- 初始项目模板，提供完整的项目骨架结构 ([#100](https://github.com/nighm/python-project-template/issues/100))
  - 影响范围：项目整体结构和开发流程 ([#100](https://github.com/nighm/python-project-template/issues/100))
  - 依赖要求：Python 3.8+，基础开发工具 ([#100](https://github.com/nighm/python-project-template/issues/100))
  - 性能影响：无显著影响 ([#100](https://github.com/nighm/python-project-template/issues/100))
- 集成主流开发工具配置 ([#101](https://github.com/nighm/python-project-template/issues/101))
  - 影响范围：代码质量和开发效率提升 ([#101](https://github.com/nighm/python-project-template/issues/101))
  - 依赖要求：black、flake8、mypy等工具 ([#101](https://github.com/nighm/python-project-template/issues/101))
  - 性能影响：开发环境构建时间增加约30秒 ([#101](https://github.com/nighm/python-project-template/issues/101))
- 添加测试框架集成 ([#102](https://github.com/nighm/python-project-template/issues/102))
  - 影响范围：测试流程和质量保证体系 ([#102](https://github.com/nighm/python-project-template/issues/102))
  - 依赖要求：pytest及相关插件 ([#102](https://github.com/nighm/python-project-template/issues/102))
  - 性能影响：CI执行时间增加约2分钟 ([#102](https://github.com/nighm/python-project-template/issues/102))
- 实现完整的文档系统 ([#103](https://github.com/nighm/python-project-template/issues/103))
  - 影响范围：项目文档和国际化支持 ([#103](https://github.com/nighm/python-project-template/issues/103))
  - 依赖要求：Sphinx文档工具链 ([#103](https://github.com/nighm/python-project-template/issues/103))
  - 性能影响：文档构建时间约1分钟 ([#103](https://github.com/nighm/python-project-template/issues/103))
- 配置GitHub Actions ([#104](https://github.com/nighm/python-project-template/issues/104))
  - 影响范围：开发流程和部署流程自动化 ([#104](https://github.com/nighm/python-project-template/issues/104))
  - 依赖要求：GitHub Actions运行环境 ([#104](https://github.com/nighm/python-project-template/issues/104))
  - 性能影响：自动化流程执行时间约5分钟 ([#104](https://github.com/nighm/python-project-template/issues/104))
- 添加Docker支持 ([#105](https://github.com/nighm/python-project-template/issues/105))
  - 影响范围：部署和运维流程标准化 ([#105](https://github.com/nighm/python-project-template/issues/105))
  - 依赖要求：Docker环境 ([#105](https://github.com/nighm/python-project-template/issues/105))
  - 性能影响：镜像构建时间约2分钟 ([#105](https://github.com/nighm/python-project-template/issues/105))

### 工程
- 优化项目结构 ([#106](https://github.com/nighm/python-project-template/issues/106))
  - 工具链：重构项目目录结构，提高可维护性 ([#106](https://github.com/nighm/python-project-template/issues/106))
  - 流程优化：简化开发流程，提高开发效率 ([#106](https://github.com/nighm/python-project-template/issues/106))
  - 规范调整：采用Python最佳实践规范 ([#106](https://github.com/nighm/python-project-template/issues/106))
- 规范化Git工作流程 ([#107](https://github.com/nighm/python-project-template/issues/107))
  - 工具链：引入Git Flow工作流，规范版本管理 ([#107](https://github.com/nighm/python-project-template/issues/107))
  - 流程优化：标准化分支管理流程 ([#107](https://github.com/nighm/python-project-template/issues/107))
  - 规范调整：统一提交信息格式规范 ([#107](https://github.com/nighm/python-project-template/issues/107))

### 文档
- 完善项目文档 ([#108](https://github.com/nighm/python-project-template/issues/108))
  - 更新范围：开发流程和规范文档完善 ([#108](https://github.com/nighm/python-project-template/issues/108))
  - 相关模块：全部核心模块文档更新 ([#108](https://github.com/nighm/python-project-template/issues/108))
- 添加示例代码 ([#109](https://github.com/nighm/python-project-template/issues/109))
  - 更新范围：示例代码和API文档补充 ([#109](https://github.com/nighm/python-project-template/issues/109))
  - 相关模块：示例模块和工具类文档 ([#109](https://github.com/nighm/python-project-template/issues/109))

## [0.1.0] - 2024-01-01

### 新增
- 项目基础框架初始化 ([#001](https://github.com/nighm/python-project-template/issues/001))
  - 影响范围：项目初始化和基础设施搭建 ([#001](https://github.com/nighm/python-project-template/issues/001))
  - 依赖要求：Python 3.8+ ([#001](https://github.com/nighm/python-project-template/issues/001))
  - 性能影响：无显著影响 ([#001](https://github.com/nighm/python-project-template/issues/001))
- 实现基础项目结构设计 ([#002](https://github.com/nighm/python-project-template/issues/002))
  - 影响范围：项目整体架构设计 ([#002](https://github.com/nighm/python-project-template/issues/002))
  - 依赖要求：无特殊依赖 ([#002](https://github.com/nighm/python-project-template/issues/002))
  - 性能影响：无显著影响 ([#002](https://github.com/nighm/python-project-template/issues/002))
- 集成Poetry进行依赖管理 ([#003](https://github.com/nighm/python-project-template/issues/003))
  - 影响范围：依赖管理系统优化 ([#003](https://github.com/nighm/python-project-template/issues/003))
  - 依赖要求：Poetry包管理器 ([#003](https://github.com/nighm/python-project-template/issues/003))
  - 性能影响：依赖安装时间优化 ([#003](https://github.com/nighm/python-project-template/issues/003))
- 配置基础测试框架 ([#004](https://github.com/nighm/python-project-template/issues/004))
  - 影响范围：测试系统基础架构 ([#004](https://github.com/nighm/python-project-template/issues/004))
  - 依赖要求：pytest及插件 ([#004](https://github.com/nighm/python-project-template/issues/004))
  - 性能影响：测试执行时间约1分钟 ([#004](https://github.com/nighm/python-project-template/issues/004))
- 搭建文档框架 ([#005](https://github.com/nighm/python-project-template/issues/005))
  - 影响范围：项目文档系统建设 ([#005](https://github.com/nighm/python-project-template/issues/005))
  - 依赖要求：Sphinx文档工具 ([#005](https://github.com/nighm/python-project-template/issues/005))
  - 性能影响：文档构建时间约30秒 ([#005](https://github.com/nighm/python-project-template/issues/005))

### 工程
- 初始化Git仓库 ([#006](https://github.com/nighm/python-project-template/issues/006))
  - 工具链：Git版本控制系统配置 ([#006](https://github.com/nighm/python-project-template/issues/006))
  - 流程优化：版本管理自动化实现 ([#006](https://github.com/nighm