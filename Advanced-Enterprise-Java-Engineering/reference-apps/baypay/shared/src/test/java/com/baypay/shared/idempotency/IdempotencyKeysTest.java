package com.baypay.shared.idempotency;

import com.baypay.shared.error.DomainValidationException;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/** Missing/short keys fail; same body hashes equal; different bodies do not. */
class IdempotencyKeysTest {

    @Test
    void requiresWellFormedKey() {
        assertThrows(DomainValidationException.class, () -> IdempotencyKeys.require(null));
        assertThrows(DomainValidationException.class, () -> IdempotencyKeys.require("short"));
        assertEquals("pay-key-001", IdempotencyKeys.require(" pay-key-001 "));
    }

    @Test
    void hashChangesWhenBodyChanges() {
        String a = IdempotencyKeys.sha256("PAYMENT_CREATE", "cust|acct|10.00|USD|");
        String b = IdempotencyKeys.sha256("PAYMENT_CREATE", "cust|acct|10.01|USD|");
        assertNotEquals(a, b);
        assertEquals(64, a.length());
    }
}
