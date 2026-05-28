# Lab 1.1 — Install Terraform & Toolchain

**Duration:** 60–90 minutes · **Week 1**

## Objectives

- Install Terraform, AWS CLI, and Git
- Verify versions meet course requirements
- Configure AWS credentials (SSO or profile)

## Steps

### 1. Install Terraform

**macOS (Homebrew):**
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

**Linux:**
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

Verify:
```bash
terraform version   # >= 1.5.0
```

### 2. Install AWS CLI v2

Follow: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

```bash
aws --version
aws sts get-caller-identity
```

### 3. Configure AWS access

**SSO (recommended for enterprises):**
```bash
aws configure sso
aws sso login --profile bal8s-lab
export AWS_PROFILE=bal8s-lab
```

**Named profile:**
```bash
aws configure --profile bal8s-lab
export AWS_PROFILE=bal8s-lab
```

### 4. Install optional tools

```bash
# macOS
brew install tflint checkov jq
```

## Deliverable

Screenshot or terminal output showing:

- `terraform version`
- `aws sts get-caller-identity`
- Account ID and region you will use

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ExpiredToken` | Re-run `aws sso login` |
| Wrong account | Check `AWS_PROFILE` and `aws sts get-caller-identity` |

## Next

[Lab 1.2 — AWS Provider](LAB-02-provider.md)
