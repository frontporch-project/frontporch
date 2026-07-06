# Test Families

These reusable local test families are intended for Django Admin, generated Asterisk config, and local dialing tests.

Seed them into the local container database with:

```bash
docker compose run --rm web python manage.py seed_test_families
```

Render generated Asterisk config after seeding:

```bash
docker compose run --rm web python manage.py render_asterisk_config
```

The four-digit values are SIP extensions and usernames. Local test device secrets use this deterministic pattern:

```text
test-<extension>
```

## Maple

| Extension | Person or device | Type |
| --- | --- | --- |
| 2642 | Maple family phone | Family phone |
| 8468 | Morgan | Parent |
| 7749 | Drew | Parent |
| 4754 | Casey | Child |
| 5249 | Jordan | Child |

## River

| Extension | Person or device | Type |
| --- | --- | --- |
| 7747 | River family phone | Family phone |
| 6255 | Taylor | Parent |
| 7981 | Riley | Parent |
| 3552 | Alex | Child |

## Cedar

| Extension | Person or device | Type |
| --- | --- | --- |
| 1440 | Cedar family phone | Family phone |
| 5963 | Sam | Parent |
| 2362 | Quinn | Parent |
| 7307 | Jamie | Child |
| 2148 | Robin | Child |
| 3152 | Sky | Child |
