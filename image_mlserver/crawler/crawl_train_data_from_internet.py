#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import hashlib
import time
import os

visited_img_links = []
def crawl():
    url = 'http://www.seed-server.com/file'
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')

    new_img_links = []
    for image in soup.find_all("div", {"class":"elgg-image"}):
        img_detail_link = image.a.get('href')
        if img_detail_link not in visited_img_links:
            new_img_links.append(image.a.get('href'))

    img_class_dict = {}
    for i, link in enumerate(new_img_links):
        visited_img_links.append(link)
        page = requests.get(link)
        html = page.text
        cookies_jar = page.cookies
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("h2", {"class":"elgg-heading-main"}).text
        image = soup.find("a", {"class":"elgg-lightbox-photo"})
        if image.get('href'):
            img_name = hashlib.md5(image.get('href').encode("ascii")).hexdigest()
            img_data = requests.get(image.get('href'), cookies=cookies_jar).content
            with open('train_data/{}.png'.format(img_name), 'wb') as handler:
                handler.write(img_data)
            img_class_dict['train_data/{}.png'.format(img_name)] = title
    return img_class_dict

#save the graph for cold start
if not os.path.exists('./train_data/'):
    os.makedirs('./train_data/')

while True:
    time.sleep(10)
    img_class_dict = crawl()

    for path, title in img_class_dict.items():
        requests.post("http://10.9.0.7:5000/add_train_data/", json={"path": "../crawler/"+path, "class": title})
    if len(img_class_dict)>0:
        requests.get("http://10.9.0.7:5000/train/")