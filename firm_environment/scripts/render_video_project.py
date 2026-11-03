"""
Генератор видеоролика Antigravity v2.5: синтез речи + киберпанк графика 1080p + сборка ffmpeg
"""

import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

FULL_TEXT = (
    "В микроструктуре современного крипторынка доли секунды решают всё. "
    "Миллионы ордеров, скрытые роботы и хаос биржевого стакана. Традиционные индикаторы опаздывают. "
    "Пришло время локального машинного интеллекта. "
    "Встречайте промышленный комплекс Antigravity два точка пять. "
    "Два специализированных локальных разума в едином контуре: легковесный Qwen круглосуточно сканирует стакан "
    "и выявляет спуфинг и айсберги, а стратегический мозг DeepSeek-R1 рассчитывает математическое преимущество. "
    "Математика Авелланеды-Стойкова и анализ дисбаланса стакана OBI. "
    "Вход строго из защищенной зоны Z2 аномальных свечей, стоп-лосс за плотностями крупных игроков и трехступенчатый вывод в безубыток. "
    "Никаких эмоций и тильта. Жесткий лимит риска — три процента капитала, аппаратный стоп двадцать пять базисных пунктов "
    "и автономный контур самоисцеления Actor-Critic. "
    "Antigravity. Полная автономность. Локальная мощность. Новая эра высокочастотного криптотрейдинга."
)

def synthesize_audio():
    # Работаем строго внутри папки storage через относительный путь
    wav_name = "voiceover.wav"
    ps_script = f'''
    Set-Location "{STORAGE_DIR.as_posix()}"
    Add-Type -AssemblyName System.Speech
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.SetOutputToWaveFile("{wav_name}")
    $text = @"
{FULL_TEXT}
"@
    $synth.Speak($text)
    $synth.Dispose()
    '''
    ps_file = STORAGE_DIR / "synth.ps1"
    ps_file.write_text(ps_script, encoding="utf-8-sig")
    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps_file)], check=True)
    wav_path = STORAGE_DIR / wav_name
    print("Аудиодорожка синтезирована:", wav_path)
    return wav_path

def create_cyberpunk_frame(title, subtitle, badge, accent_color, frame_idx):
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), color=(10, 14, 23))
    draw = ImageDraw.Draw(img)
    
    # Сетка и фон
    for x in range(0, w, 60):
        draw.line([(x, 0), (x, h)], fill=(18, 26, 42), width=1)
    for y in range(0, h, 60):
        draw.line([(0, y), (w, y)], fill=(18, 26, 42), width=1)
        
    # Декоративные неоновые рамки и углы HUD
    c = accent_color
    draw.rectangle([80, 80, w - 80, h - 80], outline=(30, 45, 70), width=2)
    # Угловые скобки
    corner_len = 50
    draw.line([(80, 80), (80 + corner_len, 80)], fill=c, width=4)
    draw.line([(80, 80), (80, 80 + corner_len)], fill=c, width=4)
    draw.line([(w - 80, 80), (w - 80 - corner_len, 80)], fill=c, width=4)
    draw.line([(w - 80, 80), (w - 80, 80 + corner_len)], fill=c, width=4)
    draw.line([(80, h - 80), (80 + corner_len, h - 80)], fill=c, width=4)
    draw.line([(80, h - 80), (80, h - 80 - corner_len)], fill=c, width=4)
    draw.line([(w - 80, h - 80), (w - 80 - corner_len, h - 80)], fill=c, width=4)
    draw.line([(w - 80, h - 80), (w - 80, h - 80 - corner_len)], fill=c, width=4)

    # Верхний бейдж
    draw.rectangle([120, 110, 520, 160], fill=(20, 32, 54), outline=c, width=2)
    draw.text((140, 125), f"SYSTEM: {badge}", fill=c)

    # Заголовок
    draw.text((120, 320), title, fill=(255, 255, 255))
    draw.text((120, 440), subtitle, fill=(160, 185, 220))
    
    # Визуализация данных внизу
    draw.rectangle([120, 680, w - 120, 920], fill=(13, 20, 35), outline=(25, 40, 65), width=2)
    draw.text((150, 710), "TELEMETRY & HARDWARE EXECUTION MATRIX", fill=(100, 140, 190))
    
    # Псевдо-свечи и графики
    for i in range(16):
        bx = 160 + i * 100
        candle_h = np.random.randint(40, 140)
        is_green = i % 2 == 0
        col = (0, 230, 140) if is_green else (255, 60, 90)
        draw.line([(bx + 20, 870 - candle_h - 20), (bx + 20, 890)], fill=col, width=2)
        draw.rectangle([bx + 10, 870 - candle_h, bx + 30, 870], fill=col)

    # Нижняя плашка
    draw.text((120, 960), "ANTIGRAVITY v2.5 | AUTONOMOUS HIGH-FREQUENCY CRYPTO FIRM | LOCAL ENGINE", fill=(80, 110, 150))
    
    out_path = STORAGE_DIR / f"scene_{frame_idx}.png"
    img.save(out_path)
    print("Кадр сохранён:", out_path)
    return out_path

def generate_scenes():
    scenes_data = [
        ("ХАОС РЫНКА И МИКРОСТРУКТУРА СТАКАНА", "Миллионы тиковых ордеров. Традиционные индикаторы опаздывают.", "MARKET_L2_ORDERBOOK", (0, 210, 255), 1),
        ("ДУЭТ НЕЙРОСЕТЕЙ: QWEN-2.5 & DEEPSEEK-R1", "Сверхбыстрый сканер аномалий + Стратегический вычислительный мозг CoT.", "DUAL_AI_CORE_ONLINE", (255, 190, 40), 2),
        ("МОДЕЛЬ АВЕЛЛАНЕДЫ-СТОЙКОВА И ЗОНЫ Z1-Z3", "Захват спреда, защита за плотностями $250k+ и трехуровневый безубыток.", "OBI_SPREAD_CAPTURE", (0, 255, 170), 3),
        ("АППАРАТНЫЙ РИСК-МЕНЕДЖМЕНТ (STOP-LOSS 25 BPS)", "Защитный купол: лимит риска 3% и автономный контур Actor-Critic.", "RISK_GOVERNANCE_ACTIVE", (255, 70, 90), 4),
        ("ПРОМЫШЛЕННЫЙ ТОРГОВЫЙ КОМПЛЕКС ANTIGRAVITY v2.5", "Полная автономность. Локальная мощность. Новая эра криптотрейдинга.", "ANTIGRAVITY_OFFICIAL", (180, 90, 255), 5)
    ]
    frame_files = []
    for t, s, b, c, idx in scenes_data:
        frame_files.append(create_cyberpunk_frame(t, s, b, c, idx))
    return frame_files

def render_final_video(audio_path, frames):
    output_mp4 = "antigravity_v25_promo.mp4"
    concat_txt = "concat.txt"
    
    with open(STORAGE_DIR / concat_txt, "w", encoding="utf-8") as f:
        for fr in frames:
            f.write(f"file '{fr.name}'\n")
            f.write("duration 9.5\n")
        f.write(f"file '{frames[-1].name}'\n")
        
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", concat_txt,
        "-i", "voiceover.wav",
        "-vf", "scale=1920:1080,fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    print("Запуск рендеринга видео через ffmpeg...")
    res = subprocess.run(cmd, cwd=str(STORAGE_DIR), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    out_file = STORAGE_DIR / output_mp4
    if out_file.exists() and out_file.stat().st_size > 1000:
        print(">>> ВИДЕОРОЛИК УСПЕШНО СКРОЕН И СРЕНДЕРЕН:", out_file)
        print("Размер файла:", out_file.stat().st_size, "байт")
        return out_file
    else:
        print("Ошибка рендеринга ffmpeg:", res.stderr)
        return None

if __name__ == "__main__":
    audio = synthesize_audio()
    frames = generate_scenes()
    render_final_video(audio, frames)
