from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.v1.routers.sockets import notify_clients
from api.utis.dependencies import UOWDep
from schemas.forums.message import MessageSchema, MessageSchemaCreate, MessageSchemaUpdate
from services.forums import ForumsService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("/", response_model=MessageSchema)
async def create_message(uow: UOWDep, message_schema: MessageSchemaCreate):
    message = await ForumsService().create_message(uow, message_schema)
    await notify_clients(f"Message created: {message.id}")
    return message


@router.get("/", response_model=List[MessageSchema])
async def read_messages(uow: UOWDep, offset: int = 0, limit: int = 10):
    messages = await ForumsService().get_messages(uow, offset=offset, limit=limit)
    return messages


@router.get("/thread/{thread_id}/", response_model=List[MessageSchema])
async def read_thread_messages(uow: UOWDep, thread_id: int, offset: int = 0, limit: int = 10):
    try:
        messages = await ForumsService().get_thread_messages(uow, thread_id=thread_id, offset=offset, limit=limit)
        return messages
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Messages not found")

@router.get("/{message_id}", response_model=MessageSchema)
async def read_message(uow: UOWDep, message_id: int):
    message = await ForumsService().get_message(uow, message_id)
    return message


@router.patch("/{message_id}", response_model=MessageSchema)
async def update_message(uow: UOWDep, message_id: int, message_schema: MessageSchemaUpdate):
    try:
        message = await ForumsService().edit_message(uow, message_id, message_schema)
        await notify_clients(f"Message updated: {message.id}")
        return message
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Message not found")


@router.delete("/{message_id}")
async def delete_message(uow: UOWDep, message_id: int):
    try:
        await ForumsService().delete_message(uow, message_id)

        await notify_clients(f"Message deleted: ({message_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Message deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Message not found")
