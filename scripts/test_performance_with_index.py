#!/usr/bin/env python
"""索引创建 → 生效验证 → 性能测试 全流程脚本。"""

import time

from sqlalchemy import text

from utils.db import engine

RUNS = 5

INDEXES = [
    (
        "idx_nickname",
        "CREATE INDEX idx_nickname ON user (nickname)",
    ),
    (
        "uk_username",
        "CREATE UNIQUE INDEX uk_username ON user (username)",
    ),
]

EXPLAIN_QUERIES = [
    ("nickname 等值查询", "SELECT * FROM user WHERE nickname = '张三'"),
    ("username 等值查询", "SELECT * FROM user WHERE username = 'test123'"),
    ("username 模糊查询", "SELECT * FROM user WHERE username LIKE '%test%'"),
]

EXPLAIN_FIELDS = ("type", "possible_keys", "key", "rows", "Extra")

BENCHMARKS = [
    ("深分页查询", "SELECT * FROM user LIMIT 10 OFFSET 50000"),
    ("模糊查询", "SELECT * FROM user WHERE username LIKE '%test%'"),
    ("昵称精确查询", "SELECT * FROM user WHERE nickname = '张三'"),
]


def create_index(conn, sql: str, name: str) -> None:
    try:
        conn.execute(text(sql))
        conn.commit()
        print(f"[成功] {name} 索引创建完成")
    except Exception as e:
        conn.rollback()
        print(f"[跳过] {name} 索引已存在或创建失败: {e}")


def create_indexes(conn) -> None:
    for name, sql in INDEXES:
        create_index(conn, sql, name)


def run_explain(conn, sql: str, label: str) -> None:
    explain_sql = f"EXPLAIN {sql}"
    rows = conn.execute(text(explain_sql)).mappings().all()
    print(f"--- EXPLAIN: {label} ---")
    print(f"SQL: {sql}")
    for row in rows:
        for field in EXPLAIN_FIELDS:
            print(f"  {field}: {row.get(field)}")
    print()


def run_all_explains(conn) -> None:
    for label, sql in EXPLAIN_QUERIES:
        run_explain(conn, sql, label)


def trimmed_average(times: list[float]) -> float:
    trimmed = sorted(times)[1:-1]
    return sum(trimmed) / len(trimmed)


def disable_query_cache(conn) -> None:
    try:
        conn.execute(text("SET SESSION query_cache_type = OFF"))
    except Exception:
        pass


def run_benchmark(conn, label: str, sql: str) -> None:
    print(f"========== {label} ==========")
    print(f"SQL: {sql}")

    times: list[float] = []
    for i in range(1, RUNS + 1):
        start = time.perf_counter()
        result = conn.execute(text(sql))
        result.fetchall()
        elapsed_ms = (time.perf_counter() - start) * 1000
        times.append(elapsed_ms)
        print(f"第 {i} 次: {elapsed_ms:.2f} ms")

    avg_ms = trimmed_average(times)
    print(f"单次耗时列表: {[round(t, 2) for t in times]}")
    print(f"最终平均耗时(ms): {avg_ms:.2f}")
    print()


def main() -> None:
    with engine.connect() as conn:
        print("===== Step 1: 创建索引 =====")
        create_indexes(conn)
        print()

        print("===== Step 2: 验证索引生效 =====")
        run_all_explains(conn)

        print("===== Step 3: 性能测试 =====")
        disable_query_cache(conn)
        for label, sql in BENCHMARKS:
            run_benchmark(conn, label, sql)


if __name__ == "__main__":
    main()
