import streamlit as st
from app_functions import RATES, convert

st.title("Convertisseur de devises")

amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
from_currency = st.selectbox("De :", RATES.keys())
to_currency = st.selectbox("Vers :", RATES.keys())

if st.button("Convertir"):
    if amount <= 0:
        st.error("Erreur : Le montant doit être strictement positif (supérieur à 0).")
    elif from_currency == to_currency:
        st.error("Erreur : La devise source et la devise cible doivent être différentes.")
    else:
        result = convert(amount, from_currency, to_currency)
        st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
