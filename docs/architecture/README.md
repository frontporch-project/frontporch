# Architecture Decision Records

Architecture Decision Records (ADRs) explain why important FrontPorch decisions were made.

Code and configuration show what the system does today. ADRs preserve the reasoning behind choices that should remain understandable years later: product philosophy, security boundaries, infrastructure assumptions, and tradeoffs that shape future work.

## When to Create an ADR

Create a new ADR when a change affects a durable architectural boundary, including:

- Product philosophy or parent-facing behavior
- Permission, privacy, or audit rules
- PBX responsibilities or generated configuration
- Networking, provisioning, or deployment assumptions
- Hardware choices that affect the family experience
- Decisions that would be expensive or confusing to reverse later

Do not create ADRs for routine implementation details, small refactors, or temporary experiments unless they establish a constraint future contributors must understand.

## Status

ADRs use one of these statuses:

- `Proposed`: under discussion and not yet binding
- `Accepted`: approved as a project constraint
- `Superseded`: replaced by a later ADR

Accepted ADRs are architectural constraints. Future changes may supersede them, but should not quietly ignore them.

## Contributor Expectations

Before making major design changes, read the accepted ADRs in this directory.

If a proposed change conflicts with an accepted ADR, either keep the existing decision or write a new ADR that explicitly supersedes it. FrontPorch should preserve the reasoning trail, not just the latest state of the repository.

