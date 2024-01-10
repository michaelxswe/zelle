from fastapi import APIRouter, Depends
from schemas.account import (
    AccountCreate,
    AccountCredentials,
    AccountRead,
    AccountUpdate,
)
from schemas.token import AccessToken
from services.account import AccountService
from utils.auth import get_access_token

router = APIRouter(prefix="/v1", tags=["Accounts"])


@router.post("/accounts", response_model=AccountRead, status_code=201)
async def create_account(
    account_data: AccountCreate,
    account_service: AccountService = Depends(),
):
    return await account_service.create_account(account_data)


@router.get("/accounts", response_model=AccountRead, status_code=200)
async def get_account(
    access_token: str = Depends(get_access_token),
    account_service: AccountService = Depends(),
):
    return await account_service.get_account_by_access_token(access_token)


@router.patch("/accounts", response_model=AccountRead, status_code=200)
async def update_account(
    account_data: AccountUpdate,
    access_token: str = Depends(get_access_token),
    account_service: AccountService = Depends(),
):
    return await account_service.update_account(account_data, access_token)


@router.delete("/accounts", response_model=None, status_code=200)
async def delete_account(
    access_token: str = Depends(get_access_token),
    account_service: AccountService = Depends(),
):
    return await account_service.delete_account(access_token)


@router.post("/accounts/sign-in", response_model=AccessToken, status_code=200)
async def sign_in(
    account_credentials: AccountCredentials,
    account_service: AccountService = Depends(),
):
    access_token = await account_service.process_sign_in(account_credentials.username, account_credentials.password)
    return access_token
