package com.baypay.payment;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.condition.EnabledIf;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.context.ActiveProfiles;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.PostgreSQLContainer;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Optional PostgreSQL mapping check. Disabled when Docker is not running.
 * Default tests use H2 with MODE=PostgreSQL.
 */
@SpringBootTest
@ActiveProfiles("test")
@EnabledIf("dockerAvailable")
class PostgresCompatibilityIT {

    static boolean dockerAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable ex) {
            return false;
        }
    }

    @ServiceConnection
    static final PostgreSQLContainer<?> POSTGRES = dockerAvailable()
            ? new PostgreSQLContainer<>("postgres:16-alpine")
            : null;

    static {
        if (POSTGRES != null) {
            POSTGRES.start();
        }
    }

    @Autowired
    private JdbcTemplate jdbc;

    @Test
    void hibernateCreatedPaymentTable() {
        Integer tables = jdbc.queryForObject(
                "select count(*) from information_schema.tables where table_name = 'payments'",
                Integer.class);
        assertEquals(1, tables);
    }
}
