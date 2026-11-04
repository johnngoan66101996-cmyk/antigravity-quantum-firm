import sqlite3
import json
from pathlib import Path

def get_detailed_report():
    desktop = Path(r"C:\Users\sugat\OneDrive\Desktop")
    
    # 1. executed_trades from trading_system.db
    for db in desktop.glob("**/trading_system.db"):
        print(f"=== DB: {db} ===")
        with sqlite3.connect(db) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM executed_trades ORDER BY rowid DESC LIMIT 10")
            rows = cur.fetchall()
            for r in rows:
                print("DB Trade:", dict(r))
                
    # 2. trade_journal.json
    for j in desktop.glob("**/trade_journal.json"):
        print(f"\n=== Journal: {j} ===")
        with open(j, "r", encoding="utf-8") as f:
            data = json.load(f)
            trades = data if isinstance(data, list) else data.get("trades", [])
            for t in trades[-10:]:
                print("Journal Trade:", t)
        break

if __name__ == "__main__":
    get_detailed_report()
