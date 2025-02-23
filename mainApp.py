import streamlit as st
import login
import state
import datetime
import calendar
import locale
import utils

locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")


# Funzione che mostra la home page dopo il login
def show_home_page():
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    st.title(f"Benvenuto, {first_name} {last_name}!")
    st.success("Accesso riuscito! 🎉")
    # Aggiungi qui altre funzionalità della home page


if "show_popup" not in st.session_state:
    st.session_state["show_popup"] = False


# Funzione per mostrare il popup
def open_popup():
    st.session_state["show_popup"] = True


# Funzione per chiudere il popup
def close_popup(choice):
    st.session_state["show_popup"] = False
    st.session_state["popup_choice"] = choice
    if choice == "Sì":
        state.clear_mystate()


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
    if not st.session_state["show_popup"]:
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

        # SEZIONE 1
        nome_pagante = st.text_input(
            "Nome e cognome pagante:", value=state.CurrentState.NOME_PAGANTE
        )
        state.CurrentState.NOME_PAGANTE = nome_pagante
        phone_number = st.text_input(
            "Numero di telefono pagante:", value=state.CurrentState.NUMERO_PAGANTE
        )
        state.CurrentState.NUMERO_PAGANTE = phone_number
        mail_pagante = st.text_input(
            "e-mail pagante:", value=state.CurrentState.EMAIL_PAGANTE
        )
        state.CurrentState.EMAIL_PAGANTE = mail_pagante
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            option = st.selectbox(
                "Attività",
                utils.operations,
                index=state.CurrentState.ATTIVITA,
                placeholder="Scegli un'operazione",
            )
            # if option is not None:
            #    state.CurrentState.ATTIVITA = utils.operations.index(option)
        with col2:
            payment = st.selectbox(
                "Modalità di pagamento",
                utils.payments,
                index=state.CurrentState.PAYMENT,
                placeholder="Scegli",
            )
            # if payment is not None:
            #    state.CurrentState.PAYMENT = utils.payments.index(payment)
        with col3:
            d = st.date_input("Data operazione", format="DD/MM/YYYY")
        col4, col5 = st.columns([2, 1])
        with col4:
            note = st.text_area("note", value=state.CurrentState.NOTE)
            state.CurrentState.NOTE = note
        with col5:
            amount = st.number_input(
                "Importo versato (€)",
                step=0.1,
                value=state.CurrentState.AMOUNT,
            )
            # state.CurrentState.IMPORTO = amount
            if st.button("Nuova operazione"):
                open_popup()

        # SEZIONE 2 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        st.markdown(
            "<hr style='border: 1px solid #FF4B4B; margin: 20px 0;'>",
            unsafe_allow_html=True,
        )
        testo_sezione2 = ""
        match option:
            case utils.Activity.SDC.value:
                testo_sezione2 = "Registrazione dati per Iscrizione SCUOLA DI COMUNITÀ"
            case utils.Activity.GIA.value:
                testo_sezione2 = "Registrazione dati per GIORNATA DI INIZIO ANNO"
            case utils.Activity.FC.value:
                testo_sezione2 = "Registrazione dati per Versamento FONDO COMUNE.  \nIl Fondo Comune viene contabilizzato da Ottobre a Settembre. Per versamenti a cavallo dell'anno contabilizzare diverse operazioni."
            case utils.Activity.LIBRITRACCE.value:
                testo_sezione2 = "Registrazione dati per VENDITA LIBRI E TRACCE"
            case utils.Activity.PAGAMANETO.value:
                testo_sezione2 = "Registrazione dati per PAGAMENTI"
            case utils.Activity.PASQUA.value:
                testo_sezione2 = "Registrazione dati per GESTI DI PASQUA"
        st.write(testo_sezione2)
        col7, col8 = st.columns(2)

        match option:
            case utils.Activity.SDC.value:
                sdc = st.radio("Ti sei iscritto correttamente?", ["Sì", "No"])

            case utils.Activity.FC.value:
                months = list(calendar.month_name)[1:]
                years = [datetime.datetime.now().year - i for i in range(3)]
                with col7:
                    month = st.selectbox(
                        "Seleziona mese", months, index=None, placeholder="Scegli"
                    )
                with col8:
                    year = st.selectbox(
                        "Seleziona anno", years, index=None, placeholder="Scegli"
                    )

            case utils.Activity.GIA.value:
                gia = st.radio("Ti sei iscritto nel modulo?", ["Sì", "No"])

            case utils.Activity.LIBRITRACCE.value:
                with col7:
                    lt_choice = st.selectbox(
                        "Operazione",
                        utils.lt_operations,
                        index=None,
                        placeholder="Scegli",
                    )
                    state.CurrentState.LT_OPERAZIONE = lt_choice
                with col8:
                    lt_placeholder = "Numero"
                    vendita = False
                    match lt_choice:
                        case utils.LTOperations.CVENDITA_C.value:
                            lt_placeholder = "Numero Tracce consegnati"
                            vendita = False
                        case utils.LTOperations.CVENDITA_R.value:
                            lt_placeholder = "Numero Tracce che sta pagando"
                            vendita = False
                        case utils.LTOperations.VENDITA.value:
                            lt_placeholder = "Numero Libri/Tracce venduti"
                            vendita = True
                    lt_amount = st.number_input(
                        lt_placeholder,
                        step=1,
                        value=state.CurrentState.LT_AMOUNT,
                    )
                if vendita:
                    books = st.selectbox(
                        "Libro/Tracce",
                        utils.books,
                        index=None,
                        placeholder="Scegli l'articolo da vendere",
                    )
                    if books == "Altro":
                        new_title = st.text_input("Inserisci il titolo")
            case utils.Activity.PAGAMANETO.value:
                new_payment = st.text_input("Inserisci che tipo di spesa si è pagato")
            case utils.Activity.PASQUA.value:
                pasqua = st.radio("CLU/ADULTI", ["CLU (5€)", "ADULTI (10€)"])
                mail_for_ticket = st.text_input(
                    "Inserire qui obbligatoriamente la mail per poter inviare il tesserino"
                )
        state.save_state()
    else:
        st.title("Attenzione")
        st.write("Sei sicuro di voler inziare con una nuova operazione?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sì"):
                close_popup("Sì")
        with col2:
            if st.button("❌ No"):
                close_popup("No")
        # st.write(st.session_state)
