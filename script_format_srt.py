import json
import sys
import os
from pathlib import Path

def format_timestamp(seconds):
    """Convierte segundos al formato de tiempo de SRT: HH:MM:SS,mmm"""
    td_hours = int(seconds // 3600)
    td_minutes = int((seconds % 3600) // 60)
    td_seconds = int(seconds % 60)
    td_milliseconds = int((seconds % 1) * 1000)
    return f"{td_hours:02}:{td_minutes:02}:{td_seconds:02},{td_milliseconds:03}"

def process_whisper_json(json_path, output_dir):
    json_path = Path(json_path)
    output_dir = Path(output_dir)
    
    if not json_path.exists():
        print(f"❌ No se encontró el JSON: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    words_list = []
    # Extraemos todas las palabras con sus tiempos
    for segment in data.get('segments', []):
        for word in segment.get('words', []):
            words_list.append({
                'word': word['word'].strip(),
                'start': word['start'],
                'end': word['end']
            })

    if not words_list:
        print(f"⚠ No se encontraron palabras en el JSON de {json_path.name}")
        return

    srt_lines = []
    current_line_words = []
    current_line_chars = 0
    line_count = 1

    for i, word_data in enumerate(words_list):
        word = word_data['word']
        start = word_data['start']
        end = word_data['end']

        # Si añadir la palabra supera los 12 caracteres, cerramos la línea actual
        if current_line_chars + len(word) + (1 if current_line_words else 0) > 12 and current_line_words:
            # Escribir línea SRT
            line_text = " ".join(current_line_words)
            line_start = format_timestamp(line_start_time)
            line_end = format_timestamp(line_end_time)
            
            srt_lines.append(f"{line_count}\n{line_start} --> {line_end}\n{line_text}\n")
            
            # Reset para la nueva línea
            line_count += 1
            current_line_words = []
            current_line_chars = 0

        # Si es el inicio de una nueva línea, guardamos el tiempo de inicio
        if not current_line_words:
            line_start_time = start
        
        current_line_words.append(word)
        current_line_chars += len(word) + (1 if len(current_line_words) > 1 else 0)
        line_end_time = end

    # Añadir la última línea si quedó algo pendiente
    if current_line_words:
        line_text = " ".join(current_line_words)
        srt_lines.append(f"{line_count}\n{format_timestamp(line_start_time)} --> {format_timestamp(line_end_time)}\n{line_text}\n")

    # Guardar el archivo final
    srt_filename = json_path.stem.replace("_mic", "") + "_12chars.srt"
    srt_path = output_dir / srt_filename
    
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(srt_lines))

    print(f"   ✔ SRT Formateado guardado en: {srt_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python script_format_srt.py <ruta_json> <directorio_salida>")
    else:
        process_whisper_json(sys.argv[1], sys.argv[2])