package com.baypay.payment.api;

import com.baypay.shared.demo.DemoIds;
import com.baypay.shared.domain.LedgerTransaction;
import com.baypay.shared.persistence.LedgerTransactionRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * BUILD-303: a completed payment posts one PAYMENT ledger row; replay does not
 * add a second; a refund posts one REFUND row for that refundId.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class LedgerPersistenceIT {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper mapper;

    @Autowired
    private LedgerTransactionRepository ledger;

    @Test
    void paymentReplayDoesNotDoublePostLedgerAndRefundAddsRefundRow() throws Exception {
        String payBody = """
                {
                  "customerId": "%s",
                  "accountId": "%s",
                  "amount": 40.00,
                  "currency": "USD",
                  "reference": "build-303-ledger"
                }
                """.formatted(DemoIds.CUSTOMER_AVERY, DemoIds.ACCOUNT_ACTIVE);

        MvcResult created = mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "build-303-pay")
                        .content(payBody))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("COMPLETED"))
                .andReturn();
        UUID paymentId = UUID.fromString(
                mapper.readTree(created.getResponse().getContentAsString()).get("paymentId").asText());

        assertEquals(1, paymentRows(paymentId).size());

        mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "build-303-pay")
                        .content(payBody))
                .andExpect(status().isOk());

        assertEquals(1, paymentRows(paymentId).size());

        MvcResult refunded = mvc.perform(post("/api/v1/refunds")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "build-303-ref")
                        .content("""
                                {"paymentId":"%s","amount":15.00,"reason":"partial"}
                                """.formatted(paymentId)))
                .andExpect(status().isCreated())
                .andReturn();
        UUID refundId = UUID.fromString(
                mapper.readTree(refunded.getResponse().getContentAsString()).get("refundId").asText());

        assertEquals(1, paymentRows(paymentId).size());
        assertEquals(LedgerTransaction.Type.REFUND, ledger.findByRefundId(refundId).orElseThrow().type());
    }

    private List<LedgerTransaction> paymentRows(UUID paymentId) {
        return ledger.findByPaymentId(paymentId).stream()
                .filter(row -> row.type() == LedgerTransaction.Type.PAYMENT)
                .toList();
    }
}
