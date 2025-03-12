import ast
import os
import re
import yaml
import time
import logging
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@dataclass
class DocConfig:
    """文档生成配置"""

    language: str
    include_private_methods: bool
    include_module_doc: bool
    include_parameters: bool
    include_return_type: bool
    include_examples: bool
    max_doc_length: int
    use_emojis: bool
    show_line_numbers: bool
    show_source_link: bool
    watch_mode: bool = False
    watch_delay: int = 2  # 延迟更新时间（秒）
    last_update: str = ""  # 最后更新时间


class ReadmeEventHandler(FileSystemEventHandler):
    """文件系统事件处理器"""

    def __init__(self, updater):
        self.updater = updater
        self.last_update = 0
        self.update_delay = updater.config.get("doc_options", {}).get("watch_delay", 2)
        self.pending_updates: Set[str] = set()
        self.is_processing = False

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            current_time = time.time()
            if current_time - self.last_update > self.update_delay:
                self.pending_updates.add(event.src_path)
                if not self.is_processing:
                    self.process_updates()

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            self.pending_updates.add(event.src_path)
            if not self.is_processing:
                self.process_updates()

    def process_updates(self):
        """处理待更新的文件"""
        try:
            self.is_processing = True
            if self.pending_updates:
                logger.info(
                    f"检测到以下文件变化:\n"
                    + "\n".join(
                        f"- {os.path.basename(f)}" for f in self.pending_updates
                    )
                )
                self.updater.update_readme()
                self.last_update = time.time()
                self.pending_updates.clear()
        finally:
            self.is_processing = False


class EnhancedReadmeUpdater:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.readme_path = os.path.join(project_root, "README.md")
        self.config_path = os.path.join(
            project_root, ".github", "config", "readme_config.yml"
        )
        self.module_pattern = re.compile(
            r"<!-- BEGIN_MODULES -->\n(.*?)\n<!-- END_MODULES -->", re.DOTALL
        )
        self.config = self._load_config()
        self.observer = None
        self.stats = {
            "total_files": 0,
            "total_classes": 0,
            "total_functions": 0,
            "start_time": None,
            "end_time": None,
        }

    def _load_config(self) -> Dict:
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)
            return {}
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {}

    def _get_doc_config(self) -> DocConfig:
        """获取文档配置"""
        doc_options = self.config.get("doc_options", {})
        style = self.config.get("style", {})
        return DocConfig(
            language=doc_options.get("language", "zh_CN"),
            include_private_methods=doc_options.get("include_private_methods", False),
            include_module_doc=doc_options.get("include_module_doc", True),
            include_parameters=doc_options.get("include_parameters", True),
            include_return_type=doc_options.get("include_return_type", True),
            include_examples=doc_options.get("include_examples", True),
            max_doc_length=doc_options.get("max_doc_length", 100),
            use_emojis=style.get("use_emojis", True),
            show_line_numbers=style.get("show_line_numbers", False),
            show_source_link=style.get("show_source_link", True),
            last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def _parse_function_info(self, node: ast.FunctionDef) -> Dict:
        """解析函数信息"""
        doc = ast.get_docstring(node) or "暂无描述"
        params = []
        returns = None
        examples = []

        # 解析函数参数
        for arg in node.args.args:
            if arg.arg != "self":
                arg_type = ""
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        arg_type = f" ({arg.annotation.id})"
                    elif isinstance(arg.annotation, ast.Subscript):
                        arg_type = f" ({self._format_type_annotation(arg.annotation)})"
                params.append(f"- {arg.arg}{arg_type}")

        # 解析返回值
        if node.returns:
            returns = self._format_type_annotation(node.returns)

        # 从文档字符串中提取示例
        if doc:
            examples = self._extract_examples(doc)

        return {
            "name": node.name,
            "doc": doc,
            "parameters": params,
            "returns": returns,
            "examples": examples,
        }

    def _format_type_annotation(self, node: ast.AST) -> str:
        """格式化类型注解"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            value = self._format_type_annotation(node.value)
            if isinstance(node.slice, ast.Name):
                return f"{value}[{node.slice.id}]"
            elif isinstance(node.slice, ast.Tuple):
                slice_args = []
                for elt in node.slice.elts:
                    if isinstance(elt, ast.Name):
                        slice_args.append(elt.id)
                return f"{value}[{', '.join(slice_args)}]"
        return "Any"

    def _extract_examples(self, docstring: str) -> List[str]:
        """从文档字符串中提取示例代码"""
        examples = []
        lines = docstring.split("\n")
        in_example = False
        current_example = []

        for line in lines:
            if "```python" in line:
                in_example = True
                continue
            elif "```" in line and in_example:
                in_example = False
                if current_example:
                    examples.append("\n".join(current_example))
                    current_example = []
                continue

            if in_example:
                current_example.append(line.strip())

        return examples

    def _generate_statistics(self) -> str:
        """生成文档统计信息"""
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
        stats = [
            "### 📊 文档统计",
            f"- 总文件数：{self.stats['total_files']}",
            f"- 总类数：{self.stats['total_classes']}",
            f"- 总函数数：{self.stats['total_functions']}",
            f"- 生成用时：{duration:.2f} 秒",
            f"- 最后更新：{self.stats['end_time'].strftime('%Y-%m-%d %H:%M:%S')}\n",
        ]
        return "\n".join(stats)

    def update_readme(self):
        """更新README.md文件"""
        try:
            self.stats["start_time"] = datetime.now()
            logger.info("开始更新文档...")
            logger.info(f"项目根目录: {self.project_root}")
            logger.info(f"README路径: {self.readme_path}")

            if not os.path.exists(self.readme_path):
                logger.info("README.md 不存在，创建新文件...")
                with open(self.readme_path, "w", encoding="utf-8") as f:
                    f.write("# 项目文档\n\n<!-- BEGIN_MODULES -->\n<!-- END_MODULES -->")

            # 重置统计信息
            self.stats.update(
                {"total_files": 0, "total_classes": 0, "total_functions": 0}
            )

            # 生成文档内容
            content = self._generate_content()

            # 更新README文件
            with open(self.readme_path, "r", encoding="utf-8") as f:
                readme_content = f.read()

            if "<!-- BEGIN_MODULES -->" not in readme_content:
                logger.info("添加模块标记...")
                readme_content += "\n\n<!-- BEGIN_MODULES -->\n<!-- END_MODULES -->"

            # 添加统计信息
            self.stats["end_time"] = datetime.now()
            stats_content = self._generate_statistics()
            content = stats_content + content

            new_content = self.module_pattern.sub(
                f"<!-- BEGIN_MODULES -->\n{content}\n<!-- END_MODULES -->",
                readme_content,
            )

            logger.info("写入更新后的内容...")
            with open(self.readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            logger.info("文档更新完成！")

        except Exception as e:
            logger.error(f"更新文档时发生错误: {e}")
            raise

    def _generate_content(self) -> str:
        """生成文档内容"""
        categorized_modules = self._collect_module_info()
        content = []

        for category, modules in categorized_modules.items():
            if modules:
                logger.info(f"处理类别 {category} 的文档...")
                content.append(self._format_doc_section(category, modules))

        return "\n".join(content)

    def _collect_module_info(self) -> Dict:
        """收集模块信息"""
        categorized_modules = {
            category: {} for category in self.config.get("categories", {})
        }

        for root, _, files in os.walk(self.project_root):
            if any(ignore in root for ignore in self.config.get("ignore_patterns", [])):
                continue

            for file in files:
                if not file.endswith(".py"):
                    continue

                self.stats["total_files"] += 1
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.project_root)
                module_name = os.path.splitext(relative_path)[0].replace(os.sep, ".")

                # 确定模块类别
                category = "other"
                for cat, info in self.config.get("categories", {}).items():
                    if Path(relative_path).match(info.get("pattern", "")):
                        category = cat
                        break

                module_info = self._parse_module(file_path)
                if category in categorized_modules:
                    categorized_modules[category][module_name] = module_info

        return categorized_modules

    def _parse_module(self, file_path: str) -> Dict:
        """解析模块文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                tree = ast.parse(content)

            module_info = {
                "classes": [],
                "functions": [],
                "module_doc": ast.get_docstring(tree) or "",
            }

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    self.stats["total_classes"] += 1
                    module_info["classes"].append(self._parse_class_info(node))
                elif isinstance(node, ast.FunctionDef):
                    if not node.name.startswith("_") or self.config.get(
                        "doc_options", {}
                    ).get("include_private_methods", False):
                        self.stats["total_functions"] += 1
                        module_info["functions"].append(self._parse_function_info(node))

            return module_info

        except Exception as e:
            logger.error(f"解析文件 {file_path} 时发生错误: {e}")
            return {"classes": [], "functions": [], "module_doc": ""}

    def _parse_class_info(self, node: ast.ClassDef) -> Dict:
        """解析类信息"""
        doc = ast.get_docstring(node) or "暂无描述"
        methods = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if not item.name.startswith("_") or self.config.get(
                    "doc_options", {}
                ).get("include_private_methods", False):
                    methods.append(self._parse_function_info(item))

        # 解析基类
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(f"{base.value.id}.{base.attr}")

        return {"name": node.name, "doc": doc, "methods": methods, "bases": bases}

    def _format_doc_section(self, category: str, modules: Dict) -> str:
        """格式化文档部分"""
        cat_info = self.config.get("categories", {}).get(category, {})
        icon = cat_info.get("icon", "📦")
        title = cat_info.get("title", category)
        description = cat_info.get("description", "")

        # 使用模板生成标题
        template = self.config.get("templates", {}).get("module_header", "")
        if not template:
            template = "### {icon} {title}\n{description}\n\n{badges}"

        # 生成徽章
        badges = []
        if self.config.get("badges", {}).get("show", True):
            badge_types = self.config.get("badges", {}).get("types", [])
            if "status" in badge_types:
                badges.append(
                    "![Status](https://img.shields.io/badge/status-active-success)"
                )
            if "version" in badge_types:
                badges.append(
                    "![Version](https://img.shields.io/badge/version-1.0.0-blue)"
                )
            if "coverage" in badge_types:
                badges.append(
                    "![Coverage](https://img.shields.io/badge/coverage-80%25-yellowgreen)"
                )
            if "last_update" in badge_types:
                badges.append(
                    f"![LastUpdate](https://img.shields.io/badge/last_update-{datetime.now().strftime('%Y---%m---%d')}-informational)"
                )

        header = template.format(
            icon=icon, title=title, description=description, badges=" ".join(badges)
        )

        content = [header]

        # 按模块名称排序
        for module_path, info in sorted(modules.items()):
            if not info["classes"] and not info["functions"]:
                continue

            # 添加模块标题
            content.append(f"\n#### 📄 {module_path}")

            # 添加模块文档
            module_doc = info.get("module_doc", "").strip()
            if module_doc:
                content.append(f"\n{module_doc}\n")

            # 处理类
            if info["classes"]:
                content.append("\n**类：**")
                for cls in info["classes"]:
                    # 使用模板生成类文档
                    class_template = self.config.get("templates", {}).get(
                        "class_header", ""
                    )
                    if not class_template:
                        class_template = "#### 📦 {class_name}\n{class_description}\n\n**功能说明：**\n{doc_string}\n\n{badges}"

                    class_content = class_template.format(
                        class_name=cls["name"],
                        class_description=cls["doc"].split("\n")[0],
                        doc_string=cls["doc"],
                        badges=" ".join(badges) if badges else "",
                    )
                    content.append(f"\n{class_content}")

                    # 如果有基类，显示继承关系
                    if cls.get("bases"):
                        content.append(f"\n**继承自：** {', '.join(cls['bases'])}")

                    # 如果类有方法，添加可折叠的方法详情
                    if cls["methods"]:
                        content.append("\n<details>")
                        content.append("<summary>查看方法详情</summary>\n")
                        content.append("**方法：**\n")
                        for method in cls["methods"]:
                            content.append(
                                f"- `{method['name']}`：{method['doc'].split('\n')[0]}"
                            )
                            if (
                                method["parameters"]
                                or method["returns"]
                                or method["examples"]
                            ):
                                content.append("  <details>")
                                content.append("  <summary>详细信息</summary>\n")
                                if method["parameters"]:
                                    content.append("  **参数：**\n  ```python")
                                    content.extend(
                                        f"  {param}" for param in method["parameters"]
                                    )
                                    content.append("  ```\n")
                                if method["returns"]:
                                    content.append(
                                        f"  **返回值：** `{method['returns']}`\n"
                                    )
                                if method["examples"]:
                                    content.append("  **示例：**\n  ```python")
                                    content.extend(
                                        f"  {example}" for example in method["examples"]
                                    )
                                    content.append("  ```")
                                content.append("  </details>")
                        content.append("</details>\n")

            # 处理函数
            if info["functions"]:
                content.append("\n**函数：**")
                for func in info["functions"]:
                    # 使用模板生成函数文档
                    function_template = self.config.get("templates", {}).get(
                        "function_header", ""
                    )
                    if not function_template:
                        function_template = "#### 🔸 {function_name}\n{function_description}\n\n**参数：**\n{parameters}\n\n**返回值：**\n{returns}\n\n**示例：**\n```python\n{example}\n```\n\n{badges}"

                    # 格式化函数信息
                    func_content = function_template.format(
                        function_name=func["name"],
                        function_description=func["doc"].split("\n")[0],
                        parameters="\n".join(func["parameters"])
                        if func["parameters"]
                        else "无",
                        returns=func["returns"] if func["returns"] else "无",
                        example="\n".join(func["examples"])
                        if func["examples"]
                        else "暂无示例",
                        badges=" ".join(badges) if badges else "",
                    )
                    content.append(f"\n{func_content}")

            content.append("\n---\n")

        return "\n".join(content)

    def start_monitoring(self):
        """启动文件监控"""
        if not self.config.get("doc_options", {}).get("watch_mode", False):
            logger.warning("监控模式未启用。请在配置文件中设置 watch_mode: true")
            return

        logger.info(f"开始监控项目目录: {self.project_root}")
        event_handler = ReadmeEventHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.project_root, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n停止监控...")
            self.observer.stop()
            self.observer.join()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="增强版README文档生成器")
    parser.add_argument("--watch", "-w", action="store_true", help="启用监控模式")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    updater = EnhancedReadmeUpdater(project_root)

    if args.watch:
        logger.info("正在启动监控模式...")
        updater.config.setdefault("doc_options", {})["watch_mode"] = True
        updater.update_readme()  # 首次更新
        updater.start_monitoring()
    else:
        updater.update_readme()
