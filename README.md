# Whisper Translator App


[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)
[![Release](https://img.shields.io/badge/Release-v1.1.0-blue)](https://github.com/TheDeceived-Be/Whisper-Translator/releases)
[![Issues](https://img.shields.io/badge/Issues-0%20open-brightgreen)](https://github.com/TheDeceived-Be/Whisper-Translator/issues)
[![Stars](https://img.shields.io/github/stars/TheDeceived-Be/Whisper-Translator?style=social)](https://github.com/TheDeceived-Be/Whisper-Translator/stargazers)
[![Download](https://img.shields.io/badge/Download-Whisper--Translator-blue?logo=github)](https://github.com/TheDeceived-Be/Whisper-Translator/releases/latest)
[![Support me on Patreon](https://img.shields.io/badge/Support--me--on-Patreon-orange?style=for-the-badge&logo=patreon)](https://www.patreon.com/The_Deceived)


## Whisper Translator
---





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


🌐 Supported Languages


English

Spanish

French

German

Japanese

Chinese

Korean

Portuguese

Italian

Dutch

Russian

(and many more!)

(Depends on DeepL API and Whisper model support.)

---

## 🔑 Setting Up DeepL API

- Sign up at [DeepL API Free](https://www.deepl.com/pro-api).
- Copy your API key.
- Enter it into the app when prompted.

---

## 🛠️ Contributing

Pull requests are welcome! Feel free to open an issue if you have ideas for improvements.



---

## 💖 Support This Project

If you find **Whisper Translator** useful and want to support its development, consider becoming a patron!

Your support helps me continue maintaining and improving the app. Even a small contribution makes a big difference.

[![Support me on Patreon](https://img.shields.io/badge/Support--me--on-Patreon-orange?style=for-the-badge&logo=patreon)](https://www.patreon.com/The_Deceived)

---


## 📜 License

This project is licensed under the [MIT License](LICENSE).


---

## 📜 Changelog
| Version | Date         | Changes                                                                 |
|:-------:|:------------:|------------------------------------------------------------------------|
| v1.2    | 2025-04-16   | - Added support for importing multiple files at once<br>- Added "Cancel" button |
| v1.1    | 2025-04-11   | - Fixed subtitle timestamp formatting<br>- Improved dark mode readability<br>- General stability improvements |
| v1.0    | 2025-04-10   | - Initial release of Whisper Translator<br>- Transcribe and translate video files<br>- DeepL Free API integration<br>- Multithreaded GUI with progress bar<br>- Export subtitles in `.srt` format |

