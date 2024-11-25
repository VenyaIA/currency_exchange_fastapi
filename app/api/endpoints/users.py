"""
Модуль для маршрутов авторизации и аутентификации пользователей.

Содержит маршруты для регистрации нового пользователя и входа в систему с выдачей JWT-токена.
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import UserAuth, UserLogin
from app.core.security import get_password_hash, authenticate_user, create_jwt_token
from app.db.database import get_async_session
from app.db.models import User

auth_router = APIRouter(
    prefix="/auth"
)


@auth_router.post("/register", response_model=dict)
async def register(user_in: UserAuth, session: AsyncSession = Depends(get_async_session)):
    """
    Регистрация нового пользователя.
    Эндпоинт принимает данные пользователя, хэширует пароль, сохраняет пользователя в базе данных
    и возвращает сообщение об успешной регистрации.
    Args:
        user_in (UserAuth): Данные пользователя для регистрации (модель UserAuth).
        session (AsyncSession): Асинхронная сессия для взаимодействия с базой данных.

    Returns:
        dict: Сообщение об успешной регистрации пользователя.

    Raises:
        HTTPException: Если пароли не совпадают.
    """
    if user_in.password == user_in.repeat_password:
        password_hash = get_password_hash(user_in.password)

        user_in = user_in.model_dump()

        user_in = User(username=user_in["username"], password=password_hash)
        session.add(user_in)
        await session.commit()
        await session.refresh(user_in)
        return {"message": "User registration was successfully!"}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@auth_router.post("/login")
async def login(user_in: UserLogin, response: Response):
    """
    Аутентификация пользователя.
    Эндпоинт проверяет учетные данные пользователя, генерирует JWT-токен при успешной аутентификации
    и добавляет его в заголовки ответа.
    Args:
        user_in (UserLogin): Данные для входа в систему (модель UserLogin).
        response (Response): Объект ответа для добавления заголовка Authorization.

    Returns:
        dict: Сообщение об успешной аутентификации.

    Raises:
        HTTPException: Если учетные данные неверны.
    """
    if authenticate_user(user_in.username, user_in.password):
        token = await create_jwt_token({"sub": user_in.username})

        response.headers["Authorization"] = "Bearer " + token
        return {"message": "User authentication was successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

