import streamlit as st
import csv
import os
from state import current_state

CREDENTIALS_FILE = "credentials.txt"


def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "w") as file:
        file.write(f"{username},{password}")


def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            data = file.read().strip()
            if data:
                return data.split(",")
    return None, None


def clear_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        os.remove(CREDENTIALS_FILE)


# Carica le credenziali dal file CSV
def load_users():
    credentials = {}
    with open("users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            credentials[row["username"]] = {
                "password": row["password"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
            }
    return credentials


def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username]["password"] == password:
            if "first_name" not in st.session_state:
                st.session_state["first_name"] = users[username]["first_name"]
                current_state.FIRST_NAME = st.session_state["first_name"]
            if "last_name" not in st.session_state:
                st.session_state["last_name"] = users[username]["last_name"]
                current_state.LAST_NAME = st.session_state["last_name"]
            save_credentials(username, password)  # Salva credenziali nel file
            # Salva le credenziali nella sessione
            st.session_state["authenticated"] = True
            current_state.save_state()
            st.rerun()
        else:
            st.error("Credenziali errate")


def logout():
    clear_credentials()
    current_state.reset_state()
    current_state.print_state()
    st.session_state.clear()
    st.session_state["authenticated"] = False
    st.rerun()
