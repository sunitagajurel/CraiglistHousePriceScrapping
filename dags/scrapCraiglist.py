from airflow import DAG
from datetime import datetime
import requests
import bs4 
import pandas as pd
from airflow.operators.python import PythonOperator

price = []
title = []
location = []
link = []
df = None 



default_args = {
    'owner': 'sunita',
    'start_date': datetime(2024, 1, 31, 2, 20)
}

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


with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    scrapping_task = PythonOperator(
        task_id='acrap_data_from_craiglist',
        python_callable=getPosts
    )