import pandas as pd
import datetime
import requests
import time
import webbrowser
import numpy
import pybithumb

con_key = ""
sec_key = ""


tickers = pybithumb.get_tickers()
daytickers = ["BTC", "ETH", "XRP", "EOS", "KLAY", "DOGE"]

bithumb = pybithumb.Bithumb(con_key, sec_key)


def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = (krw * 0.1) / float(sell_price)
    if krw > 100000:
        bithumb.buy_market_order(ticker, unit)
        print(ticker, " - 매수 : ", unit)
    else:
        print("잔고없음")

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)
    print(ticker, " - 매도 : ", unit)


while True:
    try:
        def condition(ticker):
    
            data = pybithumb.get_ohlcv(ticker, interval="minute5")
    
            df = pd.DataFrame(data)
    
            df = pd.Series(df['close'].values)
    
            unit = 2
    
            band1 = unit * numpy.std(df[len(df) - 20:len(df)])
    
            bb_center = numpy.mean(df[len(df) - 20:len(df)])
    
            band_high = bb_center + band1
    
            band_low = bb_center - band1
    
            price = pybithumb.get_current_price(ticker)
    
            print(str(ticker))
            print('현재가: ', price)
            print('볼린저밴드 상단: ', round(band_high, 2))
            print('볼린저밴드 하단: ', round(band_low, 2))

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

            now = datetime.datetime.now()

            if price > band_high or rsi > 65:
                text = '볼린저 상단 터치 + rsi 65 이상: ' + str(ticker) + ' - 매도'
                sell_crypto_currency(ticker)
                print(text)
                print(now)
    
            if price < band_low or rsi < 35:
                text = '볼린저 하단 터치 + rsi 35 이하: ' + str(ticker) + ' - 잔고 10분의1 매수'
                buy_crypto_currency(ticker)
                print(text)
                print(now)


            coin = bithumb.get_balance(ticker)[2] #잔액표시
            print(coin)

            print('')
            time.sleep(2)
    except:
        print("에러발생")

    for ticker in daytickers:
        condition(ticker)