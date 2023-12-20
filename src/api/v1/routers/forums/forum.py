from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import NoResultFound
from fastapi import status
from fastapi.responses import JSONResponse

from api.v1.routers.sockets import notify_clients
from api.utis.dependencies import UOWDep
from schemas.forums.forum import ForumSchema, ForumSchemaCreate, ForumSchemaUpdate
from services.forums import ForumsService

router = APIRouter(
    prefix="/forums",
    tags=["Forums"],
)


@router.post("/", response_model=ForumSchema)
async def create_forum(uow: UOWDep, forum_schema: ForumSchemaCreate):
    forum = await ForumsService().create_forum(uow, forum_schema)
    await notify_clients(f"Forum created: {forum.title}")
    return forum


@router.get("/", response_model=List[ForumSchema])
async def read_forums(uow: UOWDep, offset: int = 0, limit: int = 10):
    forums = await ForumsService().get_forums(uow, offset=offset, limit=limit)
    return forums


@router.get("/{forum_id}", response_model=ForumSchema)
async def read_forum(uow: UOWDep, forum_id: int):
    forum = await ForumsService().get_forum(uow, forum_id)
    return forum


@router.patch("/{forum_id}", response_model=ForumSchema)
async def update_forum(uow: UOWDep, forum_id: int, forum_schema: ForumSchemaUpdate):
    try:
        forum = await ForumsService().edit_forum(uow, forum_id, forum_schema)
        await notify_clients(f"Forum updated: {forum.title}")
        return forum
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Forum not found")


@router.delete("/{forum_id}")
async def delete_forum(uow: UOWDep, forum_id: int):
    try:
        await ForumsService().delete_forum(uow, forum_id)

        await notify_clients(f"Forum deleted: ({forum_id} ID)")

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"message": "Forum deleted successfully"})
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Forum not found")
