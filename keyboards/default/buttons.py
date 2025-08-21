from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton


def main_button_for_users():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text='📊 Qarzdorlikni ko`rish!!!'),
        KeyboardButton(text='❌ Bekor qilish')
    )
    button.adjust(1)
    return button.as_markup(resize_keyboard=True, one_time_keyboard=True)


# CONTACT
def phone_number():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True)
    )
    button.adjust(1)
    return button.as_markup(resize_keyboard=True)