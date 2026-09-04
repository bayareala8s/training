package com.baypay.labs.challenge104;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class FasterPostingLoopTest {

    private final FasterPostingLoop faster = new FasterPostingLoop();
    private final NaivePostingLoop naive = new NaivePostingLoop();

    @Test
    void matchesNaiveOnHandCraftedCases() {
        List<NaivePostingLoop.Balance> balances = List.of(
                new NaivePostingLoop.Balance("acct-0", 1_000_000.0d),
                new NaivePostingLoop.Balance("acct-1", 1_000_001.0d));
        List<NaivePostingLoop.LedgerRow> ledger = new ArrayList<>();
        ledger.add(new NaivePostingLoop.LedgerRow("hist-0", "acct-0", 100.0d));
        List<NaivePostingLoop.InboundPayment> inbound = List.of(
                new NaivePostingLoop.InboundPayment("hist-0", "acct-0", 25.0d),
                new NaivePostingLoop.InboundPayment("new-1", "acct-0", 40.0d),
                new NaivePostingLoop.InboundPayment("new-2", "acct-missing", 10.0d),
                new NaivePostingLoop.InboundPayment("new-3", "acct-1", 15.0d));

        List<NaivePostingLoop.Balance> naiveBalances = copyBalances(balances);
        List<NaivePostingLoop.LedgerRow> naiveLedger = copyLedger(ledger);
        NaivePostingLoop.Result expected = naive.post(inbound, naiveLedger, naiveBalances);
        FasterPostingLoop.Result actual = faster.post(inbound, copyLedger(ledger), copyBalances(balances));

        assertEquals(expected.postedPaymentIds(), actual.postedPaymentIds());
        assertEquals(expected.checksum(), actual.checksum());
        assertEquals(1_000_040L, Math.round(actual.balances().get(0).amountCents));
        assertEquals(1_000_016L, Math.round(actual.balances().get(1).amountCents));
    }

    @Test
    void matchesNaiveChecksumOnSeededWorkload() {
        NaivePostingLoop.Workload workload = NaivePostingLoop.generate(400, 80, 25, NaivePostingLoop.SEED);
        NaivePostingLoop.Result expected = naive.post(
                workload.inbound(), copyLedger(workload.ledger()), copyBalances(workload.balances()));
        FasterPostingLoop.Result actual = faster.post(
                workload.inbound(), copyLedger(workload.ledger()), copyBalances(workload.balances()));
        assertEquals(expected.postedPaymentIds().size(), actual.postedPaymentIds().size());
        assertEquals(expected.checksum(), actual.checksum());
        assertTrue(actual.postedPaymentIds().contains("new-avery-demo"));
    }

    private static List<NaivePostingLoop.Balance> copyBalances(List<NaivePostingLoop.Balance> source) {
        List<NaivePostingLoop.Balance> copy = new ArrayList<>();
        for (NaivePostingLoop.Balance balance : source) {
            copy.add(new NaivePostingLoop.Balance(balance.accountId, balance.amountCents));
        }
        return copy;
    }

    private static List<NaivePostingLoop.LedgerRow> copyLedger(List<NaivePostingLoop.LedgerRow> source) {
        List<NaivePostingLoop.LedgerRow> copy = new ArrayList<>();
        for (NaivePostingLoop.LedgerRow row : source) {
            copy.add(new NaivePostingLoop.LedgerRow(row.paymentId, row.accountId, row.amountCents));
        }
        return copy;
    }
}
