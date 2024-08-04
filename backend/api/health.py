from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health")
async def check_health():
    return {"status": "Active"}
