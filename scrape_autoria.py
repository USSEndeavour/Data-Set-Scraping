import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize

for i in range(20):
    #Load the webpage content
    url = 'https://auto.ria.com/uk/newauto/search/?page=%s&categoryId=1&size=100' %i
    page = requests.get(url)

    #Convert to a beautifulSoup object
    soup = bs(page.content, 'html.parser')




    ads = soup.find_all('section', class_='proposition')
    a=[]
    b=[]

    for ad in ads:
        name=(ad.find('h3', class_='proposition_name')).get_text()
        info = (ad.find('div', class_='proposition_equip')).get_text()
        price = (ad.find('span', class_='bold')).get_text()
        region = (ad.find('span', class_='item region')).get_text()
        information = (ad.find('div', class_='proposition_information')).get_text()

        try:
            engine_power = re.findall(r"(\d+) к.с.", info)[0]
        except IndexError:
            engine_power = np.nan


        try:
            engine_transmission = [x for x in word_tokenize(information) if x=='Автомат' or x=='Роботизована' or x=='Механічна' or x=='Тіптронік' or x=='Варіатор'][0]

        except IndexError:
            engine_transmission = np.nan


        
        try:
            wheel_drive = [x for x in word_tokenize(information) if x=='Повний' or x=='Передній'][0]

        except IndexError:
            wheel_drive = np.nan


        try:
            engine_volume = re.findall("\d+\.\d+", info)[0]

        except IndexError:
            engine_volume = np.nan


        a=[name, price, region, engine_power, engine_volume, engine_transmission, wheel_drive]
        b.append(a)

    df = pd.DataFrame(b, columns=['name', 'price', 'region', 'power', 'volume', 'transmission', 'wheel_drive'])
    
    df.head()
    df.to_csv('autoria%s.csv' %(i))


frames=[]

for i in range(20):
    globals()[f'df_{i}'] = pd.read_csv("autoria%s.csv" %(i))
    frames.append(globals()[f'df_{i}'])

data_frame = pd.concat(frames)
col = ['name', 'price', 'region', 'power', 'volume', 'transmission', 'wheel_drive']
data_frame = data_frame[col]
data_frame=data_frame.reset_index(drop=True)

data_frame[1000:1100]

data_frame.to_csv('collect_ria.csv')