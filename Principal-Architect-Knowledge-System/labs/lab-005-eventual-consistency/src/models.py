"""Core data models for eventual consistency simulation."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any


@dataclass
class VersionVector:
    values: dict[str, int] = field(default_factory=dict)

    def increment(self, replica_id: str) -> None:
        self.values[replica_id] = self.values.get(replica_id, 0) + 1

    def copy(self) -> VersionVector:
        return VersionVector(self.values.copy())

    def merge(self, other: VersionVector) -> None:
        for k, v in other.values.items():
            self.values[k] = max(self.values.get(k, 0), v)

    def dominates(self, other: VersionVector) -> bool:
        keys = set(self.values) | set(other.values)
        return all(self.values.get(k, 0) >= other.values.get(k, 0) for k in keys) and self.values != other.values

    def concurrent(self, other: VersionVector) -> bool:
        return not self.dominates(other) and not other.dominates(self) and self.values != other.values


@dataclass
class Record:
    value: Any
    version: VersionVector
    tombstone: bool = False


@dataclass
class ReplicationEvent:
    key: str
    record: Record
    source: str


@dataclass
class Replica:
    replica_id: str
    store: dict[str, Record] = field(default_factory=dict)
    pending_out: list[ReplicationEvent] = field(default_factory=list)

    def put(self, key: str, value: Any) -> VersionVector:
        version = VersionVector()
        if key in self.store:
            version.merge(self.store[key].version)
        version.increment(self.replica_id)
        record = Record(value=value, version=version)
        self.store[key] = record
        self.pending_out.append(ReplicationEvent(key, record, self.replica_id))
        return version.copy()

    def get(self, key: str) -> Record | None:
        return self.store.get(key)

    def apply_replication(self, event: ReplicationEvent) -> bool:
        """Idempotent apply; return True if state changed."""
        existing = self.store.get(event.key)
        incoming = event.record
        if existing is None:
            self.store[event.key] = Record(
                value=incoming.value,
                version=VersionVector(incoming.version.values.copy()),
                tombstone=incoming.tombstone,
            )
            return True
        if existing.version.dominates(incoming.version):
            return False
        if incoming.version.concurrent(existing.version):
            merged = VersionVector(existing.version.values.copy())
            merged.merge(incoming.version)
            merged.increment(self.replica_id)
            self.store[event.key] = Record(
                value=f"{existing.value}|{incoming.value}",
                version=merged,
                tombstone=incoming.tombstone,
            )
            return True
        if incoming.version.dominates(existing.version):
            self.store[event.key] = Record(
                value=incoming.value,
                version=VersionVector(incoming.version.values.copy()),
                tombstone=incoming.tombstone,
            )
            return True
        return False


@dataclass
class SessionState:
    sticky_replica: str
    last_token: dict[str, dict[str, int]] = field(default_factory=dict)

    def read_your_writes(self, replica: Replica, key: str) -> Record | None:
        record = replica.get(key)
        if record is None:
            return None
        token = self.last_token.get(key, {})
        for rid, ver in record.version.values.items():
            if ver < token.get(rid, 0):
                return None
        return record

    def record_write(self, version: VersionVector, key: str) -> None:
        self.last_token[key] = version.values.copy()


@dataclass
class Cluster:
    replicas: dict[str, Replica]
    replication_delay_ms: float = 0.0
    loss_rate: float = 0.0
    partitioned: set[str] = field(default_factory=set)

    def replicate_pending(self) -> int:
        """Deliver pending replication events with simulated network."""
        delivered = 0
        for replica in self.replicas.values():
            if replica.replica_id in self.partitioned:
                continue
            pending = list(replica.pending_out)
            replica.pending_out.clear()
            for event in pending:
                if random.random() < self.loss_rate:
                    replica.pending_out.append(event)
                    continue
                for target in self.replicas.values():
                    if target.replica_id == replica.replica_id:
                        continue
                    if target.replica_id in self.partitioned:
                        continue
                    if target.apply_replication(event):
                        delivered += 1
        return delivered

    def converge(self, max_rounds: int = 100) -> bool:
        for _ in range(max_rounds):
            if not any(r.pending_out for r in self.replicas.values()):
                break
            self.replicate_pending()
        return not any(r.pending_out for r in self.replicas.values())

    def quorum_read(self, key: str, r: int) -> Record | None:
        responses = [rep.get(key) for rep in self.replicas.values() if rep.get(key)]
        if len(responses) < r:
            return None
        return max(responses, key=lambda rec: sum(rec.version.values.values()))


@dataclass
class ReadRepair:
    def repair(self, key: str, replicas: list[Replica], latest: Record) -> int:
        """Push latest record to lagging replicas; return repair count."""
        repairs = 0
        event = ReplicationEvent(key, latest, "read-repair")
        for replica in replicas:
            if replica.apply_replication(event):
                repairs += 1
        return repairs
