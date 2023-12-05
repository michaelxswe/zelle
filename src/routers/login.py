from auth.jwt import create_token
from databases.postgresql.client import get_session
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from schemas.user import LoginCredential
from services.login_service import LoginService, get_login_service
from sqlalchemy.ext.asyncio import AsyncSession

login = APIRouter(prefix = '/api/login', tags = ['Login'])

@login.post("")
async def sign_in(
    login_credential: LoginCredential,
    session: AsyncSession = Depends(get_session),
    service: LoginService = Depends(get_login_service)
):

    user_id = await service.verify_credentials(
        username = login_credential.username,
        password = login_credential.password,
        session = session
    )
    
    token = create_token(user_id = user_id)
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"token_type": "bearer", "access_token": token}
    )