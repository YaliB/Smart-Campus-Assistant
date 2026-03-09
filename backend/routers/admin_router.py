from fastapi import APIRouter, Depends

from ..services.auth_service import get_current_admin_user

# importing all the sub-routers for different admin functionalities
from .admin import auth_routes,user_routes, faq_routes, room_routes, exam_routes, reception_routes

router = APIRouter(tags=["Admin Management"])

# Authentication route (public, no restrictions)
router.include_router(auth_routes.router)

# User management routes (protected under admin requirement)
router.include_router(
    user_routes.router,
    prefix="/users",
    dependencies=[Depends(get_current_admin_user)]
)

# Data routes (all protected under admin requirement)
router.include_router(
    faq_routes.router, 
    prefix="/faq", 
    dependencies=[Depends(get_current_admin_user)] # This ensures required admin authentication.
)

router.include_router(
    room_routes.router, 
    prefix="/rooms", 
    dependencies=[Depends(get_current_admin_user)]
)

router.include_router(
    exam_routes.router, 
    prefix="/exams", 
    dependencies=[Depends(get_current_admin_user)]
)

router.include_router(
    reception_routes.router, 
    prefix="/reception", 
    dependencies=[Depends(get_current_admin_user)]
)

