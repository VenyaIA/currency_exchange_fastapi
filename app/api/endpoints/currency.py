"""
Модуль для работы с валютными операциями через API маршруты.

Содержит маршруты для проверки авторизации, конвертации валют и получения списка доступных валют.
"""
from fastapi import APIRouter, Depends

from app.api.schemas.currency import CurrencyExch
from app.core.security import varify_user
from app.utils.external_api import get_list_currencies, currency_conversion

currency_router = APIRouter(
    prefix="/currency"
)


@currency_router.get("/testverified")
async def get_currency_exchange(verified_user: str = Depends(varify_user)):
    return {"message": "success"}


@currency_router.get("/exchange")
async def get_currency_exchange(cur_exc: CurrencyExch, verified_user: str = Depends(varify_user)):
    """
    Конвертация валют.
    Эндпоинт позволяет конвертировать валюты на основе данных, переданных в запросе.
    Args:
        cur_exc (CurrencyExch): Данные для конвертации валют (модель CurrencyExch).
        verified_user (str): Верифицированный пользователь, получаемый через Depends.
    Returns:
        dict: Результат конвертации валют.
    """
    return currency_conversion(cur_exc)


@currency_router.get("/list")
async def get_currency_list(verified_user: str = Depends(varify_user)):
    """
    Получение списка доступных валют.
    Эндпоинт возвращает список всех валют, доступных для использования в системе.
    Args:
        verified_user (str): Верифицированный пользователь, получаемый через Depends.
    Returns:
        dict: Список доступных валют.
    """
    return get_list_currencies()
