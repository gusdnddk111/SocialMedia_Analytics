##-*- coding: utf-8 -*-
import requests
import urllib
import csv
from bs4 import BeautifulSoup

book_writer=[]
book_publisher=[]

def spider(page):
    count=0
    url = 'http://www.aladin.co.kr/shop/common/wbest.aspx?BestType=MonthlyBest&BranchType=1&CID=0&cnt=1000&SortOrder=1&page=' + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    for tag in soup.findAll("div",{"class":"ss_book_list"}):
        count = count+1
        if count%2==1:
            for tag2 in tag.find("ul").findAll("li"):
                
                if unicode(tag2.text).find(u"(지은이)")>=0:
                    temp = tag2.text.split("|")

                    temp2 = unicode(temp[0]).split(u"(지은이)")
                    ##-*- coding: utf-8 -*-
                    writer = temp2[0].strip()

                    publisher = temp[1].strip()

                elif unicode(tag2.text).find(u"(엮은이)")>=0:
                    temp = tag2.text.split("|")

                    temp2 = unicode(temp[0]).split(u"(엮은이)")
                    ##-*- coding: utf-8 -*-
                    writer = temp2[0].strip()

                    publisher = temp[1].strip()

                elif unicode(tag2.text).find(u"(글)")>=0:
                    temp = tag2.text.split("|")

                    temp2 = unicode(temp[0]).split(u"(글)")
                    ##-*- coding: utf-8 -*-
                    writer = temp2[0].strip()

                    publisher = temp[1].strip()

                elif unicode(tag2.text).find(u"(원작)")>=0:
                    temp = tag2.text.split("|")

                    temp2 = unicode(temp[0]).split(u"(원작)")
                    ##-*- coding: utf-8 -*-
                    writer = temp2[0].strip()

                    publisher = temp[1].strip()

            book_writer.append(writer)
            book_publisher.append(publisher)


#1페이지부터 i-1페이지까지
for i in range(1,21):
    spider(i)


with open('./bestSeller_data.csv', 'w') as csvfile:
    fieldnames = ['book_writer','book_publisher']
    fwriter =  csv.DictWriter(csvfile, fieldnames=fieldnames)
    fwriter.writeheader()
    
    i = len(book_publisher)
    print i
    for i in range(0,i):
        fwriter.writerow({'book_writer':book_writer.pop().encode('utf-8'),'book_publisher':book_publisher.pop().encode('utf-8')})



