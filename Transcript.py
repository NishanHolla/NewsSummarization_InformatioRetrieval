import requests
from newspaper import Article
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.environ.get("GOOGLE_API")
cse_id = os.environ.get("CSE_ID")

class Transcript:

    def search_and_extract_articles(self, query, max_results=10):

        search_url = 'https://www.googleapis.com/customsearch/v1'
        params = {
            'q': query,
            'key': api_key,
            'cx': cse_id,
            'num': max_results
        }

        response = requests.get(search_url, params=params)
        search_results = response.json().get('items', [])
        
        # Extract article content from the obtained URLs
        articles_content = []
        for item in search_results:
            try:
                url = item['link']
                article = Article(url)
                article.download()
                article.parse()
                articles_content.append(article.text)
            except Exception as e:
                print("Unable to get this url",url)

        # Combine the content of all articles into a single string
        combined_text = '\n\n'.join(articles_content)

        return combined_text
