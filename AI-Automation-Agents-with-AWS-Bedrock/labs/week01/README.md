# Week 1 Labs

## Prerequisites

- AWS CLI configured (`aws sts get-caller-identity`)
- Bedrock model access enabled in your region ([Model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html))
- Python 3.11+

```bash
cd labs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

## Lab 1.1

```bash
python week01/invoke_bedrock.py --prompt "Your prompt here"
```

## Lab 1.2

```bash
python week01/compare_outputs.py > week01/comparison_results.json
```

Document findings in your Week 1 assignment.
