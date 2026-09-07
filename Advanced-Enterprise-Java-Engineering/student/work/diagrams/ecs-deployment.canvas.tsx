import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  computeDAGLayout,
  useHostTheme,
} from "cursor/canvas";

const SERVING = computeDAGLayout({
  direction: "horizontal",
  nodeWidth: 152,
  nodeHeight: 64,
  rankGap: 40,
  nodeGap: 24,
  padding: 16,
  nodes: [
    { id: "avery" },
    { id: "alb" },
    { id: "tg" },
    { id: "task" },
    { id: "jvm" },
    { id: "rds" },
  ],
  edges: [
    { from: "avery", to: "alb" },
    { from: "alb", to: "tg" },
    { from: "tg", to: "task" },
    { from: "task", to: "jvm" },
    { from: "jvm", to: "rds" },
  ],
});

const LABELS: Record<string, { title: string; sub: string }> = {
  avery: { title: "Harbor Market", sub: "POST /api/v1/payments" },
  alb: { title: "ALB", sub: "listener :80 → TG" },
  tg: { title: "Target group", sub: ":8080 liveness 200" },
  task: { title: "Fargate task", sub: "256 CPU / 512 MiB" },
  jvm: { title: "Spring Boot JAR", sub: "profile prod · Hikari" },
  rds: { title: "RDS Postgres", sub: "baypay :5432" },
};

function ServingPath() {
  const theme = useHostTheme();
  const byId = Object.fromEntries(SERVING.nodes.map((n) => [n.id, n]));

  return (
    <svg
      width="100%"
      viewBox={`0 0 ${SERVING.width} ${SERVING.height + 28}`}
      role="img"
      aria-label="Merchant request path from Harbor Market through ALB and Fargate to RDS PostgreSQL"
    >
      {SERVING.edges.map((e) => (
        <line
          key={`${e.from}-${e.to}`}
          x1={e.sourceX}
          y1={e.sourceY}
          x2={e.targetX}
          y2={e.targetY}
          stroke={theme.accent.primary}
          strokeWidth={2}
        />
      ))}
      {SERVING.nodes.map((n) => {
        const label = LABELS[n.id];
        const accent = n.id === "jvm" || n.id === "tg" || n.id === "rds";
        return (
          <g key={n.id}>
            <rect
              x={n.x}
              y={n.y}
              width={152}
              height={64}
              rx={4}
              fill={accent ? theme.fill.tertiary : theme.bg.elevated}
              stroke={accent ? theme.accent.primary : theme.stroke.primary}
              strokeWidth={accent ? 2 : 1}
            />
            <text
              x={n.x + 76}
              y={n.y + 26}
              textAnchor="middle"
              fill={theme.text.primary}
              fontSize={12}
              fontWeight={600}
            >
              {label.title}
            </text>
            <text
              x={n.x + 76}
              y={n.y + 44}
              textAnchor="middle"
              fill={theme.text.secondary}
              fontSize={10}
            >
              {label.sub}
            </text>
          </g>
        );
      })}
      <text
        x={byId.alb.x + 76}
        y={SERVING.height + 18}
        textAnchor="middle"
        fill={theme.text.tertiary}
        fontSize={10}
      >
        public + IGW
      </text>
      <text
        x={byId.rds.x + 76}
        y={SERVING.height + 18}
        textAnchor="middle"
        fill={theme.text.tertiary}
        fontSize={10}
      >
        private :5432
      </text>
    </svg>
  );
}

export default function EcsDeploymentDiagram() {
  return (
    <Stack gap={24} style={{ padding: 24 }}>
      <Stack gap={8}>
        <H1>BayPay on ECS / Fargate</H1>
        <Text tone="secondary">
          Target data plane: Amazon RDS for PostgreSQL (same contract as
          application-prod.yml and db-east). Region us-west-2. The OCI image is
          still the Spring Boot fat JAR. AEJE student apply does not create RDS
          — this picture is the design you would run if you leave H2.
        </Text>
        <Row gap={8} wrap>
          <Pill active>us-west-2</Pill>
          <Pill>port 8080</Pill>
          <Pill>/actuator/health/liveness</Pill>
          <Pill>RDS Postgres :5432</Pill>
          <Pill>SPRING_PROFILES_ACTIVE=prod</Pill>
          <Pill>256 / 512</Pill>
        </Row>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="8080" label="containerPort" />
        <Stat value="5432" label="RDS Postgres port" />
        <Stat value="prod" label="Spring profile (not local/H2)" />
        <Stat value="99.9%" label="Ops SLO (not this diagram)" tone="info" />
      </Grid>

      <Card>
        <CardHeader trailing="Avery → ALB → JAR → RDS. Not dmgr-east.">
          Serving path + data plane
        </CardHeader>
        <CardBody>
          <ServingPath />
          <Text tone="tertiary" size="small">
            Source: ACCOUNT.md · application-prod.yml · BUILD-1101. ALB teaching
            host pay-alb-student.baypay.example. JDBC
            jdbc:postgresql://…:5432/baypay via BAYPAY_DB_*.
          </Text>
        </CardBody>
      </Card>

      <H2>Full deploy stack</H2>
      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader>1. Catalog — ECR</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                Repository <Text weight="semibold">baypay/payment-service</Text>.
                Tag is immutable (git SHA or 3.9.2), never :latest.
              </Text>
              <Text tone="secondary">
                Multi-stage image: JDK builds the fat JAR; runtime is
                eclipse-temurin:21-jre, USER 10001, EXPOSE 8080, java -jar
                /app/app.jar. No BAYPAY_DB_* in ENV.
              </Text>
              <Text tone="secondary">
                Execution role pulls this image. Scan-on-push on. Jordan Voss
                owns the tag.
              </Text>
            </Stack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>2. Network — public + IGW</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                VPC, Internet Gateway, two public subnets (two AZs) so the ALB
                can spread. Route 0.0.0.0/0 → IGW.
              </Text>
              <Text tone="secondary">
                Task: assign_public_ip = true so ECR and CloudWatch work without
                a NAT Gateway. ALB SG allows 80 in; task SG allows 8080 from the
                ALB only. Task SG egress: 443 (ECR/logs) and 5432 to the RDS SG.
              </Text>
              <Text tone="secondary">
                RDS lives in private subnets in the same VPC. Intra-VPC 5432
                does not need NAT. Do not put Postgres on a public subnet and
                do not open 5432 to 0.0.0.0/0.
              </Text>
            </Stack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>3. Edge — ALB + target group</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                Internet-facing ALB on both public subnets. Listener :80 forwards
                to an IP target group on port 8080.
              </Text>
              <Text weight="semibold">
                Health: GET /actuator/health/liveness · port 8080 · matcher 200.
              </Text>
              <Text tone="secondary">
                Path / 404s (Spring). Task RUNNING + TG unhealthy = merchant
                502/503 (INCIDENT-1104). Riley owns the path. Sam owns the ALB.
              </Text>
            </Stack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>4. Compute — Fargate task</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                Cluster (Container Insights off). Task definition: Fargate,
                awsvpc, cpu 256, memory 512. Service desired_count = 1.
              </Text>
              <Text tone="secondary">
                Container name payment, containerPort 8080,
                SPRING_PROFILES_ACTIVE=prod (PostgreSQLDialect, Hikari
                jdbc/baypay). Logs to /ecs/…/payment-service, 3–7 day retention.
                H2 stays on profile local / test only.
              </Text>
              <Text tone="secondary">
                Never -Xmx equal to 512 MiB. UseContainerSupport +
                MaxRAMPercentage if you set JVM flags.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <Card>
        <CardHeader>6. Data — RDS PostgreSQL</CardHeader>
        <CardBody>
          <Grid columns={2} gap={16}>
            <Stack gap={8}>
              <Text>
                Engine: PostgreSQL. Database name <Text weight="semibold">baypay</Text>.
                Port <Text weight="semibold">5432</Text>. Matches
                application-prod.yml (PostgreSQLDialect) and teaching host
                db-east.baypay.example.
              </Text>
              <Text tone="secondary">
                JDBC URL, user, and password come from Secrets Manager
                baypay/payment/db as BAYPAY_DB_URL / USER / PASSWORD
                (valueFrom JSON keys). Never ENV in the image. Never changeme
                in git.
              </Text>
              <Text tone="secondary">
                One ACID transaction still covers payment + ledger +
                Idempotency-Key. Hikari pool jdbc/baypay — do not share it
                with nightly reporting.
              </Text>
            </Stack>
            <Stack gap={8}>
              <Text weight="semibold">Placement</Text>
              <Text tone="secondary">
                Private subnets, two AZs for the ALB story. RDS security group
                allows 5432 from the task SG only. PubliclyAccessible = false.
              </Text>
              <Text weight="semibold">What this course still refuses to apply</Text>
              <Text tone="secondary">
                Creating RDS or RDS Multi-AZ on a same-day lab invoice.
                Multi-AZ is a design sentence (failover, not a cell bounce).
                Student default remains H2 local. Destroy the instance the same
                day if you ever create one — it bills while stopped storage
                remains.
              </Text>
            </Stack>
          </Grid>
        </CardBody>
      </Card>

      <Card>
        <CardHeader>5. Trust — two IAM roles</CardHeader>
        <CardBody>
          <Table
            headers={["Principal", "Who it is", "May do", "Must not"]}
            rows={[
              [
                "Execution role",
                "Agent that starts the container",
                "ECR pull, logs, GetSecretValue on baypay/payment/db, kms:Decrypt on one CMK",
                "AdministratorAccess. rds:* . Combined with the task role",
              ],
              [
                "Task role",
                "What the JVM becomes",
                "Still no AWS API. JDBC uses injected env (user/password), not the IAM role",
                "GetSecretValue. rds:CreateDBInstance. Console admin policy",
              ],
              [
                "Sandbox user",
                "You in the console",
                "Apply / destroy in us-west-2",
                "Copy that admin policy onto either role",
              ],
            ]}
            rowTone={["info", "neutral", "warning"]}
          />
          <Text tone="tertiary" size="small">
            BUILD-1101 leaves secrets out. SECURITY-1103 / CAPSTONE-3 paper is
            valueFrom JSON keys :url:: / :username:: / :password:: — never
            changeme in git.
          </Text>
        </CardBody>
      </Card>

      <Grid columns="1.2fr 0.8fr" gap={16}>
        <Stack gap={12}>
          <H2>What is on the diagram vs not</H2>
          <Table
            headers={["Object", "On student apply?", "Why"]}
            rows={[
              ["ECR + immutable tag", "Yes (cheap) or paper", "Bits the task runs"],
              ["ECS cluster + Fargate service", "Optional apply", "Default compute"],
              ["ALB + TG + listener", "Optional apply", "Merchant path; destroy same day"],
              ["VPC + IGW + 2 public subnets", "Optional apply", "ALB spread + pull without NAT"],
              ["Execution + task roles", "Paper / apply", "Least privilege"],
              ["Secrets Manager + KMS", "Required if RDS", "BAYPAY_DB_* for prod"],
              ["RDS PostgreSQL (this picture)", "Design only", "application-prod.yml; not student apply"],
              ["RDS Multi-AZ", "No apply", "Literacy — not this invoice"],
              ["NAT Gateway", "No", "VPC 5432 does not need NAT"],
              ["EKS / ROSA", "No apply", "Valid design home only"],
              ["H2 / profile local", "Laptop + teaching Fargate", "Dies when the task dies"],
              ["dmgr-east / BayPayCell", "Absent", "AEJE-D-071 leftover ND"],
            ]}
            rowTone={[
              "success",
              "success",
              "success",
              "success",
              "info",
              "info",
              "info",
              "danger",
              "danger",
              "danger",
              "neutral",
              "neutral",
            ]}
          />
        </Stack>

        <Stack gap={12}>
          <H3>Prove after apply</H3>
          <Card>
            <CardBody>
              <Stack gap={8}>
                <Text>1. Task RUNNING is not enough.</Text>
                <Text>2. Target healthy on liveness 200.</Text>
                <Text>
                  3. POST Avery 11111111-…1111 + Idempotency-Key → 201 COMPLETED.
                </Text>
                <Text>4. Same key replay → 200 same paymentId.</Text>
                <Text>5. Frozen …222 → 422. Missing key → 400.</Text>
                <Text>
                  6. Replay survives a task replace (row is on RDS, not H2).
                </Text>
              </Stack>
            </CardBody>
          </Card>
          <Callout tone="warning" title="ALB and RDS both bill">
            desired_count = 0 does not stop the ALB. Stopping RDS does not
            erase storage cost. Expiration tags do not destroy. AEJE still
            does not apply RDS or Multi-AZ on a same-day lab. If you create
            either, destroy in us-west-2 the same day.
          </Callout>
        </Stack>
      </Grid>

      <Divider />
      <Text tone="tertiary" size="small">
        Fictional BayPay. AEJE-D-072 / AEJE-D-048 plus application-prod.yml RDS
        Postgres. Design picture — not a live apply.
      </Text>
    </Stack>
  );
}
