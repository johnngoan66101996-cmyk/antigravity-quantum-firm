import sqlite3
import json

conn = sqlite3.connect("firm_environment/storage/accounts_fleet.db")
row = conn.execute("SELECT platform, channel_name, status, credentials_token FROM fleet_accounts WHERE platform = 'Rutube'").fetchone()

print("Platform:", row[0])
print("Channel:", row[1])
print("Status:", row[2])
if row[3]:
    print("Token length:", len(row[3]))
    print("Token snippet:", row[3][:100])
else:
    print("Token: NONE")
