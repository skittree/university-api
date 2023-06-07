from fastapi import APIRouter
router = APIRouter(
    prefix="/students",
    tags=["students"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def add_student():
    return

@router.get("/{student_id}")
async def get_student():
    return

@router.put("/{student_id}")
async def update_student():
    return

@router.delete("/{student_id}")
async def delete_student():
    return