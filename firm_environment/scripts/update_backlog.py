import sqlite3

def update_backlog():
    db_path = "firm_environment/storage/autonomous_backlog.db"
    with sqlite3.connect(db_path) as conn:
        # Mark upload task as COMPLETED
        conn.execute("""
            UPDATE tasks 
            SET status = 'COMPLETED' 
            WHERE title LIKE '%Rutube%' OR title LIKE '%Upload%' OR assigned_subagent = 'AUTONOMOUS_CONTENT_PUBLISHER'
        """)
        
        # Insert next autonomous tasks
        conn.execute("""
            INSERT INTO tasks (title, assigned_subagent, priority, finops_score, status, payload_json)
            VALUES (
                'Rutube Channel Traffic & Audience Tracker',
                'AUTONOMOUS_CONTENT_PUBLISHER',
                1,
                85.0,
                'IN_PROGRESS',
                '{"channel_id": "74595918", "video": "antigravity_v25_promo.mp4", "action": "track_views_and_funnel"}'
            )
        """)
        
        conn.execute("""
            INSERT INTO tasks (title, assigned_subagent, priority, finops_score, status, payload_json)
            VALUES (
                'Quantum Arbitrage Cycle & L2 Spread Scanner',
                'QUANTUM_SCOUT',
                2,
                92.5,
                'QUEUED',
                '{"bridge": "trader_quantum_bridge.py", "universe_size": 16, "action": "scan_l2_spreads"}'
            )
        """)
        conn.commit()
        
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, assigned_subagent, status, finops_score FROM tasks ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        print("Updated tasks in autonomous_backlog.db:")
        for r in rows:
            print(" ", r)

if __name__ == "__main__":
    update_backlog()
