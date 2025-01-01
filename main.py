!pip install python-telegram-bot --upgrade
!pip install nest_asyncio
!pip install openai

# Импорт необходимых библиотек
import logging
import nest_asyncio
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, Application

# Разрешаем вложенные циклы событий
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего Telegram-бота
TOKEN = '7599840768:AAG1qGPHwdNkl3DFfvg2Wv4YM3UESIQ2JVU'

# Ваш API-ключ OpenAI
API_KEY = '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'

# Установка API-ключа OpenAI
openai.api_key = API_KEY

# Обработчик сообщений из группы
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id

    # Используем сообщение пользователя напрямую
    prompt = update.message.text
    logger.info(f"Получено сообщение от пользователя: {prompt}")

    try:
        # Отправка запроса к OpenAI API
        response = await openai.ChatCompletion.acreate(
            model="o-1 mini",  # Указание модели o-1 mini
            messages=[
                {"role": "system", "content": "Ты помощник для обработки заказов на сувенирную продукцию."},
                {"role": "user", "content": prompt}
            ]
        )

        # Извлечение ответа от OpenAI
        chatgpt_response = response.choices[0].message.content

        # Отправляем ответ пользователю
        await context.bot.send_message(chat_id=chat_id, text=chatgpt_response)

    except Exception as e:
        logger.error(f"Ошибка при обращении к OpenAI API: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Извините, произошла ошибка при обработке вашего запроса.")

# Основной запуск бота
async def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.ChatType.GROUP | filters.ChatType.SUPERGROUP, handle_group_message))

    # Run the bot until the user presses Ctrl-C
    logger.info("Запуск бота...")
    await application.initialize()
    await application.start()
    await application.stop()

# Убедитесь, что все зависимости установлены
try:
    import telegram
except ModuleNotFoundError:
    !pip install python-telegram-bot --upgrade

# Запуск бота в Google Colab
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
