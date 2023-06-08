from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def create_student(session: AsyncSession, studentschema: schemas.StudentCreate) -> models.Student:
    group_query = await session.execute(select(models.Group).where(models.Group.id == studentschema.group_id))
    # use scalar or scalar_one? this approach allows us to throw our own exception message, but scalar_one is more concise
    group = group_query.scalar()
    if group is None:
        raise NoResultFound({"statement": "Group with this id does not exist.", "params": studentschema.group_id})
    student = models.Student(**studentschema.dict(), group=group)
    session.add(student)
    try:
        await session.commit()
        return student
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Student add failed.", ex.params, ex.orig)

async def get_student(session: AsyncSession, student_id: int) -> models.Student:
    student_query = await session.execute(select(models.Student).where(models.Student.id == student_id))
    student = student_query.scalar()
    if student is None:
        raise NoResultFound({"statement": "Student with this id does not exist.", "params": student_id})
    return student

async def update_student(session: AsyncSession, student_id: int, studentschema: schemas.StudentUpdate) -> models.Student:
    student_query = await session.execute(select(models.Student).where(models.Student.id == student_id))
    student = student_query.scalar()
    if student is None:
        raise NoResultFound({"statement": "Student with this id does not exist.", "params": student_id})
    
    if studentschema.group_id:
        group_query = await session.execute(select(models.Group.id).where(models.Group.id == studentschema.group_id))
        group = group_query.scalar()
        if group is None:
            raise NoResultFound({"statement": "Group with this id does not exist.", "params": studentschema.group_id})
    
    for field, value in studentschema:
        setattr(student, field, value) if value else None

    session.add(student)
    try:
        await session.commit()
        return student
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Student update failed.", ex.params, ex.orig)

async def delete_student(session: AsyncSession, student_id: int) -> models.Student:
    student_query = await session.execute(select(models.Student).where(models.Student.id == student_id))
    student = student_query.scalar()
    if student is None:
        raise NoResultFound({"statement": "Student with this id does not exist.", "params": student_id})
    try:
        await session.delete(student)
        await session.commit()
        return student
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Student update failed.", ex.params, ex.orig)