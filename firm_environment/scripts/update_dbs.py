import sqlite3

# 1. content_calendar.db
try:
    conn = sqlite3.connect("content_calendar.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS content_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT,
        channel_id TEXT,
        title TEXT,
        status TEXT,
        video_path TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        published_at TIMESTAMP
    )
    """)
    c.execute("""
    INSERT INTO content_items (platform, channel_id, title, status, video_path, published_at)
    VALUES ('rutube', '74595918', 'ANTIGRAVITY v2.5: Промышленный торговый комплекс и квантовые агенты L2', 'IN_MODERATION', 'C:\\Users\\sugat\\OneDrive\\Desktop\\antigravity_v25_promo.mp4', CURRENT_TIMESTAMP)
    """)
    conn.commit()
    conn.close()
    print("content_calendar.db updated successfully.")
except Exception as e:
    print("content_calendar error:", e)

# 2. accounts_fleet.db
try:
    conn = sqlite3.connect("accounts_fleet.db")
    c = conn.cursor()
    c.execute("UPDATE accounts SET posts_published_count = posts_published_count + 1 WHERE platform = 'rutube'")
    conn.commit()
    conn.close()
    print("accounts_fleet.db updated successfully.")
except Exception as e:
    print("accounts_fleet error:", e)

# 3. autonomous_backlog.db
try:
    conn = sqlite3.connect("autonomous_backlog.db")
    c = conn.cursor()
    c.execute("""
    INSERT INTO backlog (task_name, category, priority, status)
    VALUES ('RUTUBE_MODERATION_MONITOR', 'MONETIZATION', 'HIGH', 'IN_PROGRESS')
    """)
    conn.commit()
    conn.close()
    print("autonomous_backlog.db updated successfully.")
except Exception as e:
    print("autonomous_backlog error:", e)
