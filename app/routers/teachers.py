from fastapi import APIRouter
router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_teachers():
    return