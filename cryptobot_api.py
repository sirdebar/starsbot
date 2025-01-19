from aiocryptopay import AioCryptoPay, Networks

CRYPTO_API_TOKEN = "319786:AAKDotTAorRkcLNhSq5yhYgtcYpHLb2z1YS"
CRYPTO_NETWORK = Networks.MAIN_NET

crypto = AioCryptoPay(token=CRYPTO_API_TOKEN, network=CRYPTO_NETWORK)


async def create_invoice(amount_rub, description="", hidden_message="", payload=""):
    rates = await crypto.get_exchange_rates()

    usdt_rate = next((rate for rate in rates if rate.source == "USDT" and rate.target == "RUB"), None)
    if not usdt_rate:
        raise Exception("Не удалось получить курс USDT/RUB")

    amount_usdt = float(amount_rub) / float(usdt_rate.rate)

    invoice = await crypto.create_invoice(
        asset="USDT",
        amount=round(amount_usdt, 2),  # Ограничиваем до 2 знаков после запятой
        description=description,
        hidden_message=hidden_message,
        payload=payload,
    )
    return invoice


async def get_invoice_status(invoice_id):
    invoices = await crypto.get_invoices(invoice_ids=invoice_id)
    if not invoices:
        raise Exception("Счет не найден")
    return invoices[0].status
