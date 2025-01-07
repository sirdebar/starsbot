def calculate_price(amount: int, star_cost: float) -> float:
    return round(amount * star_cost, 2)

def format_html_text(text: str) -> str:
    """
    Функция для безопасного форматирования текста с использованием HTML.
    """
    return text.replace("*", "").replace("_", "")
