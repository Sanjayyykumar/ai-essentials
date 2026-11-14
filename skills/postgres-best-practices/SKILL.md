---
name: "postgres-best-practices"
description: "Postgres rules for schema design, migrations, indexes, queries, RLS, locking and connection pooling. Use before writing SQL/migrations or diagnosing slow queries, timeouts, locks or connection exhaustion."
---

# Postgres best practices

> Condensed from [supabase/agent-skills](https://github.com/supabase/agent-skills) (MIT).

Apply these before writing or changing anything in a Postgres database (also from Java/Spring/JPA/Hibernate code), and when diagnosing performance. Ordered by impact.

## 1. Query performance (CRITICAL)
- Index every column used in WHERE, JOIN and ORDER BY on large tables. Check with `EXPLAIN (ANALYZE, BUFFERS)`; a Seq Scan on a big table is the red flag.
- Composite indexes: equality columns first, then range/sort columns. `(tenant_id, created_at)` serves `WHERE tenant_id=? ORDER BY created_at`.
- Covering indexes: `CREATE INDEX ... (a) INCLUDE (b, c)` to get index-only scans.
- Partial indexes for hot subsets: `WHERE deleted_at IS NULL`, `WHERE status = 'pending'`.
- Pick the index type: B-tree default; GIN for JSONB, arrays, full-text; BRIN for huge append-only time-series; GiST for ranges/geo.

## 2. Connections (CRITICAL)
- Always pool (HikariCP in app; PgBouncer for many instances). Pool size ≈ (cores × 2) + spindles, not hundreds.
- Keep `max_connections` modest; set `idle_in_transaction_session_timeout` and `idle_session_timeout`.
- PgBouncer transaction mode breaks server-side prepared statements: use `prepareThreshold=0` in pgjdbc or PgBouncer ≥1.21 with `max_prepared_statements`.

## 3. Security & RLS (CRITICAL)
- Multi-tenant tables: `ALTER TABLE t ENABLE ROW LEVEL SECURITY` + policies on tenant_id; use `FORCE ROW LEVEL SECURITY` so owners are covered too.
- RLS performance: index the policy columns; wrap function calls as `(select current_setting(...))` / `(select auth.uid())` so they evaluate once, not per row; avoid joins inside policies (use security-definer helper functions).
- Least privilege: app role gets only needed grants; no superuser from the app; revoke PUBLIC defaults.
- Write tests that query as each role/tenant and assert rows from other tenants are invisible.

## 4. Schema design (HIGH)
- Types: `bigint` / `uuid` (v7 preferred for locality) PKs, `timestamptz` not `timestamp`, `text` over `varchar(n)`, `numeric` for money, `boolean`, `jsonb` not `json`.
- Prefer `bigint generated always as identity` or UUIDv7; random UUIDv4 PKs fragment indexes.
- Index every foreign key column (Postgres does not do it automatically).
- Lowercase snake_case identifiers; never quoted mixed-case.
- Partition very large tables (time-based) when maintenance/queries suffer.

## 5. Migrations & locking (MEDIUM-HIGH)
- Safe constraint adds: `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` separately; `CREATE INDEX CONCURRENTLY`; set `lock_timeout` in migrations.
- Make migrations idempotent (`IF NOT EXISTS`).
- Keep transactions short; never hold a transaction open across network/API calls.
- Prevent deadlocks by locking rows in a consistent order (e.g. `ORDER BY id FOR UPDATE`).
- Job queues: `SELECT ... FOR UPDATE SKIP LOCKED LIMIT n`.
- App-level mutexes: `pg_advisory_xact_lock(key)`.

## 6. Data access patterns (MEDIUM)
- Kill N+1: batch with `WHERE id = ANY(?)`, JOINs, or JPA `JOIN FETCH` / `@EntityGraph` / batch size.
- Cursor (keyset) pagination: `WHERE (created_at, id) < (?, ?) ORDER BY created_at DESC, id DESC LIMIT n` instead of large OFFSET.
- Bulk writes: multi-row INSERT, JDBC batching (`reWriteBatchedInserts=true`), or `COPY`.
- Upserts: `INSERT ... ON CONFLICT (key) DO UPDATE` instead of select-then-insert.

## 7. Monitoring (LOW-MEDIUM)
- Enable `pg_stat_statements`; sort by total_exec_time to find the top offenders.
- Watch autovacuum; run `ANALYZE` after bulk loads; check bloat and dead tuples.

## 8. Advanced
- Full-text: `tsvector` generated column + GIN index, `websearch_to_tsquery`; not `LIKE '%x%'`.
- JSONB: GIN (`jsonb_path_ops` for containment `@>`), or expression B-tree indexes on extracted keys.
- Vector search: pgvector with HNSW index.

Condensed from supabase/agent-skills `supabase-postgres-best-practices` (MIT).