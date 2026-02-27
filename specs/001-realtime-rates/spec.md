# Feature Specification: Real-Time Multi-Currency Converter

**Feature Branch**: `001-realtime-rates`  
**Created**: 2026-02-27  
**Status**: Draft  
**Input**: User description: "construa uma aplicação que me ajude a realizar a conversao de moeda, do dolar para o real e vice versa, consultando alguma api publica para acompanhar o movimento do dolar em tempo real. Incluir filtro com demais formas de conversao, dolar, peso chileno e etc."

## User Scenarios & Testing

### User Story 1 - Convert USD to BRL (Priority: P1)

User needs to quickly convert a given amount in US Dollars to Brazilian Reais using current market exchange rates. This is the primary use case for the application.

**Why this priority**: Core functionality. Users expect to convert USD to BRL instantly with real-time rates. This directly addresses the main requirement and delivers immediate value.

**Independent Test**: Can be tested by entering a USD amount and verifying the converted BRL value matches the real-time rate. Delivers complete MVP: one currency pair conversion.

**Acceptance Scenarios**:

1. **Given** the user enters "100 USD", **When** the conversion completes, **Then** the application displays the equivalent amount in BRL with current market rate
2. **Given** the user specifies source amount, **When** no valid amount is provided, **Then** the system displays a clear error message
3. **Given** the exchange rate data is available, **When** the user converts, **Then** the result shows the rate used for transparency

---

### User Story 2 - Convert BRL to USD (Priority: P1)

User needs to convert Brazilian Reais to US Dollars, enabling bidirectional currency flow.

**Why this priority**: Equally critical as USD→BRL. Bidirectional conversion covers all primary use cases and maintains feature balance.

**Independent Test**: Can be tested by entering a BRL amount and verifying the converted USD value. Works independently of US1.

**Acceptance Scenarios**:

1. **Given** the user enters "500 BRL", **When** the conversion completes, **Then** the application displays the equivalent amount in USD with current market rate
2. **Given** both USD↔BRL conversions are working, **When** a user converts and then converts back, **Then** the round-trip result matches (accounting for rounding)

---

### User Story 3 - View Real-Time Exchange Rate (Priority: P2)

User wants to see the current exchange rate between currencies without performing a conversion, to understand market movement.

**Why this priority**: High value for informed decision-making. Enables users to monitor rates before converting large amounts. Important but not blocking if US1/US2 work.

**Independent Test**: Can be tested by requesting the rate display between any two currencies. Works independently and provides value on its own.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** the user requests the exchange rate for USD/BRL, **Then** the system displays the current rate with a timestamp
2. **Given** rates come from a public API, **When** the rate is displayed, **Then** it includes the last update time (freshness indicator)

---

### User Story 4 - Select Alternative Currency Pairs (Priority: P2)

User can filter or select currency pairs beyond the primary USD/BRL pair, including Chilean Peso (CLP) and other major currencies.

**Why this priority**: Extensibility requirement. Adds flexibility for users with other currency needs. Valuable but can be implemented after core conversion works.

**Independent Test**: Can be tested by converting between alternative currency pairs. Demonstrates multi-currency capability.

**Acceptance Scenarios**:

1. **Given** the application supports multiple currencies, **When** the user selects USD/CLP pair, **Then** the conversion uses the correct exchange rate for that pair
2. **Given** the currency list is available, **When** the user lists supported currencies, **Then** all available currency options are displayed clearly

---

### User Story 5 - Filter/Search Currency List (Priority: P3)

User can search or filter the available currency list by currency code or name to find their desired currency quickly.

**Why this priority**: Nice-to-have UX improvement. Reduces friction when navigating many currency options. Important for usability at scale but not essential for initial implementation.

**Independent Test**: Can be tested by searching for a currency and verifying filtered results are returned correctly.

**Acceptance Scenarios**:

1. **Given** many currencies are available, **When** the user searches for "Chile" or "CLP", **Then** the system returns Chilean Peso in results
2. **Given** the user enters a partial currency code, **When** they search, **Then** matching currency codes are displayed

---

### Edge Cases

- What happens when the API is temporarily unavailable? (Graceful error message; cached rate fallback if available)
- How does the system handle currency pairs with very large or very small amounts? (Display with appropriate precision/rounding)
- What if the user enters zero or negative amounts? (Validation error with clear guidance)
- What if the requested currency pair has no rate data? (Error message indicating data unavailable for that pair)
- What happens during API rate limit exceeding? (Graceful handling; inform user to retry)

## Requirements

### Functional Requirements

- **FR-001**: System MUST fetch real-time exchange rates from a public API for supported currencies
- **FR-002**: System MUST support bidirectional conversion between USD and BRL (USD→BRL and BRL→USD)
- **FR-003**: System MUST support at least 5 major currencies: USD, BRL, CLP, EUR, GBP
- **FR-004**: Users MUST be able to input an amount and currency pair to receive a converted result
- **FR-005**: System MUST display the exchange rate used in each conversion for transparency
- **FR-006**: System MUST validate all user inputs and reject invalid amounts (negative, non-numeric, etc.)
- **FR-007**: System MUST show exchange rate timestamps to indicate data freshness
- **FR-008**: System MUST handle API failures gracefully with clear user-facing error messages
- **FR-009**: Users MUST be able to view a list of all supported currencies
- **FR-010**: System MUST round conversion results to 2 decimal places for currency display

### Key Entities

- **ExchangeRate**: Represents the conversion ratio between two currencies (e.g., 1 USD = 5.20 BRL). Attributes: source currency, target currency, rate value, timestamp of last update, source API
- **Currency**: Represents a supported currency (e.g., USD, BRL, CLP). Attributes: currency code (3-letter ISO 4217), currency name, symbol, supported for conversion (boolean)
- **ConversionResult**: Represents the outcome of a conversion operation. Attributes: source amount, source currency, result amount, target currency, exchange rate used, conversion timestamp

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users can convert USD to BRL or BRL to USD in under 2 seconds from application start to result display
- **SC-002**: Exchange rate data is updated at least once every 5 minutes to ensure "real-time" freshness
- **SC-003**: All conversion results are accurate to within 0.01% of the actual market rate at time of conversion
- **SC-004**: 95% of conversion requests succeed without errors (assuming API availability)
- **SC-005**: Invalid inputs (negative amounts, non-currency codes, etc.) are rejected with user-friendly error messages within 500ms
- **SC-006**: Application supports at least 5 major currency pairs with visible rate display
- **SC-007**: Users can identify supported currencies and understand which pairs are available without external documentation

## Assumptions

- A public, free-tier API for exchange rates is available and reliable (e.g., exchangerate-api.com, fixer.io, currencyapi.com)
- The application interface is a CLI (Command-Line Interface) for simplicity and alignment with small project scope
- Users will perform conversions with reasonable amounts (not astronomical numbers requiring special precision handling)
- Network connectivity is available for API calls; offline mode not required for MVP
- The application targets manual, on-demand conversion requests rather than continuous monitoring
- Exchange rate precision of 2 decimal places is sufficient for user needs

## Notes & Clarifications

This specification establishes the feature scope focusing on real-time USD↔BRL conversion with extensible multi-currency support. Implementation will prioritize P1 user stories (bidirectional USD/BRL conversion) as the MVP, then add real-time rate viewing (P2), then alternative currencies (P2), with UI improvements (P3) coming last if needed.
