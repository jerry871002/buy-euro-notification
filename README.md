# Buy Euro Notification

因為要去義大利玩，幫媽媽寫這個程式看匯率 <br>
用 `requests` 和 `BeautifulSoup` 從銀行網站抓取當時的匯率，若達到特定目標時，用 ~~IFTTT~~ LINE Notify 的服務傳送訊息到 Line 群組<br>
在機器上設定 `crontab` 就可以排程執行

## Update (2020/08/01):

因為要去法國交換，這個程式又重出江湖了<br>
除了原本有的功能外，現在會在匯率有變動時才傳訊息（不然其實蠻煩的）

## Update (2022/03/30):

九月要去芬蘭讀研究所，準備開始換點歐元<br>
改成直接用 LINE Notify 傳到群組，不再透過 IFTTT

## Update (2022/06/17):

銀行的網頁改版了<br>
改成用 API 的方式抓匯率，不用再爬蟲了

## How to setup crontab?

To edit the content of crontab, enter the following command in terminal
```bash
crontab -e
```

A task in crontab is formatted as below
```
m h  dom mon dow   command
```

| Column | Range | Description        |
| ------ | ----- | ------------------ |
| m      | 0-59  |                    |
| h      | 0-23  |                    |
| dom    | 1-31  |                    |
| mon    | 1-12  |                    |
| dow    | 0-7   | 0 and 7 for Sunday |


For example, if you want to set the script to work every 15 minutes during working hours, add

```bash
0,15,30,45 9-15 * * 1-5 python3 <path-to-repo>/buy_euro.py
```

into the crontab and things will work
