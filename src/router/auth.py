from config import Settings, settings
from database.postgresql.manager import session
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from jose import jwt
from schema.account import AccountCredentials
from schema.token import JWT
from service.auth import AuthService, auth_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/sign-in", response_model=JWT, status_code=200)
async def sign_in(
    account_credentials: AccountCredentials,
    session: AsyncSession = Depends(session),
    service: AuthService = Depends(auth_service),
    settings: Settings = Depends(settings),
):
    account_id = await service.verify_account_credentials(
        account_credentials.username, account_credentials.password, session
    )

    exp = datetime.utcnow() + timedelta(minutes=30)
    encode = {"account_id": account_id, "exp": exp}
    token = jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return JWT(type="bearer", token=token)
