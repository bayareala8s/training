package com.baypay.shared.demo;

import java.util.UUID;

/**
 * Stable fictional BayPay identities used by local seed data and tests.
 */
public final class DemoIds {

    public static final UUID CUSTOMER_AVERY = UUID.fromString("11111111-1111-1111-1111-111111111111");
    public static final UUID ACCOUNT_ACTIVE = UUID.fromString("22222222-2222-2222-2222-222222222221");
    public static final UUID ACCOUNT_FROZEN = UUID.fromString("22222222-2222-2222-2222-222222222222");

    private DemoIds() {
    }
}
