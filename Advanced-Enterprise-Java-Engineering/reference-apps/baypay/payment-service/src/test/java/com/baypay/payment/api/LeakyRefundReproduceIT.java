package com.baypay.payment.api;

import com.baypay.refund.api.CreateRefundRequest;
import com.baypay.refund.application.LeakyRefundService;
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

import java.math.BigDecimal;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.doAnswer;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * FIX-304 incident: {@link LeakyRefundService} swallows a ledger failure and
 * still returns a completed refund. The HTTP-shaped result is success; treasury
 * has no REFUND row.
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles({"test", "leaky"})
class LeakyRefundReproduceIT {

    @Autowired
    private MockMvc mvc;

    @Autowired
    private ObjectMapper mapper;

    @Autowired
    private LeakyRefundService leaky;

    @Autowired
    private RefundRepository refunds;

    @MockitoSpyBean
    private LedgerTransactionRepository ledger;

    @Test
    void completedRefundSurvivesWhenLedgerSaveFails() throws Exception {
        UUID paymentId = createPayment();
        failRefundLedgerSaves();

        LeakyRefundService.CreateResult result = leaky.create(
                new CreateRefundRequest(paymentId, new BigDecimal("15.00"), "partial"),
                "fix-304-leaky-1");

        assertEquals(RefundStatus.COMPLETED, result.refund().status());
        assertTrue(refunds.findById(result.refund().id()).isPresent());
        assertTrue(ledger.findByRefundId(result.refund().id()).isEmpty());
        assertEquals(0, ledger.findByPaymentId(paymentId).stream()
                .filter(row -> row.type() == LedgerTransaction.Type.REFUND)
                .count());
    }

    private void failRefundLedgerSaves() {
        doAnswer(invocation -> {
            LedgerTransaction row = invocation.getArgument(0);
            if (row.type() == LedgerTransaction.Type.REFUND) {
                throw new IllegalStateException("ledger write failed");
            }
            return invocation.callRealMethod();
        }).when(ledger).save(any());
    }

    private UUID createPayment() throws Exception {
        String body = """
                {
                  "customerId": "%s",
                  "accountId": "%s",
                  "amount": 40.00,
                  "currency": "USD",
                  "reference": "fix-304-leaky"
                }
                """.formatted(DemoIds.CUSTOMER_AVERY, DemoIds.ACCOUNT_ACTIVE);
        var created = mvc.perform(post("/api/v1/payments")
                        .contentType(MediaType.APPLICATION_JSON)
                        .header("Idempotency-Key", "fix-304-leaky-pay")
                        .content(body))
                .andExpect(status().isCreated())
                .andReturn();
        return UUID.fromString(
                mapper.readTree(created.getResponse().getContentAsString()).get("paymentId").asText());
    }
}
