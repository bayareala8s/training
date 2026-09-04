// Instructor sketch — CAPSTONE-1 list-by-customer.
// Merge into the existing types. This file is not compiled by the reference app.
// Avery Chen: 11111111-1111-1111-1111-111111111111
// Keep POST Idempotency-Key. Do not log PAN.

// --- PaymentRepository ---
// List<Payment> findByCustomerIdOrderByCreatedAtDesc(UUID customerId);

// --- PaymentApplicationService ---
// @Transactional(readOnly = true)
// public List<Payment> listByCustomer(UUID customerId) {
//     customers.findById(customerId)
//             .orElseThrow(() -> new ResourceNotFoundException(
//                     ErrorCode.CUSTOMER_NOT_FOUND, "Customer not found: " + customerId));
//     return payments.findByCustomerIdOrderByCreatedAtDesc(customerId);
// }

// --- PaymentController (class needs @Validated for @RequestParam @NotNull) ---
// @GetMapping
// @Operation(summary = "List payments for a customer")
// public List<PaymentResponse> list(@RequestParam @NotNull UUID customerId) {
//     return payments.listByCustomer(customerId).stream()
//             .map(PaymentResponse::from)
//             .toList();
// }

package com.baypay.solution.capstone1;

/** Marker so the sketch stays in a legal compilation unit if someone javac's it. */
public final class ListPaymentsSnippet {
    private ListPaymentsSnippet() {
    }
}
