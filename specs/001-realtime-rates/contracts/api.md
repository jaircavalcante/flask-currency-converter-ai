# API Contracts: Real-Time Multi-Currency Converter

Todas rotas retornam JSON ou renderizam templates HTML (interface em Português).

## Endpoints

### GET /
- Descrição: Página principal com formulário de conversão
- Resposta: HTML (template `index.html`)

### POST /convert
- Descrição: Executa conversão entre duas moedas
- Request (form data or JSON):
  - `amount` (string/number) — valor a ser convertido
  - `source` (string) — código da moeda de origem (ISO 4217, ex: USD)
  - `target` (string) — código da moeda alvo (ISO 4217, ex: BRL)
- Response (JSON or HTML): Em caso de JSON
```json
{
  "sourceAmount": 100.0,
  "sourceCurrency": "USD",
  "resultAmount": 520.0,
  "targetCurrency": "BRL",
  "exchangeRate": 5.2,
  "rateSource": "API", // ou "CACHE"
  "rateTimestamp": "2026-02-27T14:35:22Z",
  "conversionTimestamp": "2026-02-27T14:35:23Z"
}
```
- Erros (HTTP 400/503) retornam JSON com `{ "error": "mensagem" }` ou exibem mensagem amigável em HTML.

### GET /rates?source=USD&target=BRL
- Descrição: Retorna taxa atual entre source e target
- Response (JSON):
```json
{
  "source": "USD",
  "target": "BRL",
  "rate": 5.2,
  "isFromCache": false,
  "rateTimestamp": "2026-02-27T14:35:22Z",
  "cachedAt": "2026-02-27T14:35:22Z"
}
```

### GET /currencies
- Descrição: Lista moedas suportadas
- Response (JSON):
```json
{
  "currencies": [
    {"code": "USD", "name": "Dollar (USD)"},
    {"code": "BRL", "name": "Real Brasileiro (BRL)"},
    {"code": "CLP", "name": "Peso Chileno (CLP)"},
    {"code": "EUR", "name": "Euro (EUR)"},
    {"code": "GBP", "name": "Libra Esterlina (GBP)"}
  ]
}
```

## Observações
- Endpoints aceitam `application/x-www-form-urlencoded` e `application/json` para `POST /convert`.
- Todas respostas JSON usam `UTF-8`.
- Mensagens de erro devem ser claras e em Português.
- Roteiro das URLs foi pensado para uso local (`localhost:5000`).
