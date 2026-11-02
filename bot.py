import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

TOKEN = "9139344929:AAGgzO5qYI4JTsTCx1Fhy8KOFSj3jqjntBM"
ADMIN_ID = 8849823837  # Твой ID

router = Router()

# Сюда будем сохранять ID покупателя, которому надо скинуть фотки
last_buyer_id = None


@router.message(CommandStart())
async def cmd_start(message: Message):
  global last_buyer_id
  # Если /start пишет покупатель (не ты), бот запоминает его ID
  if message.from_user.id != ADMIN_ID:
    last_buyer_id = message.from_user.id
    await message.answer("Ожидайте, скоро владелец пришлет материалы.")
    # Уведомляем тебя, что клиент зашел
    await message.bot.send_message(
        ADMIN_ID,
        f"🔔 Новый покупатель зашел в бота: {message.from_user.full_name} (ID: `{message.from_user.id}`)",
    )
  else:
    await message.answer(
        "Бот готов. Перешли сюда фотки, и я отправлю их последнему"
        " покупателю."
    )


# Всё, что ты (админ) отправляешь боту, он пересылает последнему клиенту
@router.message(F.from_user.id == ADMIN_ID)
async def admin_forward(message: Message, bot: Bot):
  global last_buyer_id
  if not last_buyer_id:
    await message.answer(
        "⚠️ Пока нет покупателей, которым можно переслать."
    )
    return

  try:
    # Пересылаем твое сообщение (фотку, текст, файл) покупателю
    await message.send_copy(chat_id=last_buyer_id)
    await message.answer("✅ Успешно отправлено покупателю!")
  except Exception as e:
    await message.answer(f"❌ Ошибка отправки: {e}")


async def main():
  bot = Bot(token=TOKEN)
  dp = Dispatcher()
  dp.include_router(router)

  print("Бот запущен...")
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  import asyncio

  asyncio.run(main())
    
