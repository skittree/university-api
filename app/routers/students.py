from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, crud
from ..db import get_session

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def add_student(student: schemas.StudentCreate, session: AsyncSession = Depends(get_session)) -> schemas.StudentOut:
    student = await crud.add_student(session, student)
    return schemas.StudentOut.from_orm(student)

@router.get("/{student_id}")
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)) -> schemas.StudentOut:
    student = await crud.get_student(session, student_id)
    return schemas.StudentOut.from_orm(student)

@router.put("/{student_id}")
async def update_student(student_id: int, student: schemas.StudentUpdate, session: AsyncSession = Depends(get_session)) -> schemas.StudentOut:
    student = await crud.update_student(session, student_id, student)
    return schemas.StudentOut.from_orm(student)

@router.delete("/{student_id}")
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)) -> schemas.StudentOut:
    student = await crud.delete_student(session, student_id)
    return schemas.StudentOut.from_orm(student)