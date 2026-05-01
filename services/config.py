"""插件配置读取工具。"""

from astrbot.api import AstrBotConfig

def get_keywords(config: AstrBotConfig) -> list[str]:
    """
    从插件配置中读取关键词，并过滤空字符串。
    """
    keywords = config.get("keywords", [])
    return [str(keyword).strip() for keyword in keywords if str(keyword).strip()]


def get_at_prompt(config: AstrBotConfig) -> str:
    """
    从插件配置中读取单独 @ 时使用的兜底提示词。
    """
    return str(config.get("at_prompt", "")).strip()
