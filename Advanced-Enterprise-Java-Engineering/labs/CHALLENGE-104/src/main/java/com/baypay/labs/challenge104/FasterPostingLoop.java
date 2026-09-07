package com.baypay.labs.challenge104;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Same outcomes as {@link NaivePostingLoop}: skip already-posted ids, skip unknown
 * accounts, sum cents onto the account. Indexes replace nested list scans.
 */
public final class FasterPostingLoop {

    public record Result(List<String> postedPaymentIds, List<NaivePostingLoop.Balance> balances, long checksum) {
    }

    public Result post(
            List<NaivePostingLoop.InboundPayment> inbound,
            List<NaivePostingLoop.LedgerRow> ledger,
            List<NaivePostingLoop.Balance> startingBalances) {
        List<NaivePostingLoop.Balance> working = new ArrayList<>(startingBalances.size());
        Map<String, NaivePostingLoop.Balance> byAccount = HashMap.newHashMap(startingBalances.size());
        for (NaivePostingLoop.Balance src : startingBalances) {
            NaivePostingLoop.Balance copy = new NaivePostingLoop.Balance(src.accountId, src.amountCents);
            working.add(copy);
            byAccount.put(copy.accountId, copy);
        }

        Set<String> seen = HashSet.newHashSet(ledger.size() + inbound.size());
        for (NaivePostingLoop.LedgerRow row : ledger) {
            seen.add(row.paymentId);
        }

        List<String> posted = new ArrayList<>();
        for (NaivePostingLoop.InboundPayment payment : inbound) {
            if (!seen.add(payment.paymentId())) {
                continue;
            }
            NaivePostingLoop.Balance found = byAccount.get(payment.accountId());
            if (found == null) {
                seen.remove(payment.paymentId());
                continue;
            }
            found.amountCents = found.amountCents + payment.amountCents();
            ledger.add(new NaivePostingLoop.LedgerRow(payment.paymentId(), payment.accountId(), found.amountCents));
            posted.add(payment.paymentId());
        }
        return new Result(posted, working, NaivePostingLoop.checksum(posted, working));
    }
}
