"""Database layer — SQLite (tests) or PostgreSQL (Docker stack)."""

from __future__ import annotations

import json
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Generator

try:
    import psycopg
    from psycopg.rows import dict_row
except ImportError:  # pragma: no cover
    psycopg = None  # type: ignore[assignment]
    dict_row = None  # type: ignore[assignment]

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "scripts" / "schema.sql"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class IdempotencyRow:
    tenant_id: str
    idempotency_key: str
    request_hash: str
    status: str
    response_status: int | None
    response_body: dict[str, Any] | None
    stripe_payment_intent_id: str | None


class Database:
    """Supports sqlite:// paths and postgresql:// URLs."""

    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self._is_sqlite = dsn.startswith("sqlite:")
        self._lock = threading.Lock()

    def migrate(self) -> None:
        if self._is_sqlite:
            with self._sqlite_conn() as conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS idempotency_keys (
                        tenant_id TEXT NOT NULL,
                        idempotency_key TEXT NOT NULL,
                        request_hash TEXT NOT NULL,
                        status TEXT NOT NULL,
                        response_status INTEGER,
                        response_body TEXT,
                        stripe_payment_intent_id TEXT,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        PRIMARY KEY (tenant_id, idempotency_key)
                    );
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id TEXT PRIMARY KEY,
                        tenant_id TEXT NOT NULL,
                        amount_cents INTEGER NOT NULL,
                        currency TEXT NOT NULL,
                        stripe_payment_intent_id TEXT UNIQUE,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS webhook_events (
                        event_id TEXT PRIMARY KEY,
                        payload TEXT NOT NULL,
                        processed_at TEXT
                    );
                    """
                )
        else:
            with self._pg_conn() as conn:
                conn.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
                conn.commit()

    @contextmanager
    def _sqlite_conn(self) -> Generator[sqlite3.Connection, None, None]:
        path = self.dsn.replace("sqlite:", "", 1)
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def _pg_conn(self) -> Generator[Any, None, None]:
        if psycopg is None:
            raise RuntimeError("psycopg not installed")
        conn = psycopg.connect(self.dsn, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    @contextmanager
    def connection(self) -> Generator[Any, None, None]:
        with self._lock:
            if self._is_sqlite:
                with self._sqlite_conn() as conn:
                    yield conn
            else:
                with self._pg_conn() as conn:
                    yield conn

    def get_idempotency(self, tenant_id: str, key: str) -> IdempotencyRow | None:
        with self.connection() as conn:
            if self._is_sqlite:
                row = conn.execute(
                    """
                    SELECT tenant_id, idempotency_key, request_hash, status,
                           response_status, response_body, stripe_payment_intent_id
                    FROM idempotency_keys WHERE tenant_id = ? AND idempotency_key = ?
                    """,
                    (tenant_id, key),
                ).fetchone()
                if not row:
                    return None
                body = json.loads(row["response_body"]) if row["response_body"] else None
                return IdempotencyRow(
                    row["tenant_id"],
                    row["idempotency_key"],
                    row["request_hash"],
                    row["status"],
                    row["response_status"],
                    body,
                    row["stripe_payment_intent_id"],
                )
            row = conn.execute(
                """
                SELECT tenant_id, idempotency_key, request_hash, status,
                       response_status, response_body, stripe_payment_intent_id
                FROM idempotency_keys WHERE tenant_id = %s AND idempotency_key = %s
                """,
                (tenant_id, key),
            ).fetchone()
            if not row:
                return None
            return IdempotencyRow(
                row["tenant_id"],
                row["idempotency_key"],
                row["request_hash"],
                row["status"],
                row["response_status"],
                row["response_body"],
                row["stripe_payment_intent_id"],
            )

    def insert_processing(
        self, tenant_id: str, key: str, request_hash: str
    ) -> bool:
        """Returns False if key already exists."""
        now = _utcnow().isoformat()
        with self.connection() as conn:
            try:
                if self._is_sqlite:
                    conn.execute(
                        """
                        INSERT INTO idempotency_keys
                        (tenant_id, idempotency_key, request_hash, status,
                         created_at, updated_at)
                        VALUES (?, ?, ?, 'processing', ?, ?)
                        """,
                        (tenant_id, key, request_hash, now, now),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO idempotency_keys
                        (tenant_id, idempotency_key, request_hash, status)
                        VALUES (%s, %s, %s, 'processing')
                        """,
                        (tenant_id, key, request_hash),
                    )
                return True
            except sqlite3.IntegrityError:
                return False
            except Exception as exc:
                if psycopg and "UniqueViolation" in type(exc).__name__:
                    return False
                if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
                    return False
                raise

    def complete_idempotency(
        self,
        tenant_id: str,
        key: str,
        response_status: int,
        response_body: dict[str, Any],
        stripe_payment_intent_id: str,
    ) -> None:
        body_json = json.dumps(response_body)
        now = _utcnow().isoformat()
        with self.connection() as conn:
            if self._is_sqlite:
                conn.execute(
                    """
                    UPDATE idempotency_keys
                    SET status = 'completed', response_status = ?, response_body = ?,
                        stripe_payment_intent_id = ?, updated_at = ?
                    WHERE tenant_id = ? AND idempotency_key = ?
                    """,
                    (
                        response_status,
                        body_json,
                        stripe_payment_intent_id,
                        now,
                        tenant_id,
                        key,
                    ),
                )
            else:
                conn.execute(
                    """
                    UPDATE idempotency_keys
                    SET status = 'completed', response_status = %s, response_body = %s,
                        stripe_payment_intent_id = %s, updated_at = NOW()
                    WHERE tenant_id = %s AND idempotency_key = %s
                    """,
                    (
                        response_status,
                        json.dumps(response_body),
                        stripe_payment_intent_id,
                        tenant_id,
                        key,
                    ),
                )

    def insert_order(
        self,
        tenant_id: str,
        amount_cents: int,
        currency: str,
        stripe_payment_intent_id: str,
        status: str = "completed",
    ) -> str:
        order_id = f"ord_{uuid.uuid4().hex[:12]}"
        now = _utcnow().isoformat()
        with self.connection() as conn:
            if self._is_sqlite:
                conn.execute(
                    """
                    INSERT INTO orders
                    (order_id, tenant_id, amount_cents, currency,
                     stripe_payment_intent_id, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        order_id,
                        tenant_id,
                        amount_cents,
                        currency,
                        stripe_payment_intent_id,
                        status,
                        now,
                    ),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO orders
                    (order_id, tenant_id, amount_cents, currency,
                     stripe_payment_intent_id, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        order_id,
                        tenant_id,
                        amount_cents,
                        currency,
                        stripe_payment_intent_id,
                        status,
                    ),
                )
        return order_id

    def count_orders(self) -> int:
        with self.connection() as conn:
            if self._is_sqlite:
                row = conn.execute("SELECT COUNT(*) AS c FROM orders").fetchone()
                return int(row["c"])
            row = conn.execute("SELECT COUNT(*) AS c FROM orders").fetchone()
            return int(row["c"])

    def list_stuck_processing(self, older_than_seconds: float) -> list[IdempotencyRow]:
        rows: list[IdempotencyRow] = []
        with self.connection() as conn:
            if self._is_sqlite:
                cur = conn.execute(
                    "SELECT tenant_id, idempotency_key, request_hash, status, "
                    "response_status, response_body, stripe_payment_intent_id "
                    "FROM idempotency_keys WHERE status = 'processing'"
                )
                for row in cur.fetchall():
                    rows.append(
                        IdempotencyRow(
                            row["tenant_id"],
                            row["idempotency_key"],
                            row["request_hash"],
                            row["status"],
                            row["response_status"],
                            json.loads(row["response_body"]) if row["response_body"] else None,
                            row["stripe_payment_intent_id"],
                        )
                    )
            else:
                cur = conn.execute(
                    """
                    SELECT tenant_id, idempotency_key, request_hash, status,
                           response_status, response_body, stripe_payment_intent_id
                    FROM idempotency_keys
                    WHERE status = 'processing'
                      AND updated_at < NOW() - (%s || ' seconds')::interval
                    """,
                    (str(int(older_than_seconds)),),
                )
                for row in cur.fetchall():
                    rows.append(
                        IdempotencyRow(
                            row["tenant_id"],
                            row["idempotency_key"],
                            row["request_hash"],
                            row["status"],
                            row["response_status"],
                            row["response_body"],
                            row["stripe_payment_intent_id"],
                        )
                    )
        return rows

    def mark_webhook_processed(self, event_id: str, payload: dict[str, Any]) -> bool:
        """Returns False if event_id already processed."""
        now = _utcnow().isoformat()
        with self.connection() as conn:
            try:
                if self._is_sqlite:
                    conn.execute(
                        """
                        INSERT INTO webhook_events (event_id, payload, processed_at)
                        VALUES (?, ?, ?)
                        """,
                        (event_id, json.dumps(payload), now),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO webhook_events (event_id, payload, processed_at)
                        VALUES (%s, %s, NOW())
                        """,
                        (event_id, json.dumps(payload)),
                    )
                return True
            except Exception as exc:
                if "unique" in str(exc).lower() or "duplicate" in str(exc).lower():
                    return False
                raise
