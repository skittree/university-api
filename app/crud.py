from datetime import datetime
from dateutil.relativedelta import relativedelta
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

async def add_course_grade(session: AsyncSession, schema: schemas.CourseGradeCreate) -> models.Grade:
    params = {"student_id": schema.student_id, "course_id": schema.course_id}
    student_query = await session.execute(
        select(models.Student)        
        .join(models.Student.courses)
        .where(
            (models.Student.id == schema.student_id)
            & (models.Course.id == schema.course_id)
        )
    )
    student = student_query.scalar()

    if student is None:
        raise NoResultFound({"statement": "Student cannot be found for the specified course.", "params": params})

    grade_query = await session.execute(select(models.Grade).where((models.Grade.student_id == schema.student_id) & (models.Grade.course_id == schema.course_id)))
    grade = grade_query.scalar()
    if grade:
        raise IntegrityError("Grade already placed for student in this course.", params, grade_query)

    grade = models.Grade(**schema.dict())
    session.add(grade)
    try:
        await session.commit()
        return grade
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Course grade add failed.", ex.params, ex.orig)

async def update_course_grade(session: AsyncSession, grade_id: int, schema: schemas.CourseGradeUpdate) -> models.Grade:
    grade_query = await session.execute(
        select(models.Grade).where(models.Grade.id == grade_id)
    )
    grade = grade_query.scalar()

    if grade is None:
        raise NoResultFound({"statement": "Grade with id cannot be found", "params": grade_id})

    grade.grade = schema.grade

    session.add(grade)
    try:
        await session.commit()
        return grade
    except IntegrityError as ex:
        await session.rollback()
        raise IntegrityError("Course grade update failed.", ex.params, ex.orig)
    
async def insert_dummy_data(session: AsyncSession):
    data = [
        models.Faculty(code="03.03.09", name="Faculty1"),
        models.Faculty(code="04.03.09", name="Faculty2"),
        models.Department(name="Mathematics Department", faculty_id=1),
        models.Department(name="Linguistics Department", faculty_id=2),
        models.Group(enrolled_at=datetime.now(), department_id=1),
        models.Group(enrolled_at=datetime.now()-relativedelta(years=1), department_id=1),
        models.Group(enrolled_at=datetime.now()-relativedelta(years=2), department_id=2),
        models.Professor(name="Professor1", phone="1111111111", address="789 Oak St", department_id=1),
        models.Professor(name="Professor2", phone="2222222222", address="456 Pine St", department_id=2),
        models.Curriculum(department_id=1, name="Beginner Math"),
        models.Curriculum(department_id=2, name="Beginner English"),
        models.Semester(curriculum_id=1, start=datetime.now(), end=datetime.now()+relativedelta(months=3)),
        models.Semester(curriculum_id=1, start=datetime.now()-relativedelta(months=3), end=datetime.now()),
    ]

    students = [
        models.Student(group_id=1, name="John Doe", phone="1234567890", address="123 Main St"),
        models.Student(group_id=1, name="Jane Smith", phone="9876543210", address="456 Elm St"),
        models.Student(group_id=2, name="Jane Doe", phone="1234563210", address="123 Elm St"),
        models.Student(group_id=3, name="John Smith", phone="9876547890", address="456 Main St"),
    ]

    course = models.Course(semester_id=1, name="Математика", students=students)

    session.add_all(data)
    session.add_all(students)
    session.add(course)
    await session.commit()