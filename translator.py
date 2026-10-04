"""
CodeAlpha Internship - Task 1: Language Translation Tool
Translates text between languages using deep-translator (Google Translate)
with a simple Tkinter GUI.
"""

import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from deep_translator import GoogleTranslator, MyMemoryTranslator

# {'english': 'en', 'telugu': 'te', ...}
LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
LANGUAGE_NAMES = sorted(name.title() for name in LANGUAGES)
SOURCE_OPTIONS = ["Auto Detect"] + LANGUAGE_NAMES


def get_code(display_name: str) -> str:
    """Convert a display name like 'Telugu' to a language code like 'te'."""
    if display_name == "Auto Detect":
        return "auto"
    return LANGUAGES[display_name.lower()]


def translate_text(text: str, source_name: str, target_name: str) -> str:
    """Translate text; try Google, then fall back to MyMemory.
    source_name / target_name are display names like 'Telugu' or 'Auto Detect'."""
    source = get_code(source_name)
    target = get_code(target_name)
    last_error = None
    for _ in range(2):
        try:
            return GoogleTranslator(source=source, target=target).translate(text)
        except Exception as e:  # e.g. rate limit (too many requests)
            last_error = e
            time.sleep(2)
    try:
        # MyMemory accepts full language names such as "english"
        src = "english" if source == "auto" else source_name.lower()
        return MyMemoryTranslator(source=src, target=target_name.lower()).translate(text)
    except Exception:
        raise last_error


class TranslatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Language Translation Tool - CodeAlpha")
        root.geometry("700x560")
        root.minsize(600, 480)

        main = ttk.Frame(root, padding=15)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Language Translation Tool",
                  font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))

        # Language selection row
        row = ttk.Frame(main)
        row.pack(fill="x", pady=5)

        ttk.Label(row, text="From:").pack(side="left")
        self.source_var = tk.StringVar(value="Auto Detect")
        ttk.Combobox(row, textvariable=self.source_var, values=SOURCE_OPTIONS,
                     state="readonly", width=18).pack(side="left", padx=(5, 15))

        ttk.Button(row, text="⇄ Swap", width=8,
                   command=self.swap_languages).pack(side="left")

        ttk.Label(row, text="To:").pack(side="left", padx=(15, 0))
        self.target_var = tk.StringVar(value="Telugu")
        ttk.Combobox(row, textvariable=self.target_var, values=LANGUAGE_NAMES,
                     state="readonly", width=18).pack(side="left", padx=5)

        # Input box
        ttk.Label(main, text="Enter text:").pack(anchor="w", pady=(10, 2))
        self.input_box = tk.Text(main, height=8, wrap="word", font=("Segoe UI", 11))
        self.input_box.pack(fill="both", expand=True)

        # Buttons
        btns = ttk.Frame(main)
        btns.pack(fill="x", pady=10)
        self.translate_btn = ttk.Button(btns, text="Translate", command=self.start_translation)
        self.translate_btn.pack(side="left")
        ttk.Button(btns, text="Copy Result", command=self.copy_result).pack(side="left", padx=8)
        ttk.Button(btns, text="Clear", command=self.clear_all).pack(side="left")

        # Output box
        ttk.Label(main, text="Translation:").pack(anchor="w", pady=(0, 2))
        self.output_box = tk.Text(main, height=8, wrap="word", font=("Segoe UI", 11),
                                  state="disabled", bg="#f4f4f4")
        self.output_box.pack(fill="both", expand=True)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status_var, foreground="gray").pack(anchor="w", pady=(8, 0))

    # ---------- actions ----------
    def swap_languages(self):
        src, tgt = self.source_var.get(), self.target_var.get()
        if src == "Auto Detect":
            messagebox.showinfo("Swap", "Pick a specific source language to swap.")
            return
        self.source_var.set(tgt)
        self.target_var.set(src)

    def start_translation(self):
        text = self.input_box.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Empty input", "Please enter some text to translate.")
            return
        self.translate_btn.config(state="disabled")
        self.status_var.set("Translating...")
        # Run in a thread so the window doesn't freeze
        threading.Thread(target=self.run_translation, args=(text,), daemon=True).start()

    def run_translation(self, text: str):
        try:
            result = translate_text(text, self.source_var.get(),
                                    self.target_var.get())
            self.root.after(0, self.show_result, result)
        except Exception as e:
            self.root.after(0, self.show_error, str(e))

    def show_result(self, result: str):
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", result)
        self.output_box.config(state="disabled")
        self.translate_btn.config(state="normal")
        self.status_var.set("Done")

    def show_error(self, message: str):
        self.translate_btn.config(state="normal")
        self.status_var.set("Error")
        messagebox.showerror("Translation failed",
                             f"Check your internet connection and try again.\n\n{message}")

    def copy_result(self):
        text = self.output_box.get("1.0", "end").strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status_var.set("Copied to clipboard")

    def clear_all(self):
        self.input_box.delete("1.0", "end")
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.config(state="disabled")
        self.status_var.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    TranslatorApp(root)
    root.mainloop()
