package com.baypay.shared.error;

/** Lookup missed. Mapped to HTTP 404. Do not use {@code Optional.orElse(null)}. */
public class ResourceNotFoundException extends BayPayException {

    public ResourceNotFoundException(ErrorCode code, String message) {
        super(code, message);
    }
}
