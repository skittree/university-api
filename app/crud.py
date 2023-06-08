from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def create_student(session: AsyncSession, studentschema: schemas.Student) -> models.Student:
    group = await session.execute(select(models.Group).where(models.Group.id == studentschema.group_id))
    group = group.scalar()
    if group is None:
        raise NoResultFound({"statement": "Group with this id does not exist.", "params": studentschema.group_id})
    student = models.Student(**studentschema.dict(), group=group)
    session.add(student)
    try:
        await session.commit()
        return student
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Student already in database.", ex.params, ex.orig)

async def get_student(session: AsyncSession, student_id: int) -> models.Student:
    student = await session.execute(select(models.Student).where(models.Student.id == student_id))
    # use scalar or scalar_one? this approach allows us to throw our own exception, but scalar_one is more concise
    student = student.scalar()
    if student is None:
        raise NoResultFound({"statement": "Student with this id does not exist.", "params": student_id})
    return student