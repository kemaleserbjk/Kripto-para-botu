import ccxt
import pandas as pd
import ta
import telegram
import time
import os

# Telegram ayarları
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Environment variable olarak ekle
CHAT_ID = os.getenv("CHAT_ID")                # Environment variable olarak ekle

bot = telegram.Bot(token=TELEGRAM_TOKEN)
exchange = ccxt.binance()

# Kontrol edilecek coin listesi (örnek 5 coin, sen 150 coin ekleyebilirsin)
COINS = [
    "BTC/USDT",
    "ETH/USDT",
    "XRP/USDT",
    "SOL/USDT",
    "DOGE/USDT"
]

def check_macd(symbol):
    try:
        # 3 günlük mumları al
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe="3d", limit=100)
        df = pd.DataFrame(ohlcv, columns=['time','open','high','low','close','volume'])

        # MACD hesapla
        macd = ta.trend.MACD(df['close'])
        df['macd'] = macd.macd()
        df['signal'] = macd.macd_signal()

        last_macd = df['macd'].iloc[-1]
        last_signal = df['signal'].iloc[-1]
