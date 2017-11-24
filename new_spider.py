#-*- coding: utf8 -*-
import urllib2
from bs4 import BeautifulSoup

def download(url):
    print 'Downloading:',url
    try:
        html=urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html=None
    return html

def getinfo_guotu3(isbn, number, position):
    url='http://find.nlc.cn/search/doSearch?query='+isbn+'&secQuery=&actualQuery='+isbn+'&searchType=2&isGroup=isGroup'
    html=download(url)
    soup1=BeautifulSoup(html,'html.parser')
    docid=soup1('h4')[0]('a')[1]['id'] #用于链接至结果页

    pubdate=soup1('ul')[3]('li')[0]['title']
    author=soup1('ul')[4]('li')[0]['title']
    publisher=soup1('p')[2]('em')[1].text.replace('\n','').replace('\t','')
    price= None
    #进入第一条结果页
    url2='http://find.nlc.cn/search/showDocDetails?docId='+docid+'&dataSource=ucs01&query='+isbn
    soup2 = BeautifulSoup(download(url2), 'html.parser')
    title=soup2.b.text
    subject=None
    callnumber=None
    for i in range(5,15):
        if (soup2('p')[i].text.replace('\n', '').replace('\t', '').strip( )[0:3] == u"关键词"):
            subject = soup2('p')[i].text.replace('\n', '').replace('\t', '').strip( )[4:]
        if (soup2('p')[i].text.replace('\n', '').replace('\t', '').strip( )[0:2] == u"分类"):
            callnumber = soup2('p')[i].text.replace('\n', '').replace('\t', '').strip( )[9:]
        if (soup2('p')[i].text.replace('\n', '').replace('\t', '').strip( )[0:4] == u"载体形态"):
            pages=soup2('p')[i].text.replace('\n','').replace('\t','').strip( )[5:]
        if (soup2('p')[i].text.replace('\n', '').replace('\t', '').strip( )[0:2] == u"摘要"):
            summary=soup2('p')[i].text.replace('\n','').replace('\t','').strip( )[2:]
        else:
            continue
    return [int(isbn), "《" + title + "》", author, publisher, pubdate, pages, price, subject, int(number), callnumber,
            summary, "国家图书馆2", None, None, position]

