# 延平中學聯絡簿telegram/line自動播送程式

<h2>示例：</h2><br>
<img src="https://github.com/chenliTW/yphshomeworkbot/raw/master/pic/run_line.png" height="500"><br>
<img src="https://github.com/chenliTW/yphshomeworkbot/raw/master/pic/run.png" height="500"><br>
<h2>使用教學：</h2><br>
1.(telegram)去跟Telegram的botfather申請token，然後把那個bot加到你要放的群組裡，並取的那個群組的chatid.<br>
1.(line)去line@申請bot並取得token，然後把那個bot加到你要放的群組裡，並取得那個群組的chatid.<br>
有問題請聯絡ab0897867564534231@gmail.com
<br>
2.填入登入資訊，由上到下依序填入學號(sid),生份證(cid),生日(bir),機器人的token(bottoken),與群組的chatid(chatid)<br>
<img src="https://github.com/chenliTW/yphshomeworkbot/raw/master/pic/setup.png" width="500">
<br>
3.設定crontab<br>
ex.*/1 * * * * python3 /yphs.py<br>
3.或著deploy on heroku<br>
