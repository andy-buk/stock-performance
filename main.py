import requests
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText

my_email = "email@gmail.com"
password = "your password"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

today = date.today()
yesterday = today - timedelta(days=1)

stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": "your api key"
}

stock_info = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_price = stock_info.json()

stock_open_today = stock_price["Time Series (Daily)"][str(today)]["1. open"]
stock_high = stock_price["Time Series (Daily)"][str(today)]["2. high"]
stock_low = stock_price["Time Series (Daily)"][str(today)]["3. low"]
stock_close = stock_price["Time Series (Daily)"][str(today)]["4. close"]
stock_close_yesterday = stock_price["Time Series (Daily)"][str(yesterday)]["4. close"]
stock_volume = stock_price["Time Series (Daily)"][str(today)]["6. volume"]
stock_change = round(((float(stock_open_today) - float(stock_close_yesterday)) / float(stock_close_yesterday) * 100), 2)

if stock_change > 0:
    up_down = "📈"
else:
    up_down = "📉"

news_parameters = {
    "apiKey": "your api key",
    "qInTitle": COMPANY_NAME
}

news_info = requests.get(NEWS_ENDPOINT, params=news_parameters)
articles = news_info.json()["articles"]

formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in articles]

message = MIMEText(f"{STOCK_NAME}: {up_down}{stock_change}%\n\nHere are some other statistics:\nOpen: "
                   f"{stock_open_today}\nClose: {stock_close}\nHigh: {stock_high}\nLow: {stock_low}\nVolume:"
                   f" {stock_volume}\n\nThis may be why...\n{formatted_articles[0]}")
message["Subject"] = f"{STOCK_NAME}: {today}"

with smtplib.SMTP("smtp.gmail.com", 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs="recipient",
                        msg=message.as_string())
