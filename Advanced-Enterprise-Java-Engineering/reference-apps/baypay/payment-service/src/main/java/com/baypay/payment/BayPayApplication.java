package com.baypay.payment;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(scanBasePackages = "com.baypay")
@EntityScan(basePackages = "com.baypay")
@EnableJpaRepositories(basePackages = "com.baypay")
public class BayPayApplication {

    public static void main(String[] args) {
        SpringApplication.run(BayPayApplication.class, args);
    }
}
