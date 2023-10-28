import requests
import os
from twilio.rest import Client




MY_TWILIO_NUMBER = "+12524944349"
account_sid = os.environ.get("MY_TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("MY_TWILIO_AUTH_TOKEN")
MY_NORMAL_NUMBER = "+250783733959"




STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


MY_STOCK_API_KEY = "B7FT1DZP79CED5BI"


MY_NEWS_API_KEY = "da9486295c984534afd2968187394ba8"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]


response = requests.get(
   f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK_NAME}&interval=min&apikey={MY_STOCK_API_KEY}")


data = response.json()["Time Series (Daily)"] #we have to used it as a json data. to get hold of a particular data we work with json data as a dictionary


#print(data) ####


data_list = [value for (key, value) in data.items()] #this is allowing us to convert our json data into a dictionary as it is very asy for us to perform our task with a list instead of a dictionary. # We are only getting hold of the value not the key too


#print(data_list) #####


yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
#print(yesterday_closing_price)


# TODO 2. - Get the day before yesterday's closing stock price


before_yesterday_data = data_list[1]
before_yesterday_closing_price = float(before_yesterday_data["4. close"])
#print(before_yesterday_closing_price)


# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = (yesterday_closing_price - before_yesterday_closing_price)
#print(difference)


up_down_emoji = None
if difference > 0:
   up_down_emoji = "🔺"


else:
   up_down_emoji = "🔻"






# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((difference / before_yesterday_closing_price) * 100)
#print(percentage_difference)


# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_difference) > 1:
   ## STEP 2: https://newsapi.org/
   # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


   # TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
   news_response = requests.get(f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey={MY_NEWS_API_KEY}")
   news_data = news_response.json()
   articles = news_data["articles"]
   #print(articles)


   # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
   three_articles = articles[:3]


   #print(three_articles)




## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.


# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.


"""This code can be represented by the one below it


formatted_articles = [f"{STOCK_NAME}: {up_down_emoji}{percentage_difference}%\nHeadlines: {article['title']}. \nBrief: {article['description']}" for article in three_articles]


print(formatted_articles)


"""


formatted_articles = [] #each item in this new list will be a single article formatted to have a headline and brief. #This is helping us send users a well formatted message.
for article in three_articles:
   headline = f"{STOCK_NAME}: {up_down_emoji}{percentage_difference}%\nHeadlines: {article['title']}." #these are helping us format our message to send
   brief = f"Brief: {article['description']}"
   formatted_article = f"{headline}\n{brief}"
   formatted_articles.append(formatted_article)




print(formatted_articles)




# TODO 9. - Send each article as a separate message via Twilio.


client = Client(account_sid, auth_token)


for article in formatted_articles:
   message = client.messages.create(
       body=article,
       from_=MY_TWILIO_NUMBER,
       to=MY_NORMAL_NUMBER
   )






# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of theJJ coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
