import requests
import os
import json
import time
import datetime
import logging
from itertools import islice
from statistics import mean
from flask import Flask, request
from dotenv import load_dotenv


def load_secrets():
    load_dotenv()

# Define Flask instance
app = Flask(__name__)

# Function to get the last "n" days of stock closing price data along with the average closing price over those "n" days
@app.route('/stockticker')
def getdailyadjustedstockprice():
    method_start_time = time.time()

    # Chekc if all parameters are present in the request
    if not all(k in request.args for k in (["symbol", "ndays"])):
        error_message =  f"\
                         Required paremeters : 'symbol', 'ndays' <br>\
                         Supplied paremeters : {[k for k in request.args]}\
                         "
        return error_message

    # Alpha Vantage REST API access Key
    api_key = os.getenv("ALPHA_API_KEY")
    try:
        # read the request parameters
        symbol = request.args.get('symbol')
        ndays = int(request.args.get('ndays'))
        # Logging configuration
        log_filename = os.path.join(os.getcwd(), 'logs/' + datetime.datetime.now().strftime("getstockprice_%Y_%m_%d.log"))
        logging.basicConfig(filename=log_filename, filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

        if(ndays <= 100):
            # Alpha Vantage REST API to get the last 100 (max) days stock price details
            getstockprice_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&apikey=" + api_key
        else:
            # Alpha Vantage REST API to get more than 100 daily stock price details
            getstockprice_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=" + symbol + "&outputsize=full&apikey=" + api_key

        # Request stock details
        response = requests.get(getstockprice_url)
        logging.info("Get Stock Price Request Submitted: " + getstockprice_url)
        json_response = response.json()
        #logging.info(json.dumps(json_response, indent=4, separators=(',', ': ')))
        logging.info(response.status_code)

        # Response Json object
        response_dictionary = {}
        # List object to store dateprice & price details 
        price_date_list=[]
        price_list =[]
        
        response_dictionary['stockname'] = symbol
        # Iterate the json response dictionary
        daily_stock_price_dict = json_response['Time Series (Daily)']
        # Fetch only ndays of data
        for key, value in islice(daily_stock_price_dict.items(), ndays):
            #logging.info(key + " - " + value['4. close'])
            date_price_dict = {"date": key, "price": value['4. close']}
            price_date_list.append(date_price_dict)
            price_list.append(float(value['4. close']))

        logging.info(price_date_list)
        logging.info(price_list)
        response_dictionary['dailyclosingprices'] = price_date_list
        avg_closing_price = round(mean(price_list), 2)
        response_dictionary['avgclosingprice'] = str(avg_closing_price)
        logging.info("Time to get response %s" % (time.time() - method_start_time))
        # convert Dictionary to json 
        logging.info(json.dumps(response_dictionary, indent=2))
        return json.dumps(response_dictionary)
    except Exception as e:
        logging.error("Error in getdailyadjustedstockprice method : " + str(e))
        return str(e)

if __name__ == '__main__':
   logging.info("Stock Ticker Web Service")
   load_secrets()
   #app.run(debug = True, host="0.0.0.0", port=5000)

