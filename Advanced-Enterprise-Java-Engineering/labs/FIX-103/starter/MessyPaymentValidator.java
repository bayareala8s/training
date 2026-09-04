package com.baypay.labs.fix103;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Deliberately poor BayPay validator used by FIX-103.
 * Do not copy this style into payment-service. Refactor in your own file.
 */
public class MessyPaymentValidator {

    public String lastReason;
    public boolean lastOk;
    public List scratch = new ArrayList();
    public Map cache = new HashMap();

    public boolean validate(
            Object customerId,
            Object accountId,
            Object amount,
            Object currency,
            Object accountCustomerId,
            Object accountStatus,
            Object accountCurrency) {
        lastOk = true;
        lastReason = null;
        try {
            scratch.add(amount);
            scratch.add(currency);
            cache.put(customerId, accountId);

            BigDecimal parsed = (BigDecimal) amount;
            if (parsed.doubleValue() <= 0.0d) {
                lastOk = false;
                lastReason = "bad amount";
            }

            String ccy = (String) currency;
            if (ccy == "USD" || ccy.equals("usd") || ccy.equals("EUR") || ccy.equals("GBP")) {
                currency = ccy.toUpperCase();
            } else {
                lastOk = false;
                lastReason = "ccy";
            }

            try {
                if (accountStatus.toString().toLowerCase() != "active") {
                    lastOk = false;
                    lastReason = "account";
                }
            } catch (Exception ignored) {
                // contractor: "status is usually present"
            }

            if (customerId.toString() != accountCustomerId.toString()) {
                lastOk = false;
                lastReason = "mismatch";
            }

            if (accountCurrency != null && currency != null
                    && !accountCurrency.toString().equals(currency.toString())) {
                lastOk = false;
                lastReason = "fx";
            }

            if (parsed != null && parsed.doubleValue() > 1000000.0d) {
                lastOk = false;
                lastReason = "ceiling";
            }

            return lastOk;
        } catch (Exception e) {
            return false;
        }
    }
}
