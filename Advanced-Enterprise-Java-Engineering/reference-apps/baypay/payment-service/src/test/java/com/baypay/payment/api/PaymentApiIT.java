package com.baypay.payment.api;

import com.baypay.shared.demo.DemoIds;
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

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
/**
 * End-to-end create/get/replay against the modular monolith. Uses Avery's
 * ACTIVE account. A frozen-account decline is covered in validation labs.
 */
class PaymentApiIT {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper mapper;

    @Test
    void createsCompletedPaymentAndReplaysIdempotentRetry() throws Exception {
        String body = paymentJson("25.00", "invoice-1001");
        MvcResult created = mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "pay-key-invoice-1001")
                        .header("X-Correlation-Id", "it-pay-1")
                        .content(body))
                .andExpect(status().isCreated())
                .andExpect(header().string("X-Correlation-Id", "it-pay-1"))
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andExpect(jsonPath("$.amount").value(25.00))
                .andReturn();

        JsonNode json = mapper.readTree(created.getResponse().getContentAsString());
        String paymentId = json.get("paymentId").asText();

        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "pay-key-invoice-1001")
                        .content(body))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.paymentId").value(paymentId))
                .andExpect(jsonPath("$.status").value("COMPLETED"));

        mvc.perform(get("/api/v1/payments/" + paymentId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.reference").value("invoice-1001"));
    }

    @Test
    void rejectsReusedKeyWithDifferentBody() throws Exception {
        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "pay-key-conflict")
                        .content(paymentJson("10.00", "a")))
                .andExpect(status().isCreated());

        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "pay-key-conflict")
                        .content(paymentJson("11.00", "a")))
                .andExpect(status().isConflict())
                .andExpect(jsonPath("$.code").value("IDEMPOTENCY_CONFLICT"));
    }

    @Test
    void declinesFrozenAccount() throws Exception {
        String body = """
                {
                  "customerId": "%s",
                  "accountId": "%s",
                  "amount": 9.99,
                  "currency": "USD",
                  "reference": "frozen"
                }
                """.formatted(DemoIds.CUSTOMER_AVERY, DemoIds.ACCOUNT_FROZEN);

        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "pay-key-frozen-001")
                        .content(body))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.status").value("DECLINED"));
    }

    @Test
    void requiresIdempotencyKey() throws Exception {
        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(paymentJson("1.00", "no-key")))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.code").value("IDEMPOTENCY_KEY_REQUIRED"));
    }

    @Test
    void openApiContractIsPublished() throws Exception {
        mvc.perform(get("/v3/api-docs"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.openapi").isString())
                .andExpect(jsonPath("$.paths['/api/v1/payments']").exists())
                .andExpect(jsonPath("$.paths['/api/v1/refunds']").exists());
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
