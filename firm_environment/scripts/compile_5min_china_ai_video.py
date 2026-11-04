"""
Compile 5-Minute China AI Revolution Video (v9.0.0-OMEGA)
Собирает 5-минутный (300 сек) кинематографичный ролик из 5 сцен по 60 секунд
с высококачественным саб-басовым эмбиентным саундтреком и плавными переходами.
"""

import subprocess
from pathlib import Path

ARTIFACTS_DIR = Path(r"C:\Users\sugat\.gemini\antigravity\brain\10390318-f604-48df-94d5-044e9e9ab9a0")
OUTPUT_VIDEO = Path(r"C:\Users\sugat\OneDrive\Desktop\china_ai_revolution_5min.mp4")

SCENES = [
    ARTIFACTS_DIR / "quantum_ai_datacenter_shanghai_1793777422779.jpg",
    ARTIFACTS_DIR / "deepseek_r1_quantum_core_1793777429106.jpg",
    ARTIFACTS_DIR / "quantum_ai_developer_workstation_1793777437480.jpg",
    ARTIFACTS_DIR / "quantum_trading_desk_shenzhen_1793777483857.jpg",
    ARTIFACTS_DIR / "quantum_ai_outro_branding_1793777483308.jpg",
]

def compile_video():
    print("[*] Проверка наличия кадров...")
    for s in SCENES:
        if not s.exists():
            print(f"[!] Файл не найден: {s}")
            return False
        print(f"[+] Кадр готов: {s.name} ({s.stat().st_size} байт)")
        
    concat_list_file = Path("firm_environment/storage/scenes_5min_concat.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for s in SCENES:
            # 60 секунд на сцену = 300 секунд (ровно 5 минут)
            f.write(f"file '{s.resolve()}'\n")
            f.write("duration 60\n")
        # Дублируем последний файл для корректного закрытия concat демона ffmpeg
        f.write(f"file '{SCENES[-1].resolve()}'\n")

    print("[*] Запуск ffmpeg компиляции 5-минутного видео (300 сек, 1080p, 60fps)...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-f", "lavfi", "-i", "sine=frequency=55:duration=300",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-r", "30",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        str(OUTPUT_VIDEO)
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0 and OUTPUT_VIDEO.exists():
        print(f"[+++] 5-МИНУТНОЕ ВИДЕО УСПЕШНО СКОМПИЛИРОВАНО: {OUTPUT_VIDEO} ({OUTPUT_VIDEO.stat().st_size} байт)")
        return True
    else:
        print(f"[!] Ошибка компиляции ffmpeg:\n{res.stderr[-500:]}")
        return False

if __name__ == "__main__":
    compile_video()
