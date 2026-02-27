# Data Model: Real-Time Multi-Currency Converter

**Phase**: 1 (Design)  
**Date**: 2026-02-27  
**Purpose**: Define all data entities, attributes, relationships, and validation rules

## Overview

Three core entities represent the domain:
1. **Currency** - Supported currencies (USD, BRL, CLP, EUR, GBP)
2. **ExchangeRate** - Conversion ratio between two currencies with freshness timestamp
3. **ConversionResult** - Result of a conversion operation with all context

No persistence layer required; all data flows through request/response.

---

## Entity: Currency

**Purpose**: Represents a supported currency that users can convert to/from

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| code | string | Yes | ISO 4217 code (3 uppercase letters) | Unique currency identifier (e.g., "USD", "BRL") |
| name | string | Yes | Non-empty string | Full currency name (e.g., "United States Dollar") |
| symbol | string | Yes | Single character or 1-2 chars | Currency symbol for display (e.g., "$", "R$") |
| supportedForConversion | boolean | Yes | Always true | Indicates currency can be used in conversions (always true in current scope) |

**Example**:
```python
class Currency:
    code: str          # "USD"
    name: str          # "United States Dollar"
    symbol: str        # "$"
    supportedForConversion: bool  # True
```

**Validation Rules**:
- `code`: Must be exactly 3 uppercase letters (ISO 4217 standard)
- `name`: Cannot be empty or null
- `symbol`: Cannot be empty or null
- Unknown currency codes → raise `InvalidCurrencyError`

**Supported Currencies** (Scope Boundary):
- USD (United States Dollar, $)
- BRL (Brazilian Real, R$)
- CLP (Chilean Peso, $)
- EUR (Euro, €)
- GBP (British Pound, £)

---

## Entity: ExchangeRate

**Purpose**: Represents the conversion ratio between two currencies at a point in time

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| sourceCurrency | string | Yes | Valid currency code | Source currency (e.g., "USD") |
| targetCurrency | string | Yes | Valid currency code | Target currency (e.g., "BRL") |
| rate | float | Yes | Positive, > 0 | Conversion ratio (e.g., 1 USD = 5.20 BRL) |
| rateTimestamp | datetime | Yes | Not in future | When this rate was last updated from API |
| cachedAt | datetime | Yes | Not in future | When this data was cached locally |
| isFromCache | boolean | Yes | true/false | Whether rate is from cache (expired) or fresh from API |

**Example**:
```python
class ExchangeRate:
    sourceCurrency: str        # "USD"
    targetCurrency: str        # "BRL"
    rate: float                # 5.20
    rateTimestamp: datetime    # 2026-02-27 14:30:00 (API datatime)
    cachedAt: datetime         # 2026-02-27 14:35:22 (local cache time)
    isFromCache: bool          # False (fresh) or True (cached, possibly expired)
```

**Validation Rules**:
- `sourceCurrency` and `targetCurrency`: Must be valid currency codes; cannot be equal (no self-conversion)
- `rate`: Must be positive (> 0). Rates are never negative or zero
- `rateTimestamp`: Cannot be in future relative to system time
- `cachedAt`: Cannot be in future relative to system time

**Example Creation**:
```python
# From fresh API call
fresh_rate = ExchangeRate(
    sourceCurrency="USD",
    targetCurrency="BRL",
    rate=5.20,
    rateTimestamp=datetime.now(),  # API provided time
    cachedAt=datetime.now(),       # Just cached
    isFromCache=False
)

# From cache (5 minutes old)
cached_rate = ExchangeRate(
    sourceCurrency="USD",
    targetCurrency="BRL",
    rate=5.20,
    rateTimestamp=datetime(2026, 2, 27, 14, 30),  # API time from 5 min ago
    cachedAt=datetime(2026, 2, 27, 14, 35),       # Cached 5 min ago
    isFromCache=True
)
```

---

## Entity: ConversionResult

**Purpose**: Represents the outcome of a currency conversion operation; all data needed to display result to user

**Attributes**:

| Field | Type | Required | Validation | Description |
|-------|------|----------|-----------|-------------|
| sourceAmount | float | Yes | Positive (>0), ≤ 999,999,999 | Amount to convert (e.g., 100.00) |
| sourceCurrency | string | Yes | Valid currency code | Source currency code (e.g., "USD") |
| resultAmount | float | Yes | Positive, rounded to 2 decimals | Converted amount (e.g., 520.00) |
| targetCurrency | string | Yes | Valid currency code | Target currency code (e.g., "BRL") |
| exchangeRate | float | Yes | Positive | Conversion rate used (e.g., 5.20) |
| conversionTimestamp | datetime | Yes | Not in future | When conversion was performed |
| rateSource | string | Yes | "API" or "CACHE" | Whether rate came from live API or cache |
| rateFreshness | string | Yes | Enum | "REAL_TIME" or "CACHED_X_MIN_AGO" |

**Example**:
```python
class ConversionResult:
    sourceAmount: float         # 100.00
    sourceCurrency: str         # "USD"
    resultAmount: float         # 520.00
    targetCurrency: str         # "BRL"
    exchangeRate: float         # 5.20
    conversionTimestamp: datetime  # 2026-02-27 14:35:22
    rateSource: str             # "API" or "CACHE"
    rateFreshness: str          # "REAL_TIME" or "CACHED_5_MIN_AGO"
```

**Validation Rules**:
- `sourceAmount`: 
  - Must be positive (> 0)
  - Cannot be negative or zero
  - Cannot exceed 999,999,999 (reasonable upper limit)
  - Validation error: "Amount must be a positive number"
  
- `sourceCurrency` and `targetCurrency`: Must differ; cannot convert currency to itself

- `resultAmount`: 
  - Calculated as: sourceAmount × exchangeRate
  - Rounded to 2 decimal places for display
  - Example: 100.00 USD × 5.204 = 520.40 BRL (rounded)

- `exchangeRate`: Must match the rate from ExchangeRate entity

- `conversionTimestamp`: Server timestamp when conversion was performed

- `rateSource`: Must be either "API" or "CACHE"

- `rateFreshness`: 
  - If from API: "REAL_TIME"
  - If from cache < 5 min old: "CACHED_LESS_THAN_5_MIN_AGO"
  - If from cache >= 5 min old: "CACHED_5_MIN_AGO"

**Calculation Logic**:
```python
def createConversionResult(sourceAmount, sourceCurrency, targetCurrency, rate, isFromCache, rateTimestamp):
    resultAmount = round(sourceAmount * rate, 2)
    
    if isFromCache:
        age = now() - rateTimestamp
        if age.total_seconds() < 300:  # 5 minutes = 300 seconds
            freshness = f"CACHED_{int(age.total_seconds()//60)}_MIN_AGO"
        else:
            freshness = "CACHED_5_PLUS_MIN_AGO"
        rateSource = "CACHE"
    else:
        freshness = "REAL_TIME"
        rateSource = "API"
    
    return ConversionResult(
        sourceAmount=sourceAmount,
        sourceCurrency=sourceCurrency,
        resultAmount=resultAmount,
        targetCurrency=targetCurrency,
        exchangeRate=rate,
        conversionTimestamp=now(),
        rateSource=rateSource,
        rateFreshness=freshness
    )
```

---

## Relationships

```
User Input (amount, source, target)
     ↓
Validation (Currency, amount range)
     ↓
Lookup ExchangeRate (source → target)
     ↓
Create ConversionResult (calculate, timestamp, source)
     ↓
Return to User
```

No direct relationships between entities (no foreign keys, no joins). Each entity is independent; ConversionResult aggregates data from Currency and ExchangeRate for display.

---

## Error Handling

**Invalid Inputs → Exception Types**:

| Scenario | Exception | HTTP Status | User Message |
|----------|-----------|------------|--------------|
| Amount is negative, zero, or non-numeric | `InvalidAmountError` | 400 | "Please enter a valid amount (must be positive)" |
| Currency code not in supported list | `InvalidCurrencyError` | 400 | "Currency code ABC is not supported" |
| Source and target are same | `InvalidPairError` | 400 | "Cannot convert currency to itself" |
| API is down, no cache available | `RateUnavailableError` | 503 | "Unable to fetch exchange rates. Please try again later." |
| API response malformed | `APIResponseError` | 503 | "Exchange rate service error. Please try again." |

---

## State Transitions (Optional)

No state machines; entities are immutable after creation. Each HTTP request creates fresh entities.

---

## Testing (Manual Verification Checklist)

✅ Coverage via manual testing during development:

**Happy Path**:
- [ ] Convert 100 USD to BRL (known rate, verify calculation)
- [ ] Convert 500 BRL to USD (known rate, verify inverse calculation)
- [ ] Round-trip conversion (100 USD → BRL → USD should match input ±0.01)

**Edge Cases**:
- [ ] Enter 0 → Error message displays
- [ ] Enter -100 → Error message displays
- [ ] Enter "abc" → Error message displays
- [ ] Enter 999999999 → Large number displays correctly rounded
- [ ] Select invalid currency code → Error message displays
- [ ] API down → Graceful error, uses cache if available

**Rate Display**:
- [ ] Timestamp shown with rate (REAL_TIME vs CACHED)
- [ ] Rate recalculation after cache expires
- [ ] Rate accuracy matches API response (within 0.01%)
