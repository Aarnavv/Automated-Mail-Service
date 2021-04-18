from random import *
import datetime as dt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas
import requests
import yagmail
import os
os.system('cls')

GMAIL = "***"
PASSWORD = "***"
W_GMAIL = "***"
W_PASSWORD = "***"
EMAIL_TO_SEND_TO = "***"
EMAILS_TO_SEND_TO = ["***",
                     "***",
                     "***"]
PYTHON_ANYWHERE_URL = "https://pythonanywhere.com"
GOOGLE_NEWS_URL = "https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/onecall"
NASA_API_URL = "https://api.nasa.gov/planetary/apod"
PIXABAY_API_URL = "https://pixabay.com/api/"
GNEWS_API_URL = "https://newsapi.org/v2/top-headlines?sources=google-news-in"
BTC_API_URL = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=INR&apikey=***"
DOGE_API_URL = "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol=DOGE&market=INR&apikey=***"
EXCHANGE_API_URL = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=INR&apikey=***"
TSLA_API_URL = "http://api.marketstack.com/v1/eod/latest?access_key=***&symbols=TSLA"
AAPL_API_URL = "http://api.marketstack.com/v1/eod/latest?access_key=***&symbols=AAPL"
AMZN_API_URL = "http://api.marketstack.com/v1/eod/latest?access_key=***&symbols=AMZN"
REL_API_URL = "http://api.marketstack.com/v1/eod/latest?access_key=***&symbols=RELIANCE.XBOM"
INFY_API_URL = "http://api.marketstack.com/v1/eod/latest?access_key=***&symbols=INFY.XBOM"
TCS_API_URL = "http://api.marketstack.com/v1/eod/latest?access_key=***&symbols=TCS.XBOM"
MY_LAT = ***
MY_LONG = ***
YAG = yagmail.SMTP(GMAIL, PASSWORD)

#----------------------------------- AUTOMATED BIRTHDAY REMINDER -------------------------------------#
now_time_bday = dt.datetime.now()
date_bday = now_time_bday.day
month_bday = now_time_bday.month
today = (month_bday, date_bday)

data_birthday = pandas.read_csv("AutomatedBirthdayReminder/birthdays.csv")
birthdays_dict = {(data_row.month, data_row.day): data_row for (index, data_row) in data_birthday.iterrows()}

if today in birthdays_dict:
    birthday_person = birthdays_dict[today]
    with open(f"AutomatedBirthdayReminder/reminder_format.txt", 'r') as f:
        lines = f.readlines()
        lines[0] = lines[0].replace("[NAME]", birthday_person["name"])
        reminder = ''.join(lines)
    subject = "Automated Birthday Reminder"
    contents = [f"{reminder}"]
    YAG.send(EMAIL_TO_SEND_TO, subject, contents)

#--------------------------------- 28 DAYS REMINDER ---------------------------#
def send_reminder_mail():
    subject = "Extend Expiry on Python Anywhere"
    contents = [f"Reminder! Extend your subscription on {PYTHON_ANYWHERE_URL}."]
    YAG.send(EMAIL_TO_SEND_TO, subject, contents)

with open("28DaysReminder/days.txt", 'r') as days_file:
    days = int(days_file.read())

days += 1

if days==27:
    send_reminder_mail()

if days==28:
    send_reminder_mail()
    with open("28DaysReminder/days.txt", 'w') as days_file:
        days_file.write("0")
else:
    with open("28DaysReminder/days.txt", 'w') as days_file:
        days_file.write(str(days))

#------------------------------------- WEATHER FORECAST ---------------------------------#
weather_parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": "***",
    "units": "metric",
}

response_weather = requests.get(url=WEATHER_API_URL, params=weather_parameters)
response_weather.raise_for_status()

weather_data = response_weather.json()

time_timestamp = weather_data["current"]["dt"]
timestamp_for_time = dt.datetime.fromtimestamp(time_timestamp).strftime('%Y-%m-%d %H:%M:%S')

date = timestamp_for_time.split(' ')[0]
time_today = timestamp_for_time.split(' ')[1]

sunrise_timestamp = weather_data["daily"][0]["sunrise"]
timestamp_for_sunrise = dt.datetime.fromtimestamp(sunrise_timestamp).strftime('%Y-%m-%d %H:%M:%S')
sunrise = timestamp_for_sunrise.split(' ')[1]

sunset_timestamp = weather_data["daily"][0]["sunset"]
timestamp_for_sunset = dt.datetime.fromtimestamp(sunset_timestamp).strftime('%Y-%m-%d %H:%M:%S')
sunset = timestamp_for_sunset.split(' ')[1]

min_temp = round(weather_data["daily"][0]["temp"]["min"])
max_temp = round(weather_data["daily"][0]["temp"]["max"])

feels_like = round(weather_data["daily"][0]["feels_like"]["day"])

desc = weather_data["daily"][0]["weather"][0]["description"].title()

weather_titles = ["Sunny with a chance of meatballs?",
                  "Hip, Hip, Hooray for the Hot Summer Day!",
                  "Looks like a rather blustery day today",
                  "Oh! The weather outside is frightful…",
                  "Rough weather ahead?",
                  "Turn up the Heat !_!"]

#---------------------------------- NEWS -------------------------------------------#
gnews_parameters = {
    "apiKey": "***"
}

response_gnews = requests.get(url=GNEWS_API_URL, params=gnews_parameters)
response_gnews.raise_for_status()

gnews_data = response_gnews.json()
gnews_titles = []
gnews_descs = []

for _ in range(1, 6):
    gnews_title = gnews_data["articles"][_]["title"]
    gnews_desc = gnews_data["articles"][_]["description"]
    gnews_titles.append(gnews_title)
    gnews_descs.append(gnews_desc)

for _ in range(len(gnews_descs)):
    if gnews_descs[_][-1] != ".":
        gnews_descs[_] = gnews_descs[_]+"."

response_BTC = requests.get(url=BTC_API_URL)
response_BTC.raise_for_status()

stocks_BTC = response_BTC.json()
price_BTC = round(float(stocks_BTC["Time Series (Digital Currency Daily)"][date]["1a. open (INR)"]))

response_DOGE = requests.get(url=DOGE_API_URL)
response_DOGE.raise_for_status()

stocks_DOGE = response_DOGE.json()
price_DOGE = round(float(stocks_DOGE["Time Series (Digital Currency Daily)"][date]["1a. open (INR)"]))

response_EXCHANGE = requests.get(url=EXCHANGE_API_URL)
response_EXCHANGE.raise_for_status()

stocks_EXCHANGE = response_EXCHANGE.json()
price_EXCHANGE = round(float(stocks_EXCHANGE["Realtime Currency Exchange Rate"]["5. Exchange Rate"]),2)

response_TSLA = requests.get(url=TSLA_API_URL)
response_TSLA.raise_for_status()

stocks_TSLA = response_TSLA.json()
price_TSLA = stocks_TSLA["data"][0]["adj_close"]

response_AAPL = requests.get(url=AAPL_API_URL)
response_AAPL.raise_for_status()

stocks_AAPL = response_AAPL.json()
price_AAPL = stocks_AAPL["data"][0]["adj_close"]

response_AMZN = requests.get(url=AMZN_API_URL)
response_AMZN.raise_for_status()

stocks_AMZN = response_AMZN.json()
price_AMZN = stocks_AMZN["data"][0]["adj_close"]

response_REL = requests.get(url=REL_API_URL)
response_REL.raise_for_status()

stocks_REL = response_REL.json()
price_REL = stocks_REL["data"][0]["adj_close"]

response_INFY = requests.get(url=INFY_API_URL)
response_INFY.raise_for_status()

stocks_INFY = response_INFY.json()
price_INFY = stocks_INFY["data"][0]["adj_close"]

response_TCS = requests.get(url=TCS_API_URL)
response_TCS.raise_for_status()

stocks_TCS = response_TCS.json()
price_TCS = stocks_TCS["data"][0]["adj_close"]

# -------------------------------- SEND DAILY MAIL ----------------------------#
for email in EMAILS_TO_SEND_TO:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Between the lines: The Cable"
    msg['From'] = GMAIL
    msg['To'] = email

    html = open("template.html", 'r', encoding='utf-8').read().format(
        title=choice(weather_titles),
        date=date,
        time=time_today,
        sunrise=sunrise,
        sunset=sunset,
        min_temp=min_temp,
        max_temp=max_temp,
        feels_like=feels_like,
        desc=desc,
        news_title_one=gnews_titles[0],
        news_desc_one=gnews_descs[0],
        news_title_two=gnews_titles[1],
        news_desc_two=gnews_descs[1],
        news_title_three=gnews_titles[2],
        news_desc_three=gnews_descs[2],
        news_title_four=gnews_titles[3],
        news_desc_four=gnews_descs[3],
        news_title_five=gnews_titles[4],
        news_desc_five=gnews_descs[4],
        BTC=price_BTC,
        DOGE=price_DOGE,
        TSLA=price_TSLA,
        AAPL=price_AAPL,
        AMZN=price_AMZN,
        RELIANCE=price_REL,
        INFY=price_INFY,
        TCS=price_TCS,
        EXCHANGE=price_EXCHANGE,
        email=email,
    )

    part1 = MIMEText(html, 'html')
    msg.attach(part1)


    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=GMAIL, password=PASSWORD)
        connection.sendmail(GMAIL, email, msg.as_string())

#------------------------------- EXTRAS ------------------------------#

#------- Attach Images from NASA/PIXABAY APIs ----------#

# nasa_parameters = {
#     "api_key": "***",
# }
# response_nasa = requests.get(url=NASA_API_URL, params=nasa_parameters)
# response_nasa.raise_for_status()

# nasa_data = response_nasa.json()

# nasa_title = nasa_data["title"].upper()
# nasa_desc = nasa_data["explanation"]
# nasa_img_url = nasa_data["url"]
# image_filename = nasa_img_url.split('/')[-1]

# pixabay_parameters = {
#     "key": "***-***"
# }
# response_pixabay = requests.get(url=PIXABAY_API_URL, params=pixabay_parameters)
# response_pixabay.raise_for_status()

# pixabay_data = response_pixabay.json()
# pixabay_image_url = pixabay_data["hits"][randint(0, 19)]["webformatURL"]
# image_filename = pixabay_image_url.split('/')[-1]

# def get_image(img_url, image_filename):
#     image = requests.get(img_url, stream=True)
#     if image.status_code == 200:
#         image.raw.decode_content = True
#         with open(f"Images/{image_filename}", 'wb') as image_file:
#             shutil.copyfileobj(image.raw, image_file)
#     else:
#         image.raise_for_status()

# get_image(image_url, image_filename)