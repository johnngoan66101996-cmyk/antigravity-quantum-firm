import sqlite3

def update_rutube():
    with sqlite3.connect("firm_environment/storage/accounts_fleet.db") as conn:
        conn.execute("""
            UPDATE fleet_accounts
            SET account_handle = 'channel/74595918',
                channel_name = 'Квантовый ИИ: Claude Code, GPT & Нейросети',
                status = 'ACTIVE',
                bio_text = 'https://rutube.ru/channel/74595918'
            WHERE platform = 'Rutube'
        """)
        conn.commit()
        row = conn.execute("SELECT platform, account_handle, channel_name, status, bio_text FROM fleet_accounts WHERE platform = 'Rutube'").fetchone()
        print("RUTUBE RECORD UPDATED:", row)

if __name__ == "__main__":
    update_rutube()
