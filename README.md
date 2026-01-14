
# THIS IS A PRE-ALPHA OF THE PROJECT. IN ORDER TO MAKE IT WORK YOU HAVE TO NEED SOME KNOWLEDGE OF THE SUBJECT 


# OBS Whisper Subtitles Generator

Automatic **offline** subtitles generator for videos recorded with OBS, powered by **Whisper (GPU)**.

This project extracts the microphone audio track from OBS recordings, transcribes it locally using OpenAI Whisper, and generates **optimized SRT subtitles** with a strict character limit per line for better readability.

---

## ✨ Features

- 🎙️ Extracts **microphone audio track** directly from OBS recordings (via FFmpeg)
- ⚡ GPU-accelerated transcription using **Whisper**
- 🇪🇸 Spanish transcription with **word-level timestamps**
- 📝 Automatic JSON → SRT conversion
- 📏 Custom subtitle formatter with **max 12 characters per line**
- 📦 Batch processing of multiple videos
- 🔒 Fully **offline** workflow (no cloud uploads, no subscriptions)

---

## 📁 Project Structure

```
obs-whisper-subtitles/
├── transcribir.py          # Main pipeline: video → audio → Whisper → SRT
├── script_format_srt.py    # Custom JSON → SRT formatter (12 chars per line)
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

### System
- Windows
- NVIDIA GPU with CUDA support

### Software
- **Python 3.9+**
- **FFmpeg** (must be available in PATH)
- **Whisper** (CLI version)

### Python dependencies
Whisper CLI installation (recommended via pip):

```bash
pip install -U openai-whisper
```

Make sure `ffmpeg` works from the command line:

```bash
ffmpeg -version
```

---

## 🎥 OBS Setup (Important)

This project assumes that:

- Your videos are recorded with **OBS**
- The **microphone audio** is recorded on a **separate audio track**

### Default configuration used in this project

- **Microphone track index:** `:a:00`

If your microphone is on a different OBS audio track, update this line in `transcribir.py`:

```python
MICROPHONE_STREAM = ":a:00"
```

---

## 📂 Input / Output Directories

Edit these paths in `transcribir.py` if needed:

```python
INPUT_DIR = Path(r"C:\\Users\\Snake\\Desktop\\transcripcion\\videos")
OUTPUT_DIR = Path(r"C:\\Users\\Snake\\Desktop\\transcripcion\\transcript_files")
```

- **INPUT_DIR** → place your OBS video files here
- **OUTPUT_DIR** → generated JSON and SRT files will be saved here

Supported video formats:
- `.mp4`
- `.avi`
- `.mov`
- `.mkv`

---

## 🚀 Usage

### 1️⃣ Place your videos

Copy your OBS recordings into the input directory:

```
INPUT_DIR/
├── video1.mp4
├── video2.mkv
```

### 2️⃣ Run the transcription pipeline

From the project directory:

```bash
python transcribir.py
```

### 3️⃣ Output

For each video, the pipeline will:

1. Extract microphone audio
2. Transcribe audio using Whisper
3. Generate a JSON transcript
4. Convert it into an optimized SRT file

Example output:

```
OUTPUT_DIR/
├── video1.json
├── video1_12chars.srt
├── video2.json
├── video2_12chars.srt
```

---

## 📝 Subtitle Formatting Logic

- Subtitles are built **word by word** using Whisper timestamps
- Lines are automatically split when they exceed **12 characters**
- Timing is preserved accurately between words
- Designed for **short, readable captions**, ideal for clips and social media

---

## ⚠️ Notes & Limitations

- Whisper model is currently set to:

```python
WHISPER_MODEL = "medium"
```

You can change it to `small`, `large`, etc., depending on your hardware.

- This project is optimized for **Spanish** transcription:

```bash
--language es
```

---

## 🧠 Why This Project?

This tool was built to:

- Avoid paid transcription services
- Maintain full privacy
- Speed up subtitle creation for video clips
- Provide consistent, readable subtitle formatting

---

## 📜 License

This project is provided as-is for personal and educational use.

---

## 🙌 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- FFmpeg

---

Happy transcribing 🚀