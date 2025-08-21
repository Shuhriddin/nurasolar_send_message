from loader import dp,bot
from aiogram import types,F
from aiogram.filters import CommandStart
from aiogram import html
from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardButton
from utils.misc.subscription import check
from data.config import CHANNELS
from aiogram.filters.callback_data import CallbackData
import os
class CheckSubs(CallbackData,prefix='ikb3'):
    check:bool
@dp.message(CommandStart())
async def start_chat(message:types.Message):
    result = str()
    btn = InlineKeyboardBuilder()
    final_status = True
    for channel in CHANNELS:
        status = True
        try:
            status = await check(user_id=message.from_user.id,
                                 channel=channel['channel_id'])
        except:
            pass
        final_status *= status
        try:
            channel = await bot.get_chat(channel['channel_id'])
        except Exception as e:
            print(e)
            pass
        if not status:
            invite_link = await channel.export_invite_link()
            btn.row(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    btn.button(text="Obunani tekshirish", callback_data=CheckSubs(check=True))
    btn.adjust(1)
    if final_status:
        await message.answer(text="Bot sizning xizmatingizda!")
    if not final_status:
        await message.answer(text=
                                  f"Iltimos bot to'liq ishlashi uchun quyidagi kanallarga obuna bo'ling!",
                             reply_markup=btn.as_markup(row_width=1))
@dp.callback_query(CheckSubs.filter())
async def test(call:types.CallbackQuery):
    await call.answer(cache_time=60)
    k = []
    final_status = False
    user_id = call.from_user.id
    kanallar = CHANNELS
    for kanal in kanallar:
        try:
            channel = await bot.get_chat(kanal['channel_id'])
        except:
            pass
        try:
            res = await bot.get_chat_member(chat_id=kanal['channel_id'], user_id=user_id)
        except:
            continue
        if res.status == 'member' or res.status == 'administrator' or res.status == 'creator':
            k.append(InlineKeyboardButton(text=f"✅ {channel.title}", url=f"{await channel.export_invite_link()}"))

        else:
            k.append(InlineKeyboardButton(text=f"❌ {channel.title}", url=f"{await channel.export_invite_link()}"))
            final_status = True
    builder = InlineKeyboardBuilder()
    builder.add(*k)
    text = "Obunani tekshirish"
    builder.button(text=text, callback_data=CheckSubs(check=True))
    builder.adjust(1)
    if final_status:
        await bot.send_message(chat_id=user_id,
                               text="Iltimos bot to'liq ishlashi uchun quyidagi kanallarga obuna bo'ling!",
                               reply_markup=builder.as_markup())
    else:
        await call.message.answer(text="Botning sizning xizmatingizda!")
    await call.message.delete()
