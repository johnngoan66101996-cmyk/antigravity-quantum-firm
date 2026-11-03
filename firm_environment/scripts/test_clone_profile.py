import os
import shutil
from pathlib import Path

def test_clone():
    edge_src = Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Edge" / "User Data" / "Default"
    dest = Path(os.environ["TEMP"]) / "edge_temp_profile" / "Default"
    
    if not edge_src.exists():
        print("Edge Default directory not found")
        return
        
    dest.mkdir(parents=True, exist_ok=True)
    
    # Copy essential state files
    items_to_copy = ["Network", "Local Storage", "Session Storage", "IndexedDB"]
    for item in items_to_copy:
        s = edge_src / item
        d = dest / item
        if s.exists():
            try:
                if s.is_dir():
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
                print(f"[+] Copied {item}")
            except Exception as e:
                print(f"[-] Could not copy {item}: {e}")

if __name__ == "__main__":
    test_clone()
