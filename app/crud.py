from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def add_student(session: AsyncSession, schema: schemas.StudentCreate) -> models.Student:
    group_query = await session.execute(select(models.Group).where(models.Group.id == schema.group_id))
    # use scalar or scalar_one? this approach allows us to throw our own exception message, but scalar_one is more concise
    group = group_query.scalar()
    if group is None:
        raise NoResultFound({"statement": "Group with this id does not exist.", "params": schema.group_id})
    student = models.Student(**schema.dict(), group=group)
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

async def update_student(session: AsyncSession, student_id: int, schema: schemas.StudentUpdate) -> models.Student:
    student_query = await session.execute(select(models.Student).where(models.Student.id == student_id))
    student = student_query.scalar()
    if student is None:
        raise NoResultFound({"statement": "Student with this id does not exist.", "params": student_id})
    
    if schema.group_id:
        group_query = await session.execute(select(models.Group.id).where(models.Group.id == schema.group_id))
        group = group_query.scalar()
        if group is None:
            raise NoResultFound({"statement": "Group with this id does not exist.", "params": schema.group_id})
    
    for field, value in schema:
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
        raise IntegrityError("Student delete failed.", ex.params, ex.orig)
    
async def get_professors(session: AsyncSession) -> list[models.Professor]:
    professor_query = await session.execute(select(models.Professor))
    return professor_query.scalars().all()

async def add_course(session: AsyncSession, schema: schemas.CourseCreate) -> models.Course:
    if schema.semester_id:
        semester_query = await session.execute(select(models.Semester).where(models.Semester.id == schema.semester_id))
        semester = semester_query.scalar()
        if semester is None:
            raise NoResultFound({"statement": "Semester with this id does not exist.", "params": schema.semester_id})
    
    course = models.Course(**schema.dict())
    session.add(course)
    try:
        await session.commit()
        return course
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Course add failed.", ex.params, ex.orig)

async def get_course(session: AsyncSession, course_id: int) -> models.Course:
    course_query = await session.execute(select(models.Course).where(models.Course.id == course_id))
    course = course_query.scalar()
    if course is None:
        raise NoResultFound({"statement": "Course with this id does not exist.", "params": course_id})
    return course

async def get_course_students(session: AsyncSession, course_id: int) -> list[models.Student]:
    course_query = await session.execute(select(models.Course).options(selectinload(models.Course.students)).where(models.Course.id == course_id))
    course = course_query.scalar()
    if course is None:
        raise NoResultFound({"statement": "Course with this id does not exist.", "params": course_id})
    return course.students