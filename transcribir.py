import subprocess
import sys
import os
import shutil
from pathlib import Path
import warnings

# --- SUPRESION DE ADVERTENCIAS ---
warnings.filterwarnings("ignore", category=UserWarning, message="Failed to launch Triton kernels.*") 

# --- CONFIGURACIÓN DE RUTAS ---
INPUT_DIR = Path(r"C:\Users\Snake\Desktop\transcripcion\videos")
OUTPUT_DIR = Path(r"C:\Users\Snake\Desktop\transcripcion\transcript_files")
TEMP_DIR = OUTPUT_DIR / "temp_audio"
WHISPER_MODEL = "medium"

# --- Pista 3 de OBS (Tu Micrófono) ---
MICROPHONE_STREAM = ":a:00" 

SUPPORTED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']

def process_single_video(video_path: Path):
    video_filename = video_path.stem
    TEMP_DIR.mkdir(exist_ok=True)
    temp_audio_path = TEMP_DIR / f"{video_filename}_mic.wav"
    
    print(f"🎬 Aislando micro de: {video_path.name}...")
    try:
        # Extraer pista 3
        subprocess.run([
            "ffmpeg", "-i", str(video_path),
            "-map", MICROPHONE_STREAM,
            "-acodec", "pcm_s16le", "-vn",
            str(temp_audio_path)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"🎤 Transcribiendo con Whisper GPU...")
        whisper_json_path = OUTPUT_DIR / f"{video_filename}_mic.json"

        # Ejecutar Whisper
        subprocess.run([
            "whisper", str(temp_audio_path),
            "--model", WHISPER_MODEL,
            "--language", "es",
            "--task", "transcribe",
            "--suppress_tokens", "50357,50361", # Evita el "Suscribite al canal"
            "--output_format", "json",
            "--word_timestamps", "True",
            "--output_dir", str(OUTPUT_DIR)
        ], check=True)
        
        # Renombrar y Formatear
        final_json_path = OUTPUT_DIR / f"{video_filename}.json"
        if whisper_json_path.exists():
            whisper_json_path.rename(final_json_path)
            
            script_path = Path(sys.argv[0]).parent / "script_format_srt.py"
            subprocess.run([
                sys.executable, str(script_path),
                str(final_json_path), str(OUTPUT_DIR)
            ], check=True)
            print(f"✔ ¡Listo!: {video_filename}")
            
    except Exception as e:
        print(f"❌ Error en {video_filename}: {e}")
    finally:
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    video_files = [p for ext in SUPPORTED_VIDEO_EXTENSIONS for p in INPUT_DIR.glob(f"*{ext}")]
    
    print(f"🚀 Procesando {len(video_files)} videos...")
    for video in video_files:
        process_single_video(video)
    print("--- Fin del proceso ---")