import pyttsx3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from docx import Document

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Read the input .docx file
def read_docx(file_path):
    doc = Document(file_path)
    full_text = [para.text for para in doc.paragraphs if para.text.strip()]
    return '\n'.join(full_text)

# Text-to-speech function
def text_to_speech():
    engine = pyttsx3.init()

    # Optional: Adjust rate and volume
    rate = engine.getProperty('rate')  # Get the current speech rate
    engine.setProperty('rate', rate - 50)  # Slow down the speech rate

    volume = engine.getProperty('volume')  # Get the current volume level
    engine.setProperty('volume', 1)  # Set volume to max

    with open("output.txt", "r", encoding="utf-8") as file:
        text = file.read()

    paragraphs = text.split("\n")  # Split by newlines for paragraphs
    for paragraph in paragraphs:
        engine.say(paragraph.strip())
        engine.runAndWait()


input_text_path = "Book2.docx"
article = read_docx(input_text_path)


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

# Speak the summary aloud
text_to_speech()