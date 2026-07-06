# ADR-001: Project Vision

## Status

Accepted

## Date

2026-06-27

## Context

Modern communication tools for children often assume general-purpose screens, app stores, public identity, notifications, social discovery, and vendor-controlled ecosystems.

FrontPorch exists for a different experience: the feeling of neighborhood landline phones, where a child has a familiar place to call trusted people and parents understand the boundaries.

## Decision

FrontPorch is a private neighborhood communication platform centered on simple voice communication for children.

The primary experience is a dedicated corded phone. Children do not need smartphones, tablets, messaging apps, or public accounts to participate.

Communication happens inside trusted communities. Parents and guardians remain in control of relationships, contacts, permissions, and exceptional access.

FrontPorch prioritizes privacy, default-deny behavior, and simplicity over feature breadth. It is not merely a PBX. The PBX is an implementation component inside a larger parent-controlled communication platform.

## Consequences

FrontPorch should favor physical simplicity over app-like convenience.

The system should avoid features that encourage social discovery, arbitrary dialing, public reachability, or child-managed identity.

Parent-facing concepts should use real-world language: family, parent, guardian, child, device, relationship, friend, cousin, grandparent, contact, permission, and conference group.

Implementation details such as SIP extensions, endpoints, AORs, dialplans, ATA credentials, phone numbers, and device identifiers should not leak into the parent experience more than necessary.

Future features must support the core idea that the phone is a place, not a general-purpose connected device.

## Future Considerations

FrontPorch may later support additional neighborhood services, but those services should preserve the same privacy, parent control, and trusted-community assumptions.

If the project expands beyond voice, new features should be evaluated against this vision before they are treated as part of the core product.

