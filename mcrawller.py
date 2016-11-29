#-*- coding: utf-8 -*-
import requests
import urllib
import csv
from bs4 import BeautifulSoup

name_list = []
review_list = []
rate_list = []

page=217
flag=1
count =0;

while flag:
    url = "http://movie.daum.net/moviedb/grade?movieId=54361&type=netizen&page=" + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    for names in soup.findAll("em",{"class":"link_profile"}):
        name_list.append(names.text)
        count = count + 1

    for rates in soup.findAll("em",{"class":"emph_grade"}):
        rate_list.append(rates.text)

    for reviews in soup.findAll("p",{"class":"desc_review"}):
        review_list.append(reviews.text.replace("\n","").replace("\"",""))

    isEnd = soup.findAll("em",{"class":"link_profile"})

    if len(isEnd)==0:
        flag=0

    page = page + 1

with open('./201221139_movie.csv', 'w') as csvfile:
    fieldnames = ['name','rate','review']
    fwriter =  csv.DictWriter(csvfile, fieldnames=fieldnames)
    fwriter.writeheader()
    
    for i in range(0,count):
        fwriter.writerow({'name':name_list.pop().encode('utf-8'),'rate':rate_list.pop().encode('utf-8'),'review':review_list.pop().encode('utf-8')})

