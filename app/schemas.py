from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BasePerson(BaseModel):
    phone: str | None = Field(None, example="+12345678901")
    address: str | None = Field(None, example="Lenina st. 6")

class StudentCreate(BasePerson):
    group_id: int = Field(..., example=1)
    name: str = Field(..., example="Dmitry")

class StudentOut(StudentCreate):
    id: int

    class Config:
        orm_mode = True

class StudentUpdate(BasePerson):
    group_id: int | None = Field(None, example=1)
    name: str | None = Field(None, example="Ivan")

class ProfessorCreate(BasePerson):
    department_id: int = Field(..., example=1)
    name: str = Field(..., example="John")

class ProfessorOut(ProfessorCreate):
    id: int

    class Config:
        orm_mode = True

class BaseCourse(BaseModel):
    desc: str = Field(None, example="Applied mathematics for first years")
    semester_id: int | None = Field(None, example=1)

class CourseCreate(BaseCourse):
    name: str = Field(..., example="Mathematics 1")

class CourseOut(CourseCreate):
    id: int

    class Config:
        orm_mode = True

class CourseUpdate(BaseCourse):
    semester_id: int | None = Field(None, example=2)
    name: str | None = Field(None, example="Mathematics 2")

class CourseGradeBase(BaseModel):
    course_id: int | None = Field(None, example=1)

class CourseGradeCreate(CourseGradeBase):
    student_id: int = Field(..., example=1)
    grade: int = Field(..., example=5)

class CourseGradeOut(CourseGradeCreate):
    id: int

    class Config:
        orm_mode = True

class CourseGradeUpdate(BaseModel):
    grade: int = Field(..., example=2)

# non-developed classes

# class Group(BaseModel):
#     id: int
#     department_id: int
#     enrolled_at: datetime

#     class Config:
#         orm_mode = True

# class Department(BaseModel):
#     id: int
#     faculty_id: int
#     name: str
#     desc: Optional[str]
#     url: Optional[str]

#     class Config:
#         orm_mode = True

# class Faculty(BaseModel):
#     id: int
#     code: str
#     name: str

#     class Config:
#         orm_mode = True

# class Curriculum(BaseModel):
#     id: int
#     department_id: Optional[int]

#     class Config:
#         orm_mode = True

# class Semester(BaseModel):
#     id: int
#     curriculum_id: Optional[int]
#     start: datetime
#     end: datetime

#     class Config:
#         orm_mode = True

# class Timeslot(BaseModel):
#     id: int
#     auditorium_id: Optional[int]
#     class_id: Optional[int]
#     exam_id: Optional[int]
#     start: datetime
#     end: datetime

#     class Config:
#         orm_mode = True

# class Class(BaseModel):
#     id: int
#     name: str

#     class Config:
#         orm_mode = True

# class Exam(BaseModel):
#     id: int
#     name: str

#     class Config:
#         orm_mode = True

# class Task(BaseModel):
#     id: int
#     course_id: int
#     name: str
#     desc: Optional[str]
#     created_at: datetime
#     deadline: Optional[datetime]

#     class Config:
#         orm_mode = True

# class Auditorium(BaseModel):
#     id: int
#     building_id: int
#     room_number: int
#     floor: int
#     max_capacity: int
#     has_projector: bool
#     has_board: bool

#     class Config:
#         orm_mode = True

# class Building(BaseModel):
#     id: int
#     department_id: Optional[int]
#     address: str
#     name: str
#     floors: Optional[int]

#     class Config:
#         orm_mode = True