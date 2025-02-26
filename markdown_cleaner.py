import re

from langdetect import detect
from nltk.corpus import stopwords

from environment_utils import Env

# Mapping from ISO 639-1 codes to NLTK stopwords language names
LANGUAGE_MAP = {
    "en": "english",
    "fr": "french",
    "es": "spanish",
    "de": "german",
    "it": "italian",
    "nl": "dutch",
    "pt": "portuguese",
    "ru": "russian",
    "sv": "swedish",
    "no": "norwegian",
    "da": "danish",
    "fi": "finnish",
}


def clean_markdown(text):
    # Detect the language of the text
    detected_lang = detect(text)

    # Convert detected language code to NLTK-compatible language name
    nltk_lang = LANGUAGE_MAP.get(
        detected_lang, "english"
    )  # Default to English if not found

    # Remove Markdown headers, links, and lists
    text = re.sub(r"\#[^\n]*", "", text)  # Remove headers
    text = re.sub(r"\[.*?\]\(.*?\)", "", text)  # Remove links
    text = re.sub(r"-+|\*+", "", text)  # Remove list markers
    # Remove punctuation and convert to lowercase
    text = re.sub(r"[^\w\s]", "", text).lower()

    # Get stopwords for detected language
    try:
        stop_words = set(stopwords.words(nltk_lang))
    except LookupError:
        # In case the detected language does not have stopwords available
        stop_words = set()

    # Remove stopwords
    text = " ".join([word for word in text.split() if word not in stop_words])

    return text


def read_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


if __name__ == "__main__":
    env = Env()
    resume_path = env.get_key("RESUME")
    resume_md = read_file(resume_path)
    cleaned_resume = clean_markdown(resume_md)
    print(cleaned_resume)
