# ADR-005: Relationship-Based Permissions

## Status

Accepted

## Date

2026-06-27

## Context

Families think in relationships, not extensions.

A parent wants to approve that Alex can call Jamie. They should not need to approve that extension `101` can call extension `102`, or understand whether a person is represented internally by a SIP endpoint, ATA credential, phone number, or device identifier.

External phone numbers create another privacy concern. Different families may know the same person by different names, and those names should not become shared global metadata.

## Decision

FrontPorch models permissions as relationships between people, not as permissions between extensions.

Parents approve:

```text
Alex <-> Jamie
```

not:

```text
101 <-> 102
```

External callers are normalized by global phone number, using E.164 format where applicable. Each family maintains its own private contact names and metadata.

For example:

```text
Family A: Sophia
Family B: Sophie
Same normalized phone number.
Different private labels.
```

The phone number is the shared identity for routing and deduplication. Family-specific contact metadata remains private.

Conference calls are allowed only when every participant is mutually approved, unless parents explicitly create an approved conference group.

## Consequences

Permission logic remains aligned with the real-world parent decision.

Children cannot gain access by discovering extensions, trying arbitrary numbers, or relying on PBX implementation details.

Families can maintain private names for contacts without forcing a global address book or revealing how another family labels the same person.

Call routing must translate relationship permissions into PBX configuration or runtime decisions, but the implementation identifiers are not the source of permission.

Conference calls cannot become a loophole around direct-call restrictions. Group communication requires either mutual approval among all participants or an explicit parent-approved conference group.

Permission changes and sensitive administrative actions must be auditable.

## Future Considerations

Future ADRs should define how relationship state maps to generated PBX configuration, how external calling is enabled, and how parent-approved conference groups are modeled.

The project should preserve the relationship-first model even if endpoint types, PBX implementation, or private networking technology changes.
