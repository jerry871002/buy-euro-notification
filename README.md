# Buy Euro

因為要去義大利玩，幫媽媽寫這個程式看匯率 <br>
用 `requests` 和 `BeautifulSoup` 從銀行網站抓取當時的匯率，若達到特定目標時，用 `IFTTT` 的服務傳送訊息到 Line 群組
在機器上設定 `crontab` 就可以排程執行

## Update(2020/08/01):

因為要去法國交換，這個程式又重出江湖了<br>
除了原本有的功能外，現在會在匯率有變動時才傳訊息（不然其實蠻煩的）
