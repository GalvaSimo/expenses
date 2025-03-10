import streamlit as st
import login
from state import current_state
import datetime
import calendar
import locale
import utils
import operations
import time
import os

locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")

operation = None
attivita = None
activity_index = None
payment_index = None


def new_operation(fname, lname):
    current_state._initialize(fname, lname)
    st.session_state.clear()
    current_state.save_state()


def save_operation(op, fname, lname):
    operations.save_to_json(op)
    container = st.empty()
    container.success("Attività salvata! ✅")
    time.sleep(2)
    container.empty()
    new_operation(fname, lname)


def reset_attivita_pronta():
    st.write("resetto attivita pronta")
    if "attivita_pronta" in st.session_state:
        st.session_state["attivita_pronta"] = False


def clearmystate(fname, lname):
    current_state._initialize(fname, lname)
    st.session_state.clear()
    current_state.save_state()
    st.stop()
    # time.sleep(1)
    # st.write("load state")
    # current_state.load_state()
    # time.sleep(1)
    # st.write("print stato")
    st.write(st.session_state)


time.sleep(0.1)
username, password = login.load_credentials()
if username and password:
    st.session_state["authenticated"] = True
    if "page" not in st.session_state:
        st.session_state["page"] = "HOME"
else:
    st.session_state["authenticated"] = False
if not st.session_state["authenticated"]:
    login.login_page()
else:
    if st.session_state["page"] == "HOME":
        with st.sidebar:
            users = login.load_users()
            if "first_name" not in st.session_state:
                st.session_state["first_name"] = users[username]["first_name"]
                current_state.FIRST_NAME = st.session_state["first_name"]
            if "last_name" not in st.session_state:
                st.session_state["last_name"] = users[username]["last_name"]
                current_state.LAST_NAME = st.session_state["last_name"]
            st.write("User: " + current_state.get_user())
            # current_state.save_state()
            if st.button("Logout"):
                login.logout()
            if st.button("Nuova operazione"):
                st.session_state["page"] = "POPUP_NUOVA"
                st.rerun()

        # SEZIONE 1
        # current_state.load_state()

        if "attivita_pronta" not in st.session_state:
            st.session_state["attivita_pronta"] = False
        current_state.load_state()
        nome_pagante = st.text_input(
            "Nome e cognome pagante:", value=current_state.NOME_PAGANTE
        )
        current_state.NOME_PAGANTE = nome_pagante
        # current_state.save_state()

        phone_number = st.text_input(
            "Numero di telefono pagante:", value=current_state.NUMERO_PAGANTE
        )
        current_state.NUMERO_PAGANTE = phone_number
        # current_state.save_state()

        mail_pagante = st.text_input(
            "e-mail pagante:", value=current_state.EMAIL_PAGANTE
        )
        current_state.EMAIL_PAGANTE = mail_pagante
        # current_state.save_state()

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if current_state.ATTIVITA is not None:
                activity_index = utils.operations.index(current_state.ATTIVITA)
            else:
                activity_index = None
            attivita = st.selectbox(
                "Attività",
                utils.operations,
                index=activity_index,
                placeholder="Scegli un'operazione",
            )
            current_state.ATTIVITA = attivita
            # current_state.save_state()
            st.session_state["attivita"] = attivita

            if st.session_state["attivita"] is not None:
                st.session_state["attivita_pronta"] = True
            else:
                st.session_state["attivita_pronta"] = False

        with col2:
            if current_state.PAYMENT is not None:
                payment_index = utils.payments.index(current_state.PAYMENT)
            else:
                payment_index = None
            payment = st.selectbox(
                "Modalità di pagamento",
                utils.payments,
                index=payment_index,
                placeholder="Scegli",
            )
            current_state.PAYMENT = payment
            # current_state.save_state()
            st.session_state["pagamento"] = payment

        with col3:
            d = st.date_input("Data operazione", format="DD/MM/YYYY")
            current_state.DATE = str(d)
            # current_state.save_state()
        col4, col5 = st.columns([2, 1])
        with col4:
            note = st.text_area("note", value=current_state.NOTE)
            current_state.NOTE = note
            # current_state.save_state()
        with col5:
            amount = st.number_input(
                "Importo versato (€)",
                step=0.1,
                value=current_state.AMOUNT,
            )
            current_state.AMOUNT = amount
            # current_state.save_state()
        # current_state.save_state()
        # SEZIONE 2 *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        if st.session_state["attivita_pronta"]:
            st.markdown(
                "<hr style='border: 1px solid #FF4B4B; margin: 20px 0;'>",
                unsafe_allow_html=True,
            )
            operation = operations.Operation(
                user=current_state.get_user(),
                name=current_state.NOME_PAGANTE,
                phone=current_state.NUMERO_PAGANTE,
                mail=current_state.EMAIL_PAGANTE,
                payment=current_state.PAYMENT,
                date=current_state.DATE,
                amount=str(current_state.AMOUNT),
                note=current_state.NOTE,
            )
            testo_sezione2 = ""
            match attivita:
                case utils.Activity.SDC.value:
                    testo_sezione2 = (
                        "Registrazione dati per Iscrizione SCUOLA DI COMUNITÀ"
                    )
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
            match attivita:
                case utils.Activity.SDC.value:
                    esito_sdc = st.radio("Ti sei iscritto correttamente?", ["Sì", "No"])
                    iscrizioneSDC = operations.convert_to_specific_operation(
                        operation, "IscrizioneSDC", esito_iscrizione=esito_sdc
                    )
                    operation = iscrizioneSDC
                case utils.Activity.FC.value:
                    months = list(calendar.month_name)[1:]
                    years = [datetime.datetime.now().year - i for i in range(3)]
                    with col7:
                        m = st.selectbox(
                            "Seleziona mese", months, index=None, placeholder="Scegli"
                        )
                    with col8:
                        y = st.selectbox(
                            "Seleziona anno", years, index=None, placeholder="Scegli"
                        )
                    fondo = operations.convert_to_specific_operation(
                        operation, "FondoComune", month=m, year=y
                    )
                    operation = fondo
                case utils.Activity.GIA.value:
                    esito_gia = st.radio("Ti sei iscritto nel modulo?", ["Sì", "No"])
                    gia = operations.convert_to_specific_operation(
                        operation, "GIA", esito_iscrizione=esito_gia
                    )
                    operation = gia
                case utils.Activity.LIBRITRACCE.value:
                    with col7:
                        if current_state.LT_OPERAZIONE is not None:
                            lt_choice_index = utils.lt_operations.index(
                                current_state.LT_OPERAZIONE
                            )
                        else:
                            lt_choice_index = None

                        lt_choice = st.selectbox(
                            "Operazione",
                            utils.lt_operations,
                            index=lt_choice_index,
                            placeholder="Scegli",
                        )
                        current_state.LT_OPERAZIONE = lt_choice
                    if lt_choice is not None:
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

                            lt_amount = st.number_input(lt_placeholder, step=1)
                        if vendita:
                            books = st.selectbox(
                                "Libro/Tracce",
                                utils.books,
                                index=None,
                                placeholder="Scegli l'articolo da vendere",
                            )
                            new_title = books
                            if books == "Altro":
                                title = st.text_input("Inserisci il titolo")
                                new_title = books + " - " + title

                            lt = operations.convert_to_specific_operation(
                                operation,
                                "LibriTracce",
                                type="Vendita",
                                article=new_title,
                                quantity=lt_amount,
                            )
                        else:
                            lt = operations.convert_to_specific_operation(
                                operation,
                                "LibriTracce",
                                type="Conto Vendita",
                                article="",
                                quantity=lt_amount,
                            )
                        operation = lt
                case utils.Activity.PAGAMANETO.value:
                    st.write("Inserisci nelle note che tipo di spesa si è pagato")
                    pagamento = operations.convert_to_specific_operation(
                        operation, "Pagamenti"
                    )
                    operation = pagamento
                case utils.Activity.CUCINA.value:
                    st.write("Inserisci nelle note che tipo di spesa si è pagato")
                    cucina = operations.convert_to_specific_operation(
                        operation, "Cucina"
                    )
                    operation = cucina
                case utils.Activity.PASQUA.value:
                    p = st.radio("CLU/ADULTI", ["CLU (5€)", "ADULTI (10€)"])
                    mail_for_ticket = st.text_input(
                        "Inserire qui obbligatoriamente la mail per poter inviare il tesserino"
                    )
                    pasqua = operations.convert_to_specific_operation(
                        operation, "Pasqua", gruppo=p, mail_iscritto=mail_for_ticket
                    )
                    operation = pasqua
            current_state.OPERATION = operation
            current_state.save_state()

        if attivita is not None:
            current_state.load_state()
            if st.button("Salva operazione"):
                st.session_state["page"] = "POPUP_SALVA"
                st.rerun()

    if st.session_state["page"] == "POPUP_NUOVA":
        st.write("Sei sicuro di voler inserire una nuova operazione?")
        col1, col2, _, _ = st.columns(4)
        if col1.button("Annulla ❌"):
            st.session_state["page"] = "HOME"
            st.rerun()

        with col2:
            if col2.button(
                "Conferma ✅",
                on_click=new_operation,
                args=[st.session_state["first_name"], st.session_state["last_name"]],
            ):
                st.session_state["page"] = "HOME"
                st.rerun()

    if st.session_state["page"] == "POPUP_SALVA":
        operation_to_save = operations.create_operation_from_json(
            current_state.OPERATION
        )
        st.write("Salvare l'operazione?")
        col1, col2, _, _ = st.columns(4)
        if col1.button("Annulla ❌"):
            st.session_state["page"] = "HOME"
            st.rerun()

        with col2:
            if col2.button(
                "Salva ✅",
                on_click=save_operation,
                args=[
                    operation_to_save,
                    st.session_state["first_name"],
                    st.session_state["last_name"],
                ],
            ):
                st.session_state["page"] = "HOME"
                st.rerun()

    # current_state.print_state()

# st.write(st.session_state)
# st.write("activity index " + str(activity_index))
