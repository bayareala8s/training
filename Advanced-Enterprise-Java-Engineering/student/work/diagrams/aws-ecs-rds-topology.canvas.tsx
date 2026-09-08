import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme,
} from "cursor/canvas";

function Topology() {
  const theme = useHostTheme();
  const W = 920;
  const H = 780;

  const box = (
    x: number,
    y: number,
    w: number,
    h: number,
    title: string,
    lines: string[],
    opts?: { accent?: boolean; dashed?: boolean },
  ) => {
    const accent = opts?.accent ?? false;
    return (
      <g>
        <rect
          x={x}
          y={y}
          width={w}
          height={h}
          rx={4}
          fill={accent ? theme.fill.tertiary : theme.bg.elevated}
          stroke={accent ? theme.accent.primary : theme.stroke.primary}
          strokeWidth={accent ? 2 : 1}
          strokeDasharray={opts?.dashed ? "5 4" : undefined}
        />
        <text
          x={x + 10}
          y={y + 18}
          fill={theme.text.primary}
          fontSize={12}
          fontWeight={600}
        >
          {title}
        </text>
        {lines.map((line, i) => (
          <text
            key={line}
            x={x + 10}
            y={y + 36 + i * 14}
            fill={theme.text.secondary}
            fontSize={10}
          >
            {line}
          </text>
        ))}
      </g>
    );
  };

  const arrow = (
    x1: number,
    y1: number,
    x2: number,
    y2: number,
    label: string,
    opts?: { dashed?: boolean },
  ) => (
    <g>
      <line
        x1={x1}
        y1={y1}
        x2={x2}
        y2={y2}
        stroke={theme.accent.primary}
        strokeWidth={1.75}
        strokeDasharray={opts?.dashed ? "5 4" : undefined}
        markerEnd="url(#arrow)"
      />
      {label ? (
        <text
          x={(x1 + x2) / 2 + 8}
          y={(y1 + y2) / 2 - 4}
          fill={theme.text.tertiary}
          fontSize={10}
        >
          {label}
        </text>
      ) : null}
    </g>
  );

  return (
    <svg
      width="100%"
      viewBox={`0 0 ${W} ${H}`}
      role="img"
      aria-label="Live BayPay ECS Fargate and RDS network topology in us-west-2 VPC 10.20.0.0/16"
    >
      <defs>
        <marker
          id="arrow"
          viewBox="0 0 10 10"
          refX={9}
          refY={5}
          markerWidth={7}
          markerHeight={7}
          orient="auto-start-reverse"
        >
          <path d="M 0 0 L 10 5 L 0 10 z" fill={theme.accent.primary} />
        </marker>
      </defs>

      {box(340, 8, 240, 52, "Internet / Harbor Market", [
        "Browser + Swagger on :80",
      ])}

      {arrow(460, 60, 460, 78, "")}
      {box(330, 80, 260, 56, "Internet Gateway", [
        "igw-087bb94969282a387",
        "Public RT: 0.0.0.0/0 → this IGW",
      ])}

      <rect
        x={16}
        y={156}
        width={888}
        height={608}
        rx={6}
        fill={theme.bg.editor}
        stroke={theme.stroke.secondary}
      />
      <text x={32} y={178} fill={theme.text.primary} fontSize={13} fontWeight={600}>
        VPC vpc-0a4ebd4109b54f11b · 10.20.0.0/16 · us-west-2
      </text>
      <text x={32} y={196} fill={theme.text.tertiary} fontSize={10}>
        DNS on · no NAT gateway · local route covers all subnets
      </text>

      <text x={200} y={228} fill={theme.text.secondary} fontSize={11} fontWeight={600}>
        us-west-2a
      </text>
      <text x={620} y={228} fill={theme.text.secondary} fontSize={11} fontWeight={600}>
        us-west-2b
      </text>

      <rect
        x={32}
        y={240}
        width={400}
        height={250}
        rx={4}
        fill={theme.fill.quaternary}
        stroke={theme.stroke.tertiary}
      />
      <rect
        x={488}
        y={240}
        width={400}
        height={250}
        rx={4}
        fill={theme.fill.quaternary}
        stroke={theme.stroke.tertiary}
      />
      <text x={48} y={260} fill={theme.text.secondary} fontSize={11} fontWeight={600}>
        Public · 10.20.1.0/24 · subnet-0d9eace5625afbf23
      </text>
      <text x={504} y={260} fill={theme.text.secondary} fontSize={11} fontWeight={600}>
        Public · 10.20.2.0/24 · subnet-0a29b8527a72430ab
      </text>

      {box(56, 276, 352, 72, "ALB ENI (2a)", [
        "baypay-ecsrd-alb · internet-facing",
        "Listener :80 → TG :8080 / liveness",
      ])}
      {box(512, 276, 352, 72, "ALB ENI (2b)", [
        "Same ALB, second AZ",
        "DNS baypay-ecsrd-alb-368413128…elb.amazonaws.com",
      ], { accent: true })}

      {box(512, 364, 352, 110, "Fargate task (running here)", [
        "10.20.2.233 · eni-07d570efb5ea815a3",
        "payment-service · profile ecs · 256 / 512",
        "Public IP on · pulls ECR via IGW :443",
        "Health: /actuator/health/liveness :8080",
      ], { accent: true })}

      <text
        x={232}
        y={400}
        textAnchor="middle"
        fill={theme.text.tertiary}
        fontSize={10}
      >
        No task in 2a right now
      </text>

      <rect
        x={32}
        y={508}
        width={400}
        height={236}
        rx={4}
        fill={theme.bg.elevated}
        stroke={theme.stroke.tertiary}
      />
      <rect
        x={488}
        y={508}
        width={400}
        height={236}
        rx={4}
        fill={theme.bg.elevated}
        stroke={theme.stroke.tertiary}
      />
      <text x={48} y={528} fill={theme.text.secondary} fontSize={11} fontWeight={600}>
        Private · 10.20.11.0/24 · subnet-063add17eccbbcdf4
      </text>
      <text x={504} y={528} fill={theme.text.secondary} fontSize={11} fontWeight={600}>
        Private · 10.20.12.0/24 · subnet-0b86d8eb6bd44f219
      </text>

      {box(56, 544, 352, 124, "RDS PostgreSQL 16 (primary)", [
        "baypay-ecsrd-pg · db.t3.micro",
        "Single-AZ in us-west-2a",
        "Not publicly accessible",
        "baypay-ecsrd-pg.c7myxlzkr5l7…:5432",
      ], { accent: true })}

      {box(512, 544, 352, 88, "RDS subnet group member", [
        "No instance in 2b (not Multi-AZ)",
        "Required second AZ for the subnet group",
      ], { dashed: true })}

      {arrow(460, 136, 460, 156, ":80")}
      {arrow(688, 348, 688, 364, ":8080 SG")}
      {arrow(688, 474, 232, 544, "JDBC :5432 · VPC local")}
      {arrow(860, 364, 860, 136, "ECR / logs / secrets :443", { dashed: true })}
    </svg>
  );
}

export default function AwsEcsRdsTopology() {
  const theme = useHostTheme();

  return (
    <Stack gap={24} style={{ padding: 24 }}>
      <Stack gap={8}>
        <H1>Live AWS network topology</H1>
        <Text tone="secondary">
          Account 277374794397 · us-west-2 · lab prefix baypay-ecsrd. Read
          left-to-right, then down the AZs. This is the running stack, not the
          required AEJE student apply.
        </Text>
        <Row gap={8} wrap>
          <Pill active>us-west-2</Pill>
          <Pill>VPC 10.20.0.0/16</Pill>
          <Pill>no NAT</Pill>
          <Pill>no Multi-AZ</Pill>
          <Pill>Fargate public IP</Pill>
          <Pill>RDS private :5432</Pill>
        </Row>
      </Stack>

      <Callout tone="info" title="How packets move">
        Clients hit the internet-facing ALB on :80. The ALB forwards to the
        Fargate ENI on :8080 in a public subnet. The task reaches RDS on :5432
        over the VPC local route — RDS has no IGW path. The task uses the IGW
        on :443 for ECR, CloudWatch Logs, and Secrets Manager. There is no NAT
        Gateway.
      </Callout>

      <Grid columns={4} gap={16}>
        <Stat value="10.20.2.233" label="Task private IP (2b)" />
        <Stat value="us-west-2a" label="RDS primary AZ" />
        <Stat value="1" label="Healthy ALB target" tone="success" />
        <Stat value="0" label="NAT / EKS / Multi-AZ" />
      </Grid>

      <Card>
        <CardHeader>AZ × subnet topology (live)</CardHeader>
        <CardBody style={{ padding: 8 }}>
          <Topology />
          <Text tone="tertiary" size="small">
            Source: AWS EC2 / ELBv2 / ECS / RDS describe · 2026-09-08 ·
            vpc-0a4ebd4109b54f11b
          </Text>
        </CardBody>
      </Card>

      <H2>Route tables</H2>
      <Table
        headers={["Table", "Destination", "Target", "Used by"]}
        rows={[
          [
            "Public RT rtb-0adae05470afa69ac",
            "10.20.0.0/16",
            "local",
            "Both public subnets + intra-VPC to RDS",
          ],
          [
            "Public RT",
            "0.0.0.0/0",
            "igw-087bb94969282a387",
            "ALB + Fargate public IP (ECR :443)",
          ],
          [
            "Private (implicit VPC main)",
            "10.20.0.0/16",
            "local only",
            "RDS subnets — no 0.0.0.0/0, no NAT",
          ],
        ]}
        striped
      />

      <H2>Security groups</H2>
      <Table
        headers={["Group", "Ingress", "Egress"]}
        rows={[
          [
            "baypay-ecsrd-alb",
            "tcp/80 from 0.0.0.0/0",
            "all (to tasks :8080)",
          ],
          [
            "baypay-ecsrd-tasks",
            "tcp/8080 from ALB SG",
            "tcp/443 0.0.0.0/0 · udp/53 VPC · tcp/5432 RDS SG",
          ],
          [
            "baypay-ecsrd-rds",
            "tcp/5432 from task SG only",
            "none required",
          ],
        ]}
        striped
      />

      <Divider />

      <H2>Control plane (outside the VPC path)</H2>
      <Text tone="secondary" style={{ color: theme.text.secondary }}>
        Not drawn as extra boxes on the AZ grid. The task still reaches them
        with the public IP through the IGW.
      </Text>
      <Table
        headers={["Service", "Role in this stack"]}
        rows={[
          [
            "ECR baypay/payment-service-ecs-demo",
            "Immutable image tag. Fargate pulls linux/amd64.",
          ],
          [
            "Secrets Manager baypay-ecsrd/db",
            "JSON url / username / password → BAYPAY_DB_*",
          ],
          [
            "CloudWatch /ecs/baypay-ecsrd/payment-service",
            "3-day retention. Container Insights off.",
          ],
          [
            "IAM execution role",
            "ECR + logs + GetSecretValue. Task role has no JDBC rights.",
          ],
        ]}
      />
    </Stack>
  );
}
