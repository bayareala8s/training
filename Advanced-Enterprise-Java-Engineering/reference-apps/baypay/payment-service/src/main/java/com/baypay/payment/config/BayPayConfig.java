package com.baypay.payment.config;

import com.baypay.payment.application.PaymentAuthorizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Clock;

@Configuration
public class BayPayConfig {

    @Bean
    Clock clock() {
        return Clock.systemUTC();
    }

    @Bean
    PaymentAuthorizer paymentAuthorizer() {
        return new PaymentAuthorizer.DefaultPaymentAuthorizer();
    }
}
