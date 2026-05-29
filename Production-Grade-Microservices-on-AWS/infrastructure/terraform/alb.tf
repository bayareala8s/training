resource "aws_lb" "main" {
  count              = local.enable_alb ? 1 : 0
  name               = substr("${local.name_prefix}-alb", 0, 32)
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb[0].id]
  subnets            = aws_subnet.public[*].id
  tags               = local.common_tags
}

resource "aws_lb_listener" "http" {
  count             = local.enable_alb ? 1 : 0
  load_balancer_arn = aws_lb.main[0].arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "BayAreaLa8s Microservices Course Platform"
      status_code  = "200"
    }
  }
}

resource "aws_lb_listener_rule" "services" {
  for_each = local.enable_alb ? local.services : {}

  listener_arn = aws_lb_listener.http[0].arn
  priority     = index(keys(local.services), each.key) + 10

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.services[each.key].arn
  }

  condition {
    path_pattern {
      values = each.value.path_patterns
    }
  }
}
