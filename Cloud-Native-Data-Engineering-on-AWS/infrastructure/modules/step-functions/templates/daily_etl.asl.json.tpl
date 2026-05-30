{
  "Comment": "RetailCo daily ETL — Module 6 Terraform default",
  "StartAt": "ValidateInput",
  "States": {
    "ValidateInput": {
      "Type": "Pass",
      "Comment": "Ensure processing_date and dataset present",
      "Parameters": {
        "processing_date.$": "$.processing_date",
        "dataset.$": "$.dataset",
        "triggered_by.$": "$.triggered_by"
      },
      "Next": "StartGlueETL"
    },
    "StartGlueETL": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "${glue_job_name}",
        "Arguments": {
          "--processing_date.$": "$.processing_date",
          "--dataset_path.$": "$.dataset"
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["States.TaskFailed", "Glue.ThrottlingException"],
          "IntervalSeconds": 30,
          "MaxAttempts": 3,
          "BackoffRate": 2
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "NotifyFailure"
        }
      ],
      "ResultPath": "$.glue",
      "Next": "RunQualityCheck"
    },
    "RunQualityCheck": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke",
      "Parameters": {
        "FunctionName": "${validation_lambda_arn}",
        "Payload": {
          "processing_date.$": "$.processing_date",
          "dataset.$": "$.dataset"
        }
      },
      "Retry": [
        {
          "ErrorEquals": ["Lambda.ServiceException", "Lambda.TooManyRequestsException"],
          "IntervalSeconds": 10,
          "MaxAttempts": 2,
          "BackoffRate": 2
        }
      ],
      "Catch": [
        {
          "ErrorEquals": ["States.ALL"],
          "ResultPath": "$.error",
          "Next": "NotifyFailure"
        }
      ],
      "ResultPath": "$.quality_result",
      "Next": "EvaluateQuality"
    },
    "EvaluateQuality": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.quality_result.Payload.pass_rate",
          "NumericGreaterThanEquals": ${pass_rate_threshold},
          "Next": "NotifySuccess"
        }
      ],
      "Default": "NotifyFailure"
    },
    "NotifySuccess": {
      "Type": "Succeed"
    },
    "NotifyFailure": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "${sns_topic_arn}",
        "Subject": "RetailCo Daily ETL FAILED",
        "Message": {
          "status": "FAILED",
          "processing_date.$": "$.processing_date",
          "error.$": "$.error"
        }
      },
      "Next": "PipelineFailed"
    },
    "PipelineFailed": {
      "Type": "Fail",
      "Error": "PipelineFailed",
      "Cause": "Quality SLO not met or upstream task failed"
    }
  }
}
