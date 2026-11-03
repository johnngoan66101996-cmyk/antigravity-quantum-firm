"""
Сохранение и верификация сессии Rutube через официальное API.
"""

import json
import sqlite3
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"

raw_cookie_str = """spid=1788450507072_560c00f67d48250f249395f4a105fed6_w7xuh0r21c6veksn; cid=9724557901788450508; wdpThemeId=dark2021; canary1={"tags_predicto":{"active":"A","term":[{"id":44,"label":"A","percent":100},{"id":45,"label":"B","percent":100}]},"new_player":{"active":"A","term":[{"id":50,"label":"A","percent":100},{"id":51,"label":"B","percent":100}]},"ds_player":{"active":"A","term":[{"id":87,"label":"A","percent":100},{"id":88,"label":"B","percent":100}]},"current_stage_ds":{"active":"A","term":[{"id":120,"label":"A","percent":100},{"id":121,"label":"B","percent":100}]}}; uuid=534fcbba-7844-4705-87fe-31184ceaa646; ajs_anonymous_id=65098b26-1830-4185-818a-20c81ff4d917; _ym_uid=1788934131740107331; _ym_d=1788934131; uxs_uid=78fb4720-ad3d-11f1-a290-47477bd8500a; session_id=9724557901788450508_1793731856361; _ym_isad=2; mdd=0; oxxfgh=fed3859d-64a6-4e11-85a6-714b4a865f8c%230%237776000000%2330000%231800000%2322820; uwyii=3ad79634-e993-4d7f-d66c-6afca98b24bd; visitorID=74595918; source_social=gid; csrftoken=cYoG4FJy0DETNi11i9Zbnw0v1OmQ7ANq; psid2=tv1upkliw6dh36osbi766tuuwhp7m9z1; uwyiert=0ec824b9-aa41-03f5-4c2e-0914d6dfb19a"""

def save_and_verify():
    # 1. Парсинг
    cookie_dict = {}
    for item in raw_cookie_str.split(";"):
        if "=" in item:
            k, v = item.strip().split("=", 1)
            cookie_dict[k.strip()] = v.strip()
            
    session_file = STORAGE_DIR / "rutube_session.json"
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(cookie_dict, f, indent=2, ensure_ascii=False)
    print(f"Куки успешно сохранены в {session_file}. Всего параметров: {len(cookie_dict)}")
    
    # 2. Обновление accounts_fleet.db
    with sqlite3.connect(STORAGE_DIR / "accounts_fleet.db") as conn:
        conn.execute("""
            UPDATE fleet_accounts
            SET credentials_token = ?, status = 'ACTIVE', account_handle = 'channel/74595918'
            WHERE platform = 'Rutube'
        """, (json.dumps(cookie_dict),))
        conn.commit()
    print("Статус канала в accounts_fleet.db обновлен на ACTIVE!")
    
    # 3. Тестовый запрос к API Rutube
    url = "https://rutube.ru/api/video/person/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": raw_cookie_str,
        "Referer": "https://studio.rutube.ru/",
        "X-CSRFToken": cookie_dict.get("csrftoken", "")
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            code = res.getcode()
            body = res.read().decode("utf-8", errors="ignore")
            print(f"RUTUBE API TEST STATUS: {code}")
            print(f"RESPONSE PREVIEW: {body[:200]}...")
    except urllib.error.HTTPError as e:
        print(f"RUTUBE API HTTP ERROR: {e.code} - {e.reason}")
    except Exception as e:
        print(f"RUTUBE API ERROR: {e}")

if __name__ == "__main__":
    save_and_verify()
