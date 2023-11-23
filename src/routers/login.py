from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth.token import create_token
from databases.pg import get_session
from schemas.user import LoginCredential
from services.login_service import LoginService, get_login_service

router = APIRouter(prefix="/api/login", tags=["Login"])


@router.post("")
async def login(
    login_credential: LoginCredential,
    session: AsyncSession = Depends(get_session),
    service: LoginService = Depends(get_login_service),
):
    user_id = await service.verify_credentials(
        username=login_credential.username, password=login_credential.password, session=session
    )
    token = create_token(user_id=user_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"token_type": "bearer", "access_token": token},
    )
