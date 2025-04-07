import fitz  # PyMuPDF
import re
import pyttsx3 

def clean_markdown_style_text(text):
    # Remove code blocks (triple backticks)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # Inline code (single backticks)
    text = re.sub(r"`([^`]*)`", r"\1", text)

    # Images ![alt](url)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    # Links [text](url)
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    # Bold and Italics (Markdown styles)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)      # Italic
    text = re.sub(r"__(.*?)__", r"\1", text)      # Bold (alt)
    text = re.sub(r"_(.*?)_", r"\1", text)        # Italic (alt)

    # Blockquotes
    text = re.sub(r"^> ?", "", text, flags=re.MULTILINE)

    # Headers (e.g., ### Header)
    text = re.sub(r"^#{1,6} ", "", text, flags=re.MULTILINE)

    # Horizontal rules (---, ***, ___)
    text = re.sub(r"^-{3,}|_{3,}|\*{3,}", "", text)

    # Lists: bullet points and numbered lists
    text = re.sub(r"^[\*\-\+] ", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

    # Clean up extra newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def text_extractor():
    doc=fitz.open("First Year B.E Syllabus Book 2023-2024.pdf")
    out=open("output.txt","w",encoding="utf-8")
    for page in doc :
        text=page.get_text()
        texts=clean_markdown_style_text(text)
        print(texts)
        out.write(texts)
    out.close()
    text_to_speech()


def text_to_speech() :
    engine=pyttsx3.init()

    with open("output.txt","r",encoding="utf-8") as file :
        text=file.read()


    engine.say(text)
    engine.runAndWait()

text_extractor()
