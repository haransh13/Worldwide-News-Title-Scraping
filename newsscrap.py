from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# Configure Chrome options and service
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
service = Service('C:/path/to/chromedriver.exe')  # Replace with the correct path to chromedriver

# Date range for filtering
today = datetime.now()
start_date = today - timedelta(days=7)
end_date = today

def classify_news(title):
    keywords = {
        'finance': ['stock', 'market', 'finance', 'economy', 'investment', 'banking', 'money', 'business', 'trade', 'inflation', 'interest rates'],
        'education': ['school', 'education', 'university', 'college', 'student', 'teacher', 'classroom', 'curriculum', 'scholarship', 'academic', 'degree'],
        'political': ['election', 'government', 'policy', 'political', 'vote', 'legislation', 'senate', 'parliament', 'campaign', 'democracy', 'candidate'],
        'war': ['war','Gaza','Palestine','Palestinian', 'conflict', 'military', 'battle', 'troops', 'army', 'navy', 'air force', 'weapon', 'invasion', 'defense', 'security'],
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

def is_date_in_range(date_str, start_date, end_date):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return False
    return start_date <= date <= end_date

def scrape_google_news(url, start_date, end_date):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
    )

    data = []
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article')

        if not articles:
            break

        for article in articles:
            title_tag = article.find('a', class_="DY5T1d")
            if title_tag:
                title = title_tag.get_text()
                link = title_tag.get('href')
                if link:
                    if link.startswith('/'):
                        href = 'https://news.google.com' + link
                    else:
                        href = link

                    # Extract the date from the article
                    date_tag = article.find('time')
                    if date_tag and date_tag.get('datetime'):
                        date_str = date_tag.get('datetime').split('T')[0]
                    else:
                        date_str = datetime.now().strftime('%Y-%m-%d')  # Fallback to current date if not found

                    if is_date_in_range(date_str, start_date, end_date):
                        category = classify_news(title)
                        data.append({
                            'date': date_str,
                            'title': title,
                            'link': href,
                            'category': category
                        })

        # Check for the presence of a "next" button or similar pagination element
        next_button = driver.find_elements(By.CSS_SELECTOR, 'a[aria-label="Next"]')
        if not next_button:
            break
        next_button[0].click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article'))
        )

    driver.quit()
    return data

# URL for Google News search for India
url = "https://news.google.com/search?q=India&hl=en-IN&gl=IN"

# Store the results
results = scrape_google_news(url, start_date, end_date)

# Create a DataFrame and save to a CSV file
df = pd.DataFrame(results, columns=['date', 'title', 'link', 'category'])
df.to_csv('google_news_scrape_filtered.csv', index=False)

print("Scraping completed. Results saved to google_news_scrape_filtered.csv")
