"""Consistency service — API/CLI orchestration over replica cluster."""

from __future__ import annotations

from typing import Any

from .models import Cluster, ReadRepair, Replica, SessionState


class ConsistencyService:
    """Manages multi-replica eventual consistency simulation."""

    def __init__(self) -> None:
        self.cluster = Cluster(replicas={f"r{i}": Replica(replica_id=f"r{i}") for i in range(1, 4)})
        self.session = SessionState(sticky_replica="r1")
        self.read_repair = ReadRepair()
        self.replication_runs = 0
        self.delivered_total = 0
        self.repair_total = 0

    def put_key(self, key: str, value: Any, replica_id: str) -> dict[str, Any]:
        replica = self._replica(replica_id)
        if replica.replica_id in self.cluster.partitioned:
            raise ValueError(f"replica {replica_id} is partitioned")
        version = replica.put(key, value)
        self.session.record_write(version, key)
        return {
            "key": key,
            "value": value,
            "replica_id": replica_id,
            "version": version.values,
            "pending_events": len(replica.pending_out),
        }

    def get_key(self, key: str, replica_id: str, session_aware: bool = False) -> dict[str, Any]:
        replica = self._replica(replica_id)
        record = (
            self.session.read_your_writes(replica, key)
            if session_aware
            else replica.get(key)
        )
        if record is None:
            return {
                "key": key,
                "replica_id": replica_id,
                "found": False,
                "value": None,
                "version": None,
            }
        return {
            "key": key,
            "replica_id": replica_id,
            "found": True,
            "value": record.value,
            "version": record.version.values,
            "tombstone": record.tombstone,
        }

    def run_replication(self) -> dict[str, Any]:
        pending_before = sum(len(r.pending_out) for r in self.cluster.replicas.values())
        delivered = self.cluster.replicate_pending()
        self.replication_runs += 1
        self.delivered_total += delivered
        pending_after = sum(len(r.pending_out) for r in self.cluster.replicas.values())
        return {
            "replication_run": self.replication_runs,
            "delivered": delivered,
            "pending_before": pending_before,
            "pending_after": pending_after,
            "partitioned": sorted(self.cluster.partitioned),
        }

    def converge(self) -> dict[str, Any]:
        ok = self.cluster.converge()
        values = {}
        for rid, replica in self.cluster.replicas.items():
            rec = replica.get("user:1")
            if rec:
                values[rid] = rec.value
        return {"converged": ok, "sample_key_user_1": values}

    def set_partition(self, replicas: list[str], enabled: bool) -> dict[str, Any]:
        for rid in replicas:
            if rid not in self.cluster.replicas:
                raise ValueError(f"unknown replica: {rid}")
            if enabled:
                self.cluster.partitioned.add(rid)
            else:
                self.cluster.partitioned.discard(rid)
        return {
            "partitioned": sorted(self.cluster.partitioned),
            "enabled": enabled,
            "replicas": replicas,
        }

    def read_repair_key(self, key: str) -> dict[str, Any]:
        latest = self.cluster.quorum_read(key, r=2)
        if latest is None:
            return {"key": key, "repaired": 0, "reason": "insufficient quorum"}
        repairs = self.read_repair.repair(key, list(self.cluster.replicas.values()), latest)
        self.repair_total += repairs
        return {
            "key": key,
            "repaired": repairs,
            "value": latest.value,
            "version": latest.version.values,
        }

    def stats(self) -> dict[str, Any]:
        pending = {rid: len(r.pending_out) for rid, r in self.cluster.replicas.items()}
        key_counts = {rid: len(r.store) for rid, r in self.cluster.replicas.items()}
        return {
            "replicas": list(self.cluster.replicas.keys()),
            "pending_events": pending,
            "key_counts": key_counts,
            "replication_runs": self.replication_runs,
            "delivered_total": self.delivered_total,
            "repair_total": self.repair_total,
            "partitioned": sorted(self.cluster.partitioned),
            "loss_rate": self.cluster.loss_rate,
        }

    def _replica(self, replica_id: str) -> Replica:
        replica = self.cluster.replicas.get(replica_id)
        if replica is None:
            raise ValueError(f"unknown replica: {replica_id}")
        return replica
