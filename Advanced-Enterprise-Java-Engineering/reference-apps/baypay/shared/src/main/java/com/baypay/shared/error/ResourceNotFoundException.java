package com.baypay.shared.error;

public class ResourceNotFoundException extends BayPayException {

    public ResourceNotFoundException(ErrorCode code, String message) {
        super(code, message);
    }
}
