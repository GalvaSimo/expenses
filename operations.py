import json
from dataclasses import dataclass, asdict
import os


@dataclass
class Operation:
    user: str
    name: str
    phone: str
    mail: str
    payment: str
    date: str
    amount: str
    note: str


@dataclass
class IscrizioneSDC(Operation):
    esito_iscrizione: str


@dataclass
class FondoComune(Operation):
    month: str
    year: str


@dataclass
class GIA(Operation):
    esito_iscrizione: str


@dataclass
class LibriTracce(Operation):
    type: str
    article: str
    quantity: str


@dataclass
class Pagamenti(Operation):
    pass


@dataclass
class Pasqua(Operation):
    gruppo: str
    mail_iscritto: str


@dataclass
class Cucina(Operation):
    pass


def save_to_json(obj):
    """
    Salva i dati dell'oggetto in un file JSON con il nome della classe,
    mantenendo una lista di tutti gli oggetti salvati.
    """
    os.makedirs("files", exist_ok=True)
    filename = os.path.join("files", f"{obj.__class__.__name__}.json")
    data = []

    # Se il file esiste, carica i dati esistenti
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []

    # Aggiunge il nuovo oggetto alla lista
    data.append(asdict(obj))

    # Scrive la lista aggiornata nel file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def convert_to_specific_operation(
    operation: Operation, operation_type: str, **extra_fields
):
    """
    Converte un oggetto Operation in una sottoclasse specifica come IscrizioneSDC, FondoComune o altre.
    """
    operation_classes = {
        "IscrizioneSDC": IscrizioneSDC,
        "FondoComune": FondoComune,
        "GIA": GIA,
        "LibriTracce": LibriTracce,
        "Pagamenti": Pagamenti,
        "Pasqua": Pasqua,
        "Cucina": Cucina,
    }

    if operation_type in operation_classes:
        return operation_classes[operation_type](**asdict(operation), **extra_fields)
    else:
        raise ValueError("Tipo di operazione non valido")


def create_operation_from_json(json_data):
    """
    Crea un'istanza di una sottoclasse di Operation a partire da un dizionario JSON.
    Prova a determinare automaticamente il tipo corretto di operazione.
    """
    operation_classes = {
        "IscrizioneSDC": IscrizioneSDC,
        "FondoComune": FondoComune,
        "GIA": GIA,
        "LibriTracce": LibriTracce,
        "Pagamenti": Pagamenti,
        "Pasqua": Pasqua,
        "Cucina": Cucina,
    }

    # Prova a determinare il tipo di operazione dai campi presenti nel JSON
    for operation_type, cls in operation_classes.items():
        cls_fields = set(cls.__annotations__.keys())  # Campi definiti nella classe
        json_fields = set(json_data.keys())  # Campi presenti nel JSON

        if cls_fields.issubset(
            json_fields
        ):  # Se tutti i campi della classe sono nel JSON
            return cls(**json_data)

    # Se nessuna sottoclasse corrisponde, ritorna un'istanza base di Operation
    return Operation(**json_data)
