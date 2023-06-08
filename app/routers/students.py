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
async def add_student(student: schemas.Student, session: AsyncSession = Depends(get_session)) -> schemas.StudentOut:
    try:
        student = await crud.create_student(session, student)
        return schemas.StudentOut.from_orm(student)
    except NoResultFound as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.args,
        )
    except IntegrityError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"statement": ex.statement, "params": ex.params},
        )

@router.get("/{student_id}")
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)) -> schemas.StudentOut:
    try:
        student = await crud.get_student(session, student_id)
        return schemas.StudentOut.from_orm(student)
    except NoResultFound as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ex.args,
        )

@router.put("/{student_id}")
async def update_student():
    return

@router.delete("/{student_id}")
async def delete_student():
    return