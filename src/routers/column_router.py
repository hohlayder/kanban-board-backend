from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.column import ColumnCreate, ColumnUpdate, ColumnOut
from src.crud import column as column_crud
from src.security import get_current_user
from src.core.database import get_db
from src.models.models import User

router = APIRouter()


@router.post("/", response_model=ColumnOut)
async def create_column(
    column_data: ColumnCreate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await column_crud.create_column(session, column_data)


@router.get("/{column_id}", response_model=ColumnOut)
async def read_column(
    column_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    column = await column_crud.get_column_by_id(session, column_id)
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


@router.get("/project/{project_id}", response_model=list[ColumnOut])
async def get_columns_by_project(
    project_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await column_crud.get_columns_by_project(session, project_id)


@router.put("/{column_id}", response_model=ColumnOut)
async def update_column(
    column_id: UUID,
    column_data: ColumnUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_column = await column_crud.update_column(session, column_id, column_data)
    if not updated_column:
        raise HTTPException(status_code=404, detail="Column not found")
    return updated_column


@router.delete("/{column_id}")
async def delete_column(
    column_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await column_crud.delete_column(session, column_id)
    if not success:
        raise HTTPException(status_code=404, detail="Column not found")
    return {"detail": "Column deleted successfully"}
