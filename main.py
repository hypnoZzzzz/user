import asyncio
import os
import requests
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

# === НАСТРОЙКИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
YOUR_TELEGRAM_ID = int(os.getenv("YOUR_TELEGRAM_ID"))
USERNAME_TO_CHECK = os.getenv("USERNAME_TO_CHECK")
CHECK_INTERVAL_SECONDS = 1800  # 30 минут

username_was_free = False

async def check_username(bot: Bot):
    global username_was_free
    url = f"https://t.me/{USERNAME_TO_CHECK}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            if not username_was_free:
                await bot.send_message(YOUR_TELEGRAM_ID, f"✅ Ник @{USERNAME_TO_CHECK} свободен!")
                print(f"[+] @{USERNAME_TO_CHECK} свободен.")
                username_was_free = True
        else:
            print(f"[-] @{USERNAME_TO_CHECK} занят.")
            username_was_free = False
    except Exception as e:
        print(f"[!] Ошибка при проверке: {e}")

async def periodic_check(bot: Bot):
    while True:
        await check_username(bot)
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    asyncio.create_task(periodic_check(bot))
    print("🔄 Бот запущен. Проверка каждые 30 минут...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
