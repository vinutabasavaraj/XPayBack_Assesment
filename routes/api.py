from fastapi import APIRouter
from src.endpoints import (create_table, user_registration)

router = APIRouter()

router.include_router(create_table.router)
router.include_router(user_registration.router)

