from flask import Flask, request
import yfinance as yf
from pandas import Series
import json

app = Flask(__name__)

opencache = {}
currentcache = {}
divratemonthlycache = {}

@app.route('/')
def hello_world():
    tsla = yf.Ticker("VTI")
    #print(tsla.info)
    print(str(tsla.info).split("dividendRate': ")[1].split(",")[0])

    print(tsla.dividends)


    return tsla.info



if __name__ == '__main__':
    app.run()


@app.route('/current_div', methods=['GET'])
def div():

    symbol = request.args['stock']
    if symbol in currentcache:
        print("used cache")
        return currentcache.get(symbol)
    else:
        stock = yf.Ticker(str(symbol))
        dividends = Series.tolist(stock.dividends)
        print(str(dividends[len(dividends) - 1]))
        currentcache[symbol] = str(dividends[len(dividends) - 1])
        return str(dividends[len(dividends) - 1])


@app.route('/div_rate', methods=['GET'])
def divRate():
    symbol = request.args['stock']

    stock = yf.Ticker(str(symbol))
    print(str(stock.info).split("dividendRate': ")[1].split(",")[0])

    return str(stock.info).split("dividendRate': ")[1].split(",")[0]

@app.route('/open', methods=['GET'])
def open():
    symbol = request.args['stock']
    if symbol in opencache:
        print("used cache")
        return opencache.get(symbol)
    else:
        stock = yf.Ticker(str(symbol))
        print(str(stock.info).split("open': ")[1].split(",")[0])
        opencache[symbol] = str(stock.info).split("open': ")[1].split(",")[0]
        return str(stock.info).split("open': ")[1].split(",")[0]


@app.route('/div_rate_monthly', methods=['GET'])
def divRateMonthly():
    symbol = request.args['stock']
    if symbol in divratemonthlycache:
        print("used cache")
        return divratemonthlycache.get(symbol)
    else:
        stock = yf.Ticker(str(symbol))
        print(str(float(str(stock.info).split("dividendRate': ")[1].split(",")[0]) / 12.0))
        divratemonthlycache[symbol] = str(float(str(stock.info).split("dividendRate': ")[1].split(",")[0]) / 12.0)
        return str(float(str(stock.info).split("dividendRate': ")[1].split(",")[0]) / 12.0)



@app.route('/current_price', methods=['GET'])
def price():
    symbol = request.args['stock']
    stock = yf.Ticker(str(symbol))
    dividends = Series.tolist(stock.dividends)


    return str(dividends[len(dividends) - 1])