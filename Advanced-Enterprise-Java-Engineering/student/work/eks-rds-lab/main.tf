# Reuses the optional ECS lab VPC + single-AZ RDS. Does not create NAT, a second
# database, or Multi-AZ. Destroy this stack before ../ecs-rds-lab/stop.sh.

data "terraform_remote_state" "ecs" {
  backend = "local"

  config = {
    path = "${path.module}/../ecs-rds-lab/terraform.tfstate"
  }
}

locals {
  vpc_id                = data.terraform_remote_state.ecs.outputs.vpc_id
  public_subnet_ids     = data.terraform_remote_state.ecs.outputs.public_subnet_ids
  rds_security_group_id = data.terraform_remote_state.ecs.outputs.rds_security_group_id
}

data "aws_iam_policy_document" "eks_cluster_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "cluster" {
  name               = "${var.name_prefix}-cluster"
  assume_role_policy = data.aws_iam_policy_document.eks_cluster_assume.json
}

resource "aws_iam_role_policy_attachment" "cluster" {
  role       = aws_iam_role.cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

data "aws_iam_policy_document" "eks_node_assume" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "node" {
  name               = "${var.name_prefix}-node"
  assume_role_policy = data.aws_iam_policy_document.eks_node_assume.json
}

resource "aws_iam_role_policy_attachment" "node_worker" {
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "node_cni" {
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "node_ecr" {
  role       = aws_iam_role.node.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_eks_cluster" "lab" {
  name     = "${var.name_prefix}-cluster"
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version

  access_config {
    authentication_mode                         = "API"
    bootstrap_cluster_creator_admin_permissions = true
  }

  vpc_config {
    subnet_ids              = local.public_subnet_ids
    endpoint_public_access  = true
    endpoint_private_access = false
  }

  depends_on = [aws_iam_role_policy_attachment.cluster]
}

resource "aws_eks_node_group" "lab" {
  cluster_name    = aws_eks_cluster.lab.name
  node_group_name = "${var.name_prefix}-ng"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = local.public_subnet_ids
  instance_types  = [var.node_instance_type]
  ami_type        = "AL2023_x86_64_STANDARD"
  capacity_type   = "ON_DEMAND"

  scaling_config {
    desired_size = 1
    max_size     = 1
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.node_worker,
    aws_iam_role_policy_attachment.node_cni,
    aws_iam_role_policy_attachment.node_ecr,
  ]
}

# Pods use the cluster SG on the node ENI. Same RDS as ECS — one extra ingress.
resource "aws_security_group_rule" "rds_from_eks" {
  type                     = "ingress"
  description              = "Postgres from EKS cluster security group"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = local.rds_security_group_id
  source_security_group_id = aws_eks_cluster.lab.vpc_config[0].cluster_security_group_id
}
