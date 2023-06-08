from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .db import init_models
from .routers import courses, grades, professors, students
from sqlalchemy.exc import IntegrityError, NoResultFound

app = FastAPI()
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(students.router)
app.include_router(professors.router)


@app.exception_handler(NoResultFound)
async def NoResultFoundHandler(request: Request, ex: NoResultFound):
    return JSONResponse(status_code = 404, content = ex.args)

@app.exception_handler(IntegrityError)
async def IntegrityErrorHandler(request: Request, ex: IntegrityError):
    return JSONResponse(status_code = 409, content = {"statement": ex.statement, "params": ex.params})

@app.on_event("startup")
async def startup():
    await init_models()

@app.get("/")
async def startup():
    return {"message": "hi :)"}