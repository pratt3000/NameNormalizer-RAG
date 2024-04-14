import requests
from lxml import html
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import re
import spacy

# Load the English NER model
nlp = spacy.load("en_core_web_sm")

def extract_entities(sentence):
    
    # Process the input sentence
    doc = nlp(sentence)
    # Extract entities from the processed document
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    filtered_entity_types = ['PERSON', 'ORG', 'NORP', 'PRODUCT', 'WORK_OF_ART', 'EVENT']

    entities = [ent.text for ent in doc.ents if ent.label_ in filtered_entity_types]

    return entities

def clean_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    cleaned_sentences = []
    for sentence in sentences:
        # Remove special characters and extra whitespace
        cleaned_sentence = re.sub(r'[^A-Za-z0-9\s]', '', sentence)
        # Remove extra whitespace at the beginning and end of the sentence
        cleaned_sentence = cleaned_sentence.strip()
        if cleaned_sentence:
            cleaned_sentences.append(cleaned_sentence)
    
    all_entities = set()
    for sentence in cleaned_sentences:
        entities = extract_entities(sentence)
        all_entities.update(entities)

    return {'sentences': cleaned_sentences, 'entities': list(all_entities)}


def get_wikipedia_link(company_name):
    search_query = f"{company_name} Wikipedia"

    response = get_response(search_query)
    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        wikipedia_link = soup.find('a', href=lambda href: href and 'wikipedia.org' in href)
        
        return wikipedia_link['href']
    else:
        print("Failed to retrieve Google search results.")
        return None
    

def get_response(query: str) -> requests.Response:
    """
    Retrieves html response by sending requests

    Args:
        query(str): This is used as search term in the Google search URL

    Returns:
        requests.Response
    """

    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
                '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
      'dpr': '1',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    search_url = f'https://www.google.com/search?q={query}&sourceid=chrome&ie=UTF-8'
    # Retrying 3 times if status code is not 200
    for retry in range(3):
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            return response
    return None


def get_api_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()  # Parse JSON response
        else:
            print("Failed to retrieve data from the API. Status code:", response.status_code)
            return None
    except requests.RequestException as e:
        print("An error occurred:", e)
        return None

def extract_company_details(response: requests.Response) -> dict:
    """
    Extracts company details from HTML response

    Args:
        response(requests.Response): Response object
    
    Returns:
        dict: Extracted company data
    
    Cite: https://github.com/scrapehero-code/google-company-search/blob/main/scraper.py 
    """
    parser = html.fromstring(response.text)

    company_name_raw = parser.xpath('//div[contains(@class, "kp-wholepage")]//*[@data-attrid="title"]//text()')
    company_name = company_name_raw[0] if company_name_raw else None
    website_raw = parser.xpath('//div[contains(@class, "kp-wholepage")]//a[@data-attrid="visit_official_site"]//@href')
    website = website_raw[0] if website_raw else None

    wikipedia_link = get_wikipedia_link(company_name) if company_name else None
    if wikipedia_link:
        wiki_name = wikipedia_link.split('/')[-1]
        api_link = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=max&explaintext&titles={wiki_name}"
        wiki_data = get_api_data(api_link)

        wiki_text = ""
        for page in wiki_data['query']['pages']:
            wiki_text += wiki_data['query']['pages'][page]['extract'] + " "
        wiki_text = clean_text(wiki_text)

    company_details = {
      'company_name': company_name,
      'company_website': website,
      'wiki_text': wiki_text if wikipedia_link else None
    } 
    return company_details


def scrape(company: str):
    response = get_response(company)
    # If the response fails, even after retries, get_response won't return any response
    if not response:
        print(f'Invalid response for company name {company}')
        return None
    company_details = extract_company_details(response)
    company_details['input_company_name'] = company

    return company_details
