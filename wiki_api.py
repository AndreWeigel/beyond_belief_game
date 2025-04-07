import pickle
import os
import requests
import nltk
import time

# Tell NLTK to look for data in the local project folder
nltk.data.path.append('./nltk_data')


def fetch_random_wikipedia_title():
    """Get a random page title from Wikipedia."""

    url = "https://en.wikipedia.org/w/api.php"

    random_params = {
        "action": "query",
        "list": "random",
        "rnlimit": 1,
        "rnnamespace": 0, #only information pages (no users)
        "format": "json"
    }
    random_response = requests.get("https://en.wikipedia.org/w/api.php", params=random_params)
    random_page = random_response.json()["query"]["random"][0]
    return  random_page["title"]


def fetch_wikipedia_page_content(title):
    """Get content from Wikipedia page."""

    extract_params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }
    extract_response = requests.get("https://en.wikipedia.org/w/api.php", params=extract_params)
    pages = extract_response.json()["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "")


def load_tokenizer():
    """Load the NLTK Punkt tokenizer."""
    model_path = os.path.join('nltk_data', 'tokenizers', 'punkt', 'english.pickle')
    with open(model_path, 'rb') as f:
        tokenizer = pickle.load(f)
    return tokenizer


def divide_sentences(text):
    """Tokenize text into sentences."""
    tokenizer = load_tokenizer()
    sentences = tokenizer.tokenize(text)
    return sentences


MINIMUM_SENTENCE_COUNT = 3
def get_valid_wikipedia_page_info():
    """Continuously fetches random Wikipedia pages until a valid page is found."""
    while True:

        page_title = fetch_random_wikipedia_title()

        page_content = fetch_wikipedia_page_content(page_title)

        sentences = divide_sentences(page_content)

        if len(sentences) >= MINIMUM_SENTENCE_COUNT:
            break
        time.sleep(0.5)
    return page_title, sentences






