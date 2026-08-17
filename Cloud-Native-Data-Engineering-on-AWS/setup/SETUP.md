# Environment Setup Guide

Complete this setup before starting Week 1.

---

## 1. AWS Account

1. Create an AWS account at [aws.amazon.com](https://aws.amazon.com)
2. Enable MFA on the root account
3. Create an IAM user named `cnde-student` with programmatic access
4. Attach the policy `PowerUserAccess` (for labs) or use the least-privilege policy in [setup/iam-policy.json](iam-policy.json)

```bash
aws configure
# AWS Access Key ID: <your-key>
# AWS Secret Access Key: <your-secret>
# Default region: us-east-1
# Default output format: json
```

Verify:

```bash
aws sts get-caller-identity
```

---

## 2. AWS CLI

Install AWS CLI v2:

**macOS:**
```bash
brew install awscli
```

**Linux:**
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install
```

**Windows:** Download from [AWS CLI install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

---

## 3. Python Environment

```bash
cd Cloud-Native-Data-Engineering-on-AWS
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Verify:

```bash
python -c "import boto3, pandas; print('OK')"
```

---

## 4. Terraform

**macOS:**
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
terraform version
```

---

## 5. Git & GitHub

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Create a GitHub repository for your course work:

```bash
git init
git remote add origin https://github.com/your-username/cloud-native-data-engineering.git
```

---

## 6. VS Code Extensions (Recommended)

- AWS Toolkit
- Python
- HashiCorp Terraform
- Markdown All in One
- YAML

---

## 7. AWS Budget Alert

1. Open AWS Console → Billing → Budgets
2. Create budget → Cost budget → $20/month
3. Set alert at 80% ($16)

---

## 8. Clone Course Repository

```bash
git clone <course-repo-url>
cd Cloud-Native-Data-Engineering-on-AWS
```

---

## Verification Checklist

- [ ] `aws sts get-caller-identity` returns your account
- [ ] `python --version` shows 3.10+
- [ ] `terraform version` shows 1.5+
- [ ] Virtual environment activated, dependencies installed
- [ ] GitHub repository created
- [ ] AWS budget alert configured

You are ready for [Module 1](../modules/module-01-foundations/README.md).
