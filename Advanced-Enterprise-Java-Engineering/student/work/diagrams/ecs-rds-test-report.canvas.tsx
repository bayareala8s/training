import {
  BarChart,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme,
} from "cursor/canvas";

const CHECKED_AT = "2026-09-08 02:25 UTC";
const ALB = "http://baypay-ecsrd-alb-368413128.us-west-2.elb.amazonaws.com";

const infra = [
  ["ECS service", "ACTIVE · desired 1 · running 1 · rollout COMPLETED", "pass"],
  ["ALB target", "10.20.2.233:8080 us-west-2b · healthy", "pass"],
  ["RDS baypay-ecsrd-pg", "available · postgres · db.t3.micro · Multi-AZ off · private", "pass"],
  ["ECS cluster", "ACTIVE · 1 running Fargate task", "pass"],
  ["GET /actuator/health/liveness", "200 {\"status\":\"UP\"}", "pass"],
] as const;

const maven = [
  ["shared", "IdempotencyKeysTest", 2],
  ["shared", "MoneyTest", 3],
  ["shared", "PaymentStateMachineTest", 10],
  ["payment-service", "PostgresCompatibilityIT", 1],
  ["payment-service", "RefundApiIT", 2],
  ["payment-service", "RefundLedgerRollbackIT", 1],
  ["payment-service", "PaymentListApiIT", 7],
  ["payment-service", "PaymentApiIT", 5],
  ["payment-service", "HealthApiIT", 1],
  ["payment-service", "LeakyRefundReproduceIT", 1],
  ["payment-service", "LedgerPersistenceIT", 1],
] as const;

const live = [
  ["Health", "GET /actuator/health/liveness → 200 UP", "200"],
  ["Health", "liveness status UP", "UP"],
  ["Health", "GET /actuator/health/readiness → 200", "200"],
  ["Health", "GET /actuator/health → 200", "200"],
  ["Health", "GET /actuator/heapdump → 404", "404"],
  ["OpenAPI", "GET /v3/api-docs → 200", "200"],
  ["OpenAPI", "publishes /api/v1/payments", "present"],
  ["OpenAPI", "publishes /api/v1/refunds", "present"],
  ["OpenAPI", "GET payments has customerId", "customerId"],
  ["OpenAPI", "OpenAPI version present", "3.1.0"],
  ["Payments", "POST payment COMPLETED → 201", "201"],
  ["Payments", "create status COMPLETED", "COMPLETED"],
  ["Payments", "create amount 25.00", "25.0"],
  ["Payments", "echo X-Correlation-Id", "live-pay-1"],
  ["Payments", "POST same Idempotency-Key → 200 replay", "200"],
  ["Payments", "replay same paymentId", "38f7d862-…"],
  ["Payments", "GET payment by id → 200", "200"],
  ["Payments", "get reference live-invoice-1001", "live-invoice-1001"],
  ["Payments", "POST conflict setup → 201", "201"],
  ["Payments", "POST reused key different body → 409", "409"],
  ["Payments", "conflict code IDEMPOTENCY_CONFLICT", "IDEMPOTENCY_CONFLICT"],
  ["Payments", "POST frozen account → 422 DECLINED", "422"],
  ["Payments", "frozen status DECLINED", "DECLINED"],
  ["Payments", "POST missing Idempotency-Key → 400", "400"],
  ["Payments", "missing key IDEMPOTENCY_KEY_REQUIRED", "IDEMPOTENCY_KEY_REQUIRED"],
  ["List", "POST list older payment", "201"],
  ["List", "POST list newer payment", "201"],
  ["List", "GET list Avery → 200", "200"],
  ["List", "list contains older+newer", "n=6"],
  ["List", "list newest first", "newer@0 older@1"],
  ["List", "list first row is Avery", "11111111-…111"],
  ["List", "GET list missing customerId → 400", "400"],
  ["List", "missing customerId VALIDATION_FAILED", "VALIDATION_FAILED"],
  ["List", "GET list unparseable customerId → 400", "400"],
  ["List", "unparseable customerId VALIDATION_FAILED", "VALIDATION_FAILED"],
  ["List", "GET list unknown customer → 404", "404"],
  ["List", "unknown customer CUSTOMER_NOT_FOUND", "CUSTOMER_NOT_FOUND"],
  ["Refunds", "POST payment for refund → 201", "201"],
  ["Refunds", "POST partial refund → 201", "201"],
  ["Refunds", "refund COMPLETED 15.00", "COMPLETED"],
  ["Refunds", "POST refund replay → 200", "200"],
  ["Refunds", "refund replay same id", "cfd8fb52-…"],
  ["Refunds", "POST over-refund → 422", "422"],
  ["Refunds", "over-refund REFUND_EXCEEDS_REMAINING", "REFUND_EXCEEDS_REMAINING"],
  ["Refunds", "GET refund by id → 200", "200"],
  ["Refunds", "refund paymentId matches", "9421ff1d-…"],
  ["Refunds", "POST payment for full refund", "201"],
  ["Refunds", "POST full refund → 201", "201"],
  ["Refunds", "GET payment after full refund", "200"],
  ["Refunds", "full refund sets REVERSED", "REVERSED"],
  ["Persistence", "GET list still includes prior RDS row", "200"],
  ["Persistence", "RDS persisted ecs-rds-demo", "found"],
] as const;

export default function EcsRdsTestReport() {
  const theme = useHostTheme();
  const mavenTotal = maven.reduce((n, row) => n + row[2], 0);

  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <H1>ECS + RDS stack verification</H1>
        <Text tone="secondary">
          Live ALB {ALB} · us-west-2 · account 277374794397 · {CHECKED_AT}
        </Text>
      </Stack>

      <Callout tone="success" title="Stack is fully working">
        All 5 AWS plane checks, 52 live API assertions, and 34 Maven tests
        passed. Avery’s rows survive in Postgres (including the earlier
        ecs-rds-demo payment). Stop the meter with student/work/ecs-rds-lab/stop.sh
        when the demo is done.
      </Callout>

      <Grid columns={4} gap={16}>
        <Stat value="91" label="Checks passed" tone="success" />
        <Stat value="0" label="Failed" />
        <Stat value="52" label="Live ALB assertions" tone="success" />
        <Stat value="34" label="Maven tests (H2 / Testcontainers)" tone="success" />
      </Grid>

      <Card>
        <CardHeader>Checks passed by suite</CardHeader>
        <CardBody>
          <BarChart
            categories={["AWS plane", "Live ALB API", "Maven (local)"]}
            series={[{ name: "Passed checks", data: [5, 52, mavenTotal], tone: "success" }]}
            height={180}
            showValues
          />
          <Text tone="tertiary" size="small">
            Count of passed checks · Source: ECS/ELBv2/RDS describe + ALB HTTP
            + ./mvnw -pl payment-service -am test · {CHECKED_AT}
          </Text>
        </CardBody>
      </Card>

      <H2>AWS plane</H2>
      <Text tone="secondary">
        Fargate task in a public subnet, single-AZ RDS in private subnets, no
        NAT / EKS / Multi-AZ.
      </Text>
      <Table
        headers={["Check", "Observed", "Result"]}
        rows={infra.map(([check, observed]) => [check, observed, "PASS"])}
        rowTone={infra.map(() => "success" as const)}
        striped
      />

      <H2>Maven · payment-service -am test</H2>
      <Text tone="secondary">
        BUILD SUCCESS. Shared unit tests plus payment-service ITs (H2 test
        profile and Testcontainers Postgres). 0 failures, 0 errors, 0 skipped.
      </Text>
      <Table
        headers={["Module", "Class", "Tests", "Result"]}
        columnAlign={["left", "left", "right", "left"]}
        rows={maven.map(([mod, cls, n]) => [mod, cls, String(n), "PASS"])}
        rowTone={maven.map(() => "success" as const)}
        striped
      />

      <Divider />

      <H2>Live ALB API · 52 / 52</H2>
      <Text tone="secondary">
        Same contracts as PaymentApiIT, PaymentListApiIT, HealthApiIT, and
        RefundApiIT, hit against the public ALB and RDS. Idle-customer empty
        list was not run live (seeder only creates Avery).
      </Text>

      <Grid columns={5} gap={12}>
        <Stack gap={4}>
          <H3>Health</H3>
          <Text>5 pass</Text>
        </Stack>
        <Stack gap={4}>
          <H3>OpenAPI</H3>
          <Text>5 pass</Text>
        </Stack>
        <Stack gap={4}>
          <H3>Payments</H3>
          <Text>15 pass</Text>
        </Stack>
        <Stack gap={4}>
          <H3>List</H3>
          <Text>12 pass</Text>
        </Stack>
        <Stack gap={4}>
          <H3>Refunds + RDS</H3>
          <Text style={{ color: theme.text.secondary }}>15 pass</Text>
        </Stack>
      </Grid>

      <Table
        headers={["Area", "Assertion", "Observed", "Result"]}
        rows={live.map(([area, name, observed]) => [area, name, observed, "PASS"])}
        rowTone={live.map(() => "success" as const)}
        striped
        stickyHeader
      />
    </Stack>
  );
}
