import streamlit as st
from openai import OpenAI

# 1. Konfiguracja
st.set_page_config(
    page_title="Mediator AI",
    page_icon="🕊️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. CSS Hack - Mobile Look
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

# 3. Nagłówek
st.title("🕊️ Mediator AI")
st.info("Wpiszcie swoje wersje, a ja poszukam wspólnych potrzeb.")

# 4. Pobieranie klucza z "Sejfu" (Secrets)
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ Błąd konfiguracji: Nie znaleziono klucza API w Secrets.")
    st.stop()

# 5. Interfejs
st.subheader("Osoba A")
text_a = st.text_area("Twoja perspektywa (A)", height=120, label_visibility="collapsed", placeholder="Osoba A: Co się stało?")

st.subheader("Osoba B")
text_b = st.text_area("Twoja perspektywa (B)", height=120, label_visibility="collapsed", placeholder="Osoba B: Co się stało?")

# 6. Logika
def analizuj_konflikt(tekst_a, tekst_b):
    client = OpenAI(api_key=api_key)
    
    prompt_systemowy = """
    Jesteś mediatorem NVC (Porozumienie Bez Przemocy).
    1. Zignoruj ataki i oceny.
    2. Wypunktuj FAKTY.
    3. Nazwij UCZUCIA i POTRZEBY obu stron.
    4. Zaproponuj KRÓTKĄ prośbę/rozwiązanie.
    Formatuj odpowiedź używając pogrubień (**tekst**), aby była czytelna na telefonie.
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

# 7. Przycisk
if st.button("🔍 Analizuj konflikt", type="primary", use_container_width=True):
    if not text_a or not text_b:
        st.warning("⚠️ Obie strony muszą coś wpisać.")
    else:
        with st.spinner('Negocjuję pokój...'):
            try:
                wynik = analizuj_konflikt(text_a, text_b)
                st.markdown("---")
                st.markdown(wynik)
                st.caption("🤖 Analiza AI. W trudnych sprawach skonsultuj się z terapeutą.")
            except Exception as e:
                st.error(f"Błąd: {e}")
