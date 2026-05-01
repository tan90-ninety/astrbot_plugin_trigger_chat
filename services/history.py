"""按群和用户维护短期消息缓存，用于触发聊天时拼接上下文提示词。"""

import time

from astrbot.api.event import AstrMessageEvent


HISTORY_LIMIT = 3
HISTORY_WINDOW_SECONDS = 180


class MessageHistory:
    """保存最近一小段时间内的用户群聊文本消息。"""

    def __init__(
        self,
        limit: int = HISTORY_LIMIT,
        window_seconds: int = HISTORY_WINDOW_SECONDS,
    ) -> None:
        """
        设置缓存条数和时间窗口。
        """
        self.limit = limit
        self.window_seconds = window_seconds
        self._records: dict[tuple[str, str], list[tuple[float, str]]] = {}

    def record(self, event: AstrMessageEvent, message: str) -> None:
        """
        记录当前群当前用户的一条非触发文本消息。
        """
        if not message:
            return

        key = self._key(event)
        now = time.time()
        records = self._recent_records(key, now)
        records.append((now, message))
        self._records[key] = records[-self.limit :]

    def build_prompt(self, event: AstrMessageEvent) -> str:
        """
        取当前群当前用户时间窗口内最近的消息，并合并为 LLM prompt。
        """
        records = self._recent_records(self._key(event), time.time())[-self.limit :]
        return "\n".join(message for _, message in records)

    def _recent_records(
        self,
        key: tuple[str, str],
        now: float,
    ) -> list[tuple[float, str]]:
        """
        过滤出仍在有效时间窗口内的缓存消息。
        """
        return [
            record
            for record in self._records.get(key, [])
            if now - record[0] <= self.window_seconds
        ]

    @staticmethod
    def _key(event: AstrMessageEvent) -> tuple[str, str]:
        """
        使用群号和发送者 ID 隔离不同用户的上下文缓存。
        """
        return event.get_group_id(), event.get_sender_id()
