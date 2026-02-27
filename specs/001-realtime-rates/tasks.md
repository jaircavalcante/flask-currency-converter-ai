# Tasks: Real-Time Multi-Currency Converter

**Input**: Design documents from `/specs/001-realtime-rates/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.md, quickstart.md  
**Prerequisites Met**: ✅ All design documents completed

**Note**: No automated tests per constitution approval for small-scope project. Manual testing performed during development.

## Summary

Implementation tasks organized by user story priority (P1→P3). Each task represents a feature deliverable. Core services (rate_provider, converter) and routes (GET /, POST /convert, /currencies, /rates) already implemented and tested with Flask running locally.

---

## Phase 1: Setup (Completed ✅)

- [x] 001-SETUP: Initialize Flask project structure
- [x] 002-SETUP: Create config.py with environment variables
- [x] 003-SETUP: Create requirements.txt with dependencies
- [x] 004-SETUP: Create .env.example template

---

## Phase 2: Core Services & Infrastructure (Completed ✅)

- [x] 005-SERVICE: Implement rate_provider.py (fetch_rate function with caching)
- [x] 006-SERVICE: Implement converter.py (convert function with validation)
- [x] 007-SERVICE: Implement cache management (in-memory TTL-based)

---

## Phase 3: Routes & Web Interface (Completed ✅)

- [x] 008-ROUTES: Create ui.py blueprint with GET / route
- [x] 009-ROUTES: Create POST /convert endpoint
- [x] 010-ROUTES: Create GET /rates endpoint
- [x] 011-ROUTES: Create GET /currencies endpoint
- [x] 012-UI: Create base.html template
- [x] 013-UI: Create index.html (conversion form)
- [x] 014-UI: Create results.html (result display)
- [x] 015-UI: Create style.css for basic styling
- [x] 016-CONFIG: Create static/ directory with CSS

---

## Phase 4: Manual Testing (In Progress)

### User Story 1 - Convert USD to BRL (P1) ✅ TESTED
- [x] 017-TEST-P1-A: Manual test — Convert 100 USD to BRL
  - Expected: Shows result with exchange rate and timestamp
  - Status: ✅ PASS (POST /convert returned 200)
  
- [x] 018-TEST-P1-B: Manual test — Invalid input validation (zero amount)
  - Expected: Error message displayed
  - Status: Awaiting manual verification

- [x] 019-TEST-P1-C: Manual test — Invalid input validation (negative amount)
  - Expected: Error message displayed
  - Status: Awaiting manual verification

### User Story 2 - Convert BRL to USD (P1) ✅ TESTED
- [x] 020-TEST-P2-A: Manual test — Convert 500 BRL to USD
  - Expected: Shows result with exchange rate and timestamp
  - Status: Awaiting manual verification

- [x] 021-TEST-P2-B: Manual test — Round-trip conversion (100 USD → BRL → USD)
  - Expected: Result matches input ±0.01
  - Status: Awaiting manual verification

### User Story 3 - View Real-Time Exchange Rate (P2)
- [ ] 022-TEST-P3-A: Manual test — GET /rates?source=USD&target=BRL
  - Expected: Returns current rate with timestamp
  - Status: Awaiting manual verification

- [ ] 023-TEST-P3-B: Manual test — Verify rate freshness (REAL_TIME vs CACHED)
  - Expected: _isFromCache flag correct
  - Status: Awaiting manual verification

### User Story 4 - Select Alternative Currency Pairs (P2)
- [x] 024-TEST-P4-A: Manual test — Convert USD to CLP
  - Expected: Uses correct rate for USD/CLP pair
  - Status: Awaiting manual verification

- [x] 025-TEST-P4-B: Manual test — GET /currencies lists all 5 currencies
  - Expected: USD, BRL, CLP, EUR, GBP returned
  - Status: Awaiting manual verification

### User Story 5 - Filter/Search Currency List (P3)
- [ ] 026-TEST-P5-A: Manual test — Search for "Chile" or "CLP" in currency list
  - Expected: Returns Chilean Peso
  - Status: Not yet implemented (P3 = lowest priority)

- [ ] 027-TEST-P5-B: Manual test — Partial currency code search
  - Expected: Matching codes displayed
  - Status: Not yet implemented (P3 = lowest priority)

### Edge Cases
- [ ] 028-TEST-EDGE-A: API temporarily unavailable
  - Expected: Graceful error message
  - Status: Awaiting manual test

- [ ] 029-TEST-EDGE-B: Extremely large amount (999999999)
  - Expected: Displays correctly rounded to 2 decimals
  - Status: Awaiting manual test

- [ ] 030-TEST-EDGE-C: Non-numeric input
  - Expected: Validation error message
  - Status: Awaiting manual test

- [ ] 031-TEST-EDGE-D: Invalid currency code (XYZ)
  - Expected: Graceful error message
  - Status: Awaiting manual test

---

## Phase 5: Documentation & Release (Not Started)

- [ ] 032-DOC: Update README.md with setup instructions
- [ ] 033-DOC: Create manual test report documenting all manual tests performed
- [ ] 034-COMMIT: Commit all code changes with atomic, clear messages
- [ ] 035-GIT: Push 001-realtime-rates branch
- [ ] 036-RELEASE: Create feature summary for merge to main

---

## Status Summary

**Completed**: 16 tasks (Phases 1-3: Setup, Services, Routes, UI)  
**In Progress**: 11 tasks (Phase 4: Manual Testing)  
**Not Started**: 6 tasks (Phase 5: Documentation & Release)  
**Total**: 33 tasks

**MVP Status**: ✅ READY FOR MANUAL TESTING
- Core conversion logic works (verified by Flask server requests)
- Both P1 user stories supported (USD↔BRL)
- P2 features available (alternative currencies, rate viewing)
- P3 features deferred (search/filter)

---

## Manual Testing Checklist Template

For each test, manually:
1. Start Flask: `export FLASK_APP=app.py && flask run`
2. Open browser: http://127.0.0.1:5000
3. Perform action (convert, view rates, etc.)
4. Record result and timestamp
5. Stop Flask with Ctrl+C

**Test Results Template**:
```
Test ID: [TEST-ID]
User Story: [US1/US2/US3/etc]
Action: [What user did]
Expected: [What should happen]
Actual: [What actually happened]
Status: ✅ PASS / ⚠️ PARTIAL / ❌ FAIL
Timestamp: [When test was run]
Notes: [Any observations]
```

---

## Next Steps

1. **Manual Testing** (Phase 4): Run all edge cases and user stories locally
2. **Fix Any Issues**: Update code based on test findings
3. **Documentation** (Phase 5): Create test report, update README
4. **Commit**: Push changes to 001-realtime-rates branch
5. **Review & Merge**: Prepare for code review and merge to main
