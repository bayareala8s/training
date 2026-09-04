package com.baypay.labs.challenge104;

import java.util.List;

/**
 * CHALLENGE-104 student stub. Leave {@link NaivePostingLoop} naive; implement this class.
 */
public final class FasterPostingLoop {

    public record Result(List<String> postedPaymentIds, List<NaivePostingLoop.Balance> balances, long checksum) {
    }

    public Result post(
            List<NaivePostingLoop.InboundPayment> inbound,
            List<NaivePostingLoop.LedgerRow> ledger,
            List<NaivePostingLoop.Balance> startingBalances) {
        throw new UnsupportedOperationException("implement CHALLENGE-104 FasterPostingLoop.post");
    }
}
