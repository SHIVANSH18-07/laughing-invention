import requests
import time
import datetime
import telegram
import asyncio
import tracemalloc

# Start memory tracking (optional)
tracemalloc.start()

# --- CONFIG ---
BOT_TOKEN = '7415190733:AAEAqwpk0dq-SqLJcUjUtAtgI-uWp4GhQK8'
CHAT_ID = '-1002641009476'
INTERVAL = 900  # 15 minutes

# Initialize bot
bot = telegram.Bot(token=BOT_TOKEN)

# Simulated function to get Nifty/BankNifty data (replace with real API later)
def get_price_data():
    return {
        'NIFTY': {
            'high': 22680,
            'low': 22400,
            'close': 22550,
            'rsi': 65,
            'ema_9': 22540,
            'ema_21': 22530,
            'volume_surge': True
        },
        'BANKNIFTY': {
            'high': 48900,
            'low': 48100,
            'close': 48500,
            'rsi': 58,
            'ema_9': 48480,
            'ema_21': 48450,
            'volume_surge': False
        }
    }

# Fibonacci Calculation
def calculate_fibonacci(high, low):
    diff = high - low
    return {
        '0.236': high - 0.236 * diff,
        '0.382': high - 0.382 * diff,
        '0.5': high - 0.5 * diff,
        '0.618': high - 0.618 * diff,
        '0.786': high - 0.786 * diff
    }

# Main scan function - needs to be async
async def scan_and_send():
    data = get_price_data()
    message = f"\n📢 [OPTIONS ALERT] {datetime.datetime.now().strftime('%H:%M:%S')}\n"

    for index, values in data.items():
        fib = calculate_fibonacci(values['high'], values['low'])
        if values['rsi'] > 55 and values['ema_9'] > values['ema_21'] and values['volume_surge']:
            strike = round(values['close'] / 50) * 50
            sl = strike - 50
            target = strike + 100
            message += f"\n{index} looks *BULLISH* 🚀:\n- BUY {strike} CE\n- SL: {sl}\n- TARGET: {target}\n- Reason: RSI > 55, EMA Bullish, Volume Surge\n"
        elif values['rsi'] < 45 and values['ema_9'] < values['ema_21'] and values['volume_surge']:
            strike = round(values['close'] / 50) * 50
            sl = strike + 50
            target = strike - 100
            message += f"\n{index} looks *BEARISH* 📉:\n- BUY {strike} PE\n- SL: {sl}\n- TARGET: {target}\n- Reason: RSI < 45, EMA Bearish, Volume Surge\n"

    if "BUY" in message:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.MARKDOWN)

# Main loop
async def main_loop():
    while True:
        await scan_and_send()
        await asyncio.sleep(INTERVAL)

# Start bot
asyncio.run(main_loop())
