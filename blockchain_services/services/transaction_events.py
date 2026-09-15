import asyncio
from typing import Dict

class TransactionStatusManager:
    def __init__(self):
        self._statuses: Dict[str, str] = {}
        self._subscribers: Dict[str, list[asyncio.Queue]] = {}

    def get_status(self, tx_id: str) -> str:
        return self._statuses.get(tx_id, "pending")

    async def mark_complete(self, tx_id: str):
        self._statuses[tx_id] = "complete"
        for queue in self._subscribers.get(tx_id, []):
            await queue.put("complete")

    def subscribe(self, tx_id: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._subscribers.setdefault(tx_id, []).append(queue)
        return queue

    def unsubscribe(self, tx_id: str, queue: asyncio.Queue):
        if tx_id in self._subscribers:
            self._subscribers[tx_id].remove(queue)

status_manager = TransactionStatusManager()