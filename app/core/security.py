from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_async_session
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
exp_time = timedelta(minutes=settings.EXPIRATION_TIME)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Сравнивает введённый пароль с хэшированным паролем.

    Args:
        plain_password (str): Введённый пароль.
        hashed_password (str): Хэш пароля из базы данных.

    Returns:
        bool: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Хэширует пароль с использованием bcrypt.

    Args:
        password (str): Пароль для хэширования.

    Returns:
        str: Хэшированный пароль.
    """
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, session: AsyncSession = Depends(get_async_session)) -> bool:
    """
    Аутентифицирует пользователя по имени и паролю.
    Args:
        username (str): Имя пользователя.
        password (str): Введённый пароль.
        session (AsyncSession): Асинхронная сессия для работы с базой данных.

    Returns:
        Optional[User]: Пользовательский объект, если аутентификация успешна, иначе False.
    """
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user:
        return True
    return False


# Функция для создания JWT токена
async def create_jwt_token(data: dict):
    """
    Создаёт JWT токен с заданными данными и временем истечения.
    Args:
        data (dict): Данные, которые будут закодированы в токене.

    Returns:
        str: Закодированный JWT токен.
    """
    data.update({"exp": datetime.utcnow() + exp_time})
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
    # кодируем токен, передавая в него наш словарь с тем, что мы хотим там разместить


def varify_user(token: str = Depends(oauth2_scheme)):
    """
    Проверяет валидность JWT токена.

    Args:
        token (str): Токен, предоставленный пользователем.

    Returns:
        Optional[str]: Имя пользователя из токена, если он валиден.

    Raises:
        HTTPException: Если токен недействителен или истёк.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="The token has expired", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
