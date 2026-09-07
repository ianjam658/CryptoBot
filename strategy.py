import pandas_ta as ta

def add_indicators(df, config):
    df['ema_fast'] = ta.ema(df['close'], length=config.EMA_FAST)
    df['ema_slow'] = ta.ema(df['close'], length=config.EMA_SLOW)
    df['rsi'] = ta.rsi(df['close'], length=config.RSI_PERIOD)
    return df

def should_buy(df, config):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    # Fast EMA crosses above Slow + RSI not overbought
    return prev['ema_fast'] < prev['ema_slow'] and last['ema_fast'] > last['ema_slow'] and last['rsi'] < config.RSI_OVERBOUGHT

def should_sell(df, config):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    # Fast EMA crosses below Slow
    return prev['ema_fast'] > prev['ema_slow'] and last['ema_fast'] < last['ema_slow'] and last['rsi'] > config.RSI_OVERSOLD
