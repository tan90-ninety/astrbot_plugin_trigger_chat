from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, register


@register("trigger_chat", "Tan", "关键词触发 LLM 对话", "0.0.1")
class TriggerChatPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def _get_keywords(self) -> list[str]:
        keywords = self.config.get("keywords", [])
        return [str(keyword).strip() for keyword in keywords if str(keyword).strip()]

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def call(self, event: AstrMessageEvent):
        """关键词命中后交给 AstrBot 默认 LLM 聊天流程处理。"""
        message = event.message_str.strip()
        if not message or not any(keyword in message for keyword in self._get_keywords()):
            return

        event.is_wake = True
        event.is_at_or_wake_command = True
        logger.info(f"关键词触发 LLM 对话: {event.message_str}")
