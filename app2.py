import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import whisper
import deepl
import os
import time
import logging

# Save log to user LOCALAPPDATA
log_dir = os.getenv('LOCALAPPDATA', os.getcwd())
log_file = os.path.join(log_dir, "WhisperTranslator", "app.log")

# Make sure folder exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Now setup logging
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s %(levelname)s:%(message)s")

# === Constants ===
MAX_RETRIES = 3
WHISPER_MODELS = ["tiny", "small", "medium", "large"]
DEEPL_LANGUAGES = {
    "English": "EN", "German": "DE", "French": "FR", "Spanish": "ES", "Italian": "IT",
    "Dutch": "NL", "Polish": "PL", "Portuguese": "PT-PT", "Russian": "RU", "Japanese": "JA",
    "Chinese": "ZH", "Finnish": "FI", "Swedish": "SV", "Norwegian": "NB", "Danish": "DA",
    "Czech": "CS", "Turkish": "TR", "Korean": "KO", "Arabic": "AR", "Hindi": "HI",
    "Ukrainian": "UK", "Vietnamese": "VI", "Greek": "EL", "Hungarian": "HU", "Romanian": "RO",
    "Hebrew": "HE", "Thai": "TH", "Indonesian": "ID", "Slovak": "SK"
}

# === Helper Functions ===
def split_text_for_subtitles(text):
    """Split text at sentences and also at manual line breaks (\n)"""
    text = text.replace('\n', '.\n')  # Treat newlines as soft sentence breaks
    lines = text.split('.')
    return [line.strip() for line in lines if line.strip()]

def translate_with_retries(translator, text, target_lang):
    """Try to translate text, retry if fails"""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return translator.translate_text(text, target_lang=target_lang).text
        except Exception as e:
            logging.error(f"Translation failed (attempt {attempt}): {e}")
            time.sleep(1)

    return None  # All retries failed

# === GUI Class ===
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Whisper + DeepL Translator")
        self.audio_path = ""
        self.output_folder = ""
        self.api_key = ""
        self.translator = None

        self.setup_gui()

    def setup_gui(self):
        # File Selection
        ttk.Label(root, text="Select Video File:").pack(pady=(10, 0))
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.pack(pady=5)
        ttk.Button(root, text="Browse Video", command=self.select_file).pack()

        # Output Folder
        ttk.Label(root, text="Select Output Folder:").pack(pady=(10, 0))
        self.folder_entry = tk.Entry(root, width=50)
        self.folder_entry.pack(pady=5)
        ttk.Button(root, text="Browse Folder", command=self.select_folder).pack()

        # API Key
        ttk.Label(root, text="DeepL Free API Key:").pack(pady=(10, 0))
        self.api_entry = tk.Entry(root, width=50, show="*")
        self.api_entry.pack(pady=5)

        # Whisper Model Selection
        ttk.Label(root, text="Whisper Model:").pack(pady=(10, 0))
        self.model_var = tk.StringVar(value="base")
        self.model_menu = ttk.Combobox(root, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly")
        self.model_menu.pack(pady=5)

        # Target Language Selection
        ttk.Label(root, text="Target Translation Language:").pack(pady=(10, 0))
        self.lang_var = tk.StringVar(value="Dutch")
        self.lang_menu = ttk.Combobox(root, textvariable=self.lang_var, values=list(DEEPL_LANGUAGES.keys()), state="readonly")
        self.lang_menu.pack(pady=5)

        # Dark Mode
        self.dark_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme).pack(pady=(10, 0))

        # Start Button
        self.start_button = ttk.Button(root, text="Start", command=self.start)
        self.start_button.pack(pady=(20, 10))

        # Progress Bar and Status
        self.progress = ttk.Progressbar(root, length=400, mode="determinate")
        self.progress.pack(pady=5)
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=5)

    def select_file(self):
        filetypes = (("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*"))
        self.audio_path = filedialog.askopenfilename(title="Select Video File", filetypes=filetypes)
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, self.audio_path)

    def select_folder(self):
        self.output_folder = filedialog.askdirectory(title="Select Output Folder")
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, self.output_folder)

    def toggle_theme(self):
        if self.dark_mode.get():
            root.configure(bg="#2e2e2e")
            style = ttk.Style()
            style.theme_use('clam')
            style.configure(".", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
        else:
            root.configure(bg="SystemButtonFace")
            style = ttk.Style()
            style.theme_use('default')

    def start(self):
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        try:
            self.start_button.config(state=tk.DISABLED)
            self.progress["value"] = 0
            self.update_status("Starting...")

            self.api_key = self.api_entry.get().strip()
            if not self.api_key:
                messagebox.showerror("Error", "Please provide a DeepL API Key.")
                self.start_button.config(state=tk.NORMAL)
                return

            self.translator = deepl.Translator(self.api_key)

            model_name = self.model_var.get()
            target_language = DEEPL_LANGUAGES[self.lang_var.get()]

            # Step 1: Transcribe
            self.update_status("Transcribing...")
            model = whisper.load_model(model_name)
            result = model.transcribe(self.audio_path, language="en")
            text = result["text"]
            self.progress["value"] = 40

            # Step 2: Split Text
            sentences = split_text_for_subtitles(text)
            self.update_status("Translating...")
            self.progress["value"] = 50

            # Step 3: Translate sentences
            translated_sentences = []
            for idx, sentence in enumerate(sentences):
                translated = translate_with_retries(self.translator, sentence, target_language)
                if translated is None:
                    user_choice = messagebox.askretrycancel("Translation Failed", "Translation failed 3 times. Retry?")
                    if user_choice:
                        translated = translate_with_retries(self.translator, sentence, target_language)
                    else:
                        skip = messagebox.askyesno("Skip Sentence?", "Skip this sentence and continue?")
                        if skip:
                            translated = sentence  # Keep original
                        else:
                            self.update_status("Cancelled by user.")
                            self.start_button.config(state=tk.NORMAL)
                            return
                translated_sentences.append(translated)

                self.progress["value"] = 50 + 50 * (idx+1) / len(sentences)
                self.root.update_idletasks()

            # Step 4: Save to .srt
            self.update_status("Saving file...")
            output_name = os.path.splitext(os.path.basename(self.audio_path))[0] + "_translated.srt"
            output_path = os.path.join(self.output_folder, output_name)

            with open(output_path, "w", encoding="utf-8") as f:
                for i, line in enumerate(translated_sentences, start=1):
                    f.write(f"{i}\n00:00:00,000 --> 00:00:05,000\n{line}\n\n")

            self.progress["value"] = 100
            self.update_status(f"Done! Saved: {output_path}")
            logging.info(f"Finished successfully. Output: {output_path}")
        except Exception as e:
            logging.exception("Fatal error during process")
            messagebox.showerror("Error", str(e))
        finally:
            self.start_button.config(state=tk.NORMAL)

    def update_status(self, msg):
        self.status_label.config(text=msg)
        logging.info(msg)

# === Main ===
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    app = TranslatorApp(root)
    root.mainloop()
