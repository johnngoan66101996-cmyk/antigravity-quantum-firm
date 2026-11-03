import urllib.request
import json

token = "9247111241:AAHf4ir2z_OHbnh3zj4Vk3P-AKd9GKP5kC8"
url = f"https://api.telegram.org/bot{token}/getUpdates"

req = urllib.request.urlopen(url, timeout=10)
data = json.loads(req.read().decode())
updates = data.get("result", [])
print(f"TOTAL UPDATES: {len(updates)}")
for u in updates:
    msg = u.get("message", {})
    chat = msg.get("chat", {})
    text = msg.get("text", "")
    print("FROM:", chat.get("first_name"), chat.get("id"), "LEN:", len(text))
    print("TEXT SNIPPET:", text[:120])
    print("---")
