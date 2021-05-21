import time
import pybithumb
import datetime

con_key = ""
sec_key = ""

tickers = pybithumb.get_tickers()
daytickers = ["BTC", "ETH", "XRP", "EOS", "KLAY", "DOGE"]


bithumb = pybithumb.Bithumb(con_key, sec_key)


def get_yesterday_ma5(ticker): # 5거래일 상승장 체크
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]

def get_target_price(ticker): # 변동성 돌파 체크
    df = pybithumb.get_ohlcv(ticker) #일봉데이타
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target


def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = (krw * 0.1) / float(sell_price)
    if krw > 100000:
        bithumb.buy_market_order(ticker, unit)
        print(ticker, " - buy : ", unit)
    else:
        print("not enough money")

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)
    print(ticker, " - sell : ", unit)



while True:
    def condition(ticker):
        now = datetime.datetime.now()
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        ma5 = get_yesterday_ma5(ticker)
        target_price = get_target_price(ticker)
        current_price = pybithumb.get_current_price(ticker)

        if mid < now < mid + datetime.timedelta(seconds=10):
            sell_crypto_currency(ticker)

        if(current_price > target_price) and (current_price > ma5):
            print(ticker, "nowPrice - ",current_price , " change - ", target_price, "5up - ", ma5)
            buy_crypto_currency(ticker)
        else:
            print("Not strategy")

        print('')
        time.sleep(2)

    try:
        for ticker in tickers:
            condition(ticker)

    except:
        time.sleep(2)
        print("error")
        print('')
