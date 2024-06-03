Setting up AWS CodePipeline involves creating and configuring the various stages of the pipeline, including source, build, test, and deploy stages. Here’s a step-by-step guide to set up AWS CodePipeline with Terraform, focusing on integrating Terraform into the pipeline to automate infrastructure deployments.

### Step-by-Step Guide to Setting Up AWS CodePipeline

#### Prerequisites

1. AWS CLI installed and configured.
2. Terraform installed.
3. GitHub repository with your Terraform configurations.

#### Step 1: Create IAM Roles and Policies

1. **Create a Role for AWS CodePipeline:**
   ```hcl
   resource "aws_iam_role" "codepipeline_role" {
     name = "CodePipelineRole"
     assume_role_policy = jsonencode({
       Version = "2012-10-17"
       Statement = [
         {
           Effect = "Allow"
           Principal = {
             Service = "codepipeline.amazonaws.com"
           }
           Action = "sts:AssumeRole"
         }
       ]
     })
   }

   resource "aws_iam_role_policy_attachment" "codepipeline_role_policy" {
     role       = aws_iam_role.codepipeline_role.name
     policy_arn = "arn:aws:iam::aws:policy/AWSCodePipelineFullAccess"
   }
   ```

2. **Create a Role for AWS CodeBuild:**
   ```hcl
   resource "aws_iam_role" "codebuild_role" {
     name = "CodeBuildRole"
     assume_role_policy = jsonencode({
       Version = "2012-10-17"
       Statement = [
         {
           Effect = "Allow"
           Principal = {
             Service = "codebuild.amazonaws.com"
           }
           Action = "sts:AssumeRole"
         }
       ]
     })
   }

   resource "aws_iam_role_policy_attachment" "codebuild_role_policy" {
     role       = aws_iam_role.codebuild_role.name
     policy_arn = "arn:aws:iam::aws:policy/AWSCodeBuildDeveloperAccess"
   }
   ```

3. **Create a Role for AWS CodeDeploy:**
   ```hcl
   resource "aws_iam_role" "codedeploy_role" {
     name = "CodeDeployRole"
     assume_role_policy = jsonencode({
       Version = "2012-10-17"
       Statement = [
         {
           Effect = "Allow"
           Principal = {
             Service = "codedeploy.amazonaws.com"
           }
           Action = "sts:AssumeRole"
         }
       ]
     })
   }

   resource "aws_iam_role_policy_attachment" "codedeploy_role_policy" {
     role       = aws_iam_role.codedeploy_role.name
     policy_arn = "arn:aws:iam::aws:policy/service-role/AWSCodeDeployRole"
   }
   ```

#### Step 2: Create an S3 Bucket for Artifact Storage

```hcl
resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "my-codepipeline-bucket"
  acl    = "private"
}
```

#### Step 3: Create a CodeBuild Project

1. **Create the Buildspec File (buildspec.yml):**
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

2. **Terraform Configuration for CodeBuild Project:**
   ```hcl
   resource "aws_codebuild_project" "build_project" {
     name          = "MyBuildProject"
     service_role  = aws_iam_role.codebuild_role.arn

     artifacts {
       type = "CODEPIPELINE"
     }

     environment {
       compute_type                = "BUILD_GENERAL1_SMALL"
       image                       = "aws/codebuild/standard:4.0"
       type                        = "LINUX_CONTAINER"
     }

     source {
       type     = "CODEPIPELINE"
       buildspec = file("buildspec.yml")
     }
   }
   ```

#### Step 4: Create the CodePipeline

1. **Terraform Configuration for CodePipeline:**
   ```hcl
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
         owner            = "ThirdParty"
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
   ```

2. **Create CodeDeploy Application and Deployment Group:**
   ```hcl
   resource "aws_codedeploy_app" "app" {
     name = "MyCodeDeployApp"
   }

   resource "aws_codedeploy_deployment_group" "deployment_group" {
     app_name              = aws_codedeploy_app.app.name
     deployment_group_name = "MyDeploymentGroup"
     service_role_arn      = aws_iam_role.codedeploy_role.arn

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

#### Step 5: Apply Terraform Configuration

1. **Initialize Terraform:**
   ```sh
   terraform init
   ```

2. **Apply the Terraform Configuration:**
   ```sh
   terraform apply -auto-approve
   ```

#### Step 6: Configure GitHub Repository

1. **Push your code to the GitHub repository:**
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-github-username/your-repo-name.git
   git push -u origin main
   ```

#### Step 7: Monitor the Pipeline

- **AWS CodePipeline Console:**
  - Navigate to the AWS CodePipeline console to monitor the progress of your pipeline.
  - Ensure that each stage (Source, Build, Deploy) executes successfully.

- **AWS CodeBuild Logs:**
  - Check AWS CodeBuild logs for detailed information about the build process.

- **AWS CodeDeploy Console:**
  - Verify that the deployment is successful and the EC2 instance is running as expected.

### Conclusion

By following these steps, you can set up AWS CodePipeline to automate the deployment of Terraform configurations. This setup ensures that your infrastructure as code is consistently and reliably deployed across your environments, leveraging the power of AWS CodePipeline, CodeBuild, and CodeDeploy.
