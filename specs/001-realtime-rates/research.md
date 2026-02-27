# Research: Real-Time Multi-Currency Converter

**Phase**: 0 (Research & Clarifications)  
**Date**: 2026-02-27  
**Purpose**: Resolve all technical unknowns before design and implementation

## Exchange Rate API Selection

### Decision: exchangerate-api.com (Free Tier)

**Rationale**: 
- Free tier provides 1,500 requests/month (50/day) - sufficient for small application
- Supports 160+ currencies including all required (USD, BRL, CLP, EUR, GBP)
- No authentication required for free tier (simplifies implementation)
- JSON response format, straightforward REST API
- Reliable uptime, well-documented API specification

**Alternatives Considered**:
1. **fixer.io** - Free tier limited to EUR base currency only; not suitable for multi-directional USD conversion
2. **currencyapi.com** - Free tier requires API key setup; slightly more complex
3. **openexchangerates.org** - Excellent service but free tier is very limited (1000/month)
4. **exchangerate.host** - Open-source, no authentication, but less reliable in China/restricted regions

**API Endpoint**: `https://api.exchangerate-api.com/v4/latest/{currency_code}`

**Example Response**:
```json
{
  "rates": {
    "BRL": 5.20,
    "CLP": 850.45,
    "EUR": 0.92,
    "GBP": 0.79,
    "USD": 1.0
  },
  "base": "USD",
  "date": "2026-02-27"
}
```

**Expected Behavior**:
- Response time: 200-500ms
- Success rate: 99%+ uptime
- Rate updates: Once per business day

---

## Rate Caching Strategy

### Decision: In-Memory Cache with 5-Minute TTL

**Rationale**:
- Real-time API calls on every conversion would exceed free tier quota quickly (1,500/month = ~50/day)
- 5-minute TTL balances "real-time" perception with API quota management
- In-memory cache is simplest implementation (no Redis/database needed, aligns with "small and simple" constitution)
- Users checking rates 5 times within 1 minute still see same rate (realistic behavior)

**Cache Implementation**:
```python
# Pseudocode
cache = {
    "USD_BRL": {"rate": 5.20, "timestamp": <5min ago>, "expires_at": <now>},
    "BRL_USD": {"rate": 0.192, "timestamp": <5min ago>, "expires_at": <now>}
}

def getCachedRate(source, target):
    key = f"{source}_{target}"
    if key in cache and not isExpired(cache[key]):
        return cache[key]["rate"]
    else:
        # Fetch from API and refresh cache
        return fetchFromAPI(source, target)
```

**Fallback Behavior**:
- If API is down and cache expired: return cached rate anyway with warning "Rate may be outdated"
- If both cache and API fail: show error "Unable to fetch exchange rate. Please try again."

---

## Python Flask Best Practices Integration

### Decision: Lightweight Flask + Blueprint Modularization

**Rationale**:
- Flask is minimal (good for small scope), avoiding Django's heavy infrastructure
- Blueprints enable modular routing without over-engineering
- Jinja2 templates (built-in) sufficient for simple HTML forms
- No ORM needed; models are simple data classes or dataclasses

**Project Structure Rationale**:
- `src/services/` - Encapsulates external API calls; isolation enables testing and reuse
- `src/models/` - Data structures; domain logic independent of Flask
- `src/routes/` - HTTP endpoint handlers; thin layer between HTTP and business logic
- No middleware bloat; error handling via try-except in route handlers
- Static typing strongly encouraged in Python per constitution ("Clear Naming")

**Flask Configuration**:
- Use `.env` file for API keys and configuration (python-dotenv)
- Development mode: `FLASK_ENV=development` with auto-reload
- Debug mode disabled in production; manual testing mode for small scope

---

## Error Handling Patterns for Third-Party API Integration

### Decision: Graceful Degradation with User-Friendly Messages

**Patterns Implemented**:

1. **Timeout Handling** (Requests take > 5 seconds)
   - Return error: "Exchange rate service is temporarily slow. Please try again."
   - Retry logic: Single retry with 2-second wait before giving up

2. **API Unavailability** (HTTP 5xx or connection error)
   - Use cached rate if available: "Using cached rate from X minutes ago" (warning)
   - If no cache: "Unable to fetch current rates. Please check your internet connection."

3. **Invalid Input** (User enters negative amount, non-numeric, invalid currency)
   - Validation happens in `converter.py` before API call
   - Error message: "Please enter a valid amount (must be positive)" 
   - Currency mismatch: "Currency pair USD/XXX not supported"

4. **Rate Limit Exceeded** (If API returns 429 Too Many Requests)
   - Surface to user: "Rate service is busy. Please wait a few minutes and try again."
   - Log: Track rate limit hits to adjust caching strategy

5. **Malformed API Response** (API returns unexpected JSON structure)
   - Treat as API failure; use GracefulDegradation pattern above
   - Log error internally for debugging

**Example Implementation in routes/conversion.py**:
```python
@conversionBlueprint.route('/convert', methods=['POST'])
def convertCurrency():
    try:
        amount = request.form.get('amount')
        source = request.form.get('source')
        target = request.form.get('target')
        
        # Validation (clean code: fail fast)
        if not isValidAmount(amount):
            return {"error": "Please enter a valid amount"}, 400
        if not isValidCurrency(source) or not isValidCurrency(target):
            return {"error": "Invalid currency code"}, 400
        
        # Conversion (service layer handles API calls)
        result = converter.convertCurrency(amount, source, target)
        return {"result": result.resultAmount, "rate": result.rate, "timestamp": result.timestamp}
    
    except APITimeoutError:
        return {"error": "Service is currently slow, please try again"}, 503
    except APICriticalError:
        return {"error": "Unable to fetch rates at this time"}, 503
```

---

## Implementation Dependencies

**Confirmed Dependencies**:
- `Flask==2.3.2` - Web framework
- `requests==2.31.0` - HTTP client for API calls
- `python-dotenv==1.0.0` - Environment variable management

**Optional (Not Included)**:
- Testing frameworks (pytest, unittest) - per constitution, manual testing only
- Database (SQLAlchemy, mongoengine) - no persistence needed
- Authentication (Flask-Login, Flask-JWT) - public application
- Logging framework (loguru, structlog) - simple print() statements suffice for MVP

---

## Browser/Environment Compatibility

**Target Environment**: Desktop browser (Chrome, Firefox, Safari, Edge)

**HTML/CSS Approach**: 
- HTML5 with basic CSS (no CSS framework like Bootstrap to keep simple)
- Form submission to Flask backend (no JavaScript AJAX needed for MVP)
- Each conversion performs a page reload showing results (simple, reliable)

**Browsers Supported**:
- Modern browsers with HTML5 form support (all current versions)
- No special polyfills or compatibility layers needed

---

## Assumptions Validated

✅ **exchangerate-api.com free tier is sufficient** for 50 conversions/day usage estimate  
✅ **5-minute rate caching** satisfies "real-time" requirement while respecting API quotas  
✅ **In-memory caching** is simplest solution for small scope (no Redis/database)  
✅ **Manual testing** is approved by constitution for small-scope projects  
✅ **HTML forms** are sufficient UI for currency conversion (no SPA needed)  

---

## Open Questions Resolved

1. **Q: Which free API to use?**  
   **A**: exchangerate-api.com - Free tier covers all requirements, well-documented, reliable

2. **Q: How often should rates be updated?**  
   **A**: Every 5 minutes via caching strategy; API rates update once/day anyway

3. **Q: How to handle API failures?**  
   **A**: Graceful degradation - use cached rates if available, user-friendly error messages otherwise

4. **Q: Do we need a database?**  
   **A**: No. Rates are fetched on-demand; no audit/history log required for MVP

5. **Q: What about testing?**  
   **A**: Manual testing only (constitutional approval). Happy path + edge cases tested manually during development

---

## Next Steps: Phase 1 Design

With all research questions resolved, Phase 1 will generate:
- `data-model.md` - Entity specifications (Currency, ExchangeRate, ConversionResult)
- `contracts/api.md` - REST API contract specification
- `quickstart.md` - Developer setup instructions
