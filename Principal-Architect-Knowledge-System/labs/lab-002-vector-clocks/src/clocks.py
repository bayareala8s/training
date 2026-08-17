"""Vector clocks, causal mailbox, and comparison primitives."""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any


class Relation(enum.Enum):
    BEFORE = "before"
    AFTER = "after"
    CONCURRENT = "concurrent"
    EQUAL = "equal"


@dataclass
class VectorClock:
    """Process-indexed vector clock."""

    size: int
    values: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.values:
            self.values = [0] * self.size

    def increment(self, process_id: int) -> None:
        self.values[process_id] += 1

    def merge(self, other: VectorClock) -> None:
        for i in range(self.size):
            self.values[i] = max(self.values[i], other.values[i])

    def copy(self) -> VectorClock:
        return VectorClock(self.size, self.values.copy())


def compare(a: VectorClock, b: VectorClock) -> Relation:
    """Compare two vector clocks."""
    if a.values == b.values:
        return Relation.EQUAL
    a_le_b = all(x <= y for x, y in zip(a.values, b.values))
    b_le_a = all(y <= x for x, y in zip(a.values, b.values))
    if a_le_b and not b_le_a:
        return Relation.BEFORE
    if b_le_a and not a_le_b:
        return Relation.AFTER
    return Relation.CONCURRENT


@dataclass
class Message:
    msg_id: str
    sender: int
    payload: Any
    clock: VectorClock
    recipient: int | None = None


@dataclass
class Process:
    process_id: int
    clock: VectorClock
    mailbox: CausalMailbox | None = None

    def local_event(self) -> VectorClock:
        self.clock.increment(self.process_id)
        return self.clock.copy()

    def send(self, target: Process, payload: Any, msg_id: str) -> Message:
        self.clock.increment(self.process_id)
        message = Message(
            msg_id, self.process_id, payload, self.clock.copy(), target.process_id
        )
        if target.mailbox:
            target.mailbox.submit(message)
        return message

    def receive(self, message: Message) -> None:
        self.clock.merge(message.clock)
        self.clock.increment(self.process_id)


@dataclass
class CausalMailbox:
    """Buffers messages until causal dependencies are satisfied."""

    delivered: list[Message] = field(default_factory=list)
    pending: list[Message] = field(default_factory=list)
    _delivered_vec: list[int] = field(default_factory=list)

    def submit(self, message: Message) -> list[Message]:
        """Submit message; return newly deliverable messages in order."""
        if not self._delivered_vec:
            self._delivered_vec = [0] * len(message.clock.values)
        self.pending.append(message)
        return self._try_deliver()

    def _try_deliver(self) -> list[Message]:
        newly: list[Message] = []
        changed = True
        while changed:
            changed = False
            for i, msg in enumerate(list(self.pending)):
                v = msg.clock.values
                s = msg.sender
                if v[s] != self._delivered_vec[s] + 1:
                    continue
                if any(v[j] > self._delivered_vec[j] + 1 for j in range(len(v)) if j != s):
                    continue
                self.pending.pop(i)
                self.delivered.append(msg)
                for j in range(len(v)):
                    self._delivered_vec[j] = max(self._delivered_vec[j], v[j])
                newly.append(msg)
                changed = True
                break
        return newly


@dataclass
class VersionVector:
    """Per-replica version counters for a data object."""

    values: dict[str, int] = field(default_factory=dict)

    def increment(self, replica_id: str) -> None:
        self.values[replica_id] = self.values.get(replica_id, 0) + 1
