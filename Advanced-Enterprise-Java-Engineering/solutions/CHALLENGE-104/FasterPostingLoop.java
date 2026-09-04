package com.baypay.labs.challenge104;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Instructor reference for CHALLENGE-104.
 * Indexes payment ids and balances once; keeps cents as long.
 * Do not copy this file into the student starter folder.
 */
public final class FasterPostingLoop {

    public record Result(List<String> postedPaymentIds, List<NaivePostingLoop.Balance> balances, long checksum) {
    }

    public Result post(
            List<NaivePostingLoop.InboundPayment> inbound,
            List<NaivePostingLoop.LedgerRow> ledger,
            List<NaivePostingLoop.Balance> startingBalances) {

        Set<String> seenPaymentIds = HashSet.newHashSet(ledger.size() + inbound.size());
        for (NaivePostingLoop.LedgerRow row : ledger) {
            seenPaymentIds.add(row.paymentId);
        }

        Map<String, Long> centsByAccount = HashMap.newHashMap(startingBalances.size());
        for (NaivePostingLoop.Balance balance : startingBalances) {
            centsByAccount.put(balance.accountId, Math.round(balance.amountCents));
        }

        List<String> posted = new ArrayList<>();
        for (NaivePostingLoop.InboundPayment payment : inbound) {
            if (!seenPaymentIds.add(payment.paymentId())) {
                continue;
            }
            Long current = centsByAccount.get(payment.accountId());
            if (current == null) {
                seenPaymentIds.remove(payment.paymentId());
                continue;
            }
            long delta = Math.round(payment.amountCents());
            centsByAccount.put(payment.accountId(), current + delta);
            posted.add(payment.paymentId());
        }

        List<NaivePostingLoop.Balance> nextBalances = new ArrayList<>(startingBalances.size());
        for (NaivePostingLoop.Balance original : startingBalances) {
            nextBalances.add(new NaivePostingLoop.Balance(
                    original.accountId, Double.valueOf(centsByAccount.get(original.accountId))));
        }
        return new Result(posted, nextBalances, NaivePostingLoop.checksum(posted, nextBalances));
    }

    public static void main(String[] args) {
        int n = args.length > 0 ? Integer.parseInt(args[0]) : NaivePostingLoop.DEFAULT_PAYMENTS;
        NaivePostingLoop.Workload workload = NaivePostingLoop.generate(
                n, NaivePostingLoop.DEFAULT_EXISTING, NaivePostingLoop.DEFAULT_ACCOUNTS, NaivePostingLoop.SEED);
        FasterPostingLoop loop = new FasterPostingLoop();
        long start = System.nanoTime();
        Result result = loop.post(workload.inbound(), workload.ledger(), workload.balances());
        long ms = (System.nanoTime() - start) / 1_000_000L;
        System.out.println("faster posted=" + result.postedPaymentIds().size()
                + " checksum=" + result.checksum()
                + " elapsedMs=" + ms
                + " n=" + n);
    }
}
