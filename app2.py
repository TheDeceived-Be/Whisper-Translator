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
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
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
    text = text.replace('\n', '.\n')
    lines = text.split('.')
    return [line.strip() for line in lines if line.strip()]

def translate_with_retries(translator, text, target_lang):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return translator.translate_text(text, target_lang=target_lang).text
        except Exception as e:
            logging.error(f"Translation failed (attempt {attempt}): {e}")
            time.sleep(1)
    return None

# === GUI Class ===
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Whisper + DeepL Translator")
        self.audio_paths = []
        self.output_folder = ""
        self.api_key = ""
        self.translator = None
        self.cancel_requested = False

        self.setup_gui()

    def setup_gui(self):
        ttk.Label(root, text="Select Video File(s):").pack(pady=(10, 0))
        self.file_entry = tk.Entry(root, width=50)
        self.file_entry.pack(pady=5)
        ttk.Button(root, text="Browse Video", command=self.select_files).pack()

        ttk.Label(root, text="Select Output Folder:").pack(pady=(10, 0))
        self.folder_entry = tk.Entry(root, width=50)
        self.folder_entry.pack(pady=5)
        ttk.Button(root, text="Browse Folder", command=self.select_folder).pack()

        ttk.Label(root, text="DeepL Free API Key:").pack(pady=(10, 0))
        self.api_entry = tk.Entry(root, width=50, show="*")
        self.api_entry.pack(pady=5)

        ttk.Label(root, text="Whisper Model:").pack(pady=(10, 0))
        self.model_var = tk.StringVar(value="base")
        self.model_menu = ttk.Combobox(root, textvariable=self.model_var, values=WHISPER_MODELS, state="readonly")
        self.model_menu.pack(pady=5)

        ttk.Label(root, text="Target Translation Language:").pack(pady=(10, 0))
        self.lang_var = tk.StringVar(value="Dutch")
        self.lang_menu = ttk.Combobox(root, textvariable=self.lang_var, values=list(DEEPL_LANGUAGES.keys()), state="readonly")
        self.lang_menu.pack(pady=5)

        self.dark_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(root, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme).pack(pady=(10, 0))

        self.start_button = ttk.Button(root, text="Start", command=self.start)
        self.start_button.pack(pady=(10, 5))

        self.cancel_button = ttk.Button(root, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=(0, 10))

        self.progress = ttk.Progressbar(root, length=400, mode="determinate")
        self.progress.pack(pady=5)
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=5)

    def select_files(self):
        filetypes = (("Video files", "*.mp4 *.mov *.avi *.mkv"), ("All files", "*.*"))
        self.audio_paths = filedialog.askopenfilenames(title="Select Video Files", filetypes=filetypes)
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, "; ".join(self.audio_paths))

    def select_folder(self):
        self.output_folder = filedialog.askdirectory(title="Select Output Folder")
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, self.output_folder)

    def toggle_theme(self):
        style = ttk.Style()
        if self.dark_mode.get():
            root.configure(bg="#2e2e2e")
            style.theme_use('clam')
            style.configure(".", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
            style.configure("TLabel", background="#2e2e2e", foreground="white")
            style.configure("TButton", background="#444444", foreground="white")
            style.configure("TEntry", fieldbackground="#3e3e3e", foreground="white")
        else:
            root.configure(bg="SystemButtonFace")
            style.theme_use('default')
            style.configure(".", background="SystemButtonFace", foreground="black")
            style.configure("TLabel", background="SystemButtonFace", foreground="black")
            style.configure("TButton", background="SystemButtonFace", foreground="black")
            style.configure("TEntry", fieldbackground="white", foreground="black")

    def start(self):
        self.cancel_requested = False
        threading.Thread(target=self.run_process, daemon=True).start()

    def cancel(self):
        self.cancel_requested = True
        self.update_status("Cancellation requested...")

    def run_process(self):
        try:
            self.start_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
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

            model = whisper.load_model(model_name)

            for file_index, path in enumerate(self.audio_paths):
                if self.cancel_requested:
                    self.update_status("Cancelled by user.")
                    break

                filename = os.path.basename(path)
                self.update_status(f"[{file_index + 1}/{len(self.audio_paths)}] Transcribing: {filename}")
                result = model.transcribe(path, language="en", word_timestamps=True)
                segments = result["segments"]
                for i, seg in enumerate(segments):
                    logging.debug(f"Segment {i+1}: {seg['start']} --> {seg['end']} | Text: {seg['text']}")

                self.progress["value"] = 40
                self.update_status("Translating...")
                self.progress["value"] = 50

                translated_segments = []
                for idx, segment in enumerate(segments):
                    if self.cancel_requested:
                        self.update_status("Cancelled by user.")
                        return

                    sentence = segment["text"]
                    if not sentence.strip():
                        continue
                    start_time = segment["start"]
                    end_time = segment["end"]

                    translated = translate_with_retries(self.translator, sentence, target_language)
                    if translated is None:
                        user_choice = messagebox.askretrycancel("Translation failed 3 times. Retry?")
                        if user_choice:
                            translated = translate_with_retries(self.translator, sentence, target_language)

                    if translated is None:
                        skip = messagebox.askyesno("Skip Sentence?", "Skip this sentence and continue?")
                        if skip:
                            translated = sentence
                        else:
                            self.update_status("Cancelled by user.")
                            self.start_button.config(state=tk.NORMAL)
                            return

                    translated_segments.append((start_time, end_time, translated))
                    self.progress["value"] = 50 + 50 * (idx + 1) / len(segments)
                    self.root.update_idletasks()

                self.update_status("Saving file...")
                output_name = os.path.splitext(os.path.basename(path))[0] + "_translated.srt"
                output_path = os.path.join(self.output_folder, output_name)

                with open(output_path, "w", encoding="utf-8") as f:
                    for idx, (start_time, end_time, sentence) in enumerate(translated_segments):
                        def format_srt_timestamp(seconds):
                            hours = int(seconds // 3600)
                            minutes = int((seconds % 3600) // 60)
                            secs = int(seconds % 60)
                            millis = int((seconds - int(seconds)) * 1000)
                            return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

                        start_timestamp = format_srt_timestamp(start_time)
                        end_timestamp = format_srt_timestamp(end_time)
                        f.write(f"{idx+1}\n{start_timestamp} --> {end_timestamp}\n{sentence}\n\n")

            self.progress["value"] = 100
            self.update_status("All files processed.")
            logging.info("Finished successfully.")

        except Exception as e:
            logging.exception("Fatal error during process")
            messagebox.showerror("Error", str(e))
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)

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
