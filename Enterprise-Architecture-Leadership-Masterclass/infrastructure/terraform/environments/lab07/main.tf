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

variable "replica_region" {
  type    = string
  default = "us-west-2"
}

variable "student_id" {
  type = string
}

variable "alert_email" {
  type    = string
  default = ""
}

variable "enable_replication" {
  type    = bool
  default = false
}

variable "expiration_date" {
  type = string
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "BayLearn"
      Course      = "EnterpriseArchitectureLeadership"
      Module      = "07"
      Environment = "Lab"
    }
  }
}

provider "aws" {
  alias  = "replica"
  region = var.replica_region

  default_tags {
    tags = {
      Project     = "BayLearn"
      Course      = "EnterpriseArchitectureLeadership"
      Module      = "07"
      Environment = "Lab"
    }
  }
}

locals {
  # Keep within S3/IAM name limits; student_id sanitized
  student_safe = lower(replace(replace(var.student_id, " ", "-"), "_", "-"))
  name_prefix  = "bl-m07-${substr(local.student_safe, 0, 12)}"
}

module "security_resilience" {
  source = "../../modules/security-resilience"

  providers = {
    aws         = aws
    aws.replica = aws.replica
  }

  name_prefix        = local.name_prefix
  student_id         = var.student_id
  aws_region         = var.aws_region
  replica_region     = var.replica_region
  enable_replication = var.enable_replication
  alert_email        = var.alert_email
  expiration_date    = var.expiration_date
}

output "name_prefix" {
  value = module.security_resilience.name_prefix
}

output "primary_bucket_name" {
  value = module.security_resilience.primary_bucket_name
}

output "replica_bucket_name" {
  value = module.security_resilience.replica_bucket_name
}

output "kms_key_arn" {
  value = module.security_resilience.kms_key_arn
}

output "settlement_writer_role_arn" {
  value = module.security_resilience.settlement_writer_role_arn
}

output "settlement_reader_role_arn" {
  value = module.security_resilience.settlement_reader_role_arn
}

output "evidence_auditor_role_arn" {
  value = module.security_resilience.evidence_auditor_role_arn
}

output "evidence_table_name" {
  value = module.security_resilience.evidence_table_name
}

output "sns_topic_arn" {
  value = module.security_resilience.sns_topic_arn
}

output "alarm_names" {
  value = module.security_resilience.alarm_names
}

output "drill_lambda_name" {
  value = module.security_resilience.drill_lambda_name
}

output "simulated_dr_guidance" {
  value = module.security_resilience.simulated_dr_guidance
}
