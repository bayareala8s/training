package com.baypay.shared.error;

public class DomainValidationException extends BayPayException {

    public DomainValidationException(String message) {
        super(ErrorCode.VALIDATION_FAILED, message);
    }

    public DomainValidationException(ErrorCode code, String message) {
        super(code, message);
    }
}
