import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.exchangerate-api.com/v4/latest')
API_KEY = os.getenv('API_KEY', '')
CACHE_TTL = int(os.getenv('CACHE_TTL', '300'))

SUPPORTED_CURRENCIES = ['USD', 'BRL', 'CLP', 'EUR', 'GBP']
