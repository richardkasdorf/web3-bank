from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from blockchain_services.services.transaction_events import status_manager

router = APIRouter(tags=["Transaction Status"])

@router.get("/transactions/{tx_id}/stream")
async def stream_transaction_status(tx_id: str):
    queue = status_manager.subscribe(tx_id)

    async def event_generator():
        yield f"data: {status_manager.get_status(tx_id)}\n\n"

        if status_manager.get_status(tx_id) == "complete":
            return

        try:
            while True:
                update = await queue.get()
                yield f"data: {update}\n\n"
                if update == "complete":
                    break
        finally:
            status_manager.unsubscribe(tx_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")