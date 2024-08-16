from deep_translator import GoogleTranslator
import requests

translator = GoogleTranslator(source='auto', target='en')

def search_movie_by_title(query):
    translated_query = translator.translate(query)
    url = f"http://www.omdbapi.com/?s={translated_query}&apikey=5a1ad64c"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return data['Search']
    return []

def get_movie_details(imdbID):
    url = f"http://www.omdbapi.com/?i={imdbID}&apikey=YOUR_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return data
    return {}
