from fastapi import APIRouter
router = APIRouter(
    prefix="/grades",
    tags=["Grades"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def add_grade():
    return

@router.put("/{grade_id}")
async def update_grade():
    return