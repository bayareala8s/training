package com.baypay.shared.domain;

/** Requested → processing → completed (or failed). */
public enum RefundStatus {
    REQUESTED,
    PROCESSING,
    COMPLETED,
    FAILED
}
