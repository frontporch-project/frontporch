# ADR-006: Zero-Touch Gateway Provisioning

## Status

Proposed

## Date

2026-06-28

## Context

FrontPorch intends to make neighborhood phone onboarding simple for families and administrators. A family should not need to understand Tailscale, SIP credentials, PBX endpoints, gateway tags, or generated configuration in order to receive a working home phone.

The current architecture uses Django as the source of truth and Tailscale as the private networking layer. That creates an opportunity for FrontPorch to eventually become the control plane for gateway onboarding instead of relying on manual steps in the Tailscale admin console.

This is not required for the initial release. The first implementation may use manually created Tailscale auth keys and manual gateway preparation. The architecture should still avoid choices that would block later automation.

## Decision

FrontPorch should anticipate zero-touch provisioning for neighborhood gateways.

In the long term, an administrator should be able to add a family in FrontPorch, enter family details, parents, children, desired phone extensions, and optional Wi-Fi credentials, then confirm provisioning.

FrontPorch should then be able to:

- Create the family records.
- Create SIP devices.
- Generate SIP credentials.
- Request a Tailscale auth key through the Tailscale API.
- Associate the gateway with the proper Tailscale tag, such as `tag:frontporch-gateway`.
- Generate the provisioning artifacts needed by the gateway.

After that, the installer should only need to power on the gateway. The gateway should automatically join the FrontPorch tailnet, authenticate with the generated auth key, receive the proper tag, connect to the PBX, begin serving local FrontPorch Wi-Fi when applicable, and become operational without interactive Tailscale login.

Gateway enrollment should use Tailscale auth keys rather than requiring an administrator to log into Tailscale on the device.

Preferred auth key properties are:

- Pre-approved.
- Tagged.
- Non-ephemeral for the enrolled gateway.
- Limited lifetime for bootstrap use.

After successful enrollment, the bootstrap auth key should no longer be needed by the gateway.

## Consequences

FrontPorch can become the operational control plane for the neighborhood network, not only a directory and PBX configuration source.

Administrators should rarely need to visit the Tailscale admin console once this capability exists.

Future data models should be able to represent gateway inventory, family assignment, provisioning status, device naming, Tailscale tags, and key lifecycle without leaking those implementation details into parent-facing concepts.

Provisioning must remain auditable because gateway enrollment changes who can participate in the private network.

Tailscale API integration introduces a dependency on Tailscale account configuration, API behavior, tag policy, and key lifecycle semantics. The boundary should remain explicit enough that FrontPorch can preserve its private-network architecture if the underlying private networking provider changes later.

Zero-touch onboarding increases the importance of secure artifact handling. Generated SIP credentials, Wi-Fi credentials, auth keys, and bootstrap configuration must be treated as sensitive material.

## Future Considerations

Future ADRs or implementation plans should define the gateway inventory model, provisioning artifact format, Tailscale API integration boundary, auth key storage rules, key rotation behavior, tag policy expectations, and operational recovery flow when enrollment fails.

The initial release may still rely on manually created auth keys, but those manual steps should be treated as temporary scaffolding rather than the long-term provisioning model.
