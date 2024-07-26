import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Function to scrape news from BBC website
def scrape_bbc_news():
    url = 'https://www.bbc.com/news/uk'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('div', class_='sc-4fedabc7-0 kZtaAl')
    news_data = []

    for article in articles:
        title_tag = article.find('h2', {'data-testid': 'card-headline'})
        if title_tag:
            title_text = title_tag.text

            link_tag = article.find_previous('a', {'data-testid': 'internal-link'})
            if link_tag:
                link = link_tag['href']
                if link.startswith('/'):
                    link = 'https://www.bbc.com' + link

                date = datetime.datetime.now().strftime('%Y-%m-%d')
                country = 'UK'
                category = classify_news(title_text)  # This function is defined below

                news_data.append([date, country, title_text, category, link])

    return news_data

# Function to classify news (simplified example)
def classify_news(title):
    keywords = {
        'finance': ['stock', 'market', 'finance', 'economy', 'investment', 'banking', 'money', 'business', 'trade', 'inflation', 'interest rates'],
        'education': ['school', 'education', 'university', 'college', 'student', 'teacher', 'classroom', 'curriculum', 'scholarship', 'academic', 'degree'],
        'political': ['election', 'government', 'policy', 'political', 'vote', 'legislation', 'senate', 'parliament', 'campaign', 'democracy', 'candidate'],
        'war': ['war', 'conflict', 'military', 'battle', 'troops', 'army', 'navy', 'air force', 'weapon', 'invasion', 'defense', 'security'],
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
    news_data.extend(scrape_bbc_news())
    
    # Convert to DataFrame
    df = pd.DataFrame(news_data, columns=['Date', 'Country', 'Title', 'Category', 'Link'])
    print(df)
    
    # Save to CSV
    df.to_csv('BBC_data.csv', index=False)
    print('News data saved to BBC_data.csv')

if __name__ == '__main__':
    main()
