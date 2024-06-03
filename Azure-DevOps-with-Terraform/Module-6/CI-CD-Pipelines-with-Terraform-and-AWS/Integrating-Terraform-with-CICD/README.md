Integrating Terraform with a CI/CD pipeline involves automating the deployment and management of your infrastructure as code. Here, we'll use AWS CodePipeline and AWS CodeBuild to automate the deployment of Terraform configurations. The example will demonstrate how to set up a pipeline that automatically deploys infrastructure changes when code is pushed to a repository.

### Example: Automating Terraform Deployments with AWS CodePipeline and CodeBuild

#### Prerequisites
1. AWS CLI installed and configured.
2. Terraform installed.
3. An AWS account with necessary permissions.
4. A GitHub repository with your Terraform configurations.

### Step-by-Step Guide

#### Step 1: Prepare Terraform Configurations

1. **Repository Structure:**
   ```plaintext
   ├── modules/
   │   ├── vpc/
   │   │   └── main.tf
   │   ├── ec2/
   │   │   └── main.tf
   ├── env/
   │   ├── dev/
   │   │   ├── main.tf
   │   │   ├── variables.tf
   │   │   └── outputs.tf
   ├── main.tf
   ├── variables.tf
   ├── outputs.tf
   ├── buildspec.yml
   └── pipeline.tf
   ```

2. **VPC Module (modules/vpc/main.tf):**
   ```hcl
   resource "aws_vpc" "main" {
     cidr_block = "10.0.0.0/16"
     tags = {
       Name = "main-vpc"
     }
   }

   resource "aws_subnet" "public" {
     count             = 2
     cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
     vpc_id            = aws_vpc.main.id
     availability_zone = element(data.aws_availability_zones.available.names, count.index)
     map_public_ip_on_launch = true
     tags = {
       Name = "public-subnet-${count.index}"
     }
   }
   ```

3. **EC2 Module (modules/ec2/main.tf):**
   ```hcl
   resource "aws_instance" "web" {
     ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2 AMI
     instance_type = "t2.micro"
     subnet_id     = var.subnet_id
     tags = {
       Name = "web-instance"
     }
   }

   variable "subnet_id" {
     description = "The ID of the subnet to deploy the instance in"
   }
   ```

4. **Environment Configuration (env/dev/main.tf):**
   ```hcl
   module "vpc" {
     source = "../../modules/vpc"
   }

   module "ec2" {
     source = "../../modules/ec2"
     subnet_id = module.vpc.public_subnet_ids[0]
   }
   ```

5. **Build Specification (buildspec.yml):**
   ```yaml
   version: 0.2

   phases:
     install:
       runtime-versions:
         terraform: 0.14
       commands:
         - terraform init
     build:
       commands:
         - terraform validate
         - terraform plan -out=tfplan
         - terraform apply -auto-approve tfplan
   ```

6. **Pipeline Configuration (pipeline.tf):**
   ```hcl
   provider "aws" {
     region = "us-west-2"
   }

   resource "aws_s3_bucket" "codepipeline_bucket" {
     bucket = "my-codepipeline-bucket"
   }

   resource "aws_iam_role" "codepipeline_role" {
     name = "codepipeline_role"
     assume_role_policy = <<EOF
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "Service": "codepipeline.amazonaws.com"
           },
           "Action": "sts:AssumeRole"
         }
       ]
     }
     EOF
   }

   resource "aws_iam_role_policy" "codepipeline_policy" {
     role = aws_iam_role.codepipeline_role.id
     policy = <<EOF
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": [
             "s3:GetObject",
             "s3:PutObject"
           ],
           "Resource": [
             "${aws_s3_bucket.codepipeline_bucket.arn}",
             "${aws_s3_bucket.codepipeline_bucket.arn}/*"
           ]
         },
         {
           "Effect": "Allow",
           "Action": [
             "codebuild:*"
           ],
           "Resource": "*"
         }
       ]
     }
     EOF
   }

   resource "aws_codepipeline" "pipeline" {
     name     = "MyPipeline"
     role_arn = aws_iam_role.codepipeline_role.arn

     artifact_store {
       type     = "S3"
       location = aws_s3_bucket.codepipeline_bucket.bucket
     }

     stage {
       name = "Source"

       action {
         name             = "Source"
         category         = "Source"
         owner            = "AWS"
         provider         = "GitHub"
         version          = "1"
         output_artifacts = ["source_output"]

         configuration = {
           Owner  = "your-github-username"
           Repo   = "your-repo-name"
           Branch = "main"
           OAuthToken = "your-github-token"
         }
       }
     }

     stage {
       name = "Build"

       action {
         name             = "Build"
         category         = "Build"
         owner            = "AWS"
         provider         = "CodeBuild"
         version          = "1"
         input_artifacts  = ["source_output"]
         output_artifacts = ["build_output"]

         configuration = {
           ProjectName = aws_codebuild_project.build_project.name
         }
       }
     }

     stage {
       name = "Deploy"

       action {
         name            = "Deploy"
         category        = "Deploy"
         owner           = "AWS"
         provider        = "CodeDeploy"
         version         = "1"
         input_artifacts = ["build_output"]

         configuration = {
           ApplicationName     = aws_codedeploy_app.app.name
           DeploymentGroupName = aws_codedeploy_deployment_group.deployment_group.name
         }
       }
     }
   }

   resource "aws_codebuild_project" "build_project" {
     name          = "MyBuildProject"
     service_role  = aws_iam_role.codepipeline_role.arn

     artifacts {
       type = "CODEPIPELINE"
     }

     environment {
       compute_type                = "BUILD_GENERAL1_SMALL"
       image                       = "aws/codebuild/standard:4.0"
       type                        = "LINUX_CONTAINER"
       environment_variable {
         name  = "AWS_DEFAULT_REGION"
         value = "us-west-2"
       }
     }

     source {
       type = "CODEPIPELINE"
       buildspec = file("buildspec.yml")
     }
   }

   resource "aws_codedeploy_app" "app" {
     name = "MyCodeDeployApp"
   }

   resource "aws_codedeploy_deployment_group" "deployment_group" {
     app_name              = aws_codedeploy_app.app.name
     deployment_group_name = "MyDeploymentGroup"
     service_role_arn      = aws_iam_role.codepipeline_role.arn

     deployment_config_name = "CodeDeployDefault.OneAtATime"

     ec2_tag_set {
       ec2_tag_filter {
         key   = "Name"
         value = "web-instance"
         type  = "KEY_AND_VALUE"
       }
     }

     auto_rollback_configuration {
       enabled = true
       events  = ["DEPLOYMENT_FAILURE"]
     }
   }
   ```

#### Step 2: Initialize and Apply Terraform Configuration

1. **Initialize Terraform:**
   ```sh
   terraform init
   ```

2. **Apply the Terraform Configuration:**
   ```sh
   terraform apply -auto-approve
   ```

#### Step 3: Configure GitHub Repository

1. **Push your code to the GitHub repository:**
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-github-username/your-repo-name.git
   git push -u origin main
   ```

#### Step 4: Monitor the Pipeline

- **AWS CodePipeline Console:**
  - Navigate to the AWS CodePipeline console to monitor the progress of your pipeline.
  - Ensure that each stage (Source, Build, Deploy) executes successfully.

- **AWS CodeBuild Logs:**
  - Check AWS CodeBuild logs for detailed information about the build process.

- **AWS CodeDeploy Console:**
  - Verify that the deployment is successful and the EC2 instance is running as expected.

### Conclusion

By following these steps, you can integrate Terraform with a CI/CD pipeline using AWS CodePipeline and CodeBuild. This setup automates the deployment of infrastructure changes, ensuring that your infrastructure as code is consistently and reliably deployed across your environments.
