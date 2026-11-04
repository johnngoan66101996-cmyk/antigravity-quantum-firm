import sqlite3
import json
from pathlib import Path

def inspect_trades():
    print("=== 1. ТОВАРНЫЙ И КВАНТОВЫЙ АРБИТРАЖ (products_arbitrage.db) ===")
    db_path = Path("firm_environment/storage/products_arbitrage.db")
    if db_path.exists():
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM arbitrage_pairs ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            print(f"Найдено записей: {len(rows)}")
            for r in rows:
                print(dict(r))
    else:
        print("База products_arbitrage.db не найдена.")

    print("\n=== 2. СКАЛЬПИНГ И БИРЖЕВЫЕ ОРДЕРА ===")
    # Check for trader/ or scalper files
    workspace_files = list(Path(".").glob("**/*order*.*")) + list(Path(".").glob("**/*trade*.*"))
    print("Найденные файлы сделок/ордеров:", [str(f) for f in workspace_files if "node_modules" not in str(f) and ".git" not in str(f)][:10])

if __name__ == "__main__":
    inspect_trades()
