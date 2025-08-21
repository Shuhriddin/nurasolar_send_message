from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loader import dp, bot
from keyboards.default.buttons import main_button_for_users, phone_number
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
import xmlrpc.client
from data.config import url, db, password

username = "admin"

# ==================== STATE =====================
class UserState(StatesGroup):
    phone = State()

# ==================== START =====================
@dp.message(F.text == '/start')
async def show_invoice_menu(message: types.Message, state: FSMContext):
    await state.clear()
    user = message.from_user.full_name
    await message.answer(f'👋 Assalomu alaykum {user}!\n\n📄 To`lovlaringiz va qarzdorligingiz haqida ma`lumot olish uchun:\n\n📲 Telefon raqamingizni yuboring!', reply_markup=phone_number())


@dp.message(F.contact)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    fullname = message.from_user.full_name

    # Raqamni tozalash
    clean_number = phone.replace(" ", "").replace("+", "").replace("-", "").replace("(", "").replace(")", "")

    # Telefonni state da saqlaymiz
    await state.update_data(phone=clean_number)

    # Odoo'ga ulanish
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    if not uid:
        await message.answer("❌ Login xato! Username yoki parol noto‘g‘ri.")
        return

    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    partners = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[
            '|',
            ['phone', 'ilike', clean_number],
            ['mobile', 'ilike', clean_number]
        ]],
        {'fields': ['id', 'name', 'phone', 'mobile'], 'limit': 1}
    )

    if partners:
        partner = partners[0]
        msg = f"✍️ {fullname}, siz ro‘yxatdan o‘tgansiz!\n" \
              f"Odoo’da kontakt: {partner['name']}\n" \
              f"Telefon: {partner['phone'] or partner['mobile']}"
        await message.answer(msg, reply_markup=main_button_for_users())
    else:
        await message.answer("❌ Telefon raqam topilmadi, iltimos administrator bilan bog‘laning.")

    # Avvalgi xabarni o‘chirish
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    except:
        pass

# ==================== CANCEL =====================
@dp.message(F.text == "❌ Bekor qilish")
async def go_to_main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    msg = "BOT KOMMANDALARI:\n👉🏻 Botni qayta ishga tushirish /start\n✍️ Sizga qanday yordam kerak? /help"
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())

# ==================== BARCHA MA'LUMOT (qarzdorlik bilan) =====================
@dp.message(F.text == '📊 Qarzdorlikni ko`rish!!!')
async def show_all_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    phone = data.get("phone")
    user = message.from_user.full_name

    if not phone:
        await message.answer("❌ Avval telefon raqamingizni yuboring", reply_markup=phone_number())
        return

    # Odoo ulanish
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})
    if not uid:
        await message.answer("❌ Login xato! Username yoki parol noto‘g‘ri.")
        return

    models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

    # Partner qidiramiz (phone yoki mobile bo‘yicha)
    partners = models.execute_kw(
        db, uid, password,
        'res.partner', 'search_read',
        [[
            '|',
            ['phone', 'ilike', phone],
            ['mobile', 'ilike', phone]
        ]],
        {'fields': ['id', 'name', 'phone', 'mobile'], 'limit': 1}
    )

    if not partners:
        await message.answer("❌ Bunday foydalanuvchi topilmadi!")
        return

    partner = partners[0]
    partner_id = partner['id']

    # Qarzdorliklarni olish
    invoices = models.execute_kw(
        db, uid, password,
        'account.move', 'search_read',
        [[
            ['partner_id', '=', partner_id],
            ['move_type', 'in', ['out_invoice', 'out_refund']],
            ['state', '=', 'posted']
        ]],
        {'fields': ['name', 'amount_total']}
    )

    # Umumiy qarzdorlikni hisoblash
    amount_total = sum(inv['amount_total'] for inv in invoices)

    if amount_total > 0:
        await message.answer(
            f"✅ {user}\n\n"
            f"💰 Sizning qarzdorligingiz: <b>{amount_total:,.2f} $</b>",
            parse_mode="HTML", reply_markup=main_button_for_users()
        )
    else:
        await message.answer(
            f"✅ {partner['name']}\n\n"
            f"✅ Sizning qarzdorligingiz yo‘q.", reply_markup=main_button_for_users()
        )