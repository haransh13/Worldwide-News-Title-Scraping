from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta

# List of countries and their respective Google News search URLs
countries = {
    'united_states': "https://news.google.com/topics/CAAqJAgKIh5DQkFTRUFvSEwyMHZNR3BuZUJJRlpXNHRSMElvQUFQAQ?hl=en-US&gl=US&ceid=US%3Aen",
    'canada': "https://news.google.com/topics/CAAqJAgKIh5DQkFTRUFvSEwyMHZNR3BuZUJJRlpXNHRSMElvQUFQAQ?hl=en-CA&gl=CA&ceid=CA%3Aen",
    'mexico': "https://news.google.com/search?q=&gl=MX&hl=es-MX",
    'guatemala': "https://news.google.com/search?q=&gl=GT&hl=es-419",
    'belize': "https://news.google.com/search?q=&gl=BZ&hl=es",
    'honduras': "https://news.google.com/search?q=&gl=HN&hl=es",
    'el_salvador': "https://news.google.com/search?q=&gl=SV&hl=es",
    'nicaragua': "https://news.google.com/search?q=&gl=NI&hl=es",
    'costa_rica': "https://news.google.com/search?q=&gl=CR&hl=es",
    'panama': "https://news.google.com/search?q=&gl=PA&hl=es",
    'cuba': "https://news.google.com/search?q=&gl=CU&hl=es",
    'jamaica': "https://news.google.com/search?q=&gl=JM&hl=en",
    'haiti': "https://news.google.com/search?q=&gl=HT&hl=fr",
    'dominican_republic': "https://news.google.com/search?q=&gl=DO&hl=es",
    'puerto_rico': "https://news.google.com/search?q=&gl=PR&hl=es",
    'colombia': "https://news.google.com/search?q=&gl=CO&hl=es",
    'venezuela': "https://news.google.com/search?q=&gl=VE&hl=es",
    'ecuador': "https://news.google.com/search?q=&gl=EC&hl=es",
    'peru': "https://news.google.com/search?q=&gl=PE&hl=es",
    'bolivia': "https://news.google.com/search?q=&gl=BO&hl=es",
    'paraguay': "https://news.google.com/search?q=&gl=PY&hl=es",
    'chile': "https://news.google.com/search?q=&gl=CL&hl=es",
    'argentina': "https://news.google.com/search?q=&gl=AR&hl=es",
    'uruguay': "https://news.google.com/search?q=&gl=UY&hl=es",
    'guyana': "https://news.google.com/search?q=&gl=GY&hl=en",
    'suriname': "https://news.google.com/search?q=&gl=SR&hl=en",
    'french_guiana': "https://news.google.com/search?q=&gl=GF&hl=fr",
    'brazil': "https://news.google.com/search?q=&gl=BR&hl=pt",
    'bermuda': "https://news.google.com/search?q=&gl=BM&hl=en",
    'bahamas': "https://news.google.com/search?q=&gl=BS&hl=en",
    'barbados': "https://news.google.com/search?q=&gl=BB&hl=en",
    'saint_lucia': "https://news.google.com/search?q=&gl=LC&hl=en",
    'saint_vincent_and_the_grenadines': "https://news.google.com/search?q=&gl=VC&hl=en",
    'grenada': "https://news.google.com/search?q=&gl=GD&hl=en",
    'trinidad_and_tobago': "https://news.google.com/search?q=&gl=TT&hl=en",
    'antigua_and_barbuda': "https://news.google.com/search?q=&gl=AG&hl=en",
    'saint_kitts_and_nevis': "https://news.google.com/search?q=&gl=KN&hl=en"
}

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

def scrape_google_news(country, url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(10)  

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('article')
    data = []

    for article in articles:
        title_tag = article.find('a', class_="JtKRv")
        if title_tag:
            title = title_tag.get_text()
            link = article.find('a', href=True)
            if link:
                href = link['href']
                if href.startswith('/'):
                    href = 'https://news.google.com' + href
                
                time_tag = article.find('time')
                if time_tag:
                    relative_time = time_tag.get_text()
                    date = None
                    if 'hour' in relative_time or 'minute' in relative_time or 'second' in relative_time:
                        date = datetime.now().strftime("%Y-%m-%d")
                    elif 'Yesterday' in relative_time:
                        date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                    elif 'day' in relative_time:
                        days_ago = int(relative_time.split()[0])
                        date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
                    
                    # Filter articles within the last 7 days
                    if date and datetime.now() - timedelta(days=7) <= datetime.strptime(date, "%Y-%m-%d"):
                        category = classify_news(title)
                        data.append({'title': title, 'link': href, 'date': date, 'category': category})

    driver.quit()
    return data

# Loop through each country and scrape news
all_news = []

for country, url in countries.items():
    try:
        print(f"Scraping news for {country}...")
        news_data = scrape_google_news(country, url)
        for item in news_data:
            item['country'] = country
        all_news.extend(news_data)
    except Exception as e:
        print(f"Failed to scrape news for {country}: {e}")

df = pd.DataFrame(all_news)
df.to_csv('google_news.csv', index=False)
print("Scraping completed and data saved to google_news.csv")
