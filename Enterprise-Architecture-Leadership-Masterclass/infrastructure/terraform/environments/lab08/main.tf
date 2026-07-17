terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "student_id" {
  type = string
}

variable "expiration_date" {
  type = string
}

variable "use_mock_bedrock" {
  type    = bool
  default = true
}

variable "bedrock_model_id" {
  type    = string
  default = "amazon.nova-micro-v1:0"
}

variable "enable_guardrails" {
  type    = bool
  default = false
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = "BayLearn"
      Course      = "EnterpriseArchitectureLeadership"
      Module      = "08"
      Environment = "Lab"
    }
  }
}

locals {
  student_safe = lower(replace(replace(var.student_id, " ", "-"), "_", "-"))
  name_prefix  = "bl-m08-${substr(local.student_safe, 0, 12)}"
}

module "ai_decision_assistant" {
  source = "../../modules/ai-decision-assistant"

  name_prefix       = local.name_prefix
  student_id        = var.student_id
  expiration_date   = var.expiration_date
  use_mock_bedrock  = var.use_mock_bedrock
  bedrock_model_id  = var.bedrock_model_id
  enable_guardrails = var.enable_guardrails
}

output "api_endpoint" {
  value = module.ai_decision_assistant.api_endpoint
}

output "api_token" {
  value     = module.ai_decision_assistant.api_token
  sensitive = true
}

output "state_machine_arn" {
  value = module.ai_decision_assistant.state_machine_arn
}

output "decisions_table_name" {
  value = module.ai_decision_assistant.decisions_table_name
}

output "artifacts_bucket" {
  value = module.ai_decision_assistant.artifacts_bucket
}

output "use_mock_bedrock" {
  value = module.ai_decision_assistant.use_mock_bedrock
}

output "bedrock_model_id" {
  value = module.ai_decision_assistant.bedrock_model_id
}

output "bedrock_enablement_notes" {
  value = module.ai_decision_assistant.bedrock_enablement_notes
}

output "infer_lambda_name" {
  value = module.ai_decision_assistant.infer_lambda_name
}
