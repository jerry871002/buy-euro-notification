import requests
import pandas
import re
from bs4 import BeautifulSoup
from datetime import datetime

TARGET = 35.05
API_KEY = 'your own key hear'

dt = datetime.now().strftime("%m/%d %H:%M")

r = requests.get("https://wwwfile.megabank.com.tw/rates2/M001/viewF_new_02_02.asp")
c = r.content
soup = BeautifulSoup(c, "html.parser")
currency_list = soup.find_all("tr", {"class": re.compile("tbcolor[12]")})

euro = []
for item in currency_list:
    currency = item.find_all("td")
    if currency[0].text == "歐元[EUR]":
        for i in range(len(currency)):
            euro.append(currency[i].text)

print(dt, euro)

if float(euro[3]) <= TARGET:
    print("Message sent.")
    requests.get("https://maker.ifttt.com/trigger/currencyLINE/with/key/{}?value1={}&value2={}&value3={}".format(API_KEY, euro[3], euro[4], dt))
