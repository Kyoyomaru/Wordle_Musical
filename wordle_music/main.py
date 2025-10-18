# importar la libreria pydub --> Poner en la terminal: pip install pydub

from pydub import AudioSegment
from pydub.playback import play


class Letra:
def __init__(self, caracter: str, posicion: int):
    self.caracter: str = caracter.upper()
    self.posicion: int = posicion
    self.estado: str = "oculta"
def marcar_letra(self,estado:str)->None:
    self.estado = estado

class Cancion:
    pass

class Jugador:
    pass

class WordleMusic:
    pass