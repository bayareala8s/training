package com.baypay.payment.config;

import com.baypay.shared.demo.DemoIds;
import com.baypay.shared.domain.Account;
import com.baypay.shared.domain.AccountStatus;
import com.baypay.shared.domain.Customer;
import com.baypay.shared.persistence.AccountRepository;
import com.baypay.shared.persistence.CustomerRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.time.Instant;

/**
 * Seeds Avery Chen and the two USD accounts used in every lab. Disabled on
 * {@code prod}. All names and amounts are synthetic.
 */
@Component
@Profile("!prod")
public class DemoDataSeeder implements ApplicationRunner {

    private static final Logger log = LoggerFactory.getLogger(DemoDataSeeder.class);

    private final CustomerRepository customers;
    private final AccountRepository accounts;

    public DemoDataSeeder(CustomerRepository customers, AccountRepository accounts) {
        this.customers = customers;
        this.accounts = accounts;
    }

    @Override
    public void run(ApplicationArguments args) {
        if (customers.existsById(DemoIds.CUSTOMER_AVERY)) {
            return;
        }
        Instant created = Instant.parse("2026-01-15T00:00:00Z");
        customers.save(new Customer(
                DemoIds.CUSTOMER_AVERY, "Avery Chen", "avery.chen@baypay.test", created));
        accounts.save(new Account(
                DemoIds.ACCOUNT_ACTIVE, DemoIds.CUSTOMER_AVERY, "USD", AccountStatus.ACTIVE, created));
        accounts.save(new Account(
                DemoIds.ACCOUNT_FROZEN, DemoIds.CUSTOMER_AVERY, "USD", AccountStatus.FROZEN, created));
        log.info("Seeded fictional BayPay customer Avery Chen with one ACTIVE and one FROZEN account");
    }
}
