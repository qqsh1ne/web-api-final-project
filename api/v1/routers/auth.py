from fastapi import APIRouter, HTTPException, Body, Form
from sqlalchemy.exc import NoResultFound
from fastapi import status

from api.utis.dependencies import UOWDep
from schemas.users import UserSchemaCreate, UserSchema
from services.users import UsersService

from api.v1.routers.sockets import notify_clients

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login/", response_model=UserSchema)
async def login(uow: UOWDep, user_schema: UserSchemaCreate):
    try:
        user = await UsersService().get_user_by_name(uow, user_name=user_schema.model_dump().get('name'))
        await notify_clients(f"User {user.name} logged in!")
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")