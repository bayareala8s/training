package com.baypay.payment.api;

import com.baypay.shared.error.BayPayException;
import com.baypay.shared.error.DomainValidationException;
import com.baypay.shared.error.ErrorCode;
import com.baypay.shared.error.ResourceNotFoundException;
import com.baypay.shared.idempotency.IdempotencyConflictException;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.net.URI;
import java.util.stream.Collectors;

@RestControllerAdvice
public class ApiExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ProblemDetail> notFound(ResourceNotFoundException ex, HttpServletRequest request) {
        return problem(HttpStatus.NOT_FOUND, ex, request);
    }

    @ExceptionHandler(IdempotencyConflictException.class)
    public ResponseEntity<ProblemDetail> conflict(IdempotencyConflictException ex, HttpServletRequest request) {
        return problem(HttpStatus.CONFLICT, ex, request);
    }

    @ExceptionHandler(DomainValidationException.class)
    public ResponseEntity<ProblemDetail> validation(DomainValidationException ex, HttpServletRequest request) {
        HttpStatus status = ex.code() == ErrorCode.IDEMPOTENCY_KEY_REQUIRED
                ? HttpStatus.BAD_REQUEST
                : HttpStatus.UNPROCESSABLE_ENTITY;
        return problem(status, ex, request);
    }

    @ExceptionHandler(BayPayException.class)
    public ResponseEntity<ProblemDetail> domain(BayPayException ex, HttpServletRequest request) {
        return problem(HttpStatus.CONFLICT, ex, request);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ProblemDetail> beanValidation(
            MethodArgumentNotValidException ex, HttpServletRequest request) {
        String detail = ex.getBindingResult().getFieldErrors().stream()
                .map(error -> error.getField() + " " + error.getDefaultMessage())
                .collect(Collectors.joining("; "));
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, detail);
        problem.setTitle("Request validation failed");
        problem.setType(URI.create("https://baypay.example/errors/VALIDATION_FAILED"));
        problem.setProperty("code", ErrorCode.VALIDATION_FAILED.name());
        problem.setInstance(URI.create(request.getRequestURI()));
        return ResponseEntity.badRequest().body(problem);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ProblemDetail> unknown(Exception ex, HttpServletRequest request) {
        log.error("Unhandled error on {}", request.getRequestURI(), ex);
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(
                HttpStatus.INTERNAL_SERVER_ERROR, "An unexpected error occurred");
        problem.setTitle("Internal error");
        problem.setInstance(URI.create(request.getRequestURI()));
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(problem);
    }

    private static ResponseEntity<ProblemDetail> problem(
            HttpStatus status, BayPayException ex, HttpServletRequest request) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, ex.getMessage());
        problem.setTitle(ex.code().name());
        problem.setType(URI.create("https://baypay.example/errors/" + ex.code().name()));
        problem.setProperty("code", ex.code().name());
        problem.setInstance(URI.create(request.getRequestURI()));
        return ResponseEntity.status(status).body(problem);
    }
}
