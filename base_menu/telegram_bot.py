import telegram
from django.conf import settings

def send_telegram_notification(message):
    """Отправляет сообщение в Telegram-чат."""
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    try:
        bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")