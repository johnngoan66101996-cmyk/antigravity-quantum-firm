"""
Database Initializer for Autonomous Firm Environment (v9.0.0-OMEGA)
Создание и верификация всех 6 локальных баз данных SQLite.
"""

import sqlite3
import os
from pathlib import Path

STORAGE_DIR = Path(__file__).resolve().parent.parent / "storage"

def init_all_databases():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. autonomous_backlog.db
    backlog_path = STORAGE_DIR / "autonomous_backlog.db"
    with sqlite3.connect(backlog_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                assigned_subagent TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                finops_score REAL DEFAULT 50.0,
                status TEXT CHECK(status IN ('QUEUED', 'IN_PROGRESS', 'WAITING_HUMAN', 'COMPLETED', 'ARCHIVED')) DEFAULT 'QUEUED',
                payload_json TEXT,
                human_action_required TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")
        
    # 2. products_arbitrage.db
    arbitrage_path = STORAGE_DIR / "products_arbitrage.db"
    with sqlite3.connect(arbitrage_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS arbitrage_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku_name TEXT NOT NULL,
                category TEXT NOT NULL,
                donor_source TEXT NOT NULL,
                donor_url TEXT,
                donor_buy_price REAL NOT NULL,
                retail_showcase TEXT NOT NULL,
                retail_sell_price REAL NOT NULL,
                logistics_cost REAL NOT NULL,
                mp_fee_rate REAL NOT NULL,
                net_profit_unit REAL NOT NULL,
                net_margin_percent REAL NOT NULL,
                roi_percent REAL NOT NULL,
                finops_score REAL NOT NULL,
                status TEXT CHECK(status IN ('DISCOVERED', 'SCORED', 'ACTIVE_PROJECT', 'REJECTED')) DEFAULT 'DISCOVERED',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    # 3. accounts_fleet.db
    accounts_path = STORAGE_DIR / "accounts_fleet.db"
    with sqlite3.connect(accounts_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fleet_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL, -- Rutube, VK, Telegram, Avito, Ozon, WB
                account_handle TEXT NOT NULL,
                channel_name TEXT NOT NULL,
                status TEXT CHECK(status IN ('PROVISIONING_REQUESTED', 'WARMUP', 'ACTIVE', 'RESTRICTED', 'BANNED')) DEFAULT 'PROVISIONING_REQUESTED',
                niche TEXT NOT NULL,
                bio_text TEXT,
                avatar_prompt TEXT,
                credentials_token TEXT,
                daily_posts_limit INTEGER DEFAULT 3,
                posts_published_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    # 4. content_calendar.db
    content_path = STORAGE_DIR / "content_calendar.db"
    with sqlite3.connect(content_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS publications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                platform TEXT NOT NULL,
                title TEXT NOT NULL,
                body_content TEXT NOT NULL,
                media_type TEXT DEFAULT 'video_clip',
                cta_link_or_text TEXT,
                status TEXT CHECK(status IN ('DRAFT', 'BUFFERED', 'PUBLISHED', 'FAILED')) DEFAULT 'DRAFT',
                scheduled_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    # 5. chat_crm.db
    chat_path = STORAGE_DIR / "chat_crm.db"
    with sqlite3.connect(chat_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dialog_threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                user_sender_id TEXT NOT NULL,
                untrusted_incoming_text TEXT NOT NULL,
                safety_check_passed BOOLEAN DEFAULT 1,
                bot_response_text TEXT NOT NULL,
                qualification_stage TEXT DEFAULT 'GREETING_AND_NEED',
                lead_status TEXT CHECK(lead_status IN ('NEW', 'QUALIFIED', 'OFFER_SENT', 'CONVERTED', 'SCAM_BLOCKED')) DEFAULT 'NEW',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    # 6. blacklist.db
    blacklist_path = STORAGE_DIR / "blacklist.db"
    with sqlite3.connect(blacklist_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS blacklist_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_type TEXT NOT NULL, -- 'supplier', 'keyword', 'user_id', 'product_sku'
                entity_value TEXT NOT NULL,
                reason TEXT NOT NULL,
                stop_factor_code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    print(f"Все 6 баз данных SQLite успешно инициализированы в: {STORAGE_DIR}")

if __name__ == "__main__":
    init_all_databases()
