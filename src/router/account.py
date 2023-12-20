from auth.guard import validate_jwt
from database.postgresql.manager import session
from fastapi import APIRouter, Depends
from schema.account import AccountCreate, AccountRead, AccountUpdate
from service.account import AccountService, account_service
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

router = APIRouter(prefix="/api/accounts", tags=["Account"])


@router.post("", response_model=AccountRead, status_code=201)
async def create_account(
    data: AccountCreate,
    session: AsyncSession = Depends(session),
    service: AccountService = Depends(account_service),
):
    return await service.create_account(data, session)


@router.get("", response_model=AccountRead, status_code=200)
async def get_account(
    claims: dict[str, Any] = Depends(validate_jwt),
    session: AsyncSession = Depends(session),
    service: AccountService = Depends(account_service),
):
    return await service.get_account(claims, session)


@router.patch("", response_model=AccountRead, status_code=200)
async def update_account(
    data: AccountUpdate,
    claims: dict[str, Any] = Depends(validate_jwt),
    session: AsyncSession = Depends(session),
    service: AccountService = Depends(account_service),
):
    return await service.update_account(data, claims, session)


@router.delete("", response_model=None, status_code=200)
async def delete_account(
    claims: dict[str, Any] = Depends(validate_jwt),
    session: AsyncSession = Depends(session),
    service: AccountService = Depends(account_service),
):
    return await service.delete_account(claims, session)
