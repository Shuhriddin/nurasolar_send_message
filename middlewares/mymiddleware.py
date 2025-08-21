from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from data.config import CHANNELS
from loader import bot
from utils.misc.subscription import check
from aiogram.filters.callback_data import CallbackData


class CheckSubs(CallbackData, prefix="ikb3"):
    check: bool


class UserCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        # event turi tekshiriladi
        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return await handler(event, data)  # boshqa eventlarni o'tkazib yuboramiz

        final_status = True
        builder = InlineKeyboardBuilder()

        for CHANNEL in CHANNELS:
            status = await check(user_id=user_id, channel=CHANNEL)
            final_status = final_status and status  # True/False yig'ib borish
            print(f"{CHANNEL}: {status}")

            channel = await bot.get_chat(CHANNEL)
            try:
                btn_text = f"{'✅' if status else '❌'} {channel.title}"
                invite_link = await channel.export_invite_link()
                builder.button(text=btn_text, url=invite_link)
            except Exception as e:
                print(f"Channel error: {e}")
                pass

        builder.button(text="Obunani tekshirish", callback_data=CheckSubs(check=True))
        builder.adjust(1)

        if not final_status:
            await bot.send_message(
                chat_id=user_id,
                text="Iltimos, bot to‘liq ishlashi uchun quyidagi kanallarga obuna bo‘ling!",
                reply_markup=builder.as_markup()
            )
        else:
            return await handler(event, data)
