from requests import get

from app.api.schemas.currency import CurrencyExch
from app.core.config import settings

headers = {"apikey": settings.APIKEY}
to_currency = "RUB"
from_currency = "USD"
amount = 100
url = "https://api.apilayer.com/currency_data"


def currency_conversion(cur_exc: CurrencyExch):
    """
    Конвертирует сумму из одной валюты в другую.
    Args:
        cur_exc (CurrencyExch): Объект с данными для конвертации (валюта "от", валюта "к", сумма).

    Returns:
        float: Результат конвертации.

    Raises:
        ValueError: Если запрос к API завершился неудачно.
    """
    val_to = cur_exc.value_to.upper()
    val_from = cur_exc.value_from
    request = get(
        f"{url}/convert?to={val_to}&from={val_from}&amount={cur_exc.amount}",
        headers=headers
    )
    return request.json()["result"]


def get_list_currencies():
    """
    Получает список доступных валют из API.
    Returns:
        dict: Словарь валют в формате {код: описание}.

    Raises:
        ValueError: Если запрос к API завершился неудачно.
    """
    request = get(url + '/list', headers=headers)
    result = request.json()["currencies"]
    return result