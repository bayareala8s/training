package com.baypay.shared.error;

/** Unchecked so application services stay readable. Callers must not swallow these (FIX-103). */
public class BayPayException extends RuntimeException {

    private final ErrorCode code;

    public BayPayException(ErrorCode code, String message) {
        super(message);
        this.code = code;
    }

    public ErrorCode code() {
        return code;
    }
}
