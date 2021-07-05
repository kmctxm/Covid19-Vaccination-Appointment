import sys
from selenium import webdriver
import time
import requests

#----------------------------------------------------------------------------
# 実行ファイルのディレクトリ指定
Edir = "C:\\Physon-Code\\Covid19-ワクチン予約"

# Webdriverのパス指定
DPath = "C:\\Physon-Code\\chromedriver.exe"

# ログイン対象のWebページURLを宣言します 
url = "https://ssc2.doctorqube.com/child-clinic-ariake/input.cgi?vMode=mode_book&stamp=534841" 

# 待ち時間設定。環境によって最適な値を指定してください
INTERVAL = 1

#----------------------------------------------------------------------------

# 起動するブラウザを宣言します 
browser = webdriver.Chrome(DPath) 
# 対象URLをブラウザで表示します。 
browser.get(url)

# サイト内でユーザー/パスワードが必要な場合はログインIDとパスワードを入力します。

# ログインIdとパスワードの入力領域を取得します。 
login_id = browser.find_element_by_xpath("//input[@id='c_code']") 
login_pw = browser.find_element_by_xpath("//input[@id='c_pass']")

userid = "" 
userpw = ""
login_id.send_keys(userid) 
login_pw.send_keys(userpw)

# 以下はサイトの作り次第。クリック操作
login_btn = browser.find_element_by_xpath(".//input[@name='bOK']") 
login_btn.click()

time.sleep(INTERVAL)
login_btn = browser.find_element_by_xpath(".//input[@name='bOK']") 
login_btn.click()

time.sleep(INTERVAL)
browser.find_element_by_link_text("新型コロナワクチンの予約").click()

time.sleep(INTERVAL)
browser.find_element_by_link_text("新型コロナワクチン1回目").click()

time.sleep(INTERVAL)
GuideMsg = browser.find_element_by_class_name('guidetext').text

if '大変申し訳ございません。' in GuideMsg: StatusMsg = GuideMsg
else: StatusMsg = '予約に空きがあります'


# LINE APIとの連携
url_items = 'https://api.line.me/v2/bot/message/broadcast'
item_data = {
    #'to': '',
    'messages': [
      {
        'type':'text',
        'text':'有明医院'
      },
      {
        'type':'text',
        'text': StatusMsg
      }
    ]
}

headers = {
  'Authorization':'Bearer <Bearer Code>',
  'Content-Type':'application/json'
  }

r_post = requests.post(url_items, headers=headers, json=item_data)
print(r_post)

# if StatusMsg =='大変申し訳ございません。ご予約はすべて埋まっております。':
browser.quit()