import streamlit as st
from app_functions import CurrencyRateError, convert, get_api_key, get_rates

st.title("Convertisseur de devises")


@st.cache_data(ttl=3600)
def load_rates(api_key):
    return get_rates(api_key=api_key)


try:
    api_key = get_api_key()
    if not api_key:
        raise CurrencyRateError(
            "Clé API manquante : définis la variable EXCHANGE_RATE_API_KEY."
        )

    rates = load_rates(api_key)
except CurrencyRateError as error:
    st.error(str(error))
    st.info(
        "Crée une clé sur exchangerate-api.com puis définis la variable "
        "d'environnement EXCHANGE_RATE_API_KEY."
    )
    st.stop()


amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
currencies = sorted(rates.keys())
from_currency = st.selectbox("De :", currencies)
to_currency = st.selectbox("Vers :", currencies)

if st.button("Convertir"):
    if amount <= 0:
        st.error("Erreur : Le montant doit être strictement positif (supérieur à 0).")
    elif from_currency == to_currency:
        st.error("Erreur : La devise source et la devise cible doivent être différentes.")
    else:
        try:
            result = convert(amount, from_currency, to_currency, rates)
            st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        except CurrencyRateError as error:
            st.error(str(error))
