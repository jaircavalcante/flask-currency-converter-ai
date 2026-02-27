# Implementation Plan: Real-Time Multi-Currency Converter

**Branch**: `001-realtime-rates` | **Date**: 2026-02-27 | **Spec**: [specs/001-realtime-rates/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-realtime-rates/spec.md`

## Summary

A Python Flask web application providing real-time currency conversion focused on USD ↔ BRL bidirectional conversion with extensible multi-currency support (CLP, EUR, GBP). The application fetches rates from a public free-tier exchange rate API and displays conversions with transparency (showing the rate used, timestamp). Priority is the P1 bidirectional USD/BRL conversion as MVP; P2 features (rate viewing, alternative currencies) extend value; P3 features (search/filter) are polish.

**Technical Approach**: Flask web framework with simple HTML forms for user input. Currency rate fetching via public REST API (e.g., exchangerate-api.com). Modular design: separation of conversion logic (models) from routing (views) and API integration (services). In-memory caching of rates with configurable TTL to balance freshness vs. API quota usage.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: 
- Flask (web framework)
- requests (HTTP client for API calls)
- python-dotenv (environment configuration)

**Storage**: N/A (stateless; API rates fetched on-demand with optional in-memory caching)

**Testing**: Manual verification only (per constitution: no automated tests for small scope). Happy path and edge cases tested manually during development.

**Target Platform**: Linux/macOS/Windows desktop web service (localhost:5000)

**Project Type**: Web service (Flask web application)

**Performance Goals**: 
- Currency conversion response in < 2 seconds (user-interactive response time)
- Exchange rate API calls cached briefly to reduce quota consumption

**Constraints**: 
- No external database required
- Free-tier exchange rate API (may have rate limitations)
- Simple HTML/Forms UI (no complex JavaScript required)

**Scale/Scope**: 
- Single feature (currency conversion)
- < 500 lines of Python code anticipated
- 5 supported currencies as scope boundary

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **All 5 principles supported by this plan**:

1. **Clean Code & Simplicity** - Flask is lightweight; conversion logic isolated in service layer, routes in views, configuration externalized. YAGNI: only features specified (no database, no auth, no logging framework). Expected codebase < 500 LOC supports readability.

2. **Clear Naming & Documentation** - API endpoints clearly named (`/convert`, `/rates`, `/currencies`). Service functions (`convertCurrency()`, `fetchExchangeRate()`) have self-documenting names. Configuration constants in separate module (e.g., `SUPPORTED_CURRENCIES`, `CACHE_TTL_SECONDS`).

3. **Single Responsibility** - Currency conversion logic (models/converter.py) independent of Flask routing. Exchange rate API client (services/rateProvider.py) separate from business logic. Routes handle only I/O (request/response).

4. **Error Handling & Robustness** - User input validation in conversion service (non-negative, numeric, valid currencies). API failure handling: graceful error responses with user-friendly messages. Edge cases: zero/negative amounts, API unavailable, rate data missing—all with clear feedback.

5. **Practical Development Workflow** - No test framework added; manual testing during development. Simple feature scope allows manual verification of core paths (USD→BRL, BRL→USD) and edge cases (invalid input, API down). Constitution explicitly approved "manual verification sufficient for small scope."

**Gate Status**: ✅ PASS - Plan aligns with constitution; no violations detected or justified.

## Project Structure

### Documentation (this feature)

```text
specs/001-realtime-rates/
├── plan.md              # This file (implementation plan)
├── spec.md              # Feature specification (completed)
├── research.md          # Phase 0 output (research findings)
├── data-model.md        # Phase 1 output (data entities)
├── quickstart.md        # Phase 1 output (getting started guide)
├── contracts/           # Phase 1 output (API contracts)
└── checklists/          # Quality gates

```

### Source Code (repository root)

```text
dolar-converter/
├── app.py                  # Flask application entry point
├── config.py               # Application configuration (API keys, settings)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
│
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── currency.py           # Currency entity definition
│   │   └── exchangeRate.py        # ExchangeRate entity definition
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rateProvider.py        # External API integration for exchange rates
│   │   ├── converter.py           # Core conversion logic
│   │   └── cache.py               # Simple in-memory rate caching
│   │
│   └── routes/
│       ├── __init__.py
│       ├── conversion.py          # POST /convert endpoint
│       ├── rates.py               # GET /rates endpoint (view current rates)
│       ├── currencies.py          # GET /currencies endpoint (list supported)
│       └── ui.py                  # GET / (homepage with conversion form)
│
├── templates/
│   ├── base.html                  # Base template with styling
│   ├── index.html                 # Homepage with conversion form
│   └── results.html               # Conversion result display
│
└── static/
    └── style.css                  # Basic styling for web interface
```

**Structure Decision**: Selected "Single Project Web Service" option. Flask application with modular structure separating concerns: API clients (services), business logic (models + converter), HTTP routing (routes), and presentation (templates/static). This aligns with constitution principle III (Single Responsibility) and principle I (Simplicity) by avoiding unnecessary framework complexity.

## Complexity Tracking

No constitution violations requiring justification. The plan:
- ✅ Stays simple: no database, no auth, no testing framework, < 500 LOC
- ✅ Uses only specified dependencies: Flask, requests, python-dotenv
- ✅ Follows clean architecture: separation of concerns across modules
- ✅ Integrates with public free API (no infrastructure overhead)
- ✅ Manual testing sufficient per constitution approval of small-scope projects

---

## Next Phases

**Phase 0 (Research)**: Generate `research.md` documenting:
- Selected exchange rate API (exchangerate-api.com, fixer.io, or currencyapi.com)
- Rate caching strategy and TTL selection
- Python Flask best practices for small applications
- Error handling patterns for third-party API integration

**Phase 1 (Design)**: Generate design documents:
- `data-model.md` - Entity definitions (Currency, ExchangeRate, ConversionResult) with validation rules
- `contracts/api.md` - REST API contracts for conversion, rate viewing, currency listing
- `quickstart.md` - Local development setup (virtual environment, dependencies, running Flask)

**Phase 2 (Tasks)**: Generate `tasks.md` with implementation tasks organized by user story priority (P1 → P3)
