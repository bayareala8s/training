package com.baypay.shared.error;

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
