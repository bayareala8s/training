package com.baypay.shared.domain;

/** Account lifecycle. FROZEN is a decline, not a missing customer. */
public enum AccountStatus {
    ACTIVE,
    FROZEN,
    CLOSED
}
