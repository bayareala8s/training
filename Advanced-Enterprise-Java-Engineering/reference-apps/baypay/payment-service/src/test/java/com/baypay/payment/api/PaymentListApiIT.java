package com.baypay.payment.api;

import com.baypay.shared.demo.DemoIds;
import com.baypay.shared.domain.Customer;
import com.baypay.shared.persistence.CustomerRepository;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.time.Instant;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.hasItem;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
/**
 * CAPSTONE-1: Harbor Market lists Avery Chen by customerId. These tests fail
 * if GET /api/v1/payments?customerId= is missing. POST still owns Idempotency-Key.
 */
class PaymentListApiIT {

    private static final UUID UNKNOWN_CUSTOMER = UUID.fromString("aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee");
    private static final UUID IDLE_CUSTOMER = UUID.fromString("cccccccc-dddd-4eee-8fff-000000000001");

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper mapper;

    @Autowired
    private CustomerRepository customers;

    @Test
    void listsAveryPaymentsNewestFirst() throws Exception {
        String olderId = createPayment("cap1-avery-older", "13.00", "cap1-invoice-older");
        String newerId = createPayment("cap1-avery-newer", "17.00", "cap1-invoice-newer");

        MvcResult listed = mvc.perform(get("/api/v1/payments")
                        .param("customerId", DemoIds.CUSTOMER_AVERY.toString())
                        .header("X-Correlation-Id", "cap1-list"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[*].paymentId", hasItem(olderId)))
                .andExpect(jsonPath("$[*].paymentId", hasItem(newerId)))
                .andExpect(jsonPath("$[0].customerId").value(DemoIds.CUSTOMER_AVERY.toString()))
                .andReturn();

        JsonNode array = mapper.readTree(listed.getResponse().getContentAsString());
        int newerIndex = indexOfPayment(array, newerId);
        int olderIndex = indexOfPayment(array, olderId);
        assertThat(newerIndex).isLessThan(olderIndex);
    }

    @Test
    void knownCustomerWithNoPaymentsReturnsEmptyArray() throws Exception {
        if (!customers.existsById(IDLE_CUSTOMER)) {
            customers.save(new Customer(
                    IDLE_CUSTOMER,
                    "Idle Statement Customer",
                    "idle.statement@baypay.test",
                    Instant.parse("2026-01-15T00:00:00Z")));
        }

        mvc.perform(get("/api/v1/payments").param("customerId", IDLE_CUSTOMER.toString()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isArray())
                .andExpect(jsonPath("$.length()").value(0));
    }

    @Test
    void missingCustomerIdIs400() throws Exception {
        mvc.perform(get("/api/v1/payments"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"));
    }

    @Test
    void unparseableCustomerIdIs400() throws Exception {
        mvc.perform(get("/api/v1/payments").param("customerId", "not-a-uuid"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("VALIDATION_FAILED"));
    }

    @Test
    void unknownCustomerIs404() throws Exception {
        mvc.perform(get("/api/v1/payments").param("customerId", UNKNOWN_CUSTOMER.toString()))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.code").value("CUSTOMER_NOT_FOUND"));
    }

    @Test
    void postStillRequiresIdempotencyKey() throws Exception {
        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(paymentJson("1.00", "cap1-no-key")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("IDEMPOTENCY_KEY_REQUIRED"));
    }

    @Test
    void openApiListsCustomerIdQuery() throws Exception {
        mvc.perform(get("/v3/api-docs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.paths['/api/v1/payments'].get").exists())
                .andExpect(jsonPath("$.paths['/api/v1/payments'].get.parameters[*].name",
                        hasItem("customerId")));
    }

    private static int indexOfPayment(JsonNode array, String paymentId) {
        for (int i = 0; i < array.size(); i++) {
            if (paymentId.equals(array.get(i).get("paymentId").asText())) {
                return i;
            }
        }
        return -1;
    }

    private String createPayment(String key, String amount, String reference) throws Exception {
        MvcResult created = mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", key)
                        .header("X-Correlation-Id", "cap1-create")
                        .content(paymentJson(amount, reference)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andReturn();
        JsonNode json = mapper.readTree(created.getResponse().getContentAsString());
        return json.get("paymentId").asText();
    }

    private static String paymentJson(String amount, String reference) {
        return """
                {
                  "customerId": "%s",
                  "accountId": "%s",
                  "amount": %s,
                  "currency": "USD",
                  "reference": "%s"
                }
                """.formatted(DemoIds.CUSTOMER_AVERY, DemoIds.ACCOUNT_ACTIVE, amount, reference);
    }
}
