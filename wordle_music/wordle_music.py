import pygame
import random
import unicodedata
from pydub import AudioSegment
from io import BytesIO

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def normalizar_texto(texto):
    texto = texto.upper().replace(" ", "")
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    texto = ''.join(c for c in texto if c.isalnum())
    return texto

class Letra:
    def __init__(self, caracter: str, posicion: int):
        self.caracter = caracter.upper()
        self.posicion = posicion
        self.estado = "incorrecta"

    def __repr__(self):
        return f"{self.caracter}({self.estado})"

class Cancion:
    def __init__(self, titulo_original: str, ruta_archivo: str):
        self.titulo_con_espacios = titulo_original.upper()
        self.titulo_original = normalizar_texto(titulo_original)
        self.ruta_archivo = ruta_archivo

        self.audio = AudioSegment.from_file(ruta_archivo, format="mp3")

        self.audio = self.audio.set_channels(2).set_frame_rate(44100).set_sample_width(2)

    def comparar_letras(self, palabra: str):
        palabra = normalizar_texto(palabra)
        resultado = []
        for i, caracter in enumerate(palabra):
            letra = Letra(caracter, i)
            if i < len(self.titulo_original):
                if caracter == self.titulo_original[i]:
                    letra.estado = "correcta"
                elif caracter in self.titulo_original:
                    letra.estado = "contenida"
            resultado.append(letra)
        return resultado

    def reproducir_fragmento(self, inicio_ms: int, duracion_ms: int):
        try:
            pygame.mixer.music.stop()

            duracion_total = len(self.audio)
            if inicio_ms >= duracion_total:
                inicio_ms = 0

            fin_ms = min(inicio_ms + duracion_ms, duracion_total)
            fragmento = self.audio[inicio_ms:fin_ms]

            if len(fragmento) < 500:
                print("Fragmento demasiado corto.")
                return

            buffer = BytesIO()
            fragmento.export(buffer, format="wav")
            buffer.seek(0)

            pygame.mixer.music.load(buffer, 'wav')
            pygame.mixer.music.play()

        except Exception as e:
            print(f"Error al reproducir fragmento: {e}")

    def reproducir_completa(self):
        try:
            pygame.mixer.music.stop()

            buffer = BytesIO()
            self.audio.export(buffer, format="wav")
            buffer.seek(0)

            pygame.mixer.music.load(buffer, 'wav')
            pygame.mixer.music.play()

        except Exception as e:
            print(f"Error al reproducir canción: {e}")

    def detener_reproduccion(self):
        try:
            pygame.mixer.music.stop()
        except:
            pass

    def esta_reproduciendo(self):
        return pygame.mixer.music.get_busy()

class Jugador:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.intentos_restantes = 6
        self.letras_usadas = set()

    def registrar_letras(self, intento: str):
        for c in normalizar_texto(intento):
            self.letras_usadas.add(c)

    def restar_intento(self):
        self.intentos_restantes -= 1

    def reiniciar_intentos(self):
        self.intentos_restantes = 6
        self.letras_usadas.clear()

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


