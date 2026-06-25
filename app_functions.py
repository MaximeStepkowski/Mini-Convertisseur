import os
import requests


API_BASE_URL = "https://v6.exchangerate-api.com/v6"
API_KEY_ENV_VAR = "EXCHANGE_RATE_API_KEY"


class CurrencyRateError(Exception):
    """Erreur liée à la récupération ou à l'utilisation des taux."""


def get_api_key() -> str | None:
    api_key = os.getenv(API_KEY_ENV_VAR)
    if api_key:
        return api_key

    env_path = ".env"
    if not os.path.exists(env_path):
        return None

    with open(env_path, encoding="utf-8") as env_file:
        for line in env_file:
            key, separator, value = line.strip().partition("=")
            if separator and key == API_KEY_ENV_VAR:
                return value.strip().strip("\"'")

    return None


def get_rates(base_currency: str = "EUR", api_key: str | None = None) -> dict[str, float]:
    if api_key is None:
        api_key = get_api_key()
    if not api_key:
        raise CurrencyRateError(
            "Clé API manquante : définis la variable EXCHANGE_RATE_API_KEY."
        )

    url = f"{API_BASE_URL}/{api_key}/latest/{base_currency}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        raise CurrencyRateError("Impossible de récupérer les taux de change.") from error
    except ValueError as error:
        raise CurrencyRateError("Réponse invalide reçue depuis l'API.") from error

    if data.get("result") != "success":
        error_type = data.get("error-type", "erreur inconnue")
        raise CurrencyRateError(f"L'API a refusé la demande : {error_type}.")

    rates = data.get("conversion_rates")
    if not isinstance(rates, dict):
        raise CurrencyRateError("Les taux de change sont absents de la réponse API.")

    return rates


def convert(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: dict[str, float],
) -> float:
    if from_currency not in rates or to_currency not in rates:
        raise CurrencyRateError("Devise introuvable dans les taux de change.")
    if amount <= 0:
        raise ValueError("Le montant doit être strictement positif (supérieur à 0).")
    if from_currency == to_currency:
        raise ValueError("La devise source et la devise cible doivent être différentes.")
    return amount * rates[to_currency] / rates[from_currency]
