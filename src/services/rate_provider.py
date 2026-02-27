import time
import requests
from datetime import datetime, timezone
from typing import Optional

from config import API_BASE_URL, API_KEY, CACHE_TTL

_cache = {}

class RateError(Exception):
    pass


def _now_ts():
    return int(time.time())


def fetch_rate(source: str, target: str) -> dict:
    """Fetch rate from cache or API. Returns dict with keys: rate, is_from_cache, rate_timestamp, cached_at"""
    key = f"{source}_{target}"
    entry = _cache.get(key)
    now = _now_ts()
    if entry and now < entry['expires_at']:
        return {
            'rate': entry['rate'],
            'is_from_cache': True,
            'rate_timestamp': entry['rate_timestamp'].isoformat(),
            'cached_at': datetime.fromtimestamp(entry['cached_at'], tz=timezone.utc).isoformat()
        }

    # fetch from API: we request base=source and read target rate
    url = f"{API_BASE_URL}/{source}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        rates = data.get('rates')
        if not rates or target not in rates:
            raise RateError('Taxa não disponível para o par solicitado')
        rate = float(rates[target])
        rate_ts = None
        # try to parse date from API if present
        date_str = data.get('date')
        if date_str:
            try:
                rate_ts = datetime.fromisoformat(date_str)
            except Exception:
                rate_ts = datetime.now(timezone.utc)
        else:
            rate_ts = datetime.now(timezone.utc)

        # cache
        _cache[key] = {
            'rate': rate,
            'rate_timestamp': rate_ts,
            'cached_at': now,
            'expires_at': now + CACHE_TTL
        }

        return {
            'rate': rate,
            'is_from_cache': False,
            'rate_timestamp': rate_ts.isoformat(),
            'cached_at': datetime.fromtimestamp(now, tz=timezone.utc).isoformat()
        }

    except requests.RequestException as e:
        # API error: fallback to expired cache if present
        if entry:
            return {
                'rate': entry['rate'],
                'is_from_cache': True,
                'rate_timestamp': entry['rate_timestamp'].isoformat(),
                'cached_at': datetime.fromtimestamp(entry['cached_at'], tz=timezone.utc).isoformat()
            }
        raise RateError(str(e))
