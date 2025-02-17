import streamlit as st

# Credenziali hardcoded (da migliorare in futuro)
USERNAME = "user"
PASSWORD = "psw"

# Funzione per il login
def login():
    st.title("Login")

    # Input per nome utente e password
    username = st.text_input("Username", value="", key="username")
    password = st.text_input("Password", value="", type="password", key="password")

    # Bottone di login
    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.success("Accesso riuscito! Benvenuto 🎉")
        else:
            st.error("Credenziali errate. Riprova.")

if __name__ == "__main__":
    login()
