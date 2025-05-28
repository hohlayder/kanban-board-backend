from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from src.schemas.user import UserOut
from src.models.models import User
from src.core.database import get_db
from src.security import get_current_user
from src.crud import project as project_crud

router = APIRouter()


@router.post("/", response_model=ProjectOut)
async def create_project(
        project_data: ProjectCreate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project = await project_crud.create_project(session, project_data)
    await project_crud.add_user_to_project(session, project.id, current_user.id)
    return project


@router.get("/", response_model=list[ProjectOut])
async def get_all_projects(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return await project_crud.get_all_projects(session)


@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
        project_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project = await project_crud.get_project_by_id(session, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectOut)
async def update_project(
        project_id: UUID,
        project_data: ProjectUpdate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    updated_project = await project_crud.update_project(session, project_id, project_data)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/{project_id}")
async def delete_project(
        project_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    success = await project_crud.delete_project(session, project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted successfully"}


@router.post("/{project_id}/users/{user_id}")
async def add_user(
        project_id: UUID,
        user_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await project_crud.add_user_to_project(session, project_id, user_id)
    return {"detail": "User added to project"}


@router.delete("/{project_id}/users/{user_id}")
async def remove_user(
        project_id: UUID,
        user_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await project_crud.remove_user_from_project(session, project_id, user_id)
    return {"detail": "User removed from project"}


@router.get("/{project_id}/users", response_model=list[UserOut])
async def list_project_users(
        project_id: UUID,
        session: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    users = await project_crud.get_project_users(session, project_id)
    return users
