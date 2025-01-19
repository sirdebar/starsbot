from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Купить для себя")],
        [KeyboardButton(text="Купить в подарок")],
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Реферальная система")],
    ],
    resize_keyboard=True
)

# Меню покупки
def buy_menu(amount, price):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить", callback_data=f"pay:{amount}:{price}")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_amount")],
    ])

# Меню выбора способа оплаты
payment_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="CryptoBot", callback_data="pay_crypto")],
    [InlineKeyboardButton(text="Другие методы (в разработке)", callback_data="pay_other_disabled")],
    [InlineKeyboardButton(text="Назад", callback_data="back_to_menu")],
])

# Кнопка закрытия заказа для администратора
admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Закрыть", callback_data="close_order")]
])
