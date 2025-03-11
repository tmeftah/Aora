from fastapi import APIRouter

health_router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Resource Not Found"},
        500: {"description": "Internal Server Error"},
    },
)


@health_router.get("/")
async def check_health():
    return {"status": "Active"}
