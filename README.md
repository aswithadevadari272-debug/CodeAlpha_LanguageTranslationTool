# Language Translation Tool

**CodeAlpha AI Internship – Task 1**

A desktop app built with Python that translates text between 100+ languages. It has a simple Tkinter interface with language dropdowns, auto language detection, a swap button, and a copy-to-clipboard option.

## Features
- Auto-detect the source language
- Choose from all languages supported by Google Translate
- Swap source and target languages
- Copy the translated text with one click
- Translation runs in a background thread, so the window never freezes

## Tech Stack
- Python 3
- [deep-translator](https://pypi.org/project/deep-translator/) (Google Translate)
- Tkinter (built into Python)

## How to Run
```bash
git clone https://github.com/<your-username>/CodeAlpha_LanguageTranslationTool.git
cd CodeAlpha_LanguageTranslationTool
pip install -r requirements.txt
python translator.py
```
An internet connection is required because translation is done online.

## How It Works
1. The user types text and picks the source and target languages.
2. The app converts language names (e.g. "Telugu") to codes (e.g. "te").
3. `GoogleTranslator(source, target).translate(text)` returns the translation.
4. The result is shown in the output box.

## Author
Aswitha Devadari
