# Instructor Notes — Module 2

## Pre-class

- Run `docker compose up` on projector machine
- Ensure Python 3.12 venv works if students run outside Docker

## Demo Script

1. POST user → GET user
2. Login → show JWT at jwt.io (decode only, don’t share secrets)
3. List products (seeded data)

## Troubleshooting

| Error | Fix |
|-------|-----|
| 409 on user | Use unique email |
| bcrypt error | `pip install passlib[bcrypt]` |

## Extension for advanced students

- API versioning middleware
- Pagination on GET /users
