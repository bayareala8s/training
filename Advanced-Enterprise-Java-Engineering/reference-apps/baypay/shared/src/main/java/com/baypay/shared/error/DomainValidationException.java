package com.baypay.shared.error;

/** Constructor / factory invariant failed. Usually HTTP 422 (400 if the key is missing). */
public class DomainValidationException extends BayPayException {

    public DomainValidationException(String message) {
        super(ErrorCode.VALIDATION_FAILED, message);
    }

    public DomainValidationException(ErrorCode code, String message) {
        super(code, message);
    }
}
