RATES = {
    "EUR": 1,
    "USD": 1.1,
    "GBP": 0.86,
    "JPY": 130
}


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    if amount <= 0:
        raise ValueError("Le montant doit être strictement positif (supérieur à 0).")
    if from_currency == to_currency:
        raise ValueError("La devise source et la devise cible doivent être différentes.")
    return amount * RATES[to_currency] / RATES[from_currency]
