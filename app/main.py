from fastapi import FastAPI
from .db import get_session, init_models
from .routers import courses, grades, students, teachers
from . import models, schemas

app = FastAPI()
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(students.router)
app.include_router(teachers.router)

@app.on_event("startup")
async def startup():
    await init_models()

@app.get("/")
async def startup():
    return {"message": "hi :)"}