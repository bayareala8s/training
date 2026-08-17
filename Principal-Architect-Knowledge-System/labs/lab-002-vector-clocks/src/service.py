"""Vector clock simulation service for API/CLI."""

from __future__ import annotations

from typing import Any

from .clocks import CausalMailbox, Message, Process, Relation, VectorClock, compare


class ProcessNotFoundError(ValueError):
    """Raised when a process id is not registered."""


class ClockService:
    """Manages simulated processes, clocks, and causal delivery."""

    def __init__(self) -> None:
        self.num_processes = 0
        self.mailbox = CausalMailbox()
        self.processes: dict[int, Process] = {}
        self.events_total = 0
        self.messages_sent = 0

    def seed_demo_processes(self, num_processes: int = 2) -> None:
        if self.processes:
            return
        self._ensure_processes(num_processes)

    def _ensure_processes(self, num_processes: int) -> None:
        if num_processes < self.num_processes:
            raise ValueError(
                f"cannot shrink process count from {self.num_processes} to {num_processes}"
            )
        if num_processes > self.num_processes:
            for i in range(self.num_processes, num_processes):
                self.processes[i] = Process(
                    i, VectorClock(num_processes), self.mailbox
                )
            for proc in self.processes.values():
                proc.clock.size = num_processes
                if len(proc.clock.values) < num_processes:
                    proc.clock.values.extend(
                        [0] * (num_processes - len(proc.clock.values))
                    )
            self.num_processes = num_processes

    def local_event(self, process_id: int, num_processes: int = 2) -> dict[str, Any]:
        self._ensure_processes(num_processes)
        if process_id not in self.processes:
            raise ProcessNotFoundError(f"process not found: {process_id}")
        clock = self.processes[process_id].local_event()
        self.events_total += 1
        return {
            "process_id": process_id,
            "event": "local",
            "clock": clock.values,
        }

    def send_message(
        self, from_process: int, to: int, payload: Any, msg_id: str
    ) -> dict[str, Any]:
        if from_process not in self.processes or to not in self.processes:
            raise ProcessNotFoundError(
                f"process not found: sender={from_process}, recipient={to}"
            )
        sender = self.processes[from_process]
        recipient = self.processes[to]
        prior = len(self.mailbox.delivered)
        message = sender.send(recipient, payload, msg_id)
        newly = self.mailbox.delivered[prior:]
        for delivered in newly:
            if delivered.recipient is not None and delivered.recipient in self.processes:
                self.processes[delivered.recipient].receive(delivered)
        self.messages_sent += 1
        return {
            "msg_id": message.msg_id,
            "from": from_process,
            "to": to,
            "payload": payload,
            "clock": message.clock.values,
            "newly_delivered": [m.msg_id for m in newly],
        }

    def delivered_messages(self) -> dict[str, Any]:
        return {
            "delivered": [
                {
                    "msg_id": m.msg_id,
                    "sender": m.sender,
                    "payload": m.payload,
                    "clock": m.clock.values,
                }
                for m in self.mailbox.delivered
            ],
            "pending_count": len(self.mailbox.pending),
        }

    def compare_clocks(self, clock_a: list[int], clock_b: list[int]) -> dict[str, Any]:
        size = max(len(clock_a), len(clock_b))
        a = VectorClock(size, clock_a + [0] * (size - len(clock_a)))
        b = VectorClock(size, clock_b + [0] * (size - len(clock_b)))
        relation = compare(a, b)
        return {
            "clock_a": a.values,
            "clock_b": b.values,
            "relation": relation.value,
        }

    def list_processes(self) -> dict[str, Any]:
        return {
            "num_processes": self.num_processes,
            "processes": [
                {
                    "process_id": pid,
                    "clock": proc.clock.values,
                }
                for pid, proc in sorted(self.processes.items())
            ],
        }

    def stats(self) -> dict[str, Any]:
        return {
            "num_processes": self.num_processes,
            "events_total": self.events_total,
            "messages_sent": self.messages_sent,
            "delivered_count": len(self.mailbox.delivered),
            "pending_count": len(self.mailbox.pending),
        }
