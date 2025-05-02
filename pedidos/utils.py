from datetime import datetime

def convertir_fecha(fecha_str):
    """
    Convierte 'dd/mm/aaaa' a objeto date
    """
    try:
        return datetime.strptime(fecha_str, '%d/%m/%Y').date()
    except ValueError:
        raise ValueError("Formato de fecha inválido. Use dd/mm/aaaa")

def convertir_datetime(fecha_hora_str):
    """
    Convierte 'dd/mm/aaaa HH:MM' a objeto datetime
    """
    try:
        return datetime.strptime(fecha_hora_str, '%d/%m/%Y %H:%M')
    except ValueError:
        raise ValueError("Formato inválido. Use dd/mm/aaaa hh:mm")