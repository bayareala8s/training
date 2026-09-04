package com.baypay.shared.idempotency;

import com.baypay.shared.error.DomainValidationException;
import com.baypay.shared.error.ErrorCode;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.HexFormat;
import java.util.Locale;

public final class IdempotencyKeys {

    public static final int MIN_LENGTH = 8;
    public static final int MAX_LENGTH = 128;
    private static final String PATTERN = "[A-Za-z0-9._-]+";

    private IdempotencyKeys() {
    }

    public static String require(String raw) {
        if (raw == null || raw.isBlank()) {
            throw new DomainValidationException(
                    ErrorCode.IDEMPOTENCY_KEY_REQUIRED,
                    "Idempotency-Key header is required");
        }
        String key = raw.trim();
        if (key.length() < MIN_LENGTH || key.length() > MAX_LENGTH || !key.matches(PATTERN)) {
            throw new DomainValidationException(
                    ErrorCode.IDEMPOTENCY_KEY_REQUIRED,
                    "Idempotency-Key must be 8-128 characters of [A-Za-z0-9._-]");
        }
        return key;
    }

    public static String sha256(String operation, String canonicalBody) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            String material = operation.toLowerCase(Locale.ROOT) + "\n" + canonicalBody;
            byte[] hash = digest.digest(material.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("SHA-256 not available", e);
        }
    }
}
