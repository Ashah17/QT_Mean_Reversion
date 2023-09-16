import datetime
from math import ceil

import requests
import bs4
import pymysql as pymy

def scrape_snp500():
    
    now = datetime.datetime.utcnow()
    #saves current time

    response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    #scrapes the list of snp500 companies from wikipedia

    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    #saves the scraped text in soup text

    symbolslist = soup.select('table')[0].select('tr')[1:]
    #selects first soup table with [0]
    #selects all rows except header row with [1:]

    symbols = []
    #loops through the table
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td') #td for table cell
        symbols.append(
            (
                tds[0].select('a')[0].text,
                'stock',
                tds[1].select('a')[0].text,
                tds[3].text,
                'USD', now, now    
            )
        )

    return symbols
        #symbols has the values from the table's cells appended

print(scrape_snp500)


def insert_in_database(symbols):
    #add symbols to sql database

    #host, username, password, db name

    db_host = "localhost"
    db_user = "root"
    db_pass = "hopkinton"
    db_name = "securities_master"

    #create connection

    con = pymy.connect(
        host = db_host, 
        user = db_user, 
        password = db_pass, 
        db = db_name,
    )


    #insert strings for db

    column_str = """ticker, instrument, name, sector,
                 currency, created_date, last_updated_date 
                  """
    
    insert_str = ("%s, " * 7)[:-2]

    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % \
        (column_str, insert_str)

    #creator cursor object to write into db

    with con: #good practice to use with 
        cur = con.cursor()
        cur.executemany(final_str, symbols)
        con.commit() #ALWAYS REMEMBER TO COMMIT CHANGES!!!!

    #execute an insert into for each symbol with the connection
    #uses the connection cursor

#only run if run by python interpreter: not every time
#because of the name == main statement

if __name__ == "__main__":
    symbols = scrape_snp500() #scrape function
    insert_in_database(symbols) #insert function
    print("%s symbols were successfully added" % len(symbols)) 
    # % in python instead of comma to print var


#success, all symbols are in!

        

    



    




    
    

