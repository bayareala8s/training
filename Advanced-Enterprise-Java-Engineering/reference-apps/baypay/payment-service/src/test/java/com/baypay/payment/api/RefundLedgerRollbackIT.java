package com.baypay.payment.api;

import com.baypay.shared.demo.DemoIds;
import com.baypay.shared.domain.LedgerTransaction;
import com.baypay.shared.domain.RefundStatus;
import com.baypay.shared.persistence.LedgerTransactionRepository;
import com.baypay.shared.persistence.RefundRepository;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.bean.override.mockito.MockitoSpyBean;
import org.springframework.test.web.servlet.MockMvc;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * FIX-304 fix: {@code RefundApplicationService} lets a ledger failure escape.
 * The transaction rolls back — HTTP is 5xx and no COMPLETED refund remains.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class RefundLedgerRollbackIT {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper mapper;

    @Autowired
    private RefundRepository refunds;

    @MockitoSpyBean
    private LedgerTransactionRepository ledger;

    @Test
    void ledgerFailureRollsBackCompletedRefund() throws Exception {
        UUID paymentId = createPayment();
        doAnswer(invocation -> {
            LedgerTransaction row = invocation.getArgument(0);
            if (row.type() == LedgerTransaction.Type.REFUND) {
                throw new IllegalStateException("ledger write failed");
            }
            return invocation.callRealMethod();
        }).when(ledger).save(any());

        mvc.perform(post("/api/v1/refunds")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "fix-304-fixed-1")
                        .content("""
                                {"paymentId":"%s","amount":15.00,"reason":"partial"}
                                """.formatted(paymentId)))
                .andExpect(status().isInternalServerError());

        assertEquals(0, refunds.findByPaymentIdAndStatus(paymentId, RefundStatus.COMPLETED).size());
        assertEquals(0, ledger.findByPaymentId(paymentId).stream()
                .filter(row -> row.type() == LedgerTransaction.Type.REFUND)
                .count());
        mvc.perform(get("/api/v1/refunds/" + UUID.fromString("00000000-0000-0000-0000-000000000304")))
                .andExpect(status().isNotFound());
        assertTrue(refunds.findAll().stream()
                .noneMatch(r -> r.paymentId().equals(paymentId) && r.status() == RefundStatus.COMPLETED));
    }

    private UUID createPayment() throws Exception {
        String body = """
                {
                  "customerId": "%s",
                  "accountId": "%s",
                  "amount": 40.00,
                  "currency": "USD",
                  "reference": "fix-304-fixed"
                }
                """.formatted(DemoIds.CUSTOMER_AVERY, DemoIds.ACCOUNT_ACTIVE);
        var created = mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "fix-304-fixed-pay")
                        .content(body))
                .andExpect(status().isCreated())
                .andReturn();
        return UUID.fromString(
                mapper.readTree(created.getResponse().getContentAsString()).get("paymentId").asText());
    }
}
