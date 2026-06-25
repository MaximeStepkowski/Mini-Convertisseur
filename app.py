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


currencies = sorted(rates.keys())

if "history" not in st.session_state:
    st.session_state.history = []

if "from_currency" not in st.session_state:
    st.session_state.from_currency = currencies[0]
if "to_currency" not in st.session_state:
    st.session_state.to_currency = currencies[1] if len(currencies) > 1 else currencies[0]

def swap_currencies():
    st.session_state.from_currency, st.session_state.to_currency = (
        st.session_state.to_currency,
        st.session_state.from_currency,
    )

amount = st.number_input("Montant :", min_value=0.0, format="%.2f")

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    from_currency = st.selectbox(
        "De :",
        currencies,
        index=currencies.index(st.session_state.from_currency),
        key="from_currency",
    )

with col2:
    st.write("")
    st.write("")
    st.button("⇄", on_click=swap_currencies)

with col3:
    to_currency = st.selectbox(
        "Vers :",
        currencies,
        index=currencies.index(st.session_state.to_currency),
        key="to_currency",
    )

if st.button("Convertir"):
        try:
            result = convert(amount, from_currency, to_currency, rates)
            st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
            st.session_state.history.append(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        except CurrencyRateError as error:
            st.error(str(error))
        except ValueError as e:
            st.error(f"Erreur : {e}")

if st.session_state.history:
    st.subheader("Historique")
    for entry in reversed(st.session_state.history):
        st.write(entry)
