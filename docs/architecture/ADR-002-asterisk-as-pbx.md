# ADR-002: Asterisk as the PBX Engine

## Status

Accepted

## Date

2026-06-27

## Context

FrontPorch needs reliable SIP registration, call routing, media handling, and conference mechanics. These are PBX concerns and should use mature telephony infrastructure.

FrontPorch also needs parent-controlled relationships, child permissions, private contact names, audit history, and default-deny policy. These are application concerns and must remain testable and inspectable outside the PBX.

## Decision

FrontPorch uses Asterisk only as the SIP and media engine.

The Django application owns all business logic. It is the source of truth for families, people, devices, relationships, contacts, permissions, conference groups, and audit history.

Asterisk configuration should be generated deterministically from Django state instead of edited manually as the primary place for business rules.

## Consequences

This creates a clear separation of concerns:

- Asterisk handles SIP registration, call setup, dialplan execution, media, and conference mechanics.
- Django decides who may communicate and records why permission-sensitive state changed.

Permission logic can be tested in ordinary application tests instead of being hidden in PBX configuration.

Generated configuration allows operators to inspect the PBX state while preserving Django as the authority.

The project keeps a future path to replace Asterisk or support another PBX implementation, because business rules are not owned by Asterisk.

Manual PBX edits that affect permissions are temporary development aids only and should not become the operating model.

## Future Considerations

The configuration generation boundary should be revisited when Django implementation begins.

Future work should define how generated files are rendered, validated, deployed, and rolled back. That process should preserve deterministic output and auditability.

