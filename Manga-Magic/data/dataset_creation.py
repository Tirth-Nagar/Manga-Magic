import numpy as np
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

root_url = 'https://www.anime-planet.com/manga/all'

def get_max_pages():
    r = requests.get(root_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    max_pages = soup.find('div', class_='pagination').find_all('a')[-2].text # -2 because the last element is 'Next'
    return int(max_pages)   

def check_text(value):
    if value:
        return value.text
    
    return np.nan

def scraper(page=1):   
    req = requests.get(root_url, params={'page': page})
    
    if req.status_code != 200:
        return []

    bs = BeautifulSoup(req.text, 'html.parser')

    container = bs.find('ul', attrs={'class': 'cardDeck'})
    items = container.findAll('li')

    data = [item_scraper(i) for i in items]
    return data

def item_scraper(item):
    info = item.a['title']
    info_bs = BeautifulSoup(info, 'html.parser')
    
    title = check_text(info_bs.h5)
    description = check_text(info_bs.p)
    rating = check_text(info_bs.find('div', attrs={'class': 'ttRating'}))
    year = check_text(info_bs.find('li', attrs={'class': 'iconYear'}))
    if year:
        year = str(year).split(' - ')[0]
    
    if info_bs.h4:
        tags = [t.text for t in info_bs.h4.nextSibling.findAll('li')]
    else:
        tags = []
    
    cover = item.a.div.img['data-src']
    
    return [title, description, rating, year, tags, cover]

max_pages = get_max_pages()
print(f'Found {max_pages} pages')

pages_data = {}

for i in range(max_pages):
    print(f'Page {i+1}')
    data = scraper(i+1)
    pages_data[i] = data

headers = ['title', 'description', 'rating', 'year', 'tags', 'cover']

full_data = []
for i in pages_data.values():
    full_data.extend(i)
    
pd.DataFrame(full_data, columns=headers).to_csv('data.csv', index=False)
