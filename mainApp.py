import streamlit as st
import login
import state
import datetime


# Funzione che mostra la home page dopo il login
def show_home_page():
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    st.title(f"Benvenuto, {first_name} {last_name}!")
    st.success("Accesso riuscito! 🎉")
    # Aggiungi qui altre funzionalità della home page


def main():
    username, password = login.load_credentials()
    if username and password:
        st.session_state["authenticated"] = True
        st.session_state["page"] = "Home"
    else:
        st.session_state["authenticated"] = False

    if "page" not in st.session_state:
        st.session_state["page"] = "Login"

    if not st.session_state["authenticated"]:
        st.session_state = state.save_state()
        login.login_page()
    else:
        with st.sidebar:
            users = login.load_users()
            if "first_name" not in st.session_state:
                st.session_state["first_name"] = users[username]["first_name"]
            if "last_name" not in st.session_state:
                st.session_state["last_name"] = users[username]["last_name"]
            n = st.session_state["first_name"]
            s = st.session_state["last_name"]
            st.write(f"Utente: {n} {s}")

            if st.button("Logout"):
                login.logout()

        nome_pagante = st.text_input(
            "Nome e cognome pagante:", value=state.NOME_PAGAMENTE
        )
        state.NOME_PAGAMENTE = nome_pagante
        phone_number = st.text_input(
            "Numero di telefono pagante:", value=state.NUMERO_PAGANTE
        )
        state.NUMERO_PAGANTE = phone_number
        mail_pagante = st.text_input("e-mail pagante:", value=state.EMAIL_PAGANTE)
        state.EMAIL_PAGANTE = mail_pagante

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            option = st.selectbox(
                "Attività",
                state.operations,
                index=None,
                placeholder="Scegli un'operazione",
            )
        with col2:
            payment = st.selectbox(
                "Modalità di pagamento",
                state.payments,
                index=None,
                placeholder="Scegli",
            )
        with col3:
            d = st.date_input("Data operazione", format="DD/MM/YYYY")

        col4, col5 = st.columns([2, 1])
        with col4:
            note = st.text_area("note")
        with col5:
            amount = st.number_input(
                "Importo versato (€)", step=0.1, format="%0.01f", value=state.IMPORTO
            )
            state.IMPORTO = amount

            st.button("Nuova operazione", on_click=state.clear_mystate)
        state.save_state()
        # st.write(st.session_state)


if __name__ == "__main__":
    main()
