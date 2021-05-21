import pandas as pd
import datetime
import requests
import time
import webbrowser
import numpy
import pyupbit

con_key = ""
sec_key = ""

tickers = pyupbit.get_tickers(fiat="KRW")

daytickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-EOS", "KRW-ETC", "KRW-DOGE", "KRW-ADA", "KRW-BCH", "KRW-MARO", "KRW-ORBS"]

myupbit = pyupbit.Upbit(con_key, sec_key)

balances = myupbit.get_balances()

def buy_crypto_currency(ticker):
    krw = myupbit.get_balance(ticker="KRW")
    unit = krw * 0.1
    if unit > 5000 and krw > 100000:
        myupbit.buy_market_order(ticker, unit)
        print(ticker, " - buy : ", unit)
    else:
        print("not enough money")


def sell_crypto_currency(ticker):
    orderbook = pyupbit.get_orderbook(ticker)
    bids_asks = orderbook[0]['orderbook_units']
    sell_price = bids_asks[0]['bid_price']

    for i in range(len(balances)):
        if ticker[4:] == balances[i]['currency']:
            avg = balances[i]['avg_buy_price']

            if (sell_price > float(avg) * 1.02):
                unit = myupbit.get_balance(ticker)
                myupbit.sell_market_order(ticker, unit)
                print(ticker, "avg-", avg, " - sell : ", unit)
            else:
                print("not enough Avg -", float(avg) * 1.02, "MY Avg -", avg)

            break


while True:
    def condition(ticker):

        data = pyupbit.get_ohlcv(ticker, interval="minute5", count=100)

        df = pd.DataFrame(data)

        df = pd.Series(df['close'].values)

        unit = 2

        band1 = unit * numpy.std(df[len(df) - 20:len(df)])

        bb_center = numpy.mean(df[len(df) - 20:len(df)])

        band_high = bb_center + band1

        band_low = bb_center - band1

        price = pyupbit.get_current_price(ticker)

        print(str(ticker))
        print('Current price: ', price)
        print('Top Bollinger Band: ', round(band_high, 2))
        print('Bottom Bollinger Band: ', round(band_low, 2))

        period = 14

        delta = df.diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss

        rsi = round(pd.Series(100 - (100 / (1 + RS)), name="RSI").iloc[-1], 1)
        print('RSI: ', rsi)

        if price > band_high and rsi > 70: #불린저 상단 터치 + rsi 70이상 매도
            sell_crypto_currency(ticker)

        if price < band_low and rsi < 30: #불린저 하단 터치 + rsi 30이하 매수
            buy_crypto_currency(ticker)

        coin = myupbit.get_balance('KRW')
        print("My KRW-", coin)

        print('')
        time.sleep(2)

    try:
        for ticker in daytickers:
            condition(ticker)

    except:
        time.sleep(2)
        print("error")
        print('')
