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
    { id: "ing" },
    { id: "svc" },
    { id: "pod" },
    { id: "jvm" },
    { id: "rds" },
  ],
  edges: [
    { from: "avery", to: "ing" },
    { from: "ing", to: "svc" },
    { from: "svc", to: "pod" },
    { from: "pod", to: "jvm" },
    { from: "jvm", to: "rds" },
  ],
});

const LABELS: Record<string, { title: string; sub: string }> = {
  avery: { title: "Harbor Market", sub: "POST /api/v1/payments" },
  ing: { title: "Ingress", sub: "payments.apps.baypay" },
  svc: { title: "Service", sub: "ClusterIP :8080" },
  pod: { title: "Pod", sub: "app=payment-service" },
  jvm: { title: "Spring Boot JAR", sub: "same OCI image as ECS" },
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
      aria-label="Merchant request path from Harbor Market through Ingress and a Pod to RDS PostgreSQL"
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
        const accent = n.id === "jvm" || n.id === "pod" || n.id === "rds";
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
        x={byId.ing.x + 76}
        y={SERVING.height + 18}
        textAnchor="middle"
        fill={theme.text.tertiary}
        fontSize={10}
      >
        kube API / LBC
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

export default function EksDeploymentDiagram() {
  return (
    <Stack gap={24} style={{ padding: 24 }}>
      <Stack gap={8}>
        <H1>BayPay on EKS</H1>
        <Text tone="secondary">
          Same OCI image as ECS: eclipse-temurin:21-jre + Spring Boot fat JAR,
          USER 10001, EXPOSE 8080. Same RDS PostgreSQL data plane
          (application-prod.yml). CLUSTER.md names. EKS is a valid design home
          — this course does not apply an EKS control plane.
        </Text>
        <Row gap={8} wrap>
          <Pill active>us-west-2</Pill>
          <Pill>namespace baypay-prod</Pill>
          <Pill>Deployment payment-service</Pill>
          <Pill>replicas 3</Pill>
          <Pill>ClusterIP :8080</Pill>
          <Pill>RDS Postgres :5432</Pill>
        </Row>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="same image" label="baypay/payment-service:<tag>" />
        <Stat value="8080" label="containerPort / Service" />
        <Stat value="3" label="replicas when healthy" />
        <Stat value="~$2.40" label="EKS control plane per day if applied" tone="warning" />
      </Grid>

      <Card>
        <CardHeader trailing="Same JAR as Fargate. Different objects.">
          Serving path + data plane
        </CardHeader>
        <CardBody>
          <ServingPath />
          <Text tone="tertiary" size="small">
            Source: CLUSTER.md · ACCOUNT.md · application-prod.yml. Ingress host
            payments.apps.baypay.example. OpenShift Route payment-route is the
            same job on a different API.
          </Text>
        </CardBody>
      </Card>

      <Callout tone="info" title="You do not build a second image for EKS">
        docker build once. Push one immutable tag to ECR. ECS task definition
        and the Kubernetes Pod spec both set image to that URI. The Dockerfile
        does not mention ECS or EKS.
      </Callout>

      <H2>Full deploy stack</H2>
      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader>1. Catalog — same ECR image</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                registry…/baypay/payment-service:&lt;immutable-tag&gt;. Never
                :latest. Multi-stage: JDK builds the JAR; runtime JRE copies
                one JAR; java -jar /app/app.jar.
              </Text>
              <Text tone="secondary">
                Node / Fargate profile pulls via the node instance role or
                pod IRSA — not a second Dockerfile. Scan-on-push still on.
              </Text>
            </Stack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>2. Workload — Deployment + Service</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                Namespace / Project baypay-prod. Deployment payment-service,
                labels app=payment-service, 3 replicas when healthy.
              </Text>
              <Text tone="secondary">
                Service ClusterIP 8080, selector app=payment-service. Empty
                Endpoints = empty target group (same class of failure as
                INCIDENT-1104 / 1006).
              </Text>
              <Text tone="secondary">
                securityContext: runAsNonRoot, runAsUser 10001. Heap must not
                equal the container memory limit.
              </Text>
            </Stack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>3. Edge — Ingress (or Route)</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                Ingress host payments.apps.baypay.example, TLS Secret
                payment-tls. Often an AWS Load Balancer Controller → ALB.
              </Text>
              <Text weight="semibold">
                kubelet probes: GET /actuator/health/liveness and
                /actuator/health/readiness on 8080. Ingress is not the probe.
              </Text>
              <Text tone="secondary">
                Running + Ready False is the kube cousin of ECS RUNNING +
                unhealthy TG. Do not bounce dmgr-east.
              </Text>
            </Stack>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>4. Config — ConfigMap + Secret</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                ConfigMap payment-config: non-secret env (profile, log level,
                JAVA_TOOL_OPTIONS). Secret baypay-db: BAYPAY_DB_USER,
                BAYPAY_DB_PASSWORD (and URL).
              </Text>
              <Text tone="secondary">
                envFrom those objects. Missing BAYPAY_DB_URL is CrashLoop
                (INCIDENT-1001 class). Never bake credentials in the image.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <Card>
        <CardHeader>5. Data — RDS PostgreSQL (same as ECS picture)</CardHeader>
        <CardBody>
          <Grid columns={2} gap={16}>
            <Stack gap={8}>
              <Text>
                Engine PostgreSQL, database baypay, port 5432. Profile prod.
                Hikari jdbc/baypay. One ACID transaction for payment + ledger +
                Idempotency-Key.
              </Text>
              <Text tone="secondary">
                Pods reach RDS on 5432 inside the VPC (pod SG or node SG →
                RDS SG). No 5432 on 0.0.0.0/0. PubliclyAccessible = false.
              </Text>
            </Stack>
            <Stack gap={8}>
              <Text>
                JDBC user/password come from Secret baypay-db, not from IRSA.
                IRSA is for AWS APIs. This app talks SQL.
              </Text>
              <Text tone="secondary">
                Multi-AZ is design, not a student apply. Intra-VPC 5432 does
                not require a NAT Gateway. Do not apply EKS to “get RDS.”
              </Text>
            </Stack>
          </Grid>
        </CardBody>
      </Card>

      <Card>
        <CardHeader>6. Identity — IRSA vs task role</CardHeader>
        <CardBody>
          <Table
            headers={["Principal", "Who it is", "May do", "Must not"]}
            rows={[
              [
                "Node / Fargate profile",
                "Pulls the image, writes some logs",
                "ECR pull for the cluster",
                "Hold BAYPAY_DB_PASSWORD",
              ],
              [
                "Service account + IRSA",
                "What the JVM becomes if it calls AWS",
                "Narrow AWS APIs only if you add them",
                "AdministratorAccess. rds:CreateDBInstance",
              ],
              [
                "Secret baypay-db",
                "Injected env for JDBC",
                "URL / user / password at runtime",
                "Live in Dockerfile ENV or git",
              ],
            ]}
            rowTone={["info", "neutral", "warning"]}
          />
        </CardBody>
      </Card>

      <Grid columns="1.2fr 0.8fr" gap={16}>
        <Stack gap={12}>
          <H2>ECS object → EKS object</H2>
          <Table
            headers={["ECS / Fargate", "EKS", "Same contract"]}
            rows={[
              ["Task definition + service", "Deployment + Service", "image, 8080, desired count / replicas"],
              ["ALB target group health", "kubelet liveness / readiness", "/actuator/health/liveness"],
              ["ALB DNS", "Ingress (or Route payment-route)", "TLS edge"],
              ["Execution role valueFrom", "Secret + envFrom", "BAYPAY_DB_*"],
              ["Task role (empty for JDBC)", "IRSA SA (empty for JDBC)", "No GetSecretValue required"],
              ["Fargate 256/512", "resources requests/limits", "heap ≠ memory limit"],
              ["desired_count = 1 (lab)", "replicas: 3 when healthy", "CLUSTER.md vs lab cheap"],
            ]}
          />
        </Stack>
        <Stack gap={12}>
          <H3>Prove (paper)</H3>
          <Card>
            <CardBody>
              <Stack gap={8}>
                <Text>1. Pods Ready 3/3. Endpoints not empty.</Text>
                <Text>2. Probes 200 on liveness and readiness.</Text>
                <Text>3. POST Avery + Idempotency-Key → 201.</Text>
                <Text>4. Replay 200 after a pod replace (RDS).</Text>
                <Text>5. Frozen …222 → 422.</Text>
              </Stack>
            </CardBody>
          </Card>
          <Callout tone="warning" title="Do not apply EKS for this course">
            Control plane ~$0.10/h (~$2.40/day) before nodes. Valid home if
            you already run Kubernetes. Not a student apply. Do not apply NAT
            or RDS Multi-AZ to make the picture look production.
          </Callout>
        </Stack>
      </Grid>

      <Divider />
      <Text tone="tertiary" size="small">
        Fictional BayPay. CLUSTER.md · AEJE-D-072. Design picture — same image
        as the ECS canvas. No live cluster.
      </Text>
    </Stack>
  );
}
