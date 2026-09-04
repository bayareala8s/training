package com.baypay.shared.persistence;

import com.baypay.shared.domain.NotificationRecord;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.UUID;

public interface NotificationRecordRepository extends JpaRepository<NotificationRecord, UUID> {
}
