from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.v1.routers.sockets import notify_clients
from api.utis.dependencies import UOWDep
from schemas.forums.thread import ThreadSchema, ThreadSchemaCreate, ThreadSchemaUpdate
from services.forums import ForumsService

router = APIRouter(
    prefix="/threads",
    tags=["Threads"],
)


@router.post("/", response_model=ThreadSchema)
async def create_thread(uow: UOWDep, thread_schema: ThreadSchemaCreate):
    thread = await ForumsService().create_thread(uow, thread_schema)
    await notify_clients(f"Thread created: {thread.title}")
    return thread


@router.get("/", response_model=List[ThreadSchema])
async def read_threads(uow: UOWDep, offset: int = 0, limit: int = 10):
    threads = await ForumsService().get_threads(uow, offset=offset, limit=limit)
    return threads


@router.get("/forum/{forum_id}/", response_model=List[ThreadSchema])
async def read_forum_threads(uow: UOWDep, forum_id: int, offset: int = 0, limit: int = 10):
    try:
        messages = await ForumsService().get_forum_threads(uow, forum_id=forum_id, offset=offset, limit=limit)
        return messages
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Threads not found")


@router.get("/{thread_id}", response_model=ThreadSchema)
async def read_thread(uow: UOWDep, thread_id: int):
    try:
        thread = await ForumsService().get_thread(uow, thread_id)
        return thread
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Thread not found")


@router.patch("/{thread_id}", response_model=ThreadSchema)
async def update_thread(uow: UOWDep, thread_id: int, thread_schema: ThreadSchemaUpdate):
    try:
        thread = await ForumsService().edit_thread(uow, thread_id, thread_schema)
        await notify_clients(f"Thread updated: {thread.title}")
        return thread
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Thread not found")


@router.delete("/{thread_id}")
async def delete_thread(uow: UOWDep, thread_id: int):
    try:
        await ForumsService().delete_thread(uow, thread_id)

        await notify_clients(f"Thread deleted: ({thread_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Thread deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Thread not found")
