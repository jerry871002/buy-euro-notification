import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='buy_euro_log.txt')

API_KEY = 'your api key here'
TARGET_PRICE = 31.5

def main():
    current_time = datetime.now().strftime("%m/%d %H:%M")

    currency_list = get_currency_list()
    euro_prices = get_euro_prices(currency_list)

    logging.info(euro_prices)

    current_price = float(euro_prices[3])
    previous_price = get_previous_price()

    if current_price <= TARGET_PRICE and current_price != previous_price:
        msg = "\n快買歐元喔！\n" \
             f"即期賣匯： {euro_prices[3]}\n" \
             f"現金賣匯： {euro_prices[4]}\n" \
             f"更新時間： {current_time}"

        response = post_to_line_chat(msg)

        if response.status_code == 200:
            logging.info("Message sent.")
        else:
            logging.error(f"Status code: {response.status_code}")
            logging.error("Something went wrong with the LINE Notify service.")

        # save current price to file
        print(euro_prices[3], file=open('previous_price.txt', 'w'))

def get_currency_list():
    r = requests.get("https://wwwfile.megabank.com.tw/rates2/M001/viewF_new_02_02.asp")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    return soup.find_all("tr", {"class": re.compile("tbcolor[12]")})

def get_euro_prices(currency_list):
    result = []
    for item in currency_list:
        currency = item.find_all("td")
        if currency[0].text == "歐元[EUR]":
            for i in range(len(currency)):
                result.append(currency[i].text)
    return result

def get_previous_price():
    try:
        with open('previous_price.txt', 'r') as f:
            result = float(f.read())
    except Exception:
        result = None
    return result

def post_to_line_chat(msg):
    headers =  {
        "Authorization": "Bearer " + TOKEN, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    return requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)

if __name__ == '__main__':
    main()
