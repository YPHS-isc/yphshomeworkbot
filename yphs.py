import requests
from bs4 import BeautifulSoup
import re
#setup
#登入個資
sid='{這裡填你的學號}'
cid='{這裡填你的生份證}'
bir='{這裡填你的生日}'
cook='{向http://www.yphs.tp.edu.tw/tea/tu2.aspx申請cookie,並填入cookie}'
#機器人
bottoken1='{向telegram申請cookie,並填入bot的token}'
chatid1='{這裡填telegram的chatid}'
#!!!do not edit after this line!!!
#!!!do not edit after this line!!!
#!!!do not edit after this line!!!
#!!!do not edit after this line!!!
#!!!do not edit after this line!!!
fr = open("log.txt", "r")
log=fr.read().split('\n')
fr.close()
fw = open("log.txt", "a")
res = requests.get('http://www.yphs.tp.edu.tw/tea/tu2.aspx')
soup = BeautifulSoup(res.text, "lxml")
VIEWSTATE=soup.find(id="__VIEWSTATE")
VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")
EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")
login = requests.post('http://www.yphs.tp.edu.tw/tea/tu2.aspx',cookies={'ASP.NET_SessionId':cook}, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),'chk_id':'學生／家長','tbx_sno':sid,'tbx_sid':cid,'tbx_sbir':bir,'but_login_stud':'登　　入'})
send = requests.get('http://www.yphs.tp.edu.tw/tea/tu2-1.aspx',cookies={'ASP.NET_SessionId':cook})
soup = BeautifulSoup(send.text, "lxml")
VIEWSTATE=soup.find(id="__VIEWSTATE")
VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")
EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")
for x in range(15,1,-1):
    num=str('')
    if(x<10):
        num='0'+str(x)
    else:
        num=str(x)
    send = requests.post('http://www.yphs.tp.edu.tw/tea/tu2-1.aspx',cookies={'ASP.NET_SessionId':cook}, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),('GridViewS$ctl'+num+'$but_vf1'):'詳細內容'})
    soup = BeautifulSoup(send.text, "lxml")
    ok=bool(True)
    for y in range(0,len(log),1):
        if soup.find(id='Lab_purport').text==log[y]:
            ok=bool(False)
    if ok==True:
        print('主旨:'+soup.find(id='Lab_purport').text,end='')
        fw.write(soup.find(id='Lab_purport').text+'\n')
        print(soup.find(id='Lab_content').text,end='')
        ans=str("")
        if(soup.find(target='_blank')):
            print(soup.find(target='_blank').get('href'))
            ans=soup.find(target='_blank').get('href')
        print('\n')
        haha=requests.get("https://api.telegram.org/bot"+bottoken1+"/sendMessage?chat_id="+chatid1+"&text=主旨:"+str(soup.find(id='Lab_purport').text)+str(soup.find(id='Lab_content').text)+ans)
fw.close()
