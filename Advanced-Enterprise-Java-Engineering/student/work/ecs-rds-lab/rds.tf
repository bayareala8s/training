resource "random_password" "db" {
  length  = 24
  special = false
}

resource "aws_db_subnet_group" "baypay" {
  name       = "${var.name_prefix}-db"
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_db_instance" "baypay" {
  identifier                 = "${var.name_prefix}-pg"
  engine                     = "postgres"
  engine_version             = "16"
  instance_class             = var.db_instance_class
  allocated_storage          = 20
  storage_type               = "gp3"
  storage_encrypted          = true
  db_name                    = "baypay"
  username                   = "baypay"
  password                   = random_password.db.result
  db_subnet_group_name       = aws_db_subnet_group.baypay.name
  vpc_security_group_ids     = [aws_security_group.rds.id]
  multi_az                   = false
  publicly_accessible        = false
  backup_retention_period    = 0
  deletion_protection        = false
  skip_final_snapshot        = true
  apply_immediately          = true
  auto_minor_version_upgrade = true
}

resource "aws_secretsmanager_secret" "db" {
  name                    = "${var.name_prefix}/db"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    url      = "jdbc:postgresql://${aws_db_instance.baypay.address}:5432/${aws_db_instance.baypay.db_name}"
    username = aws_db_instance.baypay.username
    password = random_password.db.result
  })
}
