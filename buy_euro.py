import json
import requests
from datetime import datetime
from pathlib import Path

import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=Path(__file__).parent / 'buy_euro_log.txt'
)

API_KEY = 'your api key here'
TARGET_PRICE = 31.5

def main():
    current_time = datetime.now().strftime("%m/%d %H:%M")

    currency_list = get_currency_list()
    euro_prices = get_euro_prices(currency_list)

    logging.info(euro_prices)

    if not euro_prices:
        logging.warning("No data in the response.")
        msg = (
            "\n無法從網站上抓取資料\n"
            f"更新時間： {current_time}"
        )

        response = post_to_line_chat(msg)
        if response.status_code == 200:
            logging.info("Message sent.")
        else:
            logging.error(f"Status code: {response.status_code}")
            logging.error("Something went wrong with the LINE Notify service.")
        
        return 

    current_price = float(euro_prices['spotExchangeRate']['sale'])
    previous_price = get_previous_price()

    if current_price <= TARGET_PRICE and current_price != previous_price:
        msg = (
            "\n快買歐元喔！\n"
            f"即期賣匯： {euro_prices['spotExchangeRate']['sale']}\n"
            f"現金賣匯： {euro_prices['cashExchangeRate']['sale']}\n"
            f"更新時間： {current_time}"
        )

        response = post_to_line_chat(msg)

        if response.status_code == 200:
            logging.info("Message sent.")
        else:
            logging.error(f"Status code: {response.status_code}")
            logging.error("Something went wrong with the LINE Notify service.")

        # save current price to file
        print(euro_prices['spotExchangeRate']['sale'], file=open('previous_price.txt', 'w'))

def get_currency_list():
    r = requests.post("https://www.megabank.com.tw/api/sc/RateExchange/Get_Fx_Currency")
    return json.loads(r.content.decode('utf-8'))['appRepBody']['exchangeRates']

def get_euro_prices(currency_list):
    for item in currency_list:
        if item['currency'] == 'EUR':
            return item

    # if something went wrong, return an empty dictionary
    return {}

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
