# Security Policy

FrontPorch is a kid-adjacent family communication project. Please treat security and privacy reports seriously even when the affected code looks small.

## Reporting a Vulnerability

This project does not yet have a dedicated public security contact.

Until one exists, report vulnerabilities privately to the repository maintainer. Do not open a public issue with exploit details, real phone numbers, credentials, family information, call logs, recordings, screenshots, or deployment-specific infrastructure details.

Suggested report contents:

- A short description of the issue.
- Affected files, routes, models, or generated Asterisk behavior.
- Steps to reproduce using placeholder data only.
- Expected impact, especially whether a child could be reached, discovered, or allowed to call outside approved permissions.
- Any suggested fix or mitigation.

## Sensitive Areas

Security-sensitive areas include:

- Authentication and account registration.
- Parent, guardian, and administrator authorization.
- Contact approval and child-to-family relationship approval.
- Generated Asterisk dialplan and PJSIP configuration.
- Unknown inbound calls from the public telephone network.
- Outbound PSTN calling and any outside-line behavior.
- Conference group permissions.
- SIP, VoIP provider, Asterisk Manager Interface, database, Tailscale, and deployment credentials.
- Phone-number privacy, caller ID handling, logs, recordings, voicemail, fixtures, seed data, backups, and screenshots.

## Public Examples

Public reports and patches must use fictional names and reserved example phone numbers such as `202-555-0199`. Real family, child, phone, address, email, school, neighborhood, provider account, server, or deployment data should remain in private communication only.

## Default Position

If behavior is ambiguous, FrontPorch should fail closed:

- Children should not discover other users.
- Unknown callers should not reach children.
- Children should not dial arbitrary public phone numbers.
- Permission changes should remain reviewable and auditable.
