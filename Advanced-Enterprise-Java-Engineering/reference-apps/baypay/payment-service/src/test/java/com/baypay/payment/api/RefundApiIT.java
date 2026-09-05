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

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/** Refund create against a completed payment; remaining-amount rules live in the service. */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class RefundApiIT {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper mapper;

    @Test
    void refundsCompletedPaymentAndBlocksOverRefund() throws Exception {
        String paymentId = createPayment("40.00", "refund-src-1", "pay-key-refund-src-1");

        String refundBody = """
                {"paymentId":"%s","amount":15.00,"reason":"partial"}
                """.formatted(paymentId);

        var created = mvc.perform(post("/api/v1/refunds")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "ref-key-partial-1")
                        .content(refundBody))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andExpect(jsonPath("$.amount").value(15.00))
                .andReturn();

        JsonNode json = mapper.readTree(created.getResponse().getContentAsString());
        String refundId = json.get("refundId").asText();

        mvc.perform(post("/api/v1/refunds")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "ref-key-partial-1")
                        .content(refundBody))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.refundId").value(refundId));

        mvc.perform(post("/api/v1/refunds")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "ref-key-too-much")
                        .content("""
                                {"paymentId":"%s","amount":30.00,"reason":"too much"}
                                """.formatted(paymentId)))
                .andExpect(status().isUnprocessableEntity())
                .andExpect(jsonPath("$.code").value("REFUND_EXCEEDS_REMAINING"));

        mvc.perform(get("/api/v1/refunds/" + refundId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.paymentId").value(paymentId));
    }

    @Test
    void fullRefundReversesPayment() throws Exception {
        String paymentId = createPayment("12.00", "full-refund", "pay-key-full-refund");

        mvc.perform(post("/api/v1/refunds")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "ref-key-full")
                        .content("""
                                {"paymentId":"%s","amount":12.00,"reason":"full"}
                                """.formatted(paymentId)))
                .andExpect(status().isCreated());

        mvc.perform(get("/api/v1/payments/" + paymentId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("REVERSED"));
    }

    private String createPayment(String amount, String reference, String key) throws Exception {
        String body = """
                {
                  "customerId": "%s",
                  "accountId": "%s",
                  "amount": %s,
                  "currency": "USD",
                  "reference": "%s"
                }
                """.formatted(DemoIds.CUSTOMER_AVERY, DemoIds.ACCOUNT_ACTIVE, amount, reference);
        var result = mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", key)
                        .content(body))
                .andExpect(status().isCreated())
                .andReturn();
        return mapper.readTree(result.getResponse().getContentAsString()).get("paymentId").asText();
    }
}
