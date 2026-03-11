#!/usr/bin/env python3
"""placeholder - Generate placeholder images, text, and test data.

Single-file, zero-dependency CLI.
"""

import sys
import argparse
import random
import json
import string
from datetime import datetime, timedelta


LOREM = "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua".split()
NAMES_F = ["Emma", "Olivia", "Ava", "Sophia", "Isabella", "Mia", "Charlotte", "Amelia", "Harper", "Evelyn"]
NAMES_M = ["Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas", "Henry", "Alexander"]
SURNAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
CITIES = ["New York", "London", "Tokyo", "Paris", "Berlin", "Sydney", "Toronto", "Mumbai", "São Paulo", "Cairo"]
COMPANIES = ["Acme Corp", "Globex", "Initech", "Umbrella", "Cyberdyne", "Stark Industries", "Wayne Enterprises", "Oscorp", "Tyrell Corp", "Weyland-Yutani"]


def cmd_text(args):
    r = random.Random(args.seed)
    for _ in range(args.paragraphs):
        sents = []
        for _ in range(r.randint(3, 6)):
            words = [r.choice(LOREM) for _ in range(r.randint(5, 15))]
            words[0] = words[0].capitalize()
            sents.append(" ".join(words) + ".")
        print(" ".join(sents))
        print()


def cmd_users(args):
    r = random.Random(args.seed)
    users = []
    for i in range(args.count):
        first = r.choice(NAMES_F + NAMES_M)
        last = r.choice(SURNAMES)
        user = {
            "id": i + 1, "name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@example.com",
            "age": r.randint(18, 75), "city": r.choice(CITIES),
            "company": r.choice(COMPANIES),
            "joined": (datetime(2020, 1, 1) + timedelta(days=r.randint(0, 2000))).strftime("%Y-%m-%d"),
            "active": r.random() > 0.2,
        }
        users.append(user)
    print(json.dumps(users, indent=2))


def cmd_csv(args):
    r = random.Random(args.seed)
    headers = ["id", "name", "email", "age", "city", "score"]
    print(",".join(headers))
    for i in range(args.rows):
        first = r.choice(NAMES_F + NAMES_M)
        last = r.choice(SURNAMES)
        print(f"{i+1},{first} {last},{first.lower()}.{last.lower()}@test.com,{r.randint(18,70)},{r.choice(CITIES)},{r.uniform(0,100):.1f}")


def cmd_sql(args):
    r = random.Random(args.seed)
    table = args.table
    print(f"CREATE TABLE {table} (")
    print(f"  id INTEGER PRIMARY KEY,")
    print(f"  name VARCHAR(100) NOT NULL,")
    print(f"  email VARCHAR(150) UNIQUE,")
    print(f"  age INTEGER,")
    print(f"  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    print(f");\n")
    for i in range(args.rows):
        first = r.choice(NAMES_F + NAMES_M)
        last = r.choice(SURNAMES)
        age = r.randint(18, 70)
        print(f"INSERT INTO {table} (name, email, age) VALUES ('{first} {last}', '{first.lower()}.{last.lower()}@test.com', {age});")


def main():
    p = argparse.ArgumentParser(prog="placeholder", description="Generate placeholder data")
    p.add_argument("-s", "--seed", type=int)
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("text", aliases=["t"], help="Lorem ipsum"); s.add_argument("-n", "--paragraphs", type=int, default=3)
    s = sub.add_parser("users", aliases=["u"], help="User JSON"); s.add_argument("-n", "--count", type=int, default=5)
    s = sub.add_parser("csv", help="CSV data"); s.add_argument("-n", "--rows", type=int, default=10)
    s = sub.add_parser("sql", help="SQL inserts"); s.add_argument("-n", "--rows", type=int, default=10); s.add_argument("--table", default="users")
    args = p.parse_args()
    if not args.cmd: p.print_help(); return 1
    cmds = {"text": cmd_text, "t": cmd_text, "users": cmd_users, "u": cmd_users, "csv": cmd_csv, "sql": cmd_sql}
    return cmds[args.cmd](args) or 0


if __name__ == "__main__":
    sys.exit(main())
