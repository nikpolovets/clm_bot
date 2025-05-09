import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = "7356871198:AAFwO8_eQMJzQPVDsMW3-9Dy5mdszTCmDXw"
OPENWEATHER_KEY = "b77d35b6e0fd1878bcd548c3d5f60d3b"

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code != 200:
        return "Не удалось получить данные. Убедись, что город написан правильно."
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"Сейчас в {city.title()}: {description}, {temp}°C"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    weather = get_weather(city)
    await update.message.reply_text(weather)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши мне название города, и я скажу тебе погоду.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
