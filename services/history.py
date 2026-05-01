"""按群和用户维护短期消息缓存，用于触发聊天时拼接上下文提示词。"""

import time

from astrbot.api.event import AstrMessageEvent


HISTORY_WINDOW_SECONDS = 30


class MessageHistory:
    """保存最近一小段时间内的用户群聊文本消息。"""

    def __init__(
        self,
        window_seconds: int = HISTORY_WINDOW_SECONDS,
    ) -> None:
        """
        设置缓存时间窗口。
        """
        self.window_seconds = window_seconds
        # key 为 (群号, 用户 ID)，value 为该用户在该群内的上一条非触发消息。
        # value 格式为 (发送时间戳, 消息文本)。
        self._records: dict[tuple[str, str], tuple[float, str]] = {}

    def record(self, event: AstrMessageEvent, message: str) -> None:
        """
        记录当前群当前用户的一条非触发文本消息。
        """
        if not message:
            return

        self._records[self._key(event)] = (time.time(), message)

    def build_prompt(self, event: AstrMessageEvent) -> str:
        """
        取当前群当前用户时间窗口内上一条消息，作为 LLM prompt。
        """
        record = self._recent_record(self._key(event), time.time())
        return record[1] if record else ""

    def _recent_record(
        self,
        key: tuple[str, str],
        now: float,
    ) -> tuple[float, str] | None:
        """
        获取仍在有效时间窗口内的缓存消息。
        """
        record = self._records.get(key)
        if not record or now - record[0] > self.window_seconds:
            return None
        return record

    @staticmethod
    def _key(event: AstrMessageEvent) -> tuple[str, str]:
        """
        使用群号和发送者 ID 隔离不同用户的上下文缓存。
        """
        return event.get_group_id(), event.get_sender_id()
