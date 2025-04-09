# Whisper Translator App

**Whisper Translator** is a GUI app that uses **OpenAI Whisper** to transcribe video/audio files and the **DeepL API** to translate them into another language, saving subtitles as `.srt` files.

---

## ✨ Features

- 🎥 Transcribes **video files** (MP4, MKV, etc.)
- 🌍 Translates using **DeepL Free API** (user must provide API key)
- 🧐 Supports **Whisper models**: `tiny`, `small`, `medium`, `large`
- 📝 Saves subtitles as `.srt` files
- 🌙 Optional **Dark Mode**
- 🔄 Automatic retries if translation fails
- 💜 Logs all events to `app.log`
- ⚡ Built with **Nuitka** for faster performance

---

## 👅 Download

- [Download the latest release here](https://github.com/TheDeceived-Be/Whisper-Translator/releases/latest)

*(No Python installation needed. Just download and run the `.exe`!)*

---

## ⚙️ Requirements (for building yourself)

- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---


## 🚀 How to Use

1. Launch the app (`WhisperTranslator.exe`).
2. Select a video or audio file.
3. Enter your **DeepL API key** (you can get it [here](https://www.deepl.com/pro-api)).
4. Choose your target translation language.
5. Click **Start** — and the app will create a `.srt` subtitle file!

---

## 🔑 Setting Up DeepL API

- Sign up at [DeepL API Free](https://www.deepl.com/pro-api).
- Copy your API key.
- Enter it into the app when prompted.

---

## 🛠️ Contributing

Pull requests are welcome! Feel free to open an issue if you have ideas for improvements.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

