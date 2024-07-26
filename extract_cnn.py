import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape CNN News

def scrape_cnn_news():
    url = 'https://edition.cnn.com/world'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page with status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    news_data = []
    articles = soup.find_all('a',
                             class_='container__link container__link--type-article container_lead-plus-headlines__link')

    for article in articles:
        try:
            title_tag = article.find('span', class_='container__headline-text')
            title = title_tag.text.strip() if title_tag else 'No title'

            link = 'https://edition.cnn.com' + article['href'] if article['href'].startswith('/') else 'No link'

            date = "2024-07-23"  # Assuming a static date for simplicity; update as needed
            country = 'US'  # Assuming CNN news is from the US
            category = classify_news(title)
            news_data.append([date, country, title, category, link])
        except Exception as e:
            print(f"Error parsing article: {e}")

    return news_data

def classify_news(title):
    keywords = {
        'finance': ['stock', 'market', 'finance', 'economy', 'investment', 'banking', 'money', 'business', 'trade', 'inflation', 'interest rates'],
        'education': ['school', 'education', 'university', 'college', 'student', 'teacher', 'classroom', 'curriculum', 'scholarship', 'academic', 'degree'],
        'political': ['election', 'government', 'policy', 'political', 'vote', 'legislation', 'senate', 'parliament', 'campaign', 'democracy', 'candidate'],
        'war': ['war','Gaza','Palestien','Palestinian', 'conflict', 'military', 'battle', 'troops', 'army', 'navy', 'air force', 'weapon', 'invasion', 'defense', 'security'],
        'entertainment': ['movie', 'music', 'celebrity', 'entertainment', 'concert', 'film', 'theater', 'festival', 'award', 'show', 'series', 'actor', 'actress'],
        'tech': ['technology', 'tech', 'software', 'gadget', 'innovation', 'AI', 'robotics', 'internet', 'startup', 'app', 'device', 'cybersecurity', 'IT'],
        'god': ['religion', 'faith', 'church', 'god', 'spiritual', 'worship', 'prayer', 'bible', 'holy', 'deity', 'temple', 'pastor', 'imam', 'rabbi'],
        'health': ['health', 'medicine', 'hospital', 'doctor', 'nurse', 'disease', 'virus', 'pandemic', 'treatment', 'vaccine', 'surgery', 'mental health', 'fitness', 'nutrition'],
        'sports': ['sports', 'game', 'match', 'team', 'player', 'tournament', 'championship', 'league', 'score', 'goal', 'coach', 'athlete'],
        'environment': ['environment', 'climate', 'pollution', 'recycle', 'conservation', 'wildlife', 'sustainability', 'natural disaster', 'weather', 'global warming', 'ecology'],
        'crime': ['crime', 'criminal', 'police', 'law enforcement', 'court', 'trial', 'sentence', 'verdict', 'theft', 'robbery', 'assault', 'fraud', 'murder'],
        'science': ['science', 'research', 'experiment', 'discovery', 'space', 'astronomy', 'biology', 'chemistry', 'physics', 'scientist', 'laboratory'],
        'travel': ['travel', 'tourism', 'vacation', 'trip', 'destination', 'hotel', 'flight', 'tourist', 'journey', 'adventure', 'cruise'],
        'fashion': ['fashion', 'style', 'designer', 'clothing', 'runway', 'trend', 'model', 'boutique', 'couture', 'wardrobe'],
    }
    for category, words in keywords.items():
        if any(word in title.lower() for word in words):
            return category
    return 'other'


# Main script to gather news data and save to CSV
def main():
    news_data = []

    # Scrape different sources (here only BBC for demonstration)
    news_data.extend( scrape_cnn_news())
    
    # Convert to DataFrame
    df = pd.DataFrame(news_data, columns=['Date', 'Country', 'Title', 'Category', 'Link'])
    print(df)
    
    # Save to CSV
    df.to_csv('cnn_data.csv', index=False)
    print('News data saved to cnn_data.csv')

if __name__ == '__main__':
    main()
