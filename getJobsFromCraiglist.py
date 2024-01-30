import requests 
from datetime import datetime
import bs4 
import pandas as pd


price = []
title = []
location = []
link = []
df = None 

def getPosts():
    res = requests.get('https://sfbay.craigslist.org/search/apa?availabilityMode=0&hasPic=1&postedToday=1#search=1')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    posts = soup.find_all('li', class_= 'cl-static-search-result')

    for post in posts: 
        price.append(post.find('div', class_= 'price').text.strip()[1:])
        location.append(post.find('div', class_= 'location').text.strip())
        link.append(post.find('a')['href'])
        title.append(post['title'])
    
def sendMessage():
    pass

def createDataFrame():
    global df
    df = pd.DataFrame()
    df['title'] = pd.Series(title)
    df['price'] = pd.Series(price)
    df['location'] = pd.Series(location)
    df['URL'] = pd.Series(link)


def cleanData():
    global df 
    today = datetime.today()
    df.to_csv(f'{today.year}_{today.month}_{today.day}.csv', index=False)

def insertDataFrame():
    pass

getPosts()
print(len(title),len(price))
createDataFrame()
cleanData()