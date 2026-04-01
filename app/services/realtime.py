from collections import defaultdict
from fastapi import WebSocket


class RealtimeHub:
    def __init__(self) -> None:
        self._channels: dict[str, set[WebSocket]] = defaultdict(set)

    async def connect(self, channel: str, ws: WebSocket) -> None:
        await ws.accept()
        self._channels[channel].add(ws)

    def disconnect(self, channel: str, ws: WebSocket) -> None:
        self._channels[channel].discard(ws)

    async def publish(self, channel: str, payload: dict) -> None:
        for ws in list(self._channels[channel]):
            await ws.send_json(payload)


hub = RealtimeHub()
