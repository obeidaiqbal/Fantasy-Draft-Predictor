import pandas as pd
import sqlite3
import os


def make_tables():
    list = ["PG", "SG", "SF", "PF", "C"]
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + "/" + "Predictions2026.db")
    cur = conn.cursor()
    for pos in list:
        cur.execute("SELECT * FROM Predictions2026 WHERE Pos = ?", (pos,))
        tbl = cur.fetchall()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {pos} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Player TEXT,
                Pos TEXT,
                FPTS REAL,
                FPTS_26 REAL
            )
        """)
        for player in tbl:
            cur.execute(f"INSERT OR IGNORE INTO {pos} (id, Player, Pos, FPTS, FPTS_26) VALUES (?, ?, ?, ?, ?)", player)
        conn.commit()
    conn.close()

def main():
    make_tables()

if __name__=="__main__":
    main()