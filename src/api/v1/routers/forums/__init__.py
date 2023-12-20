from fastapi import APIRouter

from .forum import router as forum_router
from .thread import router as thread_router
from .message import router as message_router

# Определение основного роутера
router = APIRouter()

# Добавление роутеров с условиями по ID
router.include_router(forum_router)
router.include_router(thread_router, prefix="/forums")
router.include_router(message_router, prefix="/forums/threads")
