# BUILD-1203 — Instructor solution

**Do not share these files with students before they submit a complete playbook.**

This folder is the answer key for configuration automation. Students are not required to install Ansible or SSH anywhere.

## Files

| File | Role |
|---|---|
| [playbook.yml](playbook.yml) | Local connection; templates both env files |
| [inventory.ini](inventory.ini) | `localhost` / `ansible_connection=local` |
| [group_vars/all.yml](group_vars/all.yml) | `baypay_db_host` and friends; password from env lookup |
| [templates/payment-service.env.j2](templates/payment-service.env.j2) | Boot env |
| [templates/server.env.j2](templates/server.env.j2) | Liberty `server.env` |

A student tree that templates both files from `BAYPAY_DB_HOST` / `baypay_db_host` and keeps the password out of git passes even if they used `host_vars` or a single template copied twice.

## What the starter got wrong

- Created `./rendered` and stopped.
- No inventory, no group_vars, no Jinja templates, no `template` tasks.

The starter was a valid-looking play. It did not render the host contract.

## Required contracts

```text
connection:  local / localhost; gather_facts false
host var:    baypay_db_host → BAYPAY_DB_HOST=db-east.baypay.example
url:         jdbc:postgresql://<host>:5432/baypay
password:    lookup env or empty — never changeme in git
outputs:     payment-service.env and Liberty server.env
validate:    read the files; optional ansible-playbook --syntax-check
```

Optional check:

```bash
ansible-playbook -i inventory.ini playbook.yml --syntax-check
```

## Diagram

AEJE-D-058: one var map renders Boot env and Liberty `server.env` on localhost.

## Scoring notes

Full marks require both templates, the host var, local connection, and no password literal. SSH inventory or `changeme` fails Security. Missing Liberty `server.env` with a complete Boot file is at most a mid Technical score. Ansible absence must not fail the lab.
