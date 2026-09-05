/**
 * Ledger posting. Today this runs in-process on the same {@code @Transactional}
 * as authorize so POST /payments returns COMPLETED. Extract to a queue when
 * posting has a different failure domain — not to draw more boxes.
 */
package com.baypay.worker;
