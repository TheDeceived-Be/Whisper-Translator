# Whisper Translator App

This is a GUI application that uses **OpenAI Whisper** to transcribe video/audio files,  
then **DeepL API** to translate the transcription into another language, and saves it as `.srt` subtitles.

## Features

- 🎥 Transcribes **video files** (MP4, MKV, etc.)
- 🌐 Translates using **DeepL Free API** (user provides API key)
- 🧠 Whisper models: **tiny**, **small**, **medium**, **large**
- 💬 Saves subtitles as `.srt` files
- 🌙 Optional **Dark Mode**
- 🔁 Automatic retries if translation fails
- 🪵 Logs everything to `app.log`
- ⚡ Built with **Nuitka** for faster performance

## Requirements

- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt
