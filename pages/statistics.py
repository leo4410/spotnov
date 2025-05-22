import streamlit as st
from functions import analysis

def title():
    st.write("Statistik")

def example_view():
    df = analysis.example_analyse()
    st.bar_chart(data=df, x="Wochentag", y="Laufnummer")
    