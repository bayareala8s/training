Creating CI/CD pipelines with Terraform and AWS involves several steps to ensure efficient deployment and management of infrastructure. Below is a detailed guide to help you set up a CI/CD pipeline using Terraform and AWS:

### CI/CD Pipeline Overview

1. **Version Control System (VCS):**
   - **GitHub/GitLab/Bitbucket:** Store your Terraform configuration files in a repository.
   
2. **Continuous Integration (CI):**
   - **Jenkins/

Creating CI/CD pipelines with Terraform and AWS involves several steps to ensure efficient deployment and management of infrastructure. Below is a detailed guide to help you set up a CI/CD pipeline using Terraform and AWS:

### CI/CD Pipeline Overview

1. **Version Control System (VCS):**
   - **GitHub/GitLab/Bitbucket:** Store your Terraform configuration files in a repository.
   
2. **Continuous Integration (CI):**
   - **Jenkins/Travis CI/GitLab CI:** Automate the testing of your Terraform code.
   
3. **Continuous Deployment (CD):**
   - **Terraform Cloud/Enterprise, AWS CodePipeline:** Manage and automate the deployment of your infrastructure.

### Detailed Steps

#### 1. Setup Version Control System (VCS)

1. **Create a Repository:**
   - Initialize a repository in GitHub, GitLab, or Bitbucket.
   - Add your Terraform configuration files.

2. **Repository Structure:**
   - Organize your Terraform code with a clear directory structure.
   ```
   ├── modules/
   ├── env/
   │   ├── dev/
   │   ├── prod/
   └── main.tf
   └── variables.tf
   └── outputs.tf
   ```

#### 2. Setup CI with Jenkins

1. **Install Jenkins:**
   - Deploy Jenkins on an EC2 instance or use Jenkins on AWS (Jenkins on Amazon EC2).

2. **Install Plugins:**
   - Install necessary plugins such as Git, Terraform, and AWS credentials.

3. **Create a Jenkins Pipeline:**
   - Define a Jenkinsfile in your repository.
   - Sample Jenkinsfile:
     ```groovy
     pipeline {
         agent any
         environment {
             AWS_CREDENTIALS = credentials('aws-credentials-id')
         }
         stages {
             stage('Checkout') {
                 steps {
                     git 'https://github.com/your-repo.git'
                 }
             }
             stage('Validate') {
                 steps {
                     sh 'terraform validate'
                 }
             }
             stage('Plan') {
                 steps {
                     sh 'terraform plan -out=tfplan'
                 }
             }
             stage('Apply') {
                 steps {
                     sh 'terraform apply tfplan'
                 }
             }
         }
     }
     ```

4. **Configure AWS Credentials:**
   - Store AWS credentials in Jenkins using the Credentials plugin.

#### 3. Setup CD with AWS CodePipeline

1. **Create an S3 Bucket:**
   - Store your build artifacts in an S3 bucket.

2. **Create a CodePipeline:**
   - Define the stages: Source, Build, Deploy.

3. **Integrate with CodeBuild:**
   - Create a build project in AWS CodeBuild.
   - Define a `buildspec.yml` file.
     ```yaml
     version: 0.2
     phases:
       install:
         runtime-versions:
           terraform: 0.14
       build:
         commands:
           - terraform init
           - terraform validate
           - terraform plan -out=tfplan
           - terraform apply -auto-approve tfplan
     ```

4. **Deploy with CodeDeploy:**
   - Use CodeDeploy to manage the deployment of your infrastructure changes.

### Best Practices

1. **State Management:**
   - Use remote state storage with AWS S3 and state locking with DynamoDB.

2. **Modularize Terraform Code:**
   - Break down your Terraform configuration into reusable modules.

3. **Secure Secrets Management:**
   - Use AWS Secrets Manager or AWS Systems Manager Parameter Store to manage sensitive information.

4. **Automated Testing:**
   - Implement automated testing for your Terraform code using tools like Terratest.

5. **Monitoring and Logging:**
   - Enable detailed monitoring and logging using AWS CloudWatch.

### Example Project Structure

```plaintext
.
├── modules/
│   ├── vpc/
│   │   └── main.tf
│   ├── ec2/
│   │   └── main.tf
├── env/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
│   ├── prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars
├── Jenkinsfile
├── buildspec.yml
├── main.tf
├── variables.tf
└── outputs.tf
```

This guide provides a comprehensive approach to setting up a CI/CD pipeline with Terraform and AWS. Each step ensures that your infrastructure is deployed and managed efficiently, with a focus on best practices and automation.


Here’s a step-by-step guide for setting up a CI/CD pipeline with Terraform and AWS for a real-world use case:

### Use Case: Deploying a Highly Available Web Application

**Scenario:** You want to deploy a highly available web application on AWS using Terraform, with a CI/CD pipeline that ensures continuous deployment of infrastructure changes.

#### Step 1: Setup Version Control System (VCS)

1. **Create a Repository:**
   - Use GitHub to create a new repository named `web-app-infra`.

2. **Repository Structure:**
   - Organize your Terraform code with a clear directory structure.
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
   │   │   ├── outputs.tf
   │   │   └── terraform.tfvars
   │   ├── prod/
   │   │   ├── main.tf
   │   │   ├── variables.tf
   │   │   ├── outputs.tf
   │   │   └── terraform.tfvars
   ├── Jenkinsfile
   ├── buildspec.yml
   ├── main.tf
   ├── variables.tf
   └── outputs.tf
   ```

3. **Initialize the Repository:**
   - Initialize your local repository and push the initial code to GitHub.
   ```sh
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-username/web-app-infra.git
   git push -u origin master
   ```

#### Step 2: Setup Jenkins for Continuous Integration (CI)

1. **Install Jenkins:**
   - Deploy Jenkins on an EC2 instance or use Jenkins on AWS.

2. **Install Plugins:**
   - Install the Git, Terraform, and AWS Credentials plugins in Jenkins.

3. **Create a Jenkins Pipeline:**
   - Define a `Jenkinsfile` in your repository.
   ```groovy
   pipeline {
       agent any
       environment {
           AWS_CREDENTIALS = credentials('aws-credentials-id')
       }
       stages {
           stage('Checkout') {
               steps {
                   git 'https://github.com/your-username/web-app-infra.git'
               }
           }
           stage('Validate') {
               steps {
                   sh 'terraform validate'
               }
           }
           stage('Plan') {
               steps {
                   sh 'terraform plan -out=tfplan'
               }
           }
           stage('Apply') {
               steps {
                   sh 'terraform apply -auto-approve tfplan'
               }
           }
       }
   }
   ```

4. **Configure AWS Credentials:**
   - Store AWS credentials in Jenkins using the Credentials plugin.

#### Step 3: Define Terraform Configuration

1. **VPC Module:**
   ```hcl
   // modules/vpc/main.tf
   resource "aws_vpc" "main" {
       cidr_block = "10.0.0.0/16"
       tags = {
           Name = "main-vpc"
       }
   }

   resource "aws_subnet" "subnet" {
       count = 2
       cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
       vpc_id     = aws_vpc.main.id
       availability_zone = element(data.aws_availability_zones.available.names, count.index)
       tags = {
           Name = "subnet-${count.index}"
       }
   }

   output "vpc_id" {
       value = aws_vpc.main.id
   }

   output "subnet_ids" {
       value = aws_subnet.subnet[*].id
   }
   ```

2. **EC2 Module:**
   ```hcl
   // modules/ec2/main.tf
   resource "aws_instance" "web" {
       ami           = "ami-0c55b159cbfafe1f0"
       instance_type = "t2.micro"
       subnet_id     = var.subnet_id
       tags = {
           Name = "web-instance"
       }
   }

   output "instance_id" {
       value = aws_instance.web.id
   }
   ```

3. **Environment Configurations:**
   ```hcl
   // env/dev/main.tf
   module "vpc" {
       source = "../../modules/vpc"
   }

   module "ec2" {
       source = "../../modules/ec2"
       subnet_id = module.vpc.subnet_ids[0]
   }

   // env/dev/terraform.tfvars
   vpc_cidr = "10.0.0.0/16"
   ```

#### Step 4: Setup AWS CodePipeline for Continuous Deployment (CD)

1. **Create an S3 Bucket:**
   - Create an S3 bucket to store build artifacts.

2. **Create a CodePipeline:**
   - Define the stages: Source, Build, Deploy.

3. **Integrate with CodeBuild:**
   - Create a build project in AWS CodeBuild.
   - Define a `buildspec.yml` file.
   ```yaml
   version: 0.2
   phases:
     install:
       runtime-versions:
         terraform: 0.14
     build:
       commands:
         - terraform init
         - terraform validate
         - terraform plan -out=tfplan
         - terraform apply -auto-approve tfplan
   ```

4. **Deploy with CodeDeploy:**
   - Use CodeDeploy to manage the deployment of your infrastructure changes.

### Step-by-Step Example Execution

1. **Commit and Push Changes:**
   - Make changes to your Terraform configuration and push them to the GitHub repository.
   ```sh
   git add .
   git commit -m "Updated VPC and EC2 configuration"
   git push
   ```

2. **Jenkins Pipeline Execution:**
   - Jenkins will automatically trigger the pipeline.
   - The pipeline will checkout the code, validate the Terraform configuration, create a plan, and apply the changes.

3. **CodePipeline Execution:**
   - AWS CodePipeline will pick up the changes from the S3 bucket.
   - CodeBuild will execute the buildspec commands.
   - CodeDeploy will deploy the infrastructure changes.

### Monitoring and Validation

1. **CloudWatch Logs:**
   - Monitor CloudWatch logs for build and deployment activities.

2. **AWS Console:**
   - Validate the infrastructure changes in the AWS Management Console.
   - Ensure the EC2 instances and VPCs are created as expected.

### Conclusion

By following these steps, you can set up a CI/CD pipeline with Terraform and AWS for deploying a highly available web application. This setup ensures that your infrastructure changes are continuously tested, validated, and deployed, providing a robust and scalable environment for your applications.


Here are additional examples of CI/CD pipelines using Terraform and AWS for different industry use cases:

### 1. Financial Services: Secure Data Processing System

**Scenario:** A financial services company needs to deploy a secure data processing system to handle sensitive customer information. The infrastructure must comply with industry regulations, ensure data encryption, and maintain high availability.

#### Infrastructure Components:
- VPC with public and private subnets
- EC2 instances in private subnets
- RDS for database management
- S3 for secure data storage
- KMS for encryption

#### Repository Structure:
```plaintext
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   ├── s3/
│   ├── kms/
├── env/
│   ├── dev/
│   ├── prod/
├── Jenkinsfile
├── buildspec.yml
├── main.tf
├── variables.tf
└── outputs.tf
```

#### Terraform Configurations:

**VPC Module:**
```hcl
resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = {
        Name = "secure-vpc"
    }
}

resource "aws_subnet" "public" {
    count = 2
    cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index)
    vpc_id = aws_vpc.main.id
    map_public_ip_on_launch = true
    availability_zone = element(data.aws_availability_zones.available.names, count.index)
    tags = {
        Name = "public-subnet-${count.index}"
    }
}

resource "aws_subnet" "private" {
    count = 2
    cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 2)
    vpc_id = aws_vpc.main.id
    availability_zone = element(data.aws_availability_zones.available.names, count.index)
    tags = {
        Name = "private-subnet-${count.index}"
    }
}
```

**RDS Module:**
```hcl
resource "aws_db_instance" "default" {
    allocated_storage = 20
    engine = "mysql"
    instance_class = "db.t2.micro"
    name = "mydb"
    username = "admin"
    password = "password"
    parameter_group_name = "default.mysql5.7"
    skip_final_snapshot = true
    vpc_security_group_ids = [aws_security_group.db.id]
    db_subnet_group_name = aws_db_subnet_group.default.name
}

resource "aws_db_subnet_group" "default" {
    name = "main"
    subnet_ids = aws_subnet.private[*].id
}

resource "aws_security_group" "db" {
    vpc_id = aws_vpc.main.id
    ingress {
        from_port = 3306
        to_port = 3306
        protocol = "tcp"
        cidr_blocks = ["10.0.0.0/16"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
```

### 2. E-commerce: Scalable Online Store

**Scenario:** An e-commerce company needs to deploy a scalable online store to handle high traffic during peak shopping seasons. The infrastructure should include load balancing, auto-scaling, and managed database services.

#### Infrastructure Components:
- VPC with public and private subnets
- EC2 instances with Auto Scaling
- RDS for MySQL database
- S3 for static content storage
- CloudFront for content delivery

#### Repository Structure:
```plaintext
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── autoscaling/
│   ├── rds/
│   ├── s3/
│   ├── cloudfront/
├── env/
│   ├── dev/
│   ├── prod/
├── Jenkinsfile
├── buildspec.yml
├── main.tf
├── variables.tf
└── outputs.tf
```

#### Terraform Configurations:

**Auto Scaling Module:**
```hcl
resource "aws_autoscaling_group" "app" {
    launch_configuration = aws_launch_configuration.app.id
    min_size = 2
    max_size = 10
    vpc_zone_identifier = aws_subnet.public[*].id
    tags = [
        {
            key                 = "Name"
            value               = "app-instance"
            propagate_at_launch = true
        },
    ]
}

resource "aws_launch_configuration" "app" {
    image_id = "ami-0c55b159cbfafe1f0"
    instance_type = "t2.micro"
    security_groups = [aws_security_group.app.id]
    user_data = <<-EOF
                #!/bin/bash
                sudo yum update -y
                sudo yum install -y httpd
                sudo systemctl start httpd
                sudo systemctl enable httpd
                echo "Welcome to the online store!" > /var/www/html/index.html
                EOF
}

resource "aws_security_group" "app" {
    vpc_id = aws_vpc.main.id
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
```

**CloudFront Module:**
```hcl
resource "aws_cloudfront_distribution" "s3_distribution" {
    origin {
        domain_name = aws_s3_bucket.static_content.bucket_domain_name
        origin_id   = "s3-origin"
    }

    default_cache_behavior {
        allowed_methods  = ["GET", "HEAD"]
        cached_methods   = ["GET", "HEAD"]
        target_origin_id = "s3-origin"
        viewer_protocol_policy = "redirect-to-https"
        forwarded_values {
            query_string = false
            cookies {
                forward = "none"
            }
        }
    }

    enabled = true
    is_ipv6_enabled = true
    comment = "S3 static content distribution"
    default_root_object = "index.html"
}
```

### 3. Healthcare: HIPAA-Compliant Application

**Scenario:** A healthcare provider needs to deploy an application that processes patient data, adhering to HIPAA compliance. The infrastructure must include strong encryption, access controls, and auditing.

#### Infrastructure Components:
- VPC with public and private subnets
- EC2 instances in private subnets
- RDS for database management
- S3 for encrypted data storage
- CloudTrail for auditing
- KMS for encryption

#### Repository Structure:
```plaintext
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   ├── s3/
│   ├── kms/
│   ├── cloudtrail/
├── env/
│   ├── dev/
│   ├── prod/
├── Jenkinsfile
├── buildspec.yml
├── main.tf
├── variables.tf
└── outputs.tf
```

#### Terraform Configurations:

**S3 Module:**
```hcl
resource "aws_s3_bucket" "data" {
    bucket = "hipaa-compliant-data-bucket"
    acl    = "private"
    server_side_encryption_configuration {
        rule {
            apply_server_side_encryption_by_default {
                sse_algorithm = "aws:kms"
                kms_master_key_id = aws_kms_key.s3_key.arn
            }
        }
    }
    versioning {
        enabled = true
    }
}

resource "aws_kms_key" "s3_key" {
    description = "KMS key for S3 bucket encryption"
    policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "Enable IAM User Permissions",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
                },
                "Action": "kms:*",
                "Resource": "*"
            },
            {
                "Sid": "Allow CloudTrail to encrypt logs",
                "Effect": "Allow",
                "Principal": {
                    "Service": "cloudtrail.amazonaws.com"
                },
                "Action": "kms:GenerateDataKey*",
                "Resource": "*",
                "Condition": {
                    "StringLike": {
                        "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:${data.aws_region.current.name}:trail/*"
                    }
                }
            }
        ]
    }
    EOF
}
```

**CloudTrail Module:**
```hcl
resource "aws_cloudtrail" "main" {
    name = "main-trail"
    s3_bucket_name = aws_s3_bucket.data.bucket
    include_global_service_events = true
    is_multi_region_trail = true
    enable_logging = true

    event_selector {
        read_write_type           = "All"
        include_management_events = true

        data_resource {
            type = "AWS::S3::Object"
            values = ["arn:aws

:s3:::${aws_s3_bucket.data.bucket}/"]
        }
    }
}
```

These examples provide detailed steps to set up CI/CD pipelines with Terraform and AWS for different industry use cases, ensuring compliance, scalability, and security for each scenario.

### Real-World Example 1: Deploying a Scalable E-commerce Application

**Scenario:** An e-commerce company needs to deploy a scalable online store that handles high traffic during peak shopping seasons. The infrastructure includes VPC, public and private subnets, an internet gateway, NAT gateway, security groups, EC2 instances with Auto Scaling, RDS for database, S3 for static content, and CloudFront for content delivery.

#### Infrastructure Components
- VPC with public and private subnets
- EC2 instances with Auto Scaling
- RDS for MySQL database
- S3 for static content storage
- CloudFront for content delivery

#### Directory Structure
```plaintext
├── modules/
│   ├── vpc/
│   │   └── main.tf
│   ├── ec2/
│   │   └── main.tf
│   ├── autoscaling/
│   │   └── main.tf
│   ├── rds/
│   │   └── main.tf
│   ├── s3/
│   │   └── main.tf
│   ├── cloudfront/
│   │   └── main.tf
├── env/
│   ├── dev/
│   ├── prod/
├── Jenkinsfile
├── buildspec.yml
├── main.tf
├── variables.tf
└── outputs.tf
```

#### Terraform Configurations

**VPC Module (modules/vpc/main.tf):**
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

resource "aws_subnet" "private" {
  count             = 2
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, count.index + 2)
  vpc_id            = aws_vpc.main.id
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
  tags = {
    Name = "private-subnet-${count.index}"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id
  tags = {
    Name = "main-gateway"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "public-route-table"
  }
}

resource "aws_route_table_association" "public_assoc" {
  count          = 2
  subnet_id      = element(aws_subnet.public[*].id, count.index)
  route_table_id = aws_route_table.public.id
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = element(aws_subnet.public[*].id, 0)
  tags = {
    Name = "nat-gateway"
  }
}

resource "aws_eip" "nat" {
  vpc = true
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "private-route-table"
  }
}

resource "aws_route_table_association" "private_assoc" {
  count          = 2
  subnet_id      = element(aws_subnet.private[*].id, count.index)
  route_table_id = aws_route_table.private.id
}
```

**EC2 and Auto Scaling Module (modules/autoscaling/main.tf):**
```hcl
resource "aws_launch_configuration" "app" {
  image_id        = "ami-0c55b159cbfafe1f0"
  instance_type   = "t2.micro"
  security_groups = [aws_security_group.app.id]
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y httpd
              sudo systemctl start httpd
              sudo systemctl enable httpd
              echo "Welcome to the online store!" > /var/www/html/index.html
              EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app" {
  launch_configuration = aws_launch_configuration.app.id
  min_size             = 1
  max_size             = 3
  desired_capacity     = 2
  vpc_zone_identifier  = aws_subnet.public[*].id
  tags = [
    {
      key                 = "Name"
      value               = "app-instance"
      propagate_at_launch = true
    },
  ]

  lifecycle {
    create_before_destroy = true
  }
}
```

**RDS Module (modules/rds/main.tf):**
```hcl
resource "aws_db_instance" "default" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "admin"
  password             = "password"
  db_subnet_group_name = aws_db_subnet_group.default.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot  = true
}

resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name = "main"
  }
}

resource "aws_security_group" "rds" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-sg"
  }
}
```

**S3 Module (modules/s3/main.tf):**
```hcl
resource "aws_s3_bucket" "static_content" {
  bucket = "my-static-content-bucket"
  acl    = "public-read"

  static_website {
    index_document = "index.html"
    error_document = "error.html"
  }

  tags = {
    Name = "static-content-bucket"
  }
}
```

**CloudFront Module (modules/cloudfront/main.tf):**
```hcl
resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.static_content.bucket_regional_domain_name
    origin_id   = "s3-origin"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3-origin"
    viewer_protocol_policy = "redirect-to-https"
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "S3 static content distribution"
  default_root_object = "index.html"

  price_class = "PriceClass_All"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name = "s3-distribution"
  }
}
```

**Environment Configuration (env/dev/main.tf):**
```hcl
module "vpc" {
  source = "../../modules/vpc"
}

module "ec2" {
  source            = "../../modules/ec2"
  subnet_id         = module.vpc.public_subnet_ids[0]
  security_group_id = aws_security_group.web_sg.id
}

module "autoscaling" {
  source = "../../modules/autoscaling"
}

module "rds" {
  source = "../../modules/rds"
}

module "s3" {
  source = "../../modules/s3"
}

module "cloudfront" {
  source = "../../modules/cloudfront"
}
```

**Build Specification (buildspec.yml):**
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

**Pipeline Configuration (pipeline.tf):**
```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "my-codepipeline-bucket"
  acl    = "private"
}

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
    type = "CODEPIPELINE"
    buildspec = file("buildspec.yml")
  }
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

### Real-World Example 2: Deploying a HIPAA-Compliant Healthcare Application

**Scenario:** A healthcare provider needs to deploy an application that processes patient data, adhering to HIPAA compliance. The infrastructure must include strong encryption, access controls, and auditing.

#### Infrastructure Components
- VPC with public and private subnets
- EC2 instances in private subnets
- RDS for database management
- S3 for encrypted data storage
- CloudTrail for auditing
- KMS for encryption

#### Directory Structure
```plaintext
├── modules/
│   ├── vpc/
│   │   └── main.tf
│   ├── ec2/
│   │   └── main.tf
│   ├── rds/
│   │   └── main.tf
│   ├── s3/
│   │   └── main.tf
│   ├── kms/
│   │   └── main.tf
│   ├── cloudtrail/
│   │   └── main.tf
├── env/
│   ├── dev/
│   ├── prod/
├── Jenkinsfile
├── buildspec.yml
├── main.tf
├── variables.tf
└── outputs.tf
```

#### Terraform Configurations

**S3 Module (modules/s3/main.tf):**
```hcl
resource "aws_s3_bucket" "data" {
  bucket = "hipaa-compliant-data-bucket"
  acl    = "private"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "aws:kms"
        kms_master_key_id = aws_kms_key.s3_key.arn
      }
    }
  }
  versioning {
    enabled = true
  }
}

resource "aws_kms_key" "s3_key" {
  description = "KMS key for S3 bucket encryption"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Enable IAM User Permissions",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
      },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "Allow CloudTrail to encrypt logs",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudtrail.amazonaws.com"
      },
      "Action": "kms:GenerateDataKey*",
      "Resource": "*",
      "Condition": {
        "StringLike": {
          "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*:${data.aws_region.current.name}:trail/*"
        }
      }
    }
  ]
}
EOF
}
```

**CloudTrail Module (modules/cloudtrail/main.tf):**
```hcl
resource "aws_cloudtrail" "main" {
  name                          = "main-trail"
  s3_bucket_name                = aws_s3_bucket.data.bucket
  include_global_service_events = true
  is_multi_region_trail         = true
  enable_logging                = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true

    data_resource {
      type   = "AWS::S3::Object"
      values = [aws_s3_bucket.data.arn]
    }
  }
}
```

**Environment Configuration (env/dev/main.tf):**
```hcl
module "vpc" {
  source = "../../modules/vpc"
}

module "ec2" {
  source            = "../../modules/ec2"
  subnet_id         = module.vpc.private_subnet_ids[0]
  security_group_id = aws_security_group.web_sg.id
}

module "rds" {
  source = "../../modules/rds"
}

module "s3" {
  source = "../../modules/s3"
}

module "cloudtrail" {
  source = "../../modules/cloudtrail"
}
```

**Build Specification (buildspec.yml):**
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

**Pipeline Configuration (pipeline.tf):**
```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "codepipeline_bucket" {
  bucket = "my-codepipeline-bucket"
  acl    = "private"
}

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
    type = "CODEPIPELINE"
    buildspec = file("buildspec.yml")
  }
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

By following these detailed steps, you can set up AWS CodePipeline to automate the deployment of Terraform configurations for real-world applications. Each example demonstrates how to deploy a specific type of infrastructure, ensuring that your infrastructure as code is consistently and reliably deployed across your environments, leveraging the power of AWS CodePipeline, CodeBuild, and CodeDeploy.
