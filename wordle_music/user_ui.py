import tkinter as tk
from tkinter import messagebox
from wordle_music import WordleMusical, Jugador, Cancion
import os


class WordleMusicalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Wordle Musical 🎵")
        self.root.geometry("700x850")
        self.root.configure(bg="#1e1e1e")

        self.juego = None
        self.cuadros = []
        self.intento_actual = tk.StringVar()
        self.botones_teclas = {}
        self.label_intentos = None
        self.btn_pista = None

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        self.crear_interfaz_inicial()

    def crear_interfaz_inicial(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root, text="🎵 WORDLE MUSICAL 🎵",
            bg="#1e1e1e", fg="#00ffb3", font=("Arial", 26, "bold")
        ).pack(pady=30)

        tk.Label(
            self.root, text="Adivina el nombre de la canción\nEscucha el fragmento y adivina el título",
            bg="#1e1e1e", fg="white", font=("Arial", 12), justify="center"
        ).pack()

        tk.Label(
            self.root, text="Ingresa tu nombre:",
            bg="#1e1e1e", fg="white", font=("Arial", 14)
        ).pack(pady=(20, 5))

        self.entrada_nombre = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.entrada_nombre.pack(pady=10)
        self.entrada_nombre.focus()
        self.entrada_nombre.bind("<Return>", lambda e: self.iniciar_juego())

        tk.Button(
            self.root, text="🎮 Comenzar Juego 🎧",
            font=("Arial", 14, "bold"), bg="#00ffb3", fg="black",
            command=self.iniciar_juego, cursor="hand2"
        ).pack(pady=20)

        tk.Label(
            self.root, text="💡 Los fragmentos se harán más largos con cada intento",
            bg="#1e1e1e", fg="#888888", font=("Arial", 10, "italic")
        ).pack(pady=10)

    def iniciar_juego(self):
        nombre = self.entrada_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Aviso", "Por favor, ingresa tu nombre.")
            return

        jugador = Jugador(nombre)
        canciones = self.cargar_canciones()

        if not canciones:
            return

        self.juego = WordleMusical(jugador, canciones)
        self.juego.seleccionar_cancion()
        self.crear_tablero()

        self.root.after(500, self.reproducir_pista)
