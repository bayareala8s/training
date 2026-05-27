resource "aws_kms_key" "this" {
  description             = "${var.name_prefix} lab CMK"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  tags                    = var.tags
}

resource "aws_kms_alias" "this" {
  name          = "alias/${var.name_prefix}"
  target_key_id = aws_kms_key.this.key_id
}

variable "name_prefix" { type = string }
variable "tags" {
  type    = map(string)
  default = {}
}

output "key_arn" { value = aws_kms_key.this.arn }
output "key_id" { value = aws_kms_key.this.key_id }
