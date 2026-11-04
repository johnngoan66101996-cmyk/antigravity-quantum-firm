import sqlite3

def revert_publication():
    db_path = "firm_environment/storage/content_calendar.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            UPDATE publications 
            SET status = 'BUFFERED' 
            WHERE platform = 'Rutube' AND status = 'PUBLISHED'
        """)
        cursor = conn.cursor()
        cursor.execute("SELECT id, platform, title, status FROM publications WHERE platform = 'Rutube'")
        print("Reverted content_calendar:", cursor.fetchall())
        
    fleet_path = "firm_environment/storage/accounts_fleet.db"
    with sqlite3.connect(fleet_path) as conn:
        conn.execute("""
            UPDATE fleet_accounts 
            SET posts_published_count = 0 
            WHERE platform = 'Rutube'
        """)
        cursor = conn.cursor()
        cursor.execute("SELECT platform, channel_name, posts_published_count FROM fleet_accounts WHERE platform = 'Rutube'")
        print("Reverted fleet_accounts:", cursor.fetchall())

if __name__ == "__main__":
    revert_publication()
