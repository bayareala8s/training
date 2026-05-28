# Week 3 — Hands-On Labs (Detailed)

**Total lab time:** ~5–6 hours · **Repository paths:** [`labs/week-03/`](../../labs/week-03/) · **Modules:** [`modules/`](../../modules/)

---

## Lab 3.1 — Build & Extend VPC Module

**Duration:** 3 hours · **Guide:** [labs/week-03/LAB-01-vpc-module.md](../../labs/week-03/LAB-01-vpc-module.md)

### Objectives

- Understand module structure in `modules/vpc/`
- Add an optional feature (VPC endpoint or database subnet tier)
- Write module README with inputs/outputs tables and examples

### Detailed procedure

1. **Review existing module:**

```bash
cd modules/vpc
terraform fmt
cat README.md variables.tf outputs.tf main.tf
```

2. **Run dev plan** using module via environment stack:

```bash
cd ../../..   # course root
make plan ENV=dev
```

3. **Choose enhancement** (lab guide options):
   - **Option A:** S3 VPC gateway endpoint in private route table
   - **Option B:** `database_subnets` variable and subnet resources
4. **Update README** with before/after `module` block example.
5. **Add validations** for new variables where appropriate.
6. **Tag release:**

```bash
git tag -a modules/vpc/v1.0.0 -m "VPC module initial release"
git push origin modules/vpc/v1.0.0   # if remote configured
```

### Success criteria

- [ ] `terraform validate` passes in `modules/vpc` and `labs/shared/environments/dev`
- [ ] README documents all new inputs/outputs
- [ ] Git tag created (or documented if no remote)

### Common issues

| Symptom | Resolution |
|---------|------------|
| Cycle error after new resources | Check subnet → route table dependencies |
| Plan wants to replace VPC | Read `forces replacement`; fix CIDR if accidental |

---

## Lab 3.2 — Compose Networking Modules

**Duration:** 2 hours · **Guide:** [labs/week-03/LAB-02-compose.md](../../labs/week-03/LAB-02-compose.md)

### Objectives

- Wire `modules/vpc` + `modules/compute` in environment stack
- Pass outputs → inputs correctly
- Validate dev, test, and prod configurations

### Detailed procedure

1. **Trace data flow** in `labs/shared/environments/dev/main.tf`:
   - `module.vpc.private_subnet_ids[0]` → `module.compute` subnet argument
   - `module.vpc.vpc_id` → compute security group VPC
2. **Stretch (optional):** Create `modules/security-group/` with egress-only default for lab host.
3. **Run validation:**

```bash
make validate
```

4. **Fix** any broken references in `test` and `prod` tfvars (CIDR, AZ lists).

### Success criteria

- [ ] `make validate` passes for dev, test, prod
- [ ] Diagram (in notes or README) showing module output → input edges
- [ ] No hard-coded subnet IDs in compute module call

### Common issues

| Symptom | Resolution |
|---------|------------|
| `Invalid index` on subnet | AZ count vs subnet list length mismatch |
| Different plan per env | Expected—verify tfvars only, not module source |

---

## Lab 3.3 — Publish Internal Module

**Duration:** 1–2 hours · **Guide:** [labs/week-03/LAB-03-publish.md](../../labs/week-03/LAB-03-publish.md)

### Objectives

- Publish module via Git tag (enterprise pattern)
- Document upgrade path and semver policy in CHANGELOG

### Detailed procedure

1. **Create** `modules/vpc/CHANGELOG.md` with `v1.0.0` features.
2. **Document versioning policy:**
   - PATCH: bug fixes
   - MINOR: backward-compatible inputs
   - MAJOR: breaking input/output changes
3. **Compare sources** in README:
   - Local: `source = "../../../../modules/vpc"`
   - Git: `source = "git::https://github.com/YOUR_ORG/tf-modules.git//vpc?ref=v1.0.0"`
4. **Write upgrade paragraph** for hypothetical `v2.0.0` breaking change.

### Success criteria

- [ ] `CHANGELOG.md` committed
- [ ] Tag matches CHANGELOG version
- [ ] Consumer upgrade steps documented (even if consumer is same repo)

---

## Lab submission

Submit:

1. Link or path to enhanced `modules/vpc/README.md`
2. `CHANGELOG.md` excerpt
3. Output snippet: `make validate` success
4. Short essay (150 words): local path vs Git `ref=` trade-offs for BayAreaLa8s

---

## Cost control

```bash
make lab-stop
```

Tag `Course=terraform-enterprise` required.
