from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime


# List of countries and their respective Google News search URLs
countries = {
    'albania': "https://news.google.com/search?q=Albania",
    'andorra': "https://news.google.com/search?q=Andorra",
    'armenia': "https://news.google.com/search?q=Armenia",
    'austria': "https://news.google.com/search?q=Austria",
    'azerbaijan': "https://news.google.com/search?q=Azerbaijan",
    'belarus': "https://news.google.com/search?q=Belarus",
    'belgium': "https://news.google.com/search?q=Belgium",
    'bosnia_and_herzegovina': "https://news.google.com/search?q=Bosnia%20and%20Herzegovina",
    'bulgaria': "https://news.google.com/search?q=Bulgaria",
    'croatia': "https://news.google.com/search?q=Croatia",
    'cyprus': "https://news.google.com/search?q=Cyprus",
    'czech_republic': "https://news.google.com/search?q=Czech%20Republic",
    'denmark': "https://news.google.com/search?q=Denmark",
    'estonia': "https://news.google.com/search?q=Estonia",
    'finland': "https://news.google.com/search?q=Finland",
    'france': "https://news.google.com/search?q=France",
    'georgia': "https://news.google.com/search?q=Georgia",
    'germany': "https://news.google.com/search?q=Germany",
    'greece': "https://news.google.com/search?q=Greece",
    'hungary': "https://news.google.com/search?q=Hungary",
    'iceland': "https://news.google.com/search?q=Iceland",
    'ireland': "https://news.google.com/search?q=Ireland",
    'italy': "https://news.google.com/search?q=Italy",
    'kazakhstan': "https://news.google.com/search?q=Kazakhstan",
    'kosovo': "https://news.google.com/search?q=Kosovo",
    'latvia': "https://news.google.com/search?q=Latvia",
    'liechtenstein': "https://news.google.com/search?q=Liechtenstein",
    'lithuania': "https://news.google.com/search?q=Lithuania",
    'luxembourg': "https://news.google.com/search?q=Luxembourg",
    'malta': "https://news.google.com/search?q=Malta",
    'moldova': "https://news.google.com/search?q=Moldova",
    'monaco': "https://news.google.com/search?q=Monaco",
    'montenegro': "https://news.google.com/search?q=Montenegro",
    'netherlands': "https://news.google.com/search?q=Netherlands",
    'north_macedonia': "https://news.google.com/search?q=North%20Macedonia",
    'norway': "https://news.google.com/search?q=Norway",
    'poland': "https://news.google.com/search?q=Poland",
    'portugal': "https://news.google.com/search?q=Portugal",
    'romania': "https://news.google.com/search?q=Romania",
    'san_marino': "https://news.google.com/search?q=San%20Marino",
    'serbia': "https://news.google.com/search?q=Serbia",
    'slovakia': "https://news.google.com/search?q=Slovakia",
    'slovenia': "https://news.google.com/search?q=Slovenia",
    'spain': "https://news.google.com/search?q=Spain",
    'sweden': "https://news.google.com/search?q=Sweden",
    'switzerland': "https://news.google.com/search?q=Switzerland",
    'turkey': "https://news.google.com/search?q=Turkey",
    'ukraine': "https://news.google.com/search?q=Ukraine",
    'united_kingdom': "https://news.google.com/search?q=United%20Kingdom",
    'vatican_city': "https://news.google.com/search?q=Vatican%20City"
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
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(10)  # Wait for the page to load

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
                    date = datetime.now().strftime("%Y-%m-%d")
                    category = classify_news(title)
                    data.append({
                        'date': date,
                        'country': country,
                        'title': title,
                        'link': href,
                        'category': category
                    })

        driver.quit()
        return data

    except NoSuchWindowException:
        print(f"Error: The browser window was closed unexpectedly while processing {country}.")
        return []

    except WebDriverException as e:
        print(f"WebDriverException encountered: {e}")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Store the results
results = []

for country, url in countries.items():
    print(f"Scraping news for {country}...")
    country_data = scrape_google_news(country, url)
    results.extend(country_data)

# Convert the results to a DataFrame and save to a CSV file
df = pd.DataFrame(results)
df.to_csv('news_data.csv', index=False)

print("Scraping completed. Data saved to 'news_data.csv'.")
