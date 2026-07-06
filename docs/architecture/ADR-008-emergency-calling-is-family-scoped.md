# ADR-008: Emergency Calling Is Family-Scoped

## Status

Accepted

## Date

2026-06-28

## Context

FrontPorch is designed as a private neighborhood communication platform.

The platform may eventually support integration with the public telephone network through one or more SIP trunks.

Unlike traditional landlines, VoIP emergency services, such as 911 in the United States, require an emergency service address to be registered with the provider.

FrontPorch is intended to support multiple participating families, each living at a different physical address.

A single shared E911 registration would create an unsafe situation where emergency responders could be dispatched to the wrong home.

This is an unacceptable design.

## Decision

Emergency calling is a responsibility of each participating family.

FrontPorch will never centralize emergency calling for multiple households.

Each family may optionally configure its own emergency-capable SIP provider and E911 registration.

Emergency calls must always be routed using the originating family's configured provider.

The PBX is responsible for determining which family originated the call and selecting the correct outbound route.

### Initial Version

The first production version of FrontPorch will not advertise itself as a replacement for a traditional telephone service.

Until family-scoped emergency routing is implemented:

- FrontPorch should not be considered a primary emergency communication system.
- Families should continue maintaining another telephone capable of reaching emergency services.
- Documentation should clearly explain this limitation.

This decision intentionally prioritizes safety over feature completeness.

### Future Architecture

Eventually each participating family may configure:

- home address
- emergency address
- preferred SIP provider
- outbound emergency trunk
- emergency contact information

For example:

Family A:

- Address A
- SIP Trunk A
- E911 Registration A

Family B:

- Address B
- SIP Trunk B
- E911 Registration B

Family C:

- Address C
- SIP Trunk C
- E911 Registration C

When a child dials `911`, FrontPorch determines:

- which physical device originated the call
- which family owns that device
- which emergency trunk belongs to that family

The PBX then routes the emergency call using the family's configured provider.

### Device Ownership

Every physical endpoint should belong to exactly one family.

Examples include:

- bedroom phone
- kitchen phone
- parent SIP application
- future mobile device

Device ownership determines emergency routing.

Emergency routing must never depend on the currently logged-in user.

## Consequences

Advantages:

- Correct emergency dispatch location.
- Scales naturally to many households.
- Keeps family responsibility explicit.
- Avoids unsafe centralized E911 configuration.

Tradeoffs:

- More complex PBX routing.
- Multiple SIP providers may exist within one FrontPorch deployment.
- Additional family onboarding requirements.
- More configuration than a shared outbound trunk.

## Design Principles

Safety takes precedence over convenience.

Emergency calling is never treated as just another outbound route.

The platform must avoid creating the false impression that emergency services are available unless they are correctly configured for the originating household.

## Future Considerations

Future versions may support:

- automatic validation that a family has configured emergency calling
- administrator warnings for households without emergency routing
- emergency call auditing
- optional emergency notifications to parents
- regional emergency numbers outside the United States
- testing tools that verify emergency configuration without placing a real emergency call

These enhancements must preserve the core architectural principle: emergency services are owned by each participating family, not by the neighborhood PBX.
