import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

# Твой токен бота
TOKEN = "9139344929:AAGgzO5qYI4JTsTCx1Fhy8KOFSj3jqjntBM"

router = Router()


# 1. Приветствие по команде /start
@router.message(CommandStart())
async def cmd_start(message: Message):
  text = "🔥 **Слив владельца Douyin Streams**\n\nНажмите кнопку ниже, чтобы получить доступ к материалам."

  keyboard = InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="⭐ Заплатить 1 звезду", callback_data="buy_content"
              )
          ]
      ]
  )

  await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")


# 2. Создание счета на 1 звезду (XTR)
@router.callback_query(F.data == "buy_content")
async def process_buy_command(callback: CallbackQuery, bot: Bot):
  # amount=1 означает ровно 1 Telegram Star (⭐)
  prices = [LabeledPrice(label="Доступ к материалам", amount=1)]

  await bot.send_invoice(
      chat_id=callback.message.chat.id,
      title="Слив владельца Douyin Streams",
      description="Доступ к эксклюзивным фотографиям (2 файла)",
      payload="douyin_secret_payload",
      currency="XTR",  # Валюта Telegram Stars
      prices=prices,
  )
  await callback.answer()


# 3. Обязательный шаг проверки перед покупкой
@router.pre_checkout_query()
async def process_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery, bot: Bot
):
  await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# 4. Успешная оплата -> Отправка двух твоих фоток альбомом
@router.message(F.successful_payment)
async def successful_payment(message: Message):
  await message.answer(
      "✅ Оплата прошла успешно! Держите обещанные материалы:"
  )

  # Твои два file_id
  media_group = [
      InputMediaPhoto(
          media=(
              "AgACAgIAAxkBAAEDIWlq6AxUxIBA6aj7gacwUAmIOe9NgQACuh1rG0upQEsrRwksXr4cugEAAwIAA3kAAz0E"
          ),
          caption="🔥 Слив владельца Douyin Streams",
      ),
      InputMediaPhoto(
          media=(
              "AgACAgIAAxkBAAEDIWxq6Ax_BRS7LAtIedmdf5y2xgzUngACuR1rG0upQEv-02Rb2GkdBAEAAwIAA3kAAz0E"
          )
      ),
  ]

  await message.answer_media_group(media=media_group)


async def main():
  bot = Bot(token=TOKEN)
  dp = Dispatcher()
  dp.include_router(router)

  print("Бот запущен...")
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())
