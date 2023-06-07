from fastapi import APIRouter
router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def add_course():
    return

@router.get("/{course_id}")
async def get_course():
    return

@router.get("/{course_id}/students")
async def get_course_students():
    return