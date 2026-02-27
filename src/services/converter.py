from datetime import datetime, timezone
from typing import Tuple

from config import SUPPORTED_CURRENCIES
from src.services.rate_provider import fetch_rate, RateError


class ConversionError(Exception):
    pass


def validate_currency(code: str) -> bool:
    return code and code.upper() in SUPPORTED_CURRENCIES


def validate_amount(amount) -> float:
    try:
        v = float(amount)
    except Exception:
        raise ConversionError('Por favor insira um valor numérico válido')
    if v <= 0:
        raise ConversionError('O valor deve ser maior que zero')
    return v


def convert(amount, source: str, target: str) -> dict:
    source = source.upper()
    target = target.upper()
    if not validate_currency(source) or not validate_currency(target):
        raise ConversionError(f'Par de moedas não suportado: {source}/{target}')
    if source == target:
        raise ConversionError('Não é possível converter a mesma moeda')

    value = validate_amount(amount)

    try:
        rate_info = fetch_rate(source, target)
    except RateError as e:
        raise ConversionError('Não foi possível obter a taxa de câmbio: ' + str(e))

    rate = float(rate_info['rate'])
    result = round(value * rate, 2)

    return {
        'sourceAmount': value,
        'sourceCurrency': source,
        'resultAmount': result,
        'targetCurrency': target,
        'exchangeRate': rate,
        'rateSource': 'CACHE' if rate_info['is_from_cache'] else 'API',
        'rateTimestamp': rate_info.get('rate_timestamp'),
        'conversionTimestamp': datetime.now(timezone.utc).isoformat()
    }
