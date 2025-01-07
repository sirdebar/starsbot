from aiogram import Router, Dispatcher
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from config import SUPPORT_CONTACT, ADMIN_CHAT_ID
from utils import calculate_price
from keyboards import main_menu, buy_menu, payment_menu, admin_menu

STAR_COST = 1.90
MIN_STARS = 50

router = Router()
user_data = {}

# Команда /start
@router.message(Command(commands=["start"]))
async def start_handler(message: Message):
    """
    Обрабатывает команду /start.
    """
    await message.answer_photo(
        photo=FSInputFile("images/menu.jpg"),
        caption=(
            f"👋 Привет, {message.from_user.username}!\n\n"
            "Добро пожаловать в <b>Telegram Stars Bot</b>! ⭐\n\n"
            "Здесь вы можете приобрести звезды для себя или в подарок.\n\n"
            "Выберите, что хотите сделать, используя клавиатуру ниже. 👇"
        ),
        reply_markup=main_menu,
        parse_mode="HTML"  # Указываем parse_mode для HTML-разметки
    )

# Купить в подарок
@router.message(lambda message: message.text == "Купить в подарок")
async def buy_gift_handler(message: Message):
    """
    Обрабатывает нажатие кнопки "Купить в подарок".
    """
    user_data[message.from_user.id] = {"gift": True, "awaiting_username": True}
    await message.answer(
        "🎁 Введите никнейм получателя звёзд (начинается с @):",
        parse_mode="HTML"
    )

# Обработка ввода никнейма
@router.message(lambda message: user_data.get(message.from_user.id, {}).get("awaiting_username"))
async def input_gift_username_handler(message: Message):
    """
    Обрабатывает ввод никнейма получателя.
    """
    username = message.text.strip()
    if not username.startswith("@"):
        await message.answer(
            "❌ Никнейм должен начинаться с '@'. Попробуйте снова.",
            parse_mode="HTML"
        )
        return

    user_data[message.from_user.id]["recipient"] = username
    user_data[message.from_user.id]["awaiting_username"] = False
    user_data[message.from_user.id]["awaiting_amount"] = True

    await message.answer(
        f"🎁 Отлично! Вы дарите звёзды пользователю {username}.\n\n"
        f"Введите количество звёзд, которое вы хотите подарить (не менее {MIN_STARS}):",
        parse_mode="HTML"
    )

# Купить для себя
@router.message(lambda message: message.text == "Купить для себя")
async def buy_self_handler(message: Message):
    """
    Обрабатывает нажатие кнопки "Купить для себя".
    """
    user_data[message.from_user.id] = {"gift": False, "awaiting_amount": True}
    await message.answer(
        f"✨ Введите количество звёзд, которое вы хотите приобрести (не менее {MIN_STARS}):",
        parse_mode="HTML"
    )

# Обработка ввода количества звезд
@router.message(lambda message: user_data.get(message.from_user.id, {}).get("awaiting_amount") and message.text.isdigit())
async def input_amount_handler(message: Message):
    """
    Обрабатывает ввод количества звёзд.
    """
    amount = int(message.text)

    if amount < MIN_STARS:
        await message.answer(
            f"❌ Вы не можете купить менее {MIN_STARS} звёзд. Пожалуйста, введите корректное количество.",
            parse_mode="HTML"
        )
        return

    price = calculate_price(amount, STAR_COST)
    user_data[message.from_user.id]["amount"] = amount
    user_data[message.from_user.id]["price"] = price
    user_data[message.from_user.id]["awaiting_amount"] = False

    gift_text = (
        f"🎁 Вы хотите подарить <b>{amount} звёзд</b> пользователю {user_data[message.from_user.id]['recipient']}.\n"
        if user_data[message.from_user.id].get("gift") else
        f"⭐ Вы хотите приобрести <b>{amount} звёзд</b>.\n"
    )

    await message.answer(
        f"{gift_text}💰 Цена за это количество: <b>{price} руб.</b>\n\n"
        "Переходим к выбору способа оплаты:",
        reply_markup=payment_menu,
        parse_mode="HTML"
    )

# Обработка выбора способа оплаты
@router.callback_query(lambda call: call.data.startswith("pay_"))
async def payment_method_handler(call: CallbackQuery):
    """
    Обрабатывает выбор способа оплаты.
    """
    payment_method = call.data.split("_")[1]  # Извлекаем метод оплаты из callback_data
    await call.message.answer(
        f"💳 Вы выбрали способ оплаты: <b>{payment_method.upper()}</b>.\n\n"
        "✅ Оплата получена. Ожидайте начисления!\n\n"
        "Среднее время зачисления звёзд: <i>15 минут</i>.\n\n"
        f"Если у вас возникли вопросы, обратитесь в поддержку: {SUPPORT_CONTACT}",
        parse_mode="HTML"
    )
    await send_order_to_admin(call.from_user)

# Уведомление администратору
async def send_order_to_admin(user):
    """
    Отправляет уведомление админу о новом заказе.
    """
    amount = user_data[user.id]["amount"]
    price = user_data[user.id]["price"]
    recipient = user_data[user.id].get("recipient", "—")

    await user.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=FSInputFile("images/admin_notification.jpg"),
        caption=(
            "📩 <b>Новый заказ!</b>\n\n"
            f"👤 Пользователь: @{user.username}\n"
            f"🎁 Подарок для: {recipient}\n"
            f"⭐ Количество: {amount}\n"
            f"💰 Сумма: {price} руб.\n\n"
            "Администратор, выдайте звёзды. 🌟"
        ),
        reply_markup=admin_menu,
        parse_mode="HTML"
    )

# Закрыть заказ
@router.callback_query(lambda call: call.data == "close_order")
async def close_order(call: CallbackQuery):
    """
    Удаляет сообщение о заказе у администратора.
    """
    await call.message.delete()
    await call.answer("✅ Заявка закрыта.", show_alert=False)

# Регистрация всех обработчиков
def setup_handlers(dp: Dispatcher):
    dp.include_router(router)
