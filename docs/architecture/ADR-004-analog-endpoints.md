# ADR-004: Analog Endpoints

## Status

Accepted

## Date

2026-06-27

## Context

The endpoint shapes the product. A screen-based endpoint invites app behavior, notifications, settings, accounts, and feature creep. A SIP desk phone exposes telephony concepts that are not meaningful to most families.

FrontPorch is trying to recreate the experience of a child having a simple landline-style phone in a known place.

## Decision

The primary FrontPorch endpoint is:

- An analog corded telephone
- A Grandstream HT802 analog telephone adapter
- A GL.iNet router running Tailscale
- The family's existing home Internet connection

SIP desk phones and smartphones are not the primary product endpoint.

## Consequences

The child experience is familiar, physical, and screen-free.

Parents can understand the phone as a household object rather than another app account or device management problem.

The hardware is inexpensive and replaceable. The analog phone, ATA, and router can be swapped independently.

The design avoids strong dependence on a single phone vendor. The analog phone can be any compatible corded handset, and the PBX boundary remains SIP-based behind the ATA.

SIP desk phones are intentionally avoided as the default because they expose extensions, menus, directories, soft keys, and configuration surfaces that do not match the parent-facing model.

Smartphones are intentionally avoided as the default because they add screens, notifications, app distribution, operating-system policy, and child-managed device behavior.

This choice may limit advanced features, but that limitation supports the product goal: simple voice communication inside parent-approved boundaries.

## Future Considerations

Future hardware ADRs may approve additional endpoint types for accessibility, operator use, or special family needs.

Any new endpoint should preserve default-deny communication, parent-controlled permissions, private contact metadata, and the simple household-phone experience for children.

