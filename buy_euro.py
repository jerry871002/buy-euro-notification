import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='buy_euro_log.txt')

TARGET = 35.05
API_KEY = 'your api key here'

def main():
    current_time = datetime.now().strftime("%m/%d %H:%M")

    currency_list = get_currency_list()
    euro_prices = get_euro_prices(currency_list)

    logging.info(euro_prices)

    current_price = float(euro_prices[3])
    previous_price = get_previous_price()

    if current_price <= TARGET and current_price != previous_price:
        response = requests.get(f"https://maker.ifttt.com/trigger/buy_euro_currency/with/key/{API_KEY}?value1={euro_prices[3]}&value2={euro_prices[4]}&value3={current_time}")

        if response.status_code == 200:
            logging.info("Message sent.")
        else:
            logging.error(f"Status code: {response.status_code}")
            logging.error("Something went wrong with the IFTTT service.")

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

if __name__ == '__main__':
    main()
