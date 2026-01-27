# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records (ADRs) for the OmniCPP Template project. ADRs document significant architectural decisions, the context, and the consequences.

## What is an ADR?

An Architecture Decision Record (ADR) is a document that describes an important architectural decision, the context, the alternatives considered, and the consequences of the decision. ADRs help teams:

- Document decisions and their rationale
- Communicate decisions to stakeholders
- Track the evolution of the architecture
- Enable future teams to understand why decisions were made

## ADR Format

Each ADR follows the standard format:

- **Status**: Proposed/Accepted/Deprecated/Superseded
- **Date**: Date of the decision
- **Context**: What is the issue that we're seeing that is motivating this decision or change?
- **Decision**: What is the change that we're proposing and/or doing?
- **Consequences**: What becomes easier or more difficult to do because of this change?
- **Alternatives Considered**: What other approaches did we consider?
- **Related ADRs**: Links to related ADRs
- **References**: Links to relevant documentation

## ADR Index

### Package Management

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-001](ADR-001-multi-package-manager-strategy.md) | Multi-package manager strategy | Accepted | 2026-01-07 |
| [ADR-002](ADR-002-priority-based-package-manager-selection.md) | Priority-based package manager selection | Accepted | 2026-01-07 |
| [ADR-003](ADR-003-package-security-verification-approach.md) | Package security verification approach | Accepted | 2026-01-07 |

### Build System

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-004](ADR-004-cmake-4-ninja-default-generator.md) | CMake 4 with Ninja as default generator | Accepted | 2026-01-07 |
| [ADR-005](ADR-005-cmake-presets-cross-platform-configuration.md) | CMake Presets for cross-platform configuration | Accepted | 2026-01-07 |
| [ADR-006](ADR-006-toolchain-file-organization.md) | Toolchain file organization | Accepted | 2026-01-07 |

### Python Architecture

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-007](ADR-007-python-scripts-consolidation.md) | Consolidation of Python scripts into omni_scripts/ | Accepted | 2026-01-07 |
| [ADR-008](ADR-008-modular-controller-pattern.md) | Modular controller pattern for build operations | Accepted | 2026-01-07 |
| [ADR-009](ADR-009-type-hints-enforcement.md) | Type hints enforcement for zero pylance errors | Accepted | 2026-01-07 |

### Cross-Platform Compilation

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-010](ADR-010-terminal-invocation-patterns.md) | Terminal invocation patterns for different compilers | Accepted | 2026-01-07 |
| [ADR-011](ADR-011-compiler-detection-selection.md) | Compiler detection and selection strategy | Accepted | 2026-01-07 |
| [ADR-012](ADR-012-cross-platform-build-configuration.md) | Cross-platform build configuration | Accepted | 2026-01-07 |

### Logging

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-013](ADR-013-dual-logging-system.md) | Dual logging system (spdlog for C++, custom for Python) | Accepted | 2026-01-07 |
| [ADR-014](ADR-014-file-rotation-retention.md) | File rotation and log retention policy | Accepted | 2026-01-07 |
| [ADR-015](ADR-015-structured-logging-format.md) | Structured logging format | Accepted | 2026-01-07 |

### C++ Standards

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-016](ADR-016-cpp23-without-modules.md) | C++23 without modules | Accepted | 2026-01-07 |
| [ADR-017](ADR-017-modern-cpp-features.md) | Modern C++ features adoption strategy | Accepted | 2026-01-07 |
| [ADR-018](ADR-018-memory-management.md) | Memory management approach (RAII, smart pointers) | Accepted | 2026-01-07 |

### Security

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-019](ADR-019-security-first-build-configuration.md) | Security-first build configuration | Accepted | 2026-01-07 |
| [ADR-020](ADR-020-dependency-integrity-verification.md) | Dependency integrity verification | Accepted | 2026-01-07 |
| [ADR-021](ADR-021-secure-terminal-invocation.md) | Secure terminal invocation | Accepted | 2026-01-07 |

### Testing

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-022](ADR-022-google-test-cpp-unit-tests.md) | Google Test for C++ unit tests | Accepted | 2026-01-07 |
| [ADR-023](ADR-023-pytest-python-tests.md) | pytest for Python tests | Accepted | 2026-01-07 |
| [ADR-024](ADR-024-code-coverage-requirements.md) | Code coverage requirements (80%) | Accepted | 2026-01-07 |

### VSCode Integration

| ADR | Title | Status | Date |
|------|-------|--------|------|
| [ADR-025](ADR-025-omnicppcontroller-single-entry-point.md) | OmniCppController.py as single entry point | Accepted | 2026-01-07 |
| [ADR-026](ADR-026-vscode-tasks-launch-configuration.md) | VSCode tasks.json and launch.json configuration | Accepted | 2026-01-07 |

## ADR Lifecycle

1. **Proposed**: ADR is proposed for discussion
2. **Accepted**: ADR is accepted and implemented
3. **Deprecated**: ADR is no longer relevant
4. **Superseded**: ADR is replaced by a new ADR

## Creating a New ADR

When creating a new ADR:

1. Use the standard ADR format
2. Include context, decision, and consequences
3. Document alternatives considered
4. Link to related ADRs
5. Add references to relevant documentation
6. Update this index file

## References

- [ADR Template](https://adr.github.io/)
- [Architecture Decision Records](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- [Coding Standards](../01_standards/coding_standards.md)
- [Current State](../00_current_state/manifest.md)
- [Future State](../04_future_state/manifest.md)
- [Threat Model](../03_threat_model/analysis.md)
