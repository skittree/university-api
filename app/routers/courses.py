from pydantic import parse_obj_as
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from .. import schemas, crud
from ..db import get_session

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def add_course(course: schemas.CourseCreate, session: AsyncSession = Depends(get_session)) -> schemas.CourseOut:
    course = await crud.add_course(session, course)
    return schemas.CourseOut.from_orm(course)

@router.get("/{course_id}")
async def get_course(course_id: int, session: AsyncSession = Depends(get_session)) -> schemas.CourseOut:
    course = await crud.get_course(session, course_id)
    return schemas.CourseOut.from_orm(course)

@router.get("/{course_id}/students")
async def get_course_students(course_id: int, session: AsyncSession = Depends(get_session)) -> list[schemas.StudentOut]:
    students = await crud.get_course_students(session, course_id)
    return parse_obj_as(list[schemas.StudentOut], students)