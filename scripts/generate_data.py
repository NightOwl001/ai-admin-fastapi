#!/usr/bin/env python
"""批量生成 10 万条用户测试数据并写入 user 表。"""

import random
import string
import subprocess
import sys
import time
from datetime import datetime, timedelta

# 1. 自动检查并安装 faker
try:
    from faker import Faker
except ImportError:
    print("未检测到 faker，正在通过 pip 自动安装...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
    from faker import Faker

from sqlalchemy.orm import Session

from model.entity import User
from utils.db import SessionLocal
from utils.jwt_util import hash_password

TOTAL_COUNT = 100_000
BATCH_SIZE = 1000
USERNAME_MIN_LEN = 8
USERNAME_MAX_LEN = 12
DEFAULT_PASSWORD = "123456"
HALF_YEAR_DAYS = 182  # 最近半年


def random_username(length: int) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


def generate_unique_username(used: set[str]) -> str:
    while True:
        length = random.randint(USERNAME_MIN_LEN, USERNAME_MAX_LEN)
        username = random_username(length)
        if username not in used:
            used.add(username)
            return username


def random_create_time() -> datetime:
    """最近半年内的随机时间"""
    now = datetime.now()
    days_ago = random.randint(0, HALF_YEAR_DAYS)
    return now - timedelta(
        days=days_ago,
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )


def build_batch(
    batch_size: int,
    used_usernames: set[str],
    fake: Faker,
    hashed_pwd: str,
) -> list[dict]:
    return [
        {
            "username": generate_unique_username(used_usernames),
            "password": hashed_pwd,
            "nickname": fake.name(),
            "create_time": random_create_time(),
            "is_deleted": False,
        }
        for _ in range(batch_size)
    ]


def generate_data(total: int = TOTAL_COUNT, batch_size: int = BATCH_SIZE) -> None:
    fake = Faker("zh_CN")
    used_usernames: set[str] = set()

    print(f"开始生成 {total:,} 条用户数据，每批 {batch_size} 条...")
    print("正在使用项目 bcrypt 加密默认密码 '123456'（仅加密一次，全量复用）...")
    hashed_pwd = hash_password(DEFAULT_PASSWORD)

    db: Session = SessionLocal()
    start_time = time.perf_counter()
    inserted = 0

    try:
        while inserted < total:
            current_batch = min(batch_size, total - inserted)
            batch_data = build_batch(current_batch, used_usernames, fake, hashed_pwd)

            db.bulk_insert_mappings(User, batch_data)
            db.commit()

            inserted += current_batch
            elapsed = time.perf_counter() - start_time
            progress = inserted / total * 100
            speed = inserted / elapsed if elapsed > 0 else 0.0
            print(
                f"进度: {inserted:,}/{total:,} ({progress:.1f}%) | "
                f"已用时间: {elapsed:.1f}s | "
                f"速度: {speed:.0f} 条/s"
            )

        total_elapsed = time.perf_counter() - start_time
        print(f"\n完成！共插入 {inserted:,} 条用户数据，总耗时 {total_elapsed:.1f}s")
    except Exception as e:
        db.rollback()
        print(f"插入失败: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_data()