from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import parse_obj_as
from fastapi import APIRouter, Depends
from .. import schemas, crud
from ..db import get_session

router = APIRouter(
    prefix="/professors",
    tags=["Professors"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_professors(session: AsyncSession = Depends(get_session)) -> list[schemas.ProfessorOut]:
    professors = await crud.get_professors(session)
    return parse_obj_as(list[schemas.ProfessorOut], professors)