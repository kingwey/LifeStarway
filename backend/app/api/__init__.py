from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.diagnosis import router as diagnosis_router
from app.api.plan import router as plan_router
from app.api.starmap import router as starmap_router
from app.api.whatif import router as whatif_router
from app.api.user import router as user_router

routers = [
    auth_router,
    profile_router,
    diagnosis_router,
    plan_router,
    starmap_router,
    whatif_router,
    user_router
]
