provider "aws" {
  region = "us-west-2" # replace with your preferred AWS region
}

data "aws_vpc" "default" {
  default = true
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "17.1.0"

  cluster_name    = "ecom-app-dev-eks-cluster"
  cluster_version = "1.29"
  subnets         = ["subnet-ebc914a1", "subnet-338fb418", "subnet-4e3fbc13", "subnet-a343f3db"] # replace with your subnet IDs
  vpc_id          = data.aws_vpc.default.id

  node_groups = {
    eks_nodes = {
      desired_capacity = 3
      max_capacity     = 3
      min_capacity     = 1

      instance_type = "t3.medium"
      key_name      = "my-key" # replace with your key name
    }
  }
}