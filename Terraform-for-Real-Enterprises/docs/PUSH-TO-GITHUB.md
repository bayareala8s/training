# Push Course to GitHub

This course is published inside the **bayareala8s/training** monorepo:

`https://github.com/bayareala8s/training/tree/main/Terraform-for-Real-Enterprises`

## Push from repository root

```bash
git clone https://github.com/bayareala8s/training.git
cd training
# edit Terraform-for-Real-Enterprises/ ...
git add Terraform-for-Real-Enterprises/
git commit -m "Update Terraform for Real Enterprises course"
git push origin main
```

## SSH

```bash
git remote set-url origin git@github.com:bayareala8s/training.git
git push origin main
```

## Verify

```bash
git log -1 --oneline
git remote -v
```

After push, enable GitHub Actions in repository settings.
