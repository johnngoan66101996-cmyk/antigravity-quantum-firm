import sqlite3
import json
from pathlib import Path

def inspect_trading_system():
    desktop = Path(r"C:\Users\sugat\OneDrive\Desktop")
    
    # 1. Search for trading_system.db
    for db_path in desktop.glob("**/trading_system.db"):
        print(f"\n--- Reading {db_path} ---")
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [t[0] for t in cursor.fetchall()]
                print("Tables:", tables)
                for t in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {t}")
                    count = cursor.fetchone()[0]
                    print(f"Table {t}: {count} records")
                    cursor.execute(f"SELECT * FROM {t} ORDER BY rowid DESC LIMIT 10")
                    rows = cursor.fetchall()
                    for r in rows:
                        print("  ", r)
        except Exception as e:
            print("Error reading db:", e)
            
    # 2. Search for trade_journal.json
    for journal_path in desktop.glob("**/trade_journal.json"):
        print(f"\n--- Reading {journal_path} ---")
        try:
            with open(journal_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    print(f"Total entries: {len(data)}")
                    print("Last 10 entries:")
                    for entry in data[-10:]:
                        print("  ", entry)
                elif isinstance(data, dict):
                    print("Keys:", list(data.keys()))
                    trades = data.get("trades", data.get("history", []))
                    print(f"Total trades: {len(trades)}")
                    for entry in trades[-10:]:
                        print("  ", entry)
        except Exception as e:
            print("Error reading json:", e)

if __name__ == "__main__":
    inspect_trading_system()
