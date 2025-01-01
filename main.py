import os
import logging
import nest_asyncio
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Разрешаем вложенные циклы событий
nest_asyncio.apply()

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Считываем токены из переменных среды
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY = os.getenv('OPENAI_API_KEY')

# Установка API-ключа OpenAI
openai.api_key = API_KEY

# Обработчик сообщений из группы
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat.id
    prompt = update.message.text
    logger.info(f"Получено сообщение от пользователя: {prompt}")

    try:
        response = await openai.ChatCompletion.acreate(
            model="o-1 mini",
            messages=[
                {"role": "system", "content": "Ты помощник для обработки заказов на сувенирную продукцию."},
                {"role": "user", "content": prompt}
            ]
        )
        chatgpt_response = response.choices[0].message.content
        await context.bot.send_message(chat_id=chat_id, text=chatgpt_response)
    except Exception as e:
        logger.error(f"Ошибка при обращении к OpenAI API: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Извините, произошла ошибка при обработке вашего запроса.")

# Основной запуск бота
async def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    group_handler = MessageHandler(filters.ChatType.GROUP | filters.ChatType.SUPERGROUP, handle_group_message)
    application.add_handler(group_handler)
    logger.info("Запуск бота...")
    await application.initialize()
    await application.start()
    await application.stop()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
