from fastapi import APIRouter

from api.v1.routers.auth import router as auth_router
from api.v1.routers.users import router as users_router
from api.v1.routers.forums import router as forums_router
from api.v1.routers.sockets import router as websockets_router

router = APIRouter(prefix='/v1')

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(forums_router)
router.include_router(websockets_router)

