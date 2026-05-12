from enum import Enum


class EstadoLibro(str, Enum):
    disponible = "disponible"
    prestado = "prestado"
