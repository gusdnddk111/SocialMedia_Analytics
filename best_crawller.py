#-*- coding: utf-8 -*-
import requests
import urllib
import csv

from bs4 import BeautifulSoup

bookURL_List=[]
book_writer=[]
book_introduce=[]
count=0

def spider(page):
    url = 'https://ridibooks.com/bestsellers/general?order=monthly&page=' + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    for tag in soup.findAll("div",{"class":"book_thumbnail_wrapper"}):
        href = tag['data-book_id_for_tracking']
        bookURL_List.append(href)

#1페이지부터 i-1페이지까지

for i in range(1,2):
    spider(i)

for i in range(0,len(bookURL_List)):

    writer = ""
    introduce = "NA"

    book_url = "https://ridibooks.com/v2/Detail?id=" + bookURL_List.pop()
    source_code = requests.get(book_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    introduce = soup.find("p",{"class":"introduce_paragraph folded"}).text.replace("\n","")

    temp = soup.find("span",{"class":"author_item_wrapper"})
    for temp in temp.findAll("a"):
        writer += temp.text
        writer += ", "

    writer = writer[:-2]

    book_writer.append(writer)
    book_introduce.append(introduce)
    
    count = count+1

with open('./bestSeller_book_data.csv', 'w') as csvfile:
    fieldnames = ['book_writer', 'book_introduce']
    fwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    fwriter.writeheader()
    fwriter.writerow("\xEF\xBB\xBF")
    for i in range(0,count):
        fwriter.writerow({'book_writer' :book_writer.pop().encode('utf-8'),'book_introduce' : book_introduce.pop().encode('utf-8')})


