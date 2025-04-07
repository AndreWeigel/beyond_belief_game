import pickle
import os
import requests
import nltk
import time
import re


# Tell NLTK to look for data in the local project folder
nltk.data.path.append('./nltk_data')
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
MINIMUM_SENTENCE_COUNT = 3

def fetch_random_wikipedia_title():
    """Get a random page title from Wikipedia."""
    try:
        random_params = {
            "action": "query",
            "list": "random",
            "rnlimit": 1,
            "rnnamespace": 0, #only information pages (no users)
            "format": "json"
        }
        random_response = requests.get(WIKIPEDIA_API_URL, params=random_params)
        random_page = random_response.json()["query"]["random"][0]
        return  random_page["title"]
    except Exception as e:
        print(f"Error fetching random wikipedia article: {e}")
        return None

def fetch_wikipedia_page_content(title):
    """Get content from Wikipedia page."""
    try:
        extract_params = {
            "action": "query",
            "prop": "extracts",
            "explaintext": True,
            "titles": title,
            "format": "json"
        }
        extract_response = requests.get(WIKIPEDIA_API_URL, params=extract_params)
        pages = extract_response.json()["query"]["pages"]
        page = next(iter(pages.values()))
        return page.get("extract", "")
    except Exception as e:
        print(f"Error fetching random wikipedia article: {e}")
        return None


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


def clean_sentences(sentences):
    cleaned = []
    for s in sentences:
        s = re.sub(r'\=\=.*?\=\=', '', s)  # remove headings
        s = re.sub(r'\[\[|\]\]', '', s)    # remove double brackets
        s = re.sub(r'\{\{.*?\}\}', '', s)  # remove templates
        s = re.sub(r'<ref.*?>.*?</ref>', '', s)  # remove references
        s = re.sub(r'\n', ' ', s)  # remove newlines
        cleaned.append(s.strip())
    return cleaned


def filter_linguistically_normal_nltk(sentences):
    cleaned = []
    for s in sentences:
        # Skip sentences that are too short or weird
        if len(s) < 20 or len(s.split()) < 3:
            continue
        elif re.match(r'^[^a-zA-Z]+$', s):
            continue  # all symbols
        if any(char in s for char in "{}[]|=*<>"):
            continue  # wiki markup leftovers
        elif s.count('.') > 3:
            continue
        else:
            cleaned.append(s.strip())
    return cleaned


def is_sentence_appropriate(sentences):
    if len(sentences) < MINIMUM_SENTENCE_COUNT:
        return False
    else:
        return True


def get_valid_wikipedia_page_info():
    """Continuously fetches random Wikipedia pages until a valid page is found."""
    while True:

        page_title = fetch_random_wikipedia_title()

        page_content = fetch_wikipedia_page_content(page_title)

        divided_sentences = divide_sentences(page_content)

        cleaned_sentences = clean_sentences(divided_sentences)

        filtered_sentences = filter_linguistically_normal_nltk(cleaned_sentences)

        if is_sentence_appropriate(filtered_sentences):
            break

        time.sleep(0.5)
    return page_title, filtered_sentences


if __name__ == "__main__":
    page_title, sentences = get_valid_wikipedia_page_info()
    print(f"Page title: {page_title}")
    print(f"Number of sentences: {len(sentences)}")
    for s in sentences:
        print(s)







