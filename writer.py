##-*- coding: utf-8 -*-
import requests
import urllib
import csv
from bs4 import BeautifulSoup

book_writer=[]

def spider(page):
    count=0
    url = 'http://foreign.aladin.co.kr/shop/common/wbest.aspx?BestType=AuthorBest&BranchType=1&CID=0&cnt=100&SortOrder=1&page=' + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    tag = soup.findAll("strong")
    
    for i in range(47,97):
        book_writer.append(tag[i].text)


#1페이지부터 i-1페이지까지
for i in range(1,3):
    spider(i)


with open('./bestSeller_data.csv', 'w') as csvfile:
    fieldnames = ['rank','book_writer']
    fwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    fwriter.writeheader()
    
    
    for i in range(0,100):
        fwriter.writerow({'rank':i,'book_writer':book_writer.pop().encode('utf-8')})



