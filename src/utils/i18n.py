"""国际化工具.

提供多语言支持的工具和配置。
"""

import gettext
import os
from functools import lru_cache
from typing import Dict, Optional

from src.config import settings

# 常量定义
LOCALE_DIR = settings.PROJECT_ROOT / "resources" / "locales"
TRANSLATIONS: Dict[str, gettext.NullTranslations] = {}


def setup_i18n() -> None:
    """初始化国际化系统.

    创建语言文件目录并加载所有支持的语言翻译。
    """
    os.makedirs(LOCALE_DIR, exist_ok=True)

    for lang in settings.SUPPORTED_LANGUAGES:
        try:
            TRANSLATIONS[lang] = gettext.translation(
                "messages",
                localedir=str(LOCALE_DIR),
                languages=[lang],
            )
        except FileNotFoundError:
            TRANSLATIONS[lang] = gettext.NullTranslations()


@lru_cache(maxsize=1024)
def get_text(message: str, lang: Optional[str] = None) -> str:
    """获取指定消息的翻译文本.

    Args:
        message: 需要翻译的消息
        lang: 目标语言代码，如果未提供则使用默认语言

    Returns:
        翻译后的文本
    """
    if not lang:
        lang = settings.DEFAULT_LANGUAGE

    if lang not in TRANSLATIONS:
        lang = settings.DEFAULT_LANGUAGE

    return TRANSLATIONS[lang].gettext(message)


def get_supported_languages() -> list[str]:
    """获取支持的语言列表.

    Returns:
        语言代码列表
    """
    return settings.SUPPORTED_LANGUAGES


# 模块导入时初始化国际化系统
setup_i18n()
