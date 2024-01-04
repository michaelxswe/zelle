from auth.guard import get_access_token
from fastapi import APIRouter, Depends
from schema.account import AccountCreate, AccountCredentials, AccountRead, AccountUpdate
from schema.token import AccessToken
from service.account import AccountService

router = APIRouter(prefix="/api/account", tags=["Account"])


@router.post("", response_model=AccountRead, status_code=201)
async def create_account(
    account_data: AccountCreate,
    account_service: AccountService = Depends(),
):
    return await account_service.create_account(account_data)


@router.get("", response_model=AccountRead, status_code=200)
async def get_account(
    access_token: str = Depends(get_access_token),
    account_service: AccountService = Depends(),
):
    return await account_service.get_account_by_access_token(access_token)


@router.patch("", response_model=AccountRead, status_code=200)
async def update_account(
    account_data: AccountUpdate,
    access_token: str = Depends(get_access_token),
    account_service: AccountService = Depends(),
):
    return await account_service.update_account(account_data, access_token)


@router.delete("", response_model=None, status_code=200)
async def delete_account(
    access_token: str = Depends(get_access_token),
    account_service: AccountService = Depends(),
):
    return await account_service.delete_account(access_token)


@router.post("/sign-in", response_model=AccessToken, status_code=200)
async def sign_in(
    account_credentials: AccountCredentials,
    account_service: AccountService = Depends(),
):
    access_token = await account_service.process_sign_in(account_credentials.username, account_credentials.password)
    return access_token
