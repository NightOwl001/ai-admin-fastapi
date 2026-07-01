#!/usr/bin/env python
"""无索引状态下的 SQL 查询性能基准测试。"""

import time

from sqlalchemy import text

from utils.db import engine

RUNS = 5

BENCHMARKS = [
    ("深分页查询", "SELECT * FROM user LIMIT 10 OFFSET 50000"),
    ("模糊查询", "SELECT * FROM user WHERE username LIKE '%test%'"),
    ("按昵称条件查询", "SELECT * FROM user WHERE nickname = '张三'"),
]


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


def run_all_benchmarks() -> None:
    with engine.connect() as conn:
        disable_query_cache(conn)
        for label, sql in BENCHMARKS:
            run_benchmark(conn, label, sql)


if __name__ == "__main__":
    run_all_benchmarks()
