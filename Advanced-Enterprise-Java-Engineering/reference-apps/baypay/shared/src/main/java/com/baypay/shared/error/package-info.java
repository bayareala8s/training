/**
 * Domain errors carry an {@link com.baypay.shared.error.ErrorCode} so HTTP
 * mapping stays in {@code ApiExceptionHandler}. Do not throw raw
 * {@code RuntimeException} from the domain, and do not log Avery Chen's
 * identifiers without a correlation id.
 */
package com.baypay.shared.error;
