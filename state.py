import json
import streamlit as st
import operations


class CurrentState:
    _instance = None  # Variabile di classe per la singola istanza
    FILE_NAME = "current_state.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrentState, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self, first_name="", last_name=""):
        """Inizializza i campi e carica lo stato da file se esiste."""

        self.FIRST_NAME = first_name
        self.LAST_NAME = last_name
        self.NOME_PAGANTE = None
        self.NUMERO_PAGANTE = None
        self.EMAIL_PAGANTE = None
        self.DATE = None
        self.AMOUNT = 0.0
        self.PAYMENT = None
        self.ATTIVITA = None
        self.NOTE = None
        self.LT_OPERAZIONE = None
        self.LT_AMOUNT = 0
        self.OPERATION = None

    def save_state(self):
        """Salva lo stato corrente in un file JSON."""
        with open(self.FILE_NAME, "w") as f:
            state_dict = self.__dict__.copy()
            if isinstance(self.OPERATION, operations.Operation):
                state_dict["OPERATION"] = (
                    self.OPERATION.__dict__
                )  # Serializza Operation
            json.dump(state_dict, f, indent=4)

    def load_state(self):
        """Carica lo stato dal file JSON se esiste."""
        try:
            with open(self.FILE_NAME, "r") as f:
                data = json.load(f)
                self.__dict__.update(data)
        except (FileNotFoundError, json.JSONDecodeError):
            pass  # Se il file non esiste o è corrotto, mantiene i valori di default

    def reset_state(self):
        """Reinizializza lo stato ai valori di default e lo salva."""
        self._initialize()
        self.save_state()

    def print_state(self):
        """Stampa a video lo stato corrente."""
        for key, value in self.__dict__.items():
            if (
                key != "_instance"
            ):  # Evita di stampare la variabile della singola istanza
                st.write(f"{key}: {value}")

    def get_user(self):
        """Restituisce il nome completo concatenato."""
        return f"{self.FIRST_NAME} {self.LAST_NAME}".strip()

    def delete_instance(cls):
        """Elimina completamente l'istanza attuale."""
        cls._instance = None


# Creazione della singola istanza accessibile dall'esterno
current_state = CurrentState()
