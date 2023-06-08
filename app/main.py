from fastapi import Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from .db import init_models, get_session
from .crud import insert_dummy_data
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
async def hello():
    return {"message": "hi :)"}

@app.post("/")
async def create_dummy_data(session: AsyncSession = Depends(get_session)):
    """Creates some dummy data in the database to test the requests"""
    await insert_dummy_data(session)
    return True