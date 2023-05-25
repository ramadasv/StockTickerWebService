# Stock Ticker Web Service on Docker Container
## Overview

This REST API service will get the last "n" days of a stocks closing price data along with the average closing price over those "n" days. The API internally uses the API service from [Alpha Adavantage](https://www.alphavantage.co/documentation/#dailyadj) to get the stock details. [Alpha Adavantage API Used in this Web Service](https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo)

## REST End points 
 * /stockticker > To get the stock closing price details for a stock
### API Parameters

> Required: ***symbol***  (The name of the equity of your choice. For example: symbol=IBM)

> Required: ***ndays***  (The last "n" number of days for which the data is needed)

Sample Request for Tesla stock
```
http://127.0.0.1:5000/stockticker?symbol=TSLA&ndays=2
```
Sample repsonse
```python
{
  "stockname": "TSLA",
  "dailyclosingprices": [
    {
      "date": "2023-05-19",
      "price": "180.14"
    },
    {
      "date": "2023-05-18",
      "price": "176.89"
    }
  ],
  "avgclosingprice": "176.96"
}
```

## Pre-requisites 
Install below softwares in your laptop. The below command are tested on Mac
```
Python
Docker Desktop 
Flask
```

## How to run the web service
### To run the service locally on your laptop (default port : 5000)
* Create a python virutal environment and activate it. `python3 -m venv <..path/StockTickerK8s/>`
* Install the python pacakges listed in requirements.txt using `pip install requirements.txt`
* Create a `.env` file with value `ALPHA_API_KEY=<Your Alpha Adavantage API key>` in the folder same as the python file "StockTickerRestAPI.py"
* Start the web service `flask --app StockTickerRestAPI run --host=0.0.0.0`
* To access the webservice use the link : 
http://127.0.0.1:5000/stockticker?symbol=TSLA&ndays=40

### To run the service in a Docker container.  [DockerHub Repo](https://hub.docker.com/r/ramadasdocker/stockticker)
* Install Docker Dekstop
* Pull the docker image and run it in the docker container
```
docker pull ramadasdocker/stockticker:1.0
docker run -d -p 5000:5000 ramadasdocker/stockticker:1.0
```

Folder Structure

```
 StockTicker
    ├── Dockerfile
    ├── README.md  
    ├── StockTickerRestAPI.py
    ├── logs
    └── requirements.txt
```

