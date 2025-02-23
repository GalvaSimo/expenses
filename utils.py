from enum import Enum


class Activity(Enum):
    SDC = "Iscrizione Scuola di Comunità"
    GIA = "Giornata d'Inizio 2025-26"
    FC = "Fondo Comune"
    LIBRITRACCE = "Libri/Tracce"
    PRELIEVO = "Prelievo"
    PAGAMANETO = "Pagamenti"
    PASQUA = "Gesti di Pasqua"
    CUCINA = "Cucina"


class LTOperations(Enum):
    VENDITA = "Vendita"
    CVENDITA_C = "Conto Vendita - Consegna"
    CVENDITA_R = "Conto Vendita - Ritiro"


books = [
    "Ho fatto tutto per essere felice",
    "Occhi che non vedono",
    "C'è speranza? Il fascino della scoperta",
    "Volantoni Natale piccoli",
    "Volantoni Natale grandi",
    "Tracce - Gennaio 2025",
    "Tracce - Febbraio 2025",
    "Altro",
]

operations = [activity.value for activity in Activity]
lt_operations = [lt_activity.value for lt_activity in LTOperations]
payments = ("Contanti", "Satispay", "POSS")
