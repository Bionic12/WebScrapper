import requests
from bs4 import BeautifulSoup
import sqlite3

def StringToInt(a):
        b=0
        for i in a:
                if i<='9' and i>='0':
                        b=b*10+int(i)
        return b

conn = sqlite3.connect('example.db')
 
try:
        conn.execute('''Drop table blogs''')
except:pass
finally: conn.execute('''CREATE TABLE blogs
             (title text, href text, comments integer )''')       






url = r'https://www.copyblogger.com/blog/'
response = requests.get(url)
soup=BeautifulSoup(response.text, "html.parser")

for i in soup.findAll("article"):
        response2=requests.get(i.header.h2.a["href"])
        soup2=BeautifulSoup(response2.text, "html.parser")
        a=soup2.find(id='comments')
        if a is not None:
                x=i.header.h2.a.text
                y=i.header.h2.a["href"]
                z=StringToInt(a.h3.text)
                conn.execute("INSERT INTO blogs VALUES ('" +x+ "','" +y+ "',"+str(z)+")")
                







numberOfPagesString=soup.findAll("span","screen-reader-text")[4].parent.text
numberOfPages=StringToInt(numberOfPagesString)
for i in range(2,numberOfPages+1):
        urli=r"https://www.copyblogger.com/blog/page/"+str(i)+r"/"
        response = requests.get(urli)
        soup=BeautifulSoup(response.text, "html.parser")
        print(i)
        for i in soup.findAll("article"):
                response2=requests.get(i.header.h2.a["href"])
                soup2=BeautifulSoup(response2.text, "html.parser")
                a=soup2.find(id='comments')
                if a is not None:
                        x=i.header.h2.a.text
                        y=i.header.h2.a["href"]
                        z=StringToInt(a.h3.text) 
                        conn.execute("INSERT INTO blogs VALUES ('" +x+ "','" +y+ "',"+str(z)+")")
                        
for r in conn.execute("Select * from blogs order by comments desc limit 10"):
        print(*r)







