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





