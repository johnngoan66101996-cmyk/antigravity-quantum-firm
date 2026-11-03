import sqlite3

with sqlite3.connect("firm_environment/storage/accounts_fleet.db") as conn:
    conn.execute("""
        INSERT OR REPLACE INTO fleet_accounts (
            platform, account_handle, channel_name, status, niche, bio_text
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "GitHub",
        "johnngoan66101996-cmyk",
        "Виталий (JohnNGOAN66101996-CMYK)",
        "ACTIVE",
        "Open-Source / ИИ-Архитектура / Код агентов",
        "https://github.com/johnngoan66101996-cmyk"
    ))
    conn.commit()
    print("GitHub profile registered in accounts_fleet.db with status ACTIVE!")
