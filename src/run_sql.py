from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute a SQL script against the wastewater SQLite database.")
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--sql", type=Path, required=True)
    args = parser.parse_args()

    sql_text = args.sql.read_text(encoding="utf-8")
    with sqlite3.connect(args.db) as conn:
        conn.executescript(sql_text)
        conn.commit()

    print(f"Executed {args.sql} against {args.db}")


if __name__ == "__main__":
    main()
