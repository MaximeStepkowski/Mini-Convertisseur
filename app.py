import streamlit as st
from app_functions import RATES, convert

st.title("Convertisseur de devises")

currencies = list(RATES.keys())

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
    if amount <= 0:
        st.error("Erreur : Le montant doit être strictement positif (supérieur à 0).")
    elif from_currency == to_currency:
        st.error("Erreur : La devise source et la devise cible doivent être différentes.")
    else:
        result = convert(amount, from_currency, to_currency)
        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
