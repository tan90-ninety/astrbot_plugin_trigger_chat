"""群聊触发条件判断工具。"""

from astrbot.api.event import AstrMessageEvent
from astrbot.api.message_components import At, Plain, Reply


def is_only_at_bot(event: AstrMessageEvent) -> bool:
    """
    判断消息是否只包含引用消息、@机器人 和空白文本。
    """
    has_at_bot = False
    for message in event.get_messages():
        if isinstance(message, Reply):
            continue
        if isinstance(message, At):
            if str(message.qq) != str(event.get_self_id()):
                return False
            has_at_bot = True
        elif isinstance(message, Plain):
            if message.text.strip():
                return False
        else:
            return False
    return has_at_bot


def contains_keyword(message: str, keywords: list[str]) -> bool:
    """
    判断文本是否包含任意配置关键词。
    """
    return bool(message and any(keyword in message for keyword in keywords))


def is_only_keyword(message: str, keywords: list[str]) -> bool:
    """
    判断文本是否只是一条独立关键词。
    """
    return bool(message and any(message == keyword for keyword in keywords))
