from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Student(BaseModel):
    group_id: int = Field(..., example=1)
    name: str = Field(..., example="Dmitry")
    phone: str | None = Field(None, example="+12345678901")
    address: str | None = Field(None, example="Lenina st. 6")

class StudentOut(Student):
    id: int

    class Config:
        orm_mode = True

class Professor(BaseModel):
    department_id: int
    name: str
    phone: Optional[str]
    address: Optional[str]

    class Config:
        orm_mode = True


class Group(BaseModel):
    id: int
    department_id: int
    enrolled_at: datetime

    class Config:
        orm_mode = True


class Department(BaseModel):
    id: int
    faculty_id: int
    name: str
    desc: Optional[str]
    url: Optional[str]

    class Config:
        orm_mode = True


class Faculty(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True


class Curriculum(BaseModel):
    id: int
    department_id: Optional[int]

    class Config:
        orm_mode = True


class Semester(BaseModel):
    id: int
    curriculum_id: Optional[int]
    start: datetime
    end: datetime

    class Config:
        orm_mode = True


class Course(BaseModel):
    id: int
    semester_id: int
    name: str
    desc: Optional[str]

    class Config:
        orm_mode = True


class Timeslot(BaseModel):
    id: int
    auditorium_id: Optional[int]
    class_id: Optional[int]
    exam_id: Optional[int]
    start: datetime
    end: datetime

    class Config:
        orm_mode = True


class Class(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Exam(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Task(BaseModel):
    id: int
    course_id: int
    name: str
    desc: Optional[str]
    created_at: datetime
    deadline: Optional[datetime]

    class Config:
        orm_mode = True


class Auditorium(BaseModel):
    id: int
    building_id: int
    room_number: int
    floor: int
    max_capacity: int
    has_projector: bool
    has_board: bool

    class Config:
        orm_mode = True


class Building(BaseModel):
    id: int
    department_id: Optional[int]
    address: str
    name: str
    floors: Optional[int]

    class Config:
        orm_mode = True


class Grade(BaseModel):
    id: int
    student_id: int
    grade: int
    task_id: Optional[int]
    exam_id: Optional[int]
    course_id: Optional[int]

    class Config:
        orm_mode = True