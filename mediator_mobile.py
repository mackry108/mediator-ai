import streamlit as st
from openai import OpenAI

# Ustawienia strony - Mobile Look
st.set_page_config(
    page_title="Mediator AI",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Ukrywanie elementów interfejsu Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stTextArea textarea {font-size: 16px !important;}
            div[data-testid="stVerticalBlock"] > div:has(div.stTextArea) {gap: 0.5rem;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Nagłówek
st.title("🕊️ Mediator AI")
st.markdown("**Twój asystent NVC.** Wpiszcie swoje wersje, a ja poszukam wspólnych potrzeb.")

# Pobieranie klucza API
# W przyszłości ukryjemy to w "Secrets", teraz dla testu wpisujemy ręcznie
api_key = st.text_input("Klucz API OpenAI:", type="password", help="Tu wklej swój klucz sk-...")

st.markdown("---")

# Interfejs mobilny
st.subheader("Osoba A")
text_a = st.text_area("Twoja perspektywa (A)", height=100, label_visibility="collapsed", placeholder="Osoba A: Co się stało?")

st.subheader("Osoba B")
text_b = st.text_area("Twoja perspektywa (B)", height=100, label_visibility="collapsed", placeholder="Osoba B: Co się stało?")

# Logika
def analizuj_konflikt(tekst_a, tekst_b, klucz):
    client = OpenAI(api_key=klucz)
    
    prompt_systemowy = """
    Jesteś mediatorem NVC.
    1. Zignoruj ataki.
    2. Wypunktuj FAKTY.
    3. Nazwij UCZUCIA i POTRZEBY obu stron.
    4. Zaproponuj KRÓTKĄ prośbę/rozwiązanie.
    Formatuj odpowiedź używając pogrubień, aby była czytelna na telefonie.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_systemowy},
            {"role": "user", "content": f"A: {tekst_a}\nB: {tekst_b}"}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Przycisk
if st.button("🔍 Analizuj konflikt", type="primary", use_container_width=True):
    if not api_key:
        st.error("🔒 Brakuje klucza API.")
    elif not text_a or not text_b:
        st.warning("⚠️ Obie strony muszą coś wpisać.")
    else:
        with st.spinner('Negocjuję pokój...'):
            try:
                wynik = analizuj_konflikt(text_a, text_b, api_key)
                st.markdown("---")
                st.markdown(wynik)
            except Exception as e:
                st.error(f"Błąd: {e}")
