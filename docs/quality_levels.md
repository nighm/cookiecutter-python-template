# 代码检查分级指南

## 一、检查级别概述

### 1.1 基础级别（Basic Level）
适用场景：
- 日常开发
- 个人项目
- 小型团队项目
- 快速原型开发

必要检查项：
1. **代码格式化**
   - Black：基础代码格式化
   - isort：导入语句排序

2. **基础语法检查**
   - Flake8：PEP 8 规范检查
   - Pylint（基础规则）：基本代码规范

3. **基础类型检查**
   - MyPy（基础配置）：基本类型提示检查

执行时机：
- 代码提交前
- Push 到主分支前

### 1.2 标准级别（Standard Level）
适用场景：
- 团队协作项目
- 生产环境代码
- 中型项目

在基础级别基础上增加：
1. **代码质量检查**
   - Pylint（完整规则）：深度代码分析
   - Radon：代码复杂度检查
   - Coverage：测试覆盖率 >= 80%

2. **安全检查**
   - Bandit：基本安全漏洞检查
   - Safety：依赖包安全检查

3. **文档检查**
   - Pydocstyle：文档风格检查
   - interrogate：文档覆盖率检查

执行时机：
- 代码审查阶段
- 合并到开发分支前
- 持续集成流程中

### 1.3 高级级别（Advanced Level）
适用场景：
- 大型商业项目
- 高可靠性要求系统
- 安全敏感应用

在标准级别基础上增加：
1. **深度安全检查**
   - Bandit（严格模式）
   - PyT：Python漏洞检测
   - Semgrep：高级语义分析

2. **性能分析**
   - Scalene：CPU和内存分析
   - py-spy：实时性能分析
   - memory_profiler：内存使用分析

3. **高级质量检查**
   - Sonar：综合代码质量分析
   - Xenon：代码复杂度门禁
   - Coverage：测试覆盖率 >= 95%

4. **依赖分析**
   - pip-audit：深度依赖安全审计
   - License检查：开源协议合规性

执行时机：
- 版本发布前
- 生产环境部署前
- 定期系统审计

## 二、场景化检查策略

### 2.1 功能开发场景
```yaml
# 日常开发检查清单
基础检查:
  - Black格式化
  - isort导入排序
  - Flake8基础检查

提交前检查:
  - MyPy类型检查
  - Pylint基础规则
  - 单元测试通过
```

### 2.2 代码审查场景
```yaml
# PR合并检查清单
质量检查:
  - Pylint完整规则
  - 圈复杂度检查
  - 测试覆盖率 >= 80%

安全检查:
  - Bandit基础扫描
  - 依赖安全检查
  
文档检查:
  - 文档完整性
  - API文档更新
```

### 2.3 发布上线场景
```yaml
# 发布检查清单
深度检查:
  - 全量静态分析
  - 安全漏洞扫描
  - 性能基准测试
  
合规检查:
  - 开源协议审计
  - 敏感信息扫描
  - 第三方依赖审计
```

## 三、自动化配置示例

### 3.1 基础级别配置
```yaml
# .pre-commit-config.yaml (基础级别)
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### 3.2 标准级别配置
```yaml
# .pre-commit-config.yaml (标准级别)
repos:
  # 包含基础级别的所有检查
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.0
    hooks:
      - id: bandit
  - repo: https://github.com/PyCQA/pylint
    rev: v2.17.0
    hooks:
      - id: pylint
        args: [--rcfile=.pylintrc]
  - repo: https://github.com/pycqa/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
```

### 3.3 高级级别配置
```yaml
# .pre-commit-config.yaml (高级级别)
repos:
  # 包含基础和标准级别的所有检查
  - repo: local
    hooks:
      - id: security-checks
        name: Security Checks
        entry: bash -c 'poetry run bandit -r . && poetry run safety check'
        language: system
      - id: performance-checks
        name: Performance Checks
        entry: bash -c 'poetry run scalene src/'
        language: system
      - id: coverage-check
        name: Coverage Check
        entry: bash -c 'poetry run pytest --cov=src --cov-fail-under=95'
        language: system
```

## 四、检查结果处理建议

### 4.1 基础级别
- 所有检查必须通过
- 允许配置少量忽略规则
- 团队共享相同的格式化配置

### 4.2 标准级别
- 允许特定场景下的规则调整
- 需要文档说明忽略规则的原因
- 定期审查代码质量报告

### 4.3 高级级别
- 严格的质量门禁制度
- 需要定期安全审计报告
- 性能基准测试记录和对比
- 自动化质量报告和趋势分析

## 五、最佳实践建议

### 5.1 渐进式采用
1. 从基础级别开始
2. 逐步引入更多检查
3. 根据项目需求调整配置

### 5.2 团队协作
1. 统一工具配置
2. 共享检查规则
3. 定期培训和交流

### 5.3 持续优化
1. 收集反馈调整规则
2. 监控检查效果
3. 及时更新工具版本 