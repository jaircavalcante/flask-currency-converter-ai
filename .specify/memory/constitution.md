# Dolar Converter Constitution

## Core Principles

### I. Clean Code & Simplicity
Code must be readable, straightforward, and self-explanatory. Favor clarity over cleverness. Single responsibility per function; avoid premature optimization or unnecessary complexity. YAGNI principle: implement only what is needed now. Maximum function length: ~30 lines unless exceptional circumstances.

### II. Clear Naming & Documentation
Use descriptive names for functions, variables, and modules. Variable names must reveal intent. Comments explain the "why" when logic is non-obvious. Function signatures must be clear—parameters and return types documented. Keep documentation close to code.

### III. Single Responsibility
Each module, class, or function has one reason to change. Currency conversion logic separate from I/O handling. No god objects. Composition preferred over inheritance. Promote reusability through focused, single-purpose units.

### IV. Error Handling & Robustness
Invalid inputs must be handled gracefully with clear error messages. No silent failures. Edge cases (boundary values, unusual inputs) anticipated and tested manually during development. Stack traces captured but user-facing errors remain user-friendly.

### V. Practical Development Workflow
No mandatory automated testing; manual verification sufficient for small scope. Code review (peer or self) required before merging. Commits must be atomic and have clear messages. Keep iteration cycles short; deploy incrementally.

## Code Quality Standards

- **Naming conventions**: camelCase for variables/functions, PascalCase for classes/types
- **Line length**: Max 100 characters (readability before strict limits)
- **Comments**: Explain intent, not what is obvious from code
- **DRY principle**: Extract repeated logic into reusable functions
- **Avoid magic numbers**: Use named constants with clear purpose

## Development Workflow

1. Feature branches from `main` with descriptive names
2. Self-review or peer-review before merge (clarity check + logic verification)
3. Clear, atomic commit messages
4. Manual testing of happy path + known edge cases
5. Merge only when code is clean and documented

## Governance

This constitution governs quality and structure decisions. Amendments must document rationale and impact on existing codebase. All decisions prioritize clarity and maintainability over feature velocity. Complexity must be justified; simple solutions preferred by default.

**Version**: 1.0.0 | **Ratified**: 2026-02-27 | **Last Amended**: 2026-02-27
