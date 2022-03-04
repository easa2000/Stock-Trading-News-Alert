import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
TWILIO_SID = "ACb0717b8deabeeb6bbc2a17e753132e02"
TWILIO_AUTH_TOKEN = "078d1aefa51403d560bcd81fb6788409"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stack_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": "XGQAOYKR9FU3ZCRG",
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stack_parameter)
data = stock_response.json()
print(data)
yesterday = data['Time Series (Daily)']

yesterday_data = [close for (close, value) in yesterday.items()]
yesterday_closing_price = yesterday[yesterday_data[0]]['4. close']

day_before_yesterday_closing_price = yesterday[yesterday_data[1]]['4. close']


difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round(difference / float(yesterday_closing_price)) * 100
print(diff_percent)


# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").


    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if abs(diff_percent) > 0:

    news_api_key = "0646a1b60d004631affb4956682d51d3"
    news_parameter = {
        "qInTitle": COMPANY_NAME,
        # "from": yesterday[yesterday_data[0]],
        "apiKey": news_api_key,
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameter)
    articles = news_response.json()["articles"]


# - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[0:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadlines: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

# TODO 9. - Send each article as a separate message via Twilio.

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+17404957366",
            to="+917530062545"

        )
        print(message.sid)

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

