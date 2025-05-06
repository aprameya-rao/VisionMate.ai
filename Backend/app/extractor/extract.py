import fitz  
import re
import pyttsx3 



def clean_markdown_style_text(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    text = re.sub(r"`([^`]*)`", r"\1", text)

    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text) 
    text = re.sub(r"\*(.*?)\*", r"\1", text)      
    text = re.sub(r"__(.*?)__", r"\1", text)      
    text = re.sub(r"_(.*?)_", r"\1", text)        

    
    text = re.sub(r"^> ?", "", text, flags=re.MULTILINE)

    
    text = re.sub(r"^#{1,6} ", "", text, flags=re.MULTILINE)

    
    text = re.sub(r"^-{3,}|_{3,}|\*{3,}", "", text)

    
    text = re.sub(r"^[\*\-\+] ", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\.\s+", "", text, flags=re.MULTILINE)

    
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

def text_extractor():
    doc=fitz.open("book1.pdf")
    out=open("output.txt","w",encoding="utf-8")
    for page in doc :
        text=page.get_text()
        texts=clean_markdown_style_text(text)
        print(texts)
        out.write(texts)
    out.close()
    text_to_speech()


def text_to_speech():
    engine = pyttsx3.init()

    
    rate = engine.getProperty('rate')  
    engine.setProperty('rate', rate - 50)  

    volume = engine.getProperty('volume') 
    engine.setProperty('volume', 1)  

    with open("output.txt", "r", encoding="utf-8") as file:
        text = file.read()

    paragraphs = text.split("\n")  
    for paragraph in paragraphs:
        engine.say(paragraph.strip())
        engine.runAndWait()



text_extractor()