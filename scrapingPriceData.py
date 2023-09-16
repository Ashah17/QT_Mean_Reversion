import datetime
import warnings
import pymysql as pymy
import requests
import json
from urllib.request import urlopen

#connect to database to get symbols list

#Alpha Vantage (Yahoo alt) API Key: 0RS77R3YPPSXBLAU

db_host = "localhost"
db_user = "root"
db_pass = "hopkinton"
db_name = "securities_master"

con = pymy.connect(
    host = db_host,
    user = db_user,
    password = db_pass,
    db = db_name
)

def list_of_tickers():
    #gets list of ticker symbols from db

    cur = con.cursor()
    cur.execute(
        "SELECT ticker, id FROM symbol"
    )
    data = cur.fetchall()

    return [(d[0]) for d in data] #don't need id so got rid of it

def daily_historic_data(ticker, start_date = (2000,1,1), end_date = datetime.date.today().timetuple()[0:3]):
    #gets data from yahoo finance


    alpha_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
    alpha_url += ticker
    alpha_url += "&outputsize=full&apikey=0RS77R3YPPSXBLAU"

    
    #url lib to read the json data url, then create json object

    link = urlopen(alpha_url)
    data = json.loads(link.read())

    try:

        prices = []

        for key in data["Time Series (Daily)"]:
            #each key is it's own day
            date = key
            open = data["Time Series (Daily)"][key]["1. open"]
            high = data["Time Series (Daily)"][key]["2. high"]
            low = data["Time Series (Daily)"][key]["3. low"]
            close = data["Time Series (Daily)"][key]["4. close"]
            volume = data["Time Series (Daily)"][key]["5. volume"]

            prices.append(
                (datetime.datetime.strptime(date, '%Y-%m-%d'),
            open, high, low, close, 0, volume)
            #adds data to prices, with 0 as the adjusted close as that isn't available
        )
            
    except Exception as e:
        print("Couldn't download %s data" % e)

    return prices

def insert_daily_data(data_vendor_id, symbol_id, daily_data):
    #takes the tuples adds to database
    
    now = datetime.datetime.utcnow()

    #add vendor id symbol id to data

    daily_data = [
        (data_vendor_id, symbol_id, d[0],
            now, now, d[1], d[2], d[3], d[4],
            d[5], d[6]) for d in daily_data
    ]

    #created new daily_data which has the old daily_data
    #fields and the vendor id symbol id as well

    #good to keep insert strings organized
    #just like before
    column_str = """
        data_vendor_id, symbol_id, price_date,
        created_date, last_updated_date,
        open_price, high_price, low_price, close_price,
        adj_close_price, volume
    """

    insert_str = ("%s, " * 11)[:-2]
    #the *11 is for the 11 columns to populate

    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" %\
        (column_str, insert_str)
    
    cur = con.cursor()
    cur.executemany(final_str, daily_data)
    con.commit()

if __name__ == "__main__":
    tickers = list_of_tickers()
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print(
            "Adding data for %s: %s out of %s" %
            (t, i+1, lentickers)
        ) #to show progress of data add
        data = daily_historic_data(t)
        insert_daily_data('1', t, data)

print("Successfully added alpha vantage data")

#worked around yahoo being unavailable, downloaded alpha vantage data (sample, not all tickers for free)

