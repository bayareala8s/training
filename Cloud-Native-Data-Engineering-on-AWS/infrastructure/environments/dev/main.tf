terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project
      Environment = var.environment
      Student     = var.student
      Course      = "cloud-native-data-engineering"
      ManagedBy   = "terraform"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "project" {
  type    = string
  default = "cnde"
}

variable "student" {
  type    = string
  default = "student"
}

variable "alert_email" {
  type        = string
  description = "Email for SNS alerts (monitoring module). Use a valid address you can confirm."
  default     = "alerts@example.com"
}

variable "enable_schedules" {
  type        = bool
  description = "Enable EventBridge schedules (costs $ if left running). Keep false for lab deploy/teardown."
  default     = false
}

# ---------------------------------------------------------------------------
# Week 1: S3 Data Lake
# ---------------------------------------------------------------------------
module "data_lake" {
  source      = "../../modules/s3-data-lake"
  project     = var.project
  environment = var.environment
  student     = var.student
  aws_region  = var.aws_region
}

# ---------------------------------------------------------------------------
# Week 2: Lambda Ingestion
# ---------------------------------------------------------------------------
module "lambda_ingestion" {
  source           = "../../modules/lambda-ingestion"
  project          = var.project
  environment      = var.environment
  student          = var.student
  data_lake_bucket = module.data_lake.bucket_name
  enable_schedule  = var.enable_schedules
}

# ---------------------------------------------------------------------------
# Week 3: Glue ETL
# ---------------------------------------------------------------------------
module "glue_etl" {
  source      = "../../modules/glue-etl"
  project     = var.project
  environment = var.environment
  student     = var.student
  aws_region  = var.aws_region
  bucket_name = module.data_lake.bucket_name
}

# ---------------------------------------------------------------------------
# Week 4: Quality Validation Lambda (stub for Step Functions)
# ---------------------------------------------------------------------------
module "quality_validation" {
  source           = "../../modules/quality-validation"
  project          = var.project
  environment      = var.environment
  student          = var.student
  data_lake_bucket = module.data_lake.bucket_name
}

# ---------------------------------------------------------------------------
# Week 8: Monitoring (before Step Functions — SNS topic used by SFN)
# ---------------------------------------------------------------------------
module "monitoring" {
  source                = "../../modules/monitoring"
  project               = var.project
  environment           = var.environment
  student               = var.student
  aws_region            = var.aws_region
  alert_email           = var.alert_email
  glue_job_names        = [module.glue_etl.glue_job_name]
  lambda_function_names = module.lambda_ingestion.lambda_function_names
  data_lake_bucket      = module.data_lake.bucket_name
}

# ---------------------------------------------------------------------------
# Week 6: Step Functions Orchestration
# ---------------------------------------------------------------------------
module "step_functions" {
  source                = "../../modules/step-functions"
  project               = var.project
  environment           = var.environment
  student               = var.student
  aws_region            = var.aws_region
  bucket_name           = module.data_lake.bucket_name
  glue_job_name         = module.glue_etl.glue_job_name
  validation_lambda_arn = module.quality_validation.validation_lambda_arn
  sns_topic_arn         = module.monitoring.sns_critical_topic_arn
  enable_schedule       = var.enable_schedules
}

# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------
output "data_lake_bucket" {
  description = "S3 data lake bucket name"
  value       = module.data_lake.bucket_name
}

output "zone_prefixes" {
  description = "Data lake zone prefixes"
  value       = module.data_lake.zone_prefixes
}

output "lambda_function_names" {
  value = module.lambda_ingestion.lambda_function_names
}

output "glue_job_name" {
  value = module.glue_etl.glue_job_name
}

output "glue_catalog_database" {
  value = module.glue_etl.glue_catalog_database
}

output "cleaned_crawler_name" {
  value = module.glue_etl.cleaned_crawler_name
}

output "state_machine_arn" {
  value = module.step_functions.state_machine_arn
}

output "state_machine_name" {
  value = module.step_functions.state_machine_name
}

output "dashboard_name" {
  value = module.monitoring.dashboard_name
}

output "sns_critical_topic_arn" {
  value = module.monitoring.sns_critical_topic_arn
}

output "quality_validation_lambda" {
  value = module.quality_validation.validation_lambda_name
}
