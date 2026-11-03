import shutil
from pathlib import Path

def main():
    src_dir = Path("trader-skill")
    dst_dir = Path(r"C:\Users\sugat\.gemini\config\skills")
    
    trader_folders = [d for d in src_dir.iterdir() if d.is_dir() and d.name.startswith("trader-")]
    print(f"Found {len(trader_folders)} trader skills:")
    
    for folder in trader_folders:
        target = dst_dir / folder.name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(folder, target)
        print(f"  [+] Installed {folder.name} -> {target}")

if __name__ == "__main__":
    main()
