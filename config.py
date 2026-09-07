import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
SYMBOL = os.getenv("SYMBOL", "BTCUSDT")
QUANTITY = float(os.getenv("QUANTITY", "0.0005"))

# Strategy Params
INTERVAL = "5m"
EMA_FAST = 20
EMA_SLOW = 50
RSI_PERIOD = 14
RSI_OVERBOUGHT = 65
RSI_OVERSOLD = 35
STOP_LOSS_PERCENT = 2.0
LOOP_SECONDS = 60

if not API_KEY or not API_SECRET:
    raise ValueError("API keys not found! Create a.env file from.env.example")
