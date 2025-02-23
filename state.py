import streamlit as st
import os
import json

STATE_FILE = "session_state.json"


class CurrentState:
    FIRST_NAME = ""
    LAST_NAME = ""
    PAGE = ""

    NOME_PAGANTE = ""
    NUMERO_PAGANTE = ""
    EMAIL_PAGANTE = ""
    AMOUNT = 0.0
    PAYMENT = None
    ATTIVITA = None
    NOTE = ""
    LT_OPERAZIONE = None
    LT_AMOUNT = 0


def printState():
    for nome, valore in vars(CurrentState).items():
        if not nome.startswith("__"):  # Esclude attributi speciali della classe
            st.write(nome, "=", valore)


def clear_mystate():
    CurrentState.NOME_PAGANTE = ""
    CurrentState.NUMERO_PAGANTE = ""
    CurrentState.EMAIL_PAGANTE = ""
    CurrentState.PAYMENT = None
    CurrentState.AMOUNT = 0.0
    CurrentState.ATTIVITA = None
    CurrentState.NOTE = ""
    CurrentState.LT_OPERAZIONE = None
    CurrentState.LT_AMOUNT = 0


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
