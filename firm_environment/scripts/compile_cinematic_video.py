import subprocess
from pathlib import Path

def compile_video():
    brain_dir = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
    desktop_output = Path(r"C:\Users\sugat\OneDrive\Desktop\antigravity_v25_promo.mp4")
    storage_output = Path(r"firm_environment\storage\antigravity_v25_cinematic.mp4")
    
    s1 = brain_dir / "cybernetic_financial_data_stream_1793771807999.jpg"
    s2 = brain_dir / "scene_2_dual_ai_core_1793774031102.jpg"
    s3 = brain_dir / "scene_3_orderbook_spread_capture_1793774204899.jpg"
    s4 = brain_dir / "scene_4_cybernetic_vault_shield_1793774307929.jpg"
    s5 = brain_dir / "scene_5_algorithmic_trading_terminal_1793774386662.jpg"
    
    # Create input list for concat
    list_file = Path("firm_environment/storage/scenes_cinematic.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        f.write(f"file '{s1.resolve()}'\nduration 8\n")
        f.write(f"file '{s2.resolve()}'\nduration 10\n")
        f.write(f"file '{s3.resolve()}'\nduration 10\n")
        f.write(f"file '{s4.resolve()}'\nduration 10\n")
        f.write(f"file '{s5.resolve()}'\nduration 8\n")
        f.write(f"file '{s5.resolve()}'\n") # repeat last file as per ffmpeg concat spec
        
    # Generate video with synthetic high-tech ambient audio (sub-bass pulses + synth pulse)
    # Using ffmpeg lavfi audio synth: aevalsrc for deep sub-bass and drone
    audio_filter = "sine=frequency=60:duration=46"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-f", "lavfi", "-i", audio_filter,
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(storage_output)
    ]
    
    print("[*] Running ffmpeg compile...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[+] Video compiled successfully: {storage_output} ({storage_output.stat().st_size} bytes)")
        # Copy to Desktop
        import shutil
        shutil.copy2(storage_output, desktop_output)
        print(f"[+] Replaced Desktop video: {desktop_output} ({desktop_output.stat().st_size} bytes)")
    else:
        print("[-] ffmpeg failed:", res.stderr[-500:])

if __name__ == "__main__":
    compile_video()
