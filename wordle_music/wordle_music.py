import pygame
import random
import unicodedata
from pydub import AudioSegment
from io import BytesIO


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



