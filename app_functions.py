RATES = {
    "EUR": 1,
    "USD": 1.1,
    "GBP": 0.86,
    "JPY": 130
}


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    return amount * RATES[to_currency] / RATES[from_currency]
