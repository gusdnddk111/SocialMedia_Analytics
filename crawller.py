#-*- coding: utf-8 -*-
import requests
import urllib
import csv
from bs4 import BeautifulSoup

count=0

bookURL_List=[]
book_name = []
book_price = []
book_writer = []
book_publisher = []
book_category = []
book_page = []
book_size = []
book_cover = []
book_weight = []
book_ISBN = []
book_date = []
book_sales_point = []

def spider(page):
    url = 'http://www.aladin.co.kr/shop/common/wnew.aspx?ViewRowsCount=50&ViewType=Detail&BranchType=1&PublishDay=168&NewType=SpecialNew&page=' + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    for tag in soup.findAll("a",{"class":"bo3"}):
        href = tag.get('href')
        bookURL_List.append(href)


#1페이지부터 i-1페이지까지
for i in range(1,2):
    spider(i)

#책 하나하나 정보 크롤링하기
#for i in range(0,len(bookURL_List)):
for i in range(0,1):
    book_url = bookURL_List.pop()
    source_code = requests.get(book_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    
    name = "NA"
    price = "NA"
    writer = "NA"
    publisher = "NA"
    category = "NA"
    page = "NA"
    size = "NA"
    cover = "NA"
    weight = "NA"
    ISBN = "NA"
    date = "NA"
    sales_point = "NA"


    name = soup.find("a",{"class":"p_topt01"}).text
    #책이름
    price = soup.find("span",{"class":"p_new_price_ph"}).text
    #책가격
    sales_point = soup.find("ul",{"class":"r_topsidebox"}).find("div").find("strong").text
    #판매량
    category = soup.findAll("a",{"class":"ml"})[1].text
    #카테고리
    book_info = soup.find("div",{"class":"p_goodstd03"}).find("table").text
    #책정보
    book_info2 = soup.find("a",{"class":"np_af"}).parent.text.replace("\n","")
    #책 정보2

    #책정보를 | 기준으로 파싱

    book_info_parsing = book_info.split("|")

    for i in range(0,len(book_info_parsing)):
        if unicode(book_info_parsing[i]).find(u"쪽")>=0:
            #-*- coding: utf-8 -*-
            page = (book_info_parsing[i]).strip()
            page = page[:len(page)-1]
            #책 쪽수
        elif book_info_parsing[i].find("mm")>=0:
            if book_info_parsing[i].find("(")>=0:
                size = book_info_parsing[i].split("(")[0].strip()
                #책 크기
            else:
                size = book_info_parsing[i].strip()
                #책 크기
        elif unicode(book_info_parsing[i]).find(u"본")>=0:
            #-*- coding: utf-8 -*-
            cover = book_info_parsing[i].strip()
            #책 커버
        elif book_info_parsing[i].find("g")>=0:
            weight = book_info_parsing[i].replace("g","").strip()
            #책 무게
        elif book_info_parsing[i].find("ISBN")>=0:
            ISBN = book_info_parsing[i].split(":")[1].strip()
            #책 ISBN
        
    
    #책 정보2를 | 기준으로 파싱

    book_info2_parsing = book_info2.split("|")

    for i in range(0,len(book_info2_parsing)):
        book_writers = book_info2_parsing[i].strip()
        if unicode(book_writers).find(u"(지은이)")>=0:
            temp  = unicode(book_writers).split(u"(지은이)")
            #-*- coding: utf-8 -*-    
            writer = temp[0].strip()
            
            if i>0:
                for j in range(i-1,-1,-1):
                    writer += ", " + book_info2_parsing[j].strip()
        elif unicode(book_writers).find(u"(엮은이)")>=0:
            temp  = unicode(book_writers).split(u"(엮은이)")
            #-*- coding: utf-8 -*-
            writer = temp[0].strip()
        elif unicode(book_writers).find(u"(글)")>=0:
            temp  = unicode(book_writers).split(u"(글)")
            #-*- coding: utf-8 -*-
            writer = temp[0].strip()
        elif unicode(book_writers).find(u"(원작)")>=0:
            temp  = unicode(book_writers).split(u"(원작)")
            #-*- coding: utf-8 -*-
            writer = temp[0].strip()
        
        #작가
    if writer == "NA":
        writer = book_info2_parsing[0]

    temp=0;
    if unicode(book_info2_parsing[len(book_info2_parsing)-1]).find(u"원제")>=0:
        temp=1;

    #-*- coding: utf-8 -*-
    publisher = book_info2_parsing[len(book_info2_parsing)-2-temp].strip()
    #출판사
    date = book_info2_parsing[len(book_info2_parsing)-1-temp].strip()
    #출판날짜

    #-*- coding: utf-8 -*-

    print "name        : " , name
    print "writer      : " , writer
    print "date        : " , date
    print "price       : " , price
    print "cover       : " , cover
    print "page        : " , page
    print "size        : " , size
    print "weight      : " , weight
    print "category    : " , category
    print "ISBN        : " , ISBN
    print "publisher   : " , publisher
    print "sales point : " , sales_point
    print "--------------------------------------------"

    book_name.append(name)
    book_writer.append(writer)
    book_date.append(date)
    book_price.append(price)
    book_cover.append(cover)
    book_page.append(page)
    book_size.append(size)
    book_weight.append(weight)
    book_category.append(category)
    book_ISBN.append(ISBN)
    book_publisher.append(publisher)
    book_sales_point.append(sales_point)

    count = count+1

with open('./book_data.csv', 'w') as csvfile:
    fieldnames = ['book_name','book_writer','book_date','book_price','book_cover','book_page','book_size','book_weight','book_category','book_ISBN','book_publisher','sales_point']
    fwriter =  csv.DictWriter(csvfile, fieldnames=fieldnames)
    fwriter.writeheader()
    fwriter.writerow("\xEF\xBB\xBF")
    for i in range(0,count):
        fwriter.writerow({'book_name':book_name.pop().encode('utf-8'),'book_writer':book_writer.pop().encode('utf-8'),'book_date':book_date.pop().encode('utf-8'),'book_price':book_price.pop().encode('utf-8'),'book_cover':book_cover.pop().encode('utf-8'),'book_page':book_page.pop().encode('utf-8'),'book_size':book_size.pop().encode('utf-8'),'book_weight':book_weight.pop().encode('utf-8'),'book_category':book_category.pop().encode('utf-8'),'book_ISBN':book_ISBN.pop().encode('utf-8'),'book_publisher':book_publisher.pop().encode('utf-8'),'sales_point':book_sales_point.pop().encode('utf-8')})


