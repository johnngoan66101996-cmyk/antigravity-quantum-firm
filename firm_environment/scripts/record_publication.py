import sqlite3
from datetime import datetime

def update_publication():
    db_path = "firm_environment/storage/content_calendar.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Check if there is already a buffered publication
    cursor.execute("SELECT id, platform, title, status FROM publications WHERE platform = 'Rutube'")
    rows = cursor.fetchall()
    print("Found existing Rutube publications:", rows)
    
    if rows:
        cursor.execute("""
            UPDATE publications 
            SET status = 'PUBLISHED' 
            WHERE platform = 'Rutube'
        """)
        print(f"[+] Updated {cursor.rowcount} publication(s) to PUBLISHED")
    else:
        cursor.execute("""
            INSERT INTO publications (account_id, platform, title, body_content, media_type, cta_link_or_text, status, scheduled_at)
            VALUES (1, 'Rutube', 
                    'ANTIGRAVITY v2.5: Промышленный торговый комплекс и квантовые агенты L2', 
                    'Демонстрация работы автономного квантово-когнитивного ядра и торговых агентов Antigravity v2.5. Репозиторий: https://github.com/johnngoan66101996-cmyk/antigravity-quantum-firm', 
                    'video_clip', 
                    'https://github.com/johnngoan66101996-cmyk/antigravity-quantum-firm', 
                    'PUBLISHED', ?)
        """, (now,))
        print("[+] Inserted new PUBLISHED publication record")
        
    # Also update accounts_fleet.db incrementing posts_published_count
    fleet_path = "firm_environment/storage/accounts_fleet.db"
    with sqlite3.connect(fleet_path) as f_conn:
        f_conn.execute("""
            UPDATE fleet_accounts 
            SET posts_published_count = posts_published_count + 1 
            WHERE platform = 'Rutube'
        """)
        f_cursor = f_conn.cursor()
        f_cursor.execute("SELECT platform, channel_name, posts_published_count FROM fleet_accounts WHERE platform = 'Rutube'")
        print("Updated Fleet Accounts:", f_cursor.fetchall())
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_publication()
