"""Consistent hash ring with virtual nodes."""

from __future__ import annotations

import hashlib
from bisect import bisect_left
from dataclasses import dataclass, field


class RingEmptyError(LookupError):
    """Raised when lookup is attempted on an empty ring."""


def hash_position(value: str) -> int:
    """Stable 64-bit ring position from SHA-256."""
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], byteorder="big", signed=False)


@dataclass
class HashRing:
    """Consistent hash ring with virtual nodes."""

    _ring: dict[int, str] = field(default_factory=dict)
    _sorted_positions: list[int] = field(default_factory=list)
    ring_version: int = 0

    def add_node(self, node_id: str, vnode_count: int = 128) -> None:
        """Add a physical node with virtual node positions on the ring."""
        if node_id in set(self._ring.values()):
            return
        for i in range(vnode_count):
            pos = hash_position(f"{node_id}:{i}")
            self._ring[pos] = node_id
        self._rebuild_index()

    def remove_node(self, node_id: str) -> None:
        """Remove all virtual nodes belonging to a physical node."""
        to_remove = [pos for pos, nid in self._ring.items() if nid == node_id]
        for pos in to_remove:
            del self._ring[pos]
        self._rebuild_index()

    def get_node(self, key: str) -> str:
        """Return the physical node responsible for key."""
        if not self._sorted_positions:
            raise RingEmptyError("cannot resolve key on empty ring")
        pos = hash_position(key)
        idx = bisect_left(self._sorted_positions, pos)
        if idx == len(self._sorted_positions):
            idx = 0
        return self._ring[self._sorted_positions[idx]]

    def nodes(self) -> list[str]:
        return sorted(set(self._ring.values()))

    def vnode_count(self) -> int:
        return len(self._ring)

    def _rebuild_index(self) -> None:
        self._sorted_positions = sorted(self._ring.keys())
        self.ring_version += 1


def redistribution_ratio(keys: list[str], before: HashRing, after: HashRing) -> float:
    """Fraction of keys that changed owner between two ring states."""
    if not keys:
        return 0.0
    moved = sum(1 for k in keys if before.get_node(k) != after.get_node(k))
    return moved / len(keys)


def modulo_node(key: str, n: int) -> int:
    """Naive modulo partition for comparison."""
    return hash_position(key) % n
