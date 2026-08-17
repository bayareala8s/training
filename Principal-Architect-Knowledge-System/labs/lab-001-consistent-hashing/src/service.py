"""Ring service — simulations and stats for API/CLI."""

from __future__ import annotations

import copy
from typing import Any

from .ring import HashRing, hash_position, modulo_node, redistribution_ratio


class RingService:
    """Manages a hash ring with demo simulations."""

    def __init__(self) -> None:
        self.ring = HashRing()
        self.lookups_total = 0

    def add_node(self, node_id: str, vnode_count: int = 128) -> dict[str, Any]:
        self.ring.add_node(node_id, vnode_count)
        return {
            "node_id": node_id,
            "vnode_count": vnode_count,
            "ring_version": self.ring.ring_version,
            "nodes": self.ring.nodes(),
            "total_vnodes": self.ring.vnode_count(),
        }

    def remove_node(self, node_id: str) -> dict[str, Any]:
        if node_id not in self.ring.nodes():
            raise ValueError(f"node not found: {node_id}")
        self.ring.remove_node(node_id)
        return {
            "removed": node_id,
            "ring_version": self.ring.ring_version,
            "nodes": self.ring.nodes(),
            "total_vnodes": self.ring.vnode_count(),
        }

    def lookup(self, key: str) -> dict[str, Any]:
        self.lookups_total += 1
        return {
            "key": key,
            "hash": hash_position(key),
            "node": self.ring.get_node(key),
            "ring_version": self.ring.ring_version,
        }

    def balance_stats(self, key_count: int = 100_000) -> dict[str, Any]:
        if not self.ring.nodes():
            raise ValueError("ring is empty")
        counts: dict[str, int] = {n: 0 for n in self.ring.nodes()}
        for i in range(key_count):
            node = self.ring.get_node(f"item:{i}")
            counts[node] += 1
        mean = key_count / len(counts)
        variance = sum((c - mean) ** 2 for c in counts.values()) / len(counts)
        cv = (variance**0.5) / mean if mean else 0.0
        return {
            "key_count": key_count,
            "nodes": len(counts),
            "distribution": counts,
            "coefficient_of_variation": round(cv, 4),
        }

    def compare_churn(self, key_count: int = 5_000) -> dict[str, Any]:
        keys = [f"k:{i}" for i in range(key_count)]
        ring_before = copy.deepcopy(self.ring)
        ring_after = HashRing()
        for node in self.ring.nodes():
            ring_after.add_node(node, vnode_count=64)
        ring_after.add_node(f"n{len(self.ring.nodes())}", vnode_count=64)
        n_before = len(ring_before.nodes())
        n_after = len(ring_after.nodes())
        consistent = redistribution_ratio(keys, ring_before, ring_after)
        modulo_before = {k: modulo_node(k, n_before) for k in keys}
        modulo_after = {k: modulo_node(k, n_after) for k in keys}
        modulo = sum(1 for k in keys if modulo_before[k] != modulo_after[k]) / len(keys)
        return {
            "keys": key_count,
            "nodes_before": n_before,
            "nodes_after": n_after,
            "consistent_hashing_churn": round(consistent, 4),
            "modulo_hashing_churn": round(modulo, 4),
            "consistent_wins": consistent < modulo,
        }

    def node_failure_simulation(self, node_id: str, key_count: int = 10_000) -> dict[str, Any]:
        if node_id not in self.ring.nodes():
            raise ValueError(f"node not found: {node_id}")
        keys = [f"key:{i}" for i in range(key_count)]
        before = {k: self.ring.get_node(k) for k in keys}
        snapshot = copy.deepcopy(self.ring)
        snapshot.remove_node(node_id)
        after = {k: snapshot.get_node(k) for k in keys}
        moved = sum(1 for k in keys if before[k] != after[k])
        return {
            "failed_node": node_id,
            "keys_sampled": key_count,
            "keys_redistributed": moved,
            "redistribution_ratio": round(moved / key_count, 4),
            "expected_approx": round(1 / max(len(self.ring.nodes()), 1), 4),
        }

    def stats(self) -> dict[str, Any]:
        return {
            "nodes": self.ring.nodes(),
            "node_count": len(self.ring.nodes()),
            "total_vnodes": self.ring.vnode_count(),
            "ring_version": self.ring.ring_version,
            "lookups_total": self.lookups_total,
        }

    def seed_demo_cluster(self) -> None:
        if self.ring.nodes():
            return
        for node in ("node-a", "node-b", "node-c"):
            self.ring.add_node(node, vnode_count=128)
