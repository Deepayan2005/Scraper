
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
import json, time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/scrap')
def handle_requests():
    text = str(request.args.get('input'))

    page = requests.get('https://timesofindia.indiatimes.com/briefs/'+text)
# Getting page HTML through request
    soup = BeautifulSoup(page.content, 'html.parser')

    news = soup.find('div', class_="briefs_outer clearfix").find_all('div', class_="brief_box")
    list = []

    for data in news:
        try:
            s2 = BeautifulSoup(str(data), 'html.parser')
            det = s2.find('div', class_='posrel')
            title = s2.find('h2').find('a').text
            desc = s2.find('p').find('a').text
            link = s2.find('h2').find('a').get('href')
            mainLink = "https://timesofindia.indiatimes.com" + link
            img = det.find('img').get('data-src')

            send = {'title':title,"image":img,"desc":desc,"mainLink":mainLink}
            list.append(send)
        except AttributeError as attr:
            print("Sorry")
    return json.dumps(list)


@app.route('/details')
def give_details():
    text = str(request.args.get('input'))
    page = requests.get(text)
    soup = BeautifulSoup(page.content, 'html.parser')
    news = soup.find('div',class_='_s30J clearfix')
    return json.dumps({'text':news.text})

