import streamlit as st
import os
import json

STATE_FILE = "session_state.json"
FIRST_NAME = ""
LAST_NAME = ""
PAGE = ""

NOME_PAGAMENTE = ""
NUMERO_PAGANTE = ""
EMAIL_PAGANTE = ""
IMPORTO = 0.0

operations = (
    "Iscrizione Scuola di Comunità",
    "Giornata d'Inizio 2025-26",
    "Fondo Comune",
    "Prelievo",
    "Pagamenti",
    "Gesti di Pasqua, Cucina",
)
payments = ("Contanti", "Satispay", "POSS")


def clear_mystate():
    global NOME_PAGAMENTE
    NOME_PAGAMENTE = ""
    global NUMERO_PAGANTE
    NUMERO_PAGANTE = ""
    global EMAIL_PAGANTE
    EMAIL_PAGANTE = ""
    global IMPORTO
    IMPORTO = 0.0


def save_state():
    serializable_state = {
        key: value
        for key, value in st.session_state.items()
        if isinstance(value, (str, int, float, bool, list, dict))
    }
    with open(STATE_FILE, "w") as file:
        json.dump(serializable_state, file)
    return serializable_state


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as file:
            state = json.load(file)
            st.session_state.update(state)


def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
