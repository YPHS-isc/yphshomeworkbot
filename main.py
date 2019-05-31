# !/usr/bin/python 
# coding:utf-8 
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

#紀錄檔PATH(建議絕對位置)
log_path='./log.txt'

#登入聯絡簿的個資
sid=''#學號(Ex. 10731187)
cid=''#生份證號(Ex. A123456789)
bir=''#生日(Ex. 2000/1/1)

#line or telegram module

#platform='telegram'
platform='line'

if platform=='line':
    from linebot import LineBotApi
    from linebot.models import TextSendMessage
    #line api token
    bottoken=''
    #line chat id
    chatid=''

    line_bot_api = LineBotApi(bottoken)

if platform=='telegram':
    #telegram bot token
    bottoken=''
    #telegram group chat id
    chatid=''

#課表
cls=[['學校活動','英文','化學','國文','地理','生物','公民','歷史','數學'],
     ['彈性課程','地科','數學','數學','資訊','西洋影視','國文','國文','英文'],
     ['數學','物理','生活科技','體育','國文','化學','音樂','英文','英文'],
     ['數學','論孟選讀','生物','多元選修','歷史','化學','英文','國防','物理'],
     ['彈性課程','英文','數學','地理','公民','國文','體育','物理','社團'],[],[]]

def open_log():
    global log
    global fw
    try:
        fr = open(log_path, "r")
        log=fr.read().split('\n')
        fr.close()
    except:
        fw = open(log_path, "w+")
        log=''
        return
    fw = open(log_path, "a")
    return

def login_homework():
    res = requests.get('http://www.yphs.tp.edu.tw/tea/tu2.aspx')
    soup = BeautifulSoup(res.text, "lxml")
    VIEWSTATE=soup.find(id="__VIEWSTATE")
    VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")
    EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")
    res=requests.post('http://www.yphs.tp.edu.tw/tea/tu2.aspx', allow_redirects=False, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),'chk_id':'學生／家長','tbx_sno':sid,'tbx_sid':cid,'tbx_sbir':bir,'but_login_stud':'登　　入'})
    global cook
    cook=res.cookies['ASP.NET_SessionId']
    return

def crawl_and_fetch_today_homework(tomorrow_calendar,tomorrow_class_table):
    send = requests.get('http://www.yphs.tp.edu.tw/tea/tu2-1.aspx',cookies={'ASP.NET_SessionId':cook})
    soup = BeautifulSoup(send.text, "lxml")
    VIEWSTATE=soup.find(id="__VIEWSTATE")
    VIEWSTATEGENERATOR=soup.find(id="__VIEWSTATEGENERATOR")
    EVENTVALIDATION=soup.find(id="__EVENTVALIDATION")
    for x in range(15,1,-1):#第一頁1~15則
        try:#用try怕有頁面沒15則post
            #數字轉文字
            num=str('')
            if(x<10):
                num='0'+str(x)
            else:
                num=str(x)
            #爬內文
            send = requests.post('http://www.yphs.tp.edu.tw/tea/tu2-1.aspx',cookies={'ASP.NET_SessionId':cook}, data = {'__VIEWSTATE':VIEWSTATE.get('value'),'__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR.get('value'),'__EVENTVALIDATION':EVENTVALIDATION.get('value'),('GridViewS$ctl'+num+'$but_vf1'):'詳細內容'})
            soup = BeautifulSoup(send.text, "lxml")
            #檢查市否已發過
            ok=bool(True)
            for y in range(0,len(log),1):
                if soup.find(id='Lab_purport').text==log[y]:
                    ok=bool(False)
            if ok==True:#沒發過
                fw.write(soup.find(id='Lab_purport').text+'\n')
                post_title=str('[主旨:'+str(soup.find(id='Lab_purport').text)+']')
                post_content=str(soup.find(id='Lab_content').text)
                post_attachment=str(' ')
                if(soup.find(target='_blank')):
                    post_attachment=soup.find(target='_blank').get('href')
                send_word=post_title+'\n'+post_content+'\n'+post_attachment
                if(str(soup.find(id='Lab_purport').text).find('聯絡簿')>=0 and datetime.today().weekday()<4):
                    send_word=send_word+'\n***系統訊息***\n'+tomorrow_calendar+'\n'+tomorrow_class_table
                if(str(soup.find(id='Lab_purport').text).find('聯絡簿')>=0 and datetime.today().weekday() == 4 ):
                    send_word=send_word
                post(send_word)
        except:
            pass
    return

def crawl_tomorrow_calendar():
    res = requests.get('http://www.yphs.tp.edu.tw/yphs/gr2.aspx')
    soup = BeautifulSoup(res.text, "lxml")
    calendar='明日行事曆:\n 全校:'+soup.find_all(color="#404040")[16].text
    if(soup.find_all(color="#404040")[16].text==' '):
        calendar+='N/A'
    calendar=calendar+'\n 高一:'+soup.find_all(color="#404040")[21].text
    if(soup.find_all(color="#404040")[21].text==' '):
        calendar+='N/A'
    return calendar

def fetch_tomorrow_class_table():
    count=int(0)
    tomorrow_class='\n明日課表:\n 早上:\n  '
    for i in cls[(datetime.today().weekday()+1)%7]:
        if(count==4):
            tomorrow_class+='\n 下午:\n  '
        tomorrow_class+='['+i+']'
        if(count<8 and count!=3):
            tomorrow_class+='->'
        count+=1
    return tomorrow_class

def post(send_word):
    if platform=='line':
        line_bot_api.push_message(chatid,TextSendMessage(text=send_word,wrap=True))
    if platform=='telegram':
        requests.get("https://api.telegram.org/bot"+bottoken+"/sendMessage?chat_id="+chatid+"&text="+send_word)
'''

!!!contact ab0897867564534231@gmail.com for this function!!!

def crawl_message_board():
    res = requests.get('http://59.120.227.144:11300/line/api.php')
    soup = BeautifulSoup(res.text, "lxml")
    message_board = soup.find_all('td')
    message='\n\n留言板( http://59.120.227.144:11300/line/ ) : \n'
    for i in range(0,len(message_board),3):
        message=message+'第'+str(int((i/3)+1))+'則:\n-'+message_board[i+1].text+"\n--來自:"+message_board[i+2].text+'\n'
    return message
'''

def close_log():
    fw.close()

def main():
    open_log()
    login_homework()
    crawl_and_fetch_today_homework(crawl_tomorrow_calendar(),fetch_tomorrow_class_table())
    close_log()

    #星期天提醒明天要上課
    if(datetime.today().weekday()==6 and datetime.today().hour == 21 and datetime.today().minute<10):
        send_word='[主旨:機器人訊息]\n***系統訊息***\n'+crawl_tomorrow_calendar()+'\n'+fetch_tomorrow_class_table()
        post(send_word)
main()