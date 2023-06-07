from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from .db import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="students")
    courses = relationship("Course", secondary="course_students", back_populates="students")

class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)
    courses = relationship("Course", secondary="course_professors", back_populates="professors")
    department = relationship("Department", back_populates="professors")

class Group(Base):
    __tablename__ = "groups"
 
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="groups")

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    name = Column(String, nullable=False)
    desc = Column(String)
    url = Column(String)
    faculty = relationship("Faculty", back_populates="departments")
    buildings = relationship("Building", back_populates="departments")
    professors = relationship("Professor", back_populates="departments")

class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Curriculum(Base):
    __tablename__ = "curriculums"

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    department = relationship("Department", back_populates="groups")

class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True)
    curriculum_id = Column(Integer, ForeignKey("curriculums.id"))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    curriculum = relationship("Curriculum", back_populates="semesters")
    courses = relationship("Course", back_populates="semesters")

# it is possible to facilitate the same split with less tables via a "roles" table, emulating the "participant" class in the UML diagram
# for the current implementation i believe having separate tables (students and professors, students/profs to course) yields the best performance

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"))
    name = Column(String, nullable=False)
    desc = Column(String)
    students = relationship("Student", secondary="course_students", back_populates="courses")
    professors = relationship("Professor", secondary="course_professors", back_populates="courses")
    tasks = relationship("Task", back_populates="courses")
    grades = relationship("Grade", back_populates="courses")
    semester = relationship("Semester", back_populates="courses")

course_students = Table("course_students", Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("student_id", ForeignKey("students.id"), primary_key=True)
)

course_professors = Table("course_professors", Base.metadata,
    Column("course_id", ForeignKey("courses.id"), primary_key=True),
    Column("professor_id", ForeignKey("professors.id"), primary_key=True)
)

# the approach of saving NULLable columns, while violating the 3NF rule, can help us make less requests at the cost of extra disk space
# we can find the exact thing that occupies the timeslot by just retrieving this table

# if we were to add this relationship to Class and Exam tables instead, 
# looking up timeslot availability would require us to check both the class and exam tables

class Timeslot(Base):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True)
    auditorium_id = Column(Integer, ForeignKey("auditoriums.id"))
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    auditorium = relationship("Auditorium", back_populates="timeslots")
    classes = relationship("Class", back_populates="timeslots", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="timeslots", cascade="all, delete-orphan")
    # add unique constraints to ensure we can only have the class/exam take one timeslot
    __table_args__ = (UniqueConstraint('class_id'), UniqueConstraint('exam_id'))
    

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timeslot = relationship("Timeslot", back_populates="classes")

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    timeslot = relationship("Timeslot", back_populates="exams")
    grades = relationship("Grade", back_populates="exams")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    deadline = Column(DateTime)
    course = relationship("Course", back_populates="tasks")
    grades = relationship("Grade", back_populates="tasks")

class Auditorium(Base):
    __tablename__ = "auditoriums"

    id = Column(Integer, primary_key=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    room_number = Column(Integer, nullable=False)
    floor = Column(Integer)
    max_capacity = Column(Integer)
    has_projector = Column(Boolean, nullable=False)
    has_board = Column(Boolean, nullable=False)
    building = relationship("Building", back_populates="auditoriums")
    timeslots = relationship("Timeslot", back_populates="auditoriums")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.id"))
    address = Column(String, nullable=False)
    name = Column(String, nullable=False)
    floors = Column(Integer)
    auditoriums = relationship("Auditorium", back_populates="buildings")
    department = relationship("Department", back_populates="buildings")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    grade = Column(Integer, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    student = relationship("Student", back_populates="grades")
    task = relationship("Task", back_populates="grades")
    exam = relationship("Exam", back_populates="grades")
    course = relationship("Course", back_populates="grades")