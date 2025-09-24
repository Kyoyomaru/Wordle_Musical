# importar la libreria pydub --> Poner en la terminal: pip install pydub

from pydub import AudioSegment
from pydub.playback import play


class Letra:
    def __init__(self,caracter: str):
        self.caracter= caracter.upper()
        self.estado= "indefinido"
    def marcar_posicion_correcta(self):
        self.estado= "posicion correcta"
    def marcar_posicion_incorrecta(self):
        self.estado= "Posicion Incorrecta"
    def marcar_no_palabra(self):
        self.estado= "No en la palabra"




    def __str__(self):
        if self.estado == "posicion correcta":
            return "[{self.caracter}]"

        elif self.estado == "posicion incorrecta":
            return "[{self.caracteer}]"

        else:
            return"{self.caracter}"



class Cancion:
    pass

class Jugador:
    pass

class WordleMusic:
    pass