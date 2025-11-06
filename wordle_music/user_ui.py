
      def crear_tablero(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Encabezado
        frame_header = tk.Frame(self.root, bg="#1e1e1e")
        frame_header.pack(pady=10)

        tk.Label(
            frame_header, text=f"🎮 Jugador: {self.juego.jugador.nombre}",
            bg="#1e1e1e", fg="#00ffb3", font=("Arial", 14, "bold")
        ).pack(side="left", padx=20)

        # Contador de intentos
        self.label_intentos = tk.Label(
            frame_header, text=f"❤️ Intentos: {self.juego.jugador.intentos_restantes}/6",
            bg="#1e1e1e", fg="white", font=("Arial", 12, "bold")
        )
        self.label_intentos.pack(side="left", padx=20)

        # Botón reproducir pista
        self.btn_pista = tk.Button(
            self.root, text="🔊 Reproducir Pista",
            command=self.reproducir_pista,
            font=("Arial", 12, "bold"), bg="#6c5ce7", fg="white", cursor="hand2"
        )
        self.btn_pista.pack(pady=5)

        # Tablero
        self.frame_tablero = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_tablero.pack(pady=15)

        longitud = self.juego.inicializar_tablero()
        self.crear_filas(longitud)

        # Campo de entrada
        tk.Label(
            self.root, text="Escribe tu respuesta:",
            bg="#1e1e1e", fg="white", font=("Arial", 11)
        ).pack()

        self.entry = tk.Entry(
            self.root, textvariable=self.intento_actual,
            font=("Arial", 18, "bold"), justify="center", width=20
        )
        self.entry.pack(pady=10)
        self.entry.focus()
        self.entry.bind("<Return>", lambda e: self.enviar_intento())

        # Botón enviar
        tk.Button(
            self.root, text="✅ Enviar Respuesta",
            command=self.enviar_intento,
            font=("Arial", 14, "bold"), bg="#00ffb3", fg="black", cursor="hand2"
        ).pack(pady=10)

        # Teclado virtual
        self.crear_teclado()

        # Info adicional
        tk.Label(
            self.root, text="💡 Los espacios y acentos no importan",
            bg="#1e1e1e", fg="#888888", font=("Arial", 9, "italic")
        ).pack(pady=5)

    def crear_filas(self, longitud):
        self.cuadros.clear()
        for i in range(6):
            fila = []
            for j in range(longitud):
                lbl = tk.Label(
                    self.frame_tablero, text="", width=4, height=2,
                    font=("Consolas", 20, "bold"),
                    relief="solid", borderwidth=2,
                    bg="#2e2e2e", fg="white"
                )
                lbl.grid(row=i, column=j, padx=3, pady=3)
                fila.append(lbl)
            self.cuadros.append(fila)

    # === Teclado virtual ===
    def crear_teclado(self):
        self.frame_teclado = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_teclado.pack(pady=10)

        filas = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

        for fila in filas:
            fila_frame = tk.Frame(self.frame_teclado, bg="#1e1e1e")
            fila_frame.pack()
            for letra in fila:
                btn = tk.Button(
                    fila_frame, text=letra, width=4, height=2,
                    font=("Consolas", 11, "bold"),
                    bg="#3e3e3e", fg="white",
                    command=lambda l=letra: self.agregar_letra(l),
                    cursor="hand2"
                )
                btn.pack(side="left", padx=2, pady=2)
                self.botones_teclas[letra] = btn

    def agregar_letra(self, letra):
        """Agrega letra al campo."""
        actual = self.intento_actual.get().upper()
        if len(actual) < len(self.juego.cancion_actual.titulo_original):
            self.intento_actual.set(actual + letra)

    def reproducir_pista(self):
        """Reproduce el fragmento actual."""
        if self.juego and self.juego.cancion_actual:
            duracion = self.juego.obtener_duracion_fragmento()
            self.juego.cancion_actual.reproducir_fragmento(0, duracion)

            # Feedback visual
            self.btn_pista.config(bg="#a29bfe", text="🔊 Reproduciendo...")
            self.root.after(int(duracion), lambda: self.btn_pista.config(
                bg="#6c5ce7", text="🔊 Reproducir Pista"
            ))

    # === Enviar intento ===
    def enviar_intento(self):
        intento = self.intento_actual.get().strip().upper()
        self.intento_actual.set("")

        if not intento:
            messagebox.showwarning("Aviso", "Escribe una respuesta antes de enviar.")
            return

        longitud = len(self.juego.cancion_actual.titulo_original)
        if len(intento) != longitud:
            messagebox.showwarning(
                "Aviso",
                f"La respuesta debe tener {longitud} letras.\n"
                f"Has escrito {len(intento)} letras."
            )
            return

        resultado = self.juego.cancion_actual.comparar_letras(intento)
        fila_idx = len(self.juego.tablero)

        # Actualizar tablero con animación
        for j, letra in enumerate(resultado):
            cuadro = self.cuadros[fila_idx][j]
            cuadro.config(text=letra.caracter)

            if letra.estado == "correcta":
                cuadro.config(bg="#00ff66", fg="black")
            elif letra.estado == "contenida":
                cuadro.config(bg="#ffd700", fg="black")
            else:
                cuadro.config(bg="#555555", fg="white")

        # Actualizar teclado
        for letra in resultado:
            boton = self.botones_teclas.get(letra.caracter)
            if boton:
                color_actual = boton.cget("bg")
                if letra.estado == "correcta":
                    boton.config(bg="#00ff66", fg="black")
                elif letra.estado == "contenida" and color_actual != "#00ff66":
                    boton.config(bg="#ffd700", fg="black")
                elif letra.estado == "incorrecta" and color_actual not in ("#00ff66", "#ffd700"):
                    boton.config(bg="#555555", fg="white")

        correcto = self.juego.validar_intento(intento)

        # Actualizar contador de intentos
        if self.label_intentos:
            self.label_intentos.config(text=f"❤️ Intentos: {self.juego.jugador.intentos_restantes}/6")

        self.root.update_idletasks()

        if correcto:
            self.juego.cancion_actual.detener_reproduccion()
            messagebox.showinfo(
                "¡CORRECTO! 🎉",
                f"🎉 ¡Felicidades {self.juego.jugador.nombre}!\n\n"
                f"Has adivinado la canción:\n"
                f"🎵 {self.juego.cancion_actual.titulo_con_espacios}\n\n"
                f"¡Ahora escucha la canción completa!"
            )
            self.juego.cancion_actual.reproducir_completa()
            self.root.after(2000, self.reiniciar_juego)
        elif self.juego.juego_terminado():
            self.juego.cancion_actual.detener_reproduccion()
            messagebox.showinfo(
                "Fin del juego 😢",
                f"😢 ¡Ups! Te quedaste sin intentos.\n\n"
                f"La canción era:\n"
                f"🎵 {self.juego.cancion_actual.titulo_con_espacios}\n\n"
                f"¡Escúchala ahora!"
            )
            self.juego.cancion_actual.reproducir_completa()
            self.root.after(2000, self.reiniciar_juego)
        else:
            # Reproducir siguiente fragmento (más largo)
            self.root.after(500, self.reproducir_pista)

    # === Reinicio limpio ===
    def reiniciar_juego(self):
        if self.juego and self.juego.cancion_actual:
            self.juego.cancion_actual.detener_reproduccion()

        if messagebox.askyesno("Nueva Ronda", "¿Quieres jugar otra ronda? 🎮"):
            self.juego.reiniciar()
            self.crear_tablero()
            self.root.after(500, self.reproducir_pista)
        else:
            self.cerrar_aplicacion()

    def cerrar_aplicacion(self):
        """Detiene todo audio antes de cerrar."""
        if self.juego and self.juego.cancion_actual:
            self.juego.cancion_actual.detener_reproduccion()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WordleMusicalGUI(root)
    root.mainloop()
