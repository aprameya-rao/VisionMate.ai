import pyttsx3
import nltk
import fitz  
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


nltk.download('punkt')
nltk.download('stopwords')

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def text_to_speech(file_path):
    engine = pyttsx3.init()

   
    rate = engine.getProperty('rate')  
    engine.setProperty('rate', rate - 50)  

    volume = engine.getProperty('volume')  
    engine.setProperty('volume', 1)  

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    paragraphs = text.split("\n")  
    for paragraph in paragraphs:
        if paragraph.strip():  
            engine.say(paragraph.strip())
            engine.runAndWait()


input_text_path = "book1.pdf"
article = read_pdf(input_text_path)


sentences = sent_tokenize(article)
words = word_tokenize(article.lower())
stop_words = set(stopwords.words("english"))
filtered_words = [word for word in words if word.isalpha() and word not in stop_words]


word_freq = {}
for word in filtered_words:
    word_freq[word] = word_freq.get(word, 0) + 1


sentence_ranks = {}
for sentence in sentences:
    sentence_words = word_tokenize(sentence.lower())
    sentence_ranks[sentence] = sum(word_freq.get(word, 0) for word in sentence_words)


top_sentences = sorted(sentence_ranks, key=sentence_ranks.get, reverse=True)[:3]
summary_text = ' '.join(top_sentences)


with open("summary.txt", "w", encoding="utf-8") as file:
    file.write(summary_text)


text_to_speech("summary.txt")
