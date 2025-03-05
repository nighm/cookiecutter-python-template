"""Sphinx文档配置文件."""

import os
import sys
from datetime import datetime

# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.abspath('../..'))

# 项目信息
project = 'Python项目模板'
copyright = f'{datetime.now().year}, Your Company'
author = 'Your Name'
version = '0.1.0'
release = '0.1.0'

# 文档生成配置
extensions = [
    'sphinx.ext.autodoc',      # 自动生成API文档
    'sphinx.ext.napoleon',     # 支持Google风格的文档字符串
    'sphinx.ext.viewcode',     # 添加源代码链接
    'sphinx.ext.coverage',     # 文档覆盖率检查
    'sphinx.ext.githubpages',  # GitHub Pages支持
]

# 主题设置
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# 语言设置
language = 'zh_CN'

# 源文件设置
source_suffix = '.rst'
master_doc = 'index'

# 排除的模式
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# autodoc设置
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
