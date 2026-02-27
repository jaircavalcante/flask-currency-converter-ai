# Quickstart — Real-Time Multi-Currency Converter

## Requisitos
- Python 3.11+
- Internet para consultar API de câmbio

## Instalação (local)

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale dependências:

```bash
pip install -r requirements.txt
```

3. Copie variáveis de ambiente:

```bash
cp .env.example .env
# Edite .env se precisar (API_BASE_URL, API_KEY se aplicável)
```

4. Execute a aplicação em modo de desenvolvimento:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Acesse `http://127.0.0.1:5000` no navegador.

## Observações
- Para este MVP usamos `exchangerate-api.com` como provedor. Ajuste `API_BASE_URL` em `.env` se quiser outro provedor.
- Não há banco de dados — cache em memória com TTL de 5 minutos.
