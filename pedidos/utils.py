from datetime import datetime
from django.core.exceptions import ValidationError

def convertir_fecha(fecha_str):
    """
    Convierte una fecha en formato 'dd/mm/yyyy' a un objeto datetime.date.
    Lanza ValidationError si el formato es incorrecto.
    """
    try:
        return datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        raise ValidationError("La fecha debe estar en formato dd/mm/aaaa")
