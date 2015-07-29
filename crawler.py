import requests
from bs4 import BeautifulSoup
import urllib2,cookielib
import MySQLdb

#response=requests.get("https://www.v2ex.com",verify=False)
#soup1=BeautifulSoup(response.text)
url="https://www.v2ex.com"
hdr={'Accept':'text/html,application/xtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Charest':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
     'User-Agent':"Magic Browser"}
req=urllib2.Request(url,headers=hdr)
page=urllib2.urlopen(req)
content=page.read()
soup=BeautifulSoup(content)
#table=soup.find('div',attrs={"id":"Wrapper"})
#spans=table.find('div',attrs={"class":"content"})
#main=spans.find('div',attrs={"id":"Main"})
#box=main.find('div',attrs={"class":"box"})

items=soup.findAll('div',attrs={"class":"cell item"})
message=[]

def SelectByAuthor(author):
   try:
       db=MySQLdb.connect(host="localhost",uer="root",passwd="zhangyige",db="webinfo",port=3306,use_unicode=True,charset="utf8mb4")
       cursor=db.cursor()
       authorlist=cursor.exeute("select topic_name,link from v2ex where author='%s'" % (author))
       db.commit()
       cursor.close()
       db.close()
       return authorlist
   except MySQLdb.Error,e:
       print 'mysql error %d: %s' % (e.args[0],e.args[1])

def SelectBySubject(subject):
    try:
        db=MySQLdb.connect(host="localhost",user="root",passwd="zhangyige",db="webinfo",port=3306,use_unicode=True,charset="utf8mb4")
        cursor=db.cursor()
        subjectlist=cursor.execute("select topic_name,link from v2ex where author='%s'" % (subject))
        db.commit()
        cursor.close()
        db.close()
        print (subjectlist)
    except MySQLdb.Error,e:
        print 'mysql error %d: %s' % (e.args[0],e.args[1])



for item in items:
    spans=item.findAll('span',attrs={"class":"item_title"})

    for span in spans:
        print("start:"+span.text.lower())
        links=[a.attrs.get('href') for a in span.select('a[href^=/t]')]
        nelink="https://www.v2ex.com"+links[0]
        list.append(message,nelink)
        list.append(message,span.text.lower())
        print(nelink)
       # sub_url=requests.get(nelink,verify=False)
       # sub_soup=BeautifulSoup(sub_url.text)
        sub_req=urllib2.Request(nelink,headers=hdr)
        sub_page=urllib2.urlopen(sub_req)
        sub_content=sub_page.read()
        sub_soup=BeautifulSoup(sub_content)
        p=[a.get_text() for a in sub_soup.select('div.markdown_body')]
        if p:
           print(p[0])
           list.append(message,p[0])
        else:
           list.append(p,"No more Content")
           print("No more Content!")
           list.append(message,p[0])

    spans2=item.findAll('span',attrs={"class":"small fade"})

    for span2 in spans2:
         classify=span2.find('a',attrs={"class":"node"})
         list.append(message,classify.text.lower())
         print("subject:"+classify.text.lower())
         #type(classify.text.lower())
         print(type(classify.text.lower()))
    strong=item.find('strong')
    print("author:"+strong.text.lower())
    list.append(message,strong.text.lower())

    try:
          conn=MySQLdb.connect(host='localhost',user='root',passwd='zhangyige',db='webinfo',port=3306,use_unicode=True,charset="utf8mb4")

          cur=conn.cursor()
          cur.execute('SET NAMES utf8mb4;')
          count=cur.execute("select * from v2ex where link='%s'" %( message[0]) )
          print(message[1])
          print(count)

          if count==0:
             cur.execute("insert into v2ex(topic_name,subject,author,content,link) values('%s','%s','%s','%s','%s')" % (message[1],message[3],message[4],message[2],message[0]))
             print 'ok'
          message=[]
          conn.commit()
          cur.close()
          conn.close()

    except MySQLdb.Error,e:
          print "mysql error %d:%s" % (e.args[0],e.args[1])
