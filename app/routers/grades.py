from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from .. import schemas, crud
from ..db import get_session

router = APIRouter(
    prefix="/grades",
    tags=["Grades"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def add_grade(grade: schemas.CourseGradeCreate, session: AsyncSession = Depends(get_session)) -> schemas.CourseGradeOut:
    grade = await crud.add_course_grade(session, grade)
    return schemas.CourseGradeOut.from_orm(grade)

@router.put("/{grade_id}")
async def update_grade(grade_id: int, grade: schemas.CourseGradeUpdate, session: AsyncSession = Depends(get_session)) -> schemas.CourseGradeOut:
    grade = await crud.update_course_grade(session, grade_id, grade)
    return schemas.CourseGradeOut.from_orm(grade)