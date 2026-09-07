import time
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
import config
from strategy import add_indicators, should_buy, should_sell

client = Client(config.API_KEY, config.API_SECRET)

def get_data():
    klines = client.get_klines(symbol=config.SYMBOL, interval=config.INTERVAL, limit=200)
    df = pd.DataFrame(klines, columns=['time','open','high','low','close','vol','close_time','qav','trades','taker_base','taker_quote','ignore'])
    df['close'] = pd.to_numeric(df['close'])
    df = add_indicators(df, config)
    return df

def buy():
    try:
        order = client.order_market_buy(symbol=config.SYMBOL, quantity=config.QUANTITY)
        price = float(order['fills'][0]['price'])
        print(f"[BUY] {config.QUANTITY} {config.SYMBOL} @ {price}")
        return price
    except BinanceAPIException as e:
        print(f"Buy failed: {e}")
        return None

def sell():
    try:
        order = client.order_market_sell(symbol=config.SYMBOL, quantity=config.QUANTITY)
        price = float(order['fills'][0]['price'])
        print(f"[SELL] {config.QUANTITY} {config.SYMBOL} @ {price}")
        return True
    except BinanceAPIException as e:
        print(f"Sell failed: {e}")
        return False

if __name__ == "__main__":
    print(f"Bot started for {config.SYMBOL} | Qty: {config.QUANTITY}")
    in_position = False
    entry_price = 0

    while True:
        try:
            df = get_data()
            last = df.iloc[-1]
            print(f"Price: {last['close']:.2f} | EMA {config.EMA_FAST}/{config.EMA_SLOW}: {last['ema_fast']:.2f}/{last['ema_slow']:.2f} | RSI: {last['rsi']:.2f} | Pos: {in_position}")

            if in_position and last['close'] < entry_price * (1 - config.STOP_LOSS_PERCENT/100):
                print("STOP LOSS HIT!")
                if sell(): in_position = False

            elif not in_position and should_buy(df, config):
                p = buy()
                if p:
                    in_position = True
                    entry_price = p

            elif in_position and should_sell(df, config):
                if sell(): in_position = False

            time.sleep(config.LOOP_SECONDS)

        except Exception as e:
            print(f"Loop error: {e}")
            time.sleep(10)
