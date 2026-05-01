"""AstrBot 插件入口，负责把触发条件转换为默认 LLM 聊天请求。"""

from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register

from .services.config import get_at_prompt, get_keywords
from .services.history import MessageHistory
from .services.triggers import contains_keyword, is_only_at_bot

class TriggerChatPlugin(Star):
    """关键词或单独 @ 触发 AstrBot 默认聊天流程的插件。"""

    def __init__(self, context: Context, config: AstrBotConfig):
        """
        保存插件配置，并初始化按群和用户隔离的短期消息缓存。
        """
        super().__init__(context)
        self.config = config
        self.history = MessageHistory()

    def _set_llm_prompt(self, event: AstrMessageEvent, prompt: str) -> None:
        """
        将事件改写成 AstrBot 默认 LLM 流程可处理的唤醒消息。
        """
        event.message_str = prompt
        event.message_obj.message_str = prompt
        event.is_wake = True
        event.is_at_or_wake_command = True

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def call(self, event: AstrMessageEvent):
        """
        仅处理群聊消息；非触发消息进入缓存，触发消息使用缓存构造 prompt。
        """
        message = event.message_str.strip()
        triggered_by_at = is_only_at_bot(event)
        triggered_by_keyword = contains_keyword(message, get_keywords(self.config))

        if not triggered_by_at and not triggered_by_keyword:
            self.history.record(event, message)
            return

        prompt = self.history.build_prompt(event) or get_at_prompt(self.config)
        self._set_llm_prompt(event, prompt)
        trigger_type = "单独 @" if triggered_by_at else "关键词"
        logger.info(f"{trigger_type}触发 LLM 对话: {event.message_str}")
