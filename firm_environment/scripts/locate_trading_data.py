import os
from pathlib import Path

def find_trades():
    desktop = Path(r"C:\Users\sugat\OneDrive\Desktop")
    print("Поиск баз данных и логов сделок...")
    
    # Search for sqlite db files or json trade logs
    all_dbs = list(desktop.glob("**/*.db")) + list(desktop.glob("**/*.sqlite*"))
    for db in all_dbs:
        if ".git" not in str(db):
            print("DB:", db)
            
    # Search for trade logs or history
    logs = list(desktop.glob("**/trade*.json")) + list(desktop.glob("**/deals*.json")) + list(desktop.glob("**/orders*.json"))
    for log in logs:
        if ".git" not in str(log):
            print("Log:", log)

if __name__ == "__main__":
    find_trades()
