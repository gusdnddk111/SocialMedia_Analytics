#-*- coding: utf-8 -*-
import requests
import urllib

from bs4 import BeautifulSoup

bookURL_List=[]

def spider(page):
    url = 'http://www.aladin.co.kr/shop/common/wnew.aspx?ViewRowsCount=50&ViewType=Detail&BranchType=1&PublishDay=168&NewType=SpecialNew&page=' + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    for tag in soup.findAll("a",{"class":"bo3"}):
        href = tag.get('href')
        bookURL_List.append(href)

    print (len(bookURL_List))


#1페이지부터 i-1페이지까지
for i in range(1,2):
    spider(i)

fp = open("book_data.txt", 'w')
fp.write("제목\t작가\t출판사\t출판날짜\t가격\t페이지수\t크기\t표지\t무게\t분류\tISBN\tsales point\n")

#책 하나하나 정보 크롤링하기
for i in range(0,len(bookURL_List)):
    book_url = bookURL_List.pop()
    source_code = requests.get(book_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    
    book_name = "NA"
    book_price = "NA"
    book_writer = "NA"
    book_publisher = "NA"
    book_category = "NA"
    book_page = "NA"
    book_size = "NA"
    book_cover = "NA"
    book_weight = "NA"
    book_ISBN = "NA"
    book_date = "NA"
    sales_point = "NA"


    book_name = soup.find("a",{"class":"p_topt01"}).text
    #책이름
    book_price = soup.find("span",{"class":"p_new_price_ph"}).text
    #책가격
    sales_point = soup.find("ul",{"class":"r_topsidebox"}).find("div").find("strong").text
    #판매량
    book_category = soup.findAll("a",{"class":"ml"})[1].text
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
            book_page = (book_info_parsing[i]).strip()
            book_page = book_page[:len(book_page)-1]
            #책 쪽수
        elif book_info_parsing[i].find("mm")>=0:
            if book_info_parsing[i].find("(")>=0:
                book_size = book_info_parsing[i].split("(")[0].strip()
                #책 크기
            else:
                book_size = book_info_parsing[i].strip()
                #책 크기
        elif unicode(book_info_parsing[i]).find(u"본")>=0:
            #-*- coding: utf-8 -*-
            book_cover = book_info_parsing[i].strip()
            #책 커버
        elif book_info_parsing[i].find("g")>=0:
            book_weight = book_info_parsing[i].replace("g","").strip()
            #책 무게
        elif book_info_parsing[i].find("ISBN")>=0:
            book_ISBN = book_info_parsing[i].split(":")[1].strip()
            #책 ISBN
        
    
    #책 정보2를 | 기준으로 파싱

    book_info2_parsing = book_info2.split("|")

    for i in range(0,len(book_info2_parsing)):
        book_writers = book_info2_parsing[i].strip()
        if unicode(book_writers).find(u"(지은이)")>=0:
            temp  = unicode(book_writers).split(u"(지은이)")
            #-*- coding: utf-8 -*-    
            book_writer = temp[0].strip()
            
            if i>0:
                for j in range(i-1,-1,-1):
                    book_writer += ", " + book_info2_parsing[j].strip()
        elif unicode(book_writers).find(u"(엮은이)")>=0:
            temp  = unicode(book_writers).split(u"(엮은이)")
            #-*- coding: utf-8 -*-
            book_writer = temp[0].strip()
        elif unicode(book_writers).find(u"(글)")>=0:
            temp  = unicode(book_writers).split(u"(글)")
            #-*- coding: utf-8 -*-
            book_writer = temp[0].strip()
        elif unicode(book_writers).find(u"(원작)")>=0:
            temp  = unicode(book_writers).split(u"(원작)")
            #-*- coding: utf-8 -*-
            book_writer = temp[0].strip()
        
        #작가
    if book_writer == "NA":
        book_writer = book_info2_parsing[0]

    temp=0;
    if unicode(book_info2_parsing[len(book_info2_parsing)-1]).find(u"원제")>=0:
        temp=1;

    #-*- coding: utf-8 -*-
    book_publisher = book_info2_parsing[len(book_info2_parsing)-2-temp].strip()
    #출판사
    book_date = book_info2_parsing[len(book_info2_parsing)-1-temp].strip()
    #출판날짜

    #-*- coding: utf-8 -*-

    print "name        : " , book_name
    print "writer      : " , book_writer
    print "date        : " , book_date
    print "price       : " , book_price
    print "cover       : " , book_cover
    print "page        : " , book_page
    print "size        : " , book_size
    print "weight      : " , book_weight
    print "category    : " , book_category
    print "ISBN        : " , book_ISBN
    print "publisher   : " , book_publisher
    print "sales point : " , sales_point
    print "--------------------------------------------"


    book_string = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (book_name, book_writer, book_publisher, book_date, book_price, book_page, book_size, book_cover, book_weight, book_category, book_ISBN, sales_point)
    
    fp.write(book_string.encode("utf-8"))

fp.close()
