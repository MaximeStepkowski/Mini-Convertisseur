import streamlit as st
from app_functions import RATES, convert

st.title("Convertisseur de devises")

amount = st.number_input("Montant :", min_value=0.0, format="%.2f")
from_currency = st.selectbox("De :", RATES.keys())
to_currency = st.selectbox("Vers :", RATES.keys())

if st.button("Convertir"):
    result = convert(amount, from_currency, to_currency)
    st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
