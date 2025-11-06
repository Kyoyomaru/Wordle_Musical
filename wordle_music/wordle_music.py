import pygame
import random
import unicodedata
from pydub import AudioSegment
from io import BytesIO

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def normalizar_texto(texto):
    """Elimina espacios, acentos y caracteres especiales."""
    texto = texto.upper().replace(" ", "")
    # Eliminar acentos
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    # Mantener solo letras y números
    texto = ''.join(c for c in texto if c.isalnum())
    return texto

class WordleMusical:
    def __init__(self,jugador: Jugador,canciones:list):
        self.jugador = jugador
        self.canciones = canciones
        self.cancion_actual = None
        self.tablero = []

    def seleccionar_cancion(self):
        self.cancion_actual = random.choice(self.canciones)

    def inicializar_tablero(self):
        self.tablero = []
        self.jugador.reiniciar_intentos()
        return len(self.cancion_actual.titulo_original)
    def validar_intento(self,palabra:str):
        self.jugador.registrar_letras(palabra)
        resultado=self.cancion_actual.comparar_letras(palabra)
        self.tablero.append(resultado)

        palabra_normalizada = normalizar_texto(palabra)
        if palabra_normalizada == self.cancion_actual.titulo_original:
            return True
        else:
                self.jugador.restar_intento()
                return False
    def juego_terminado(self):
        return self.jugador.intentos_restantes <= 0
    def reiniciar(self):
        if self.cancion_actual:
            self.cancion_actual.detener_reproduccion()
        self.tablero = []
        self.jugador.reiniciar_intentos()
        self.seleccionar_cancion()


