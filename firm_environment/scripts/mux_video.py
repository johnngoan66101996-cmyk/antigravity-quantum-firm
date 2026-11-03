"""
Сборка финального промо-видео Antigravity v2.5 через ffmpeg
"""

import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"

def assemble_video():
    concat_file = STORAGE_DIR / "concat_scenes.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for i in range(1, 6):
            f.write(f"file 'scene_{i}.png'\n")
            f.write("duration 6.7\n")
        f.write("file 'scene_5.png'\n")

    output_mp4 = STORAGE_DIR / "antigravity_v25_promo.mp4"
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", "concat_scenes.txt",
        "-i", "voice.wav",
        "-vf", "scale=1920:1080,fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        "antigravity_v25_promo.mp4"
    ]
    
    res = subprocess.run(cmd, cwd=str(STORAGE_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if output_mp4.exists() and output_mp4.stat().st_size > 10000:
        print(">>> ВИДЕОРОЛИК УСПЕШНО СКОМПИЛИРОВАН:", output_mp4)
        print("Размер файла:", output_mp4.stat().st_size, "байт")
        return output_mp4
    else:
        print("Ошибка сборки:", res.stderr)
        return None

if __name__ == "__main__":
    assemble_video()
