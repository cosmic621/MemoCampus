import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import json
import os

class MemoCampus:
    def __init__(self, root):
        self.root = root
        self.root.title("MemoCampus - Gestor de Entregas")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1a1a2e")

        self.entregas = []
        self.postits = []
        self.drag_data = {"x": 0, "y": 0, "items": None}
        self.archivo_datos = "memocampus_datos.json"

        self.cargar_datos()
        self.crear_interfaz()
        self.actualizar_vista()
        self.verificar_alertas()

    def crear_interfaz(self):
        
        panel_izq = tk.Frame(self.root, bg="#16213e", width=350)
        panel_izq.pack(side="left", fill="both", padx=0, pady=0)
        panel_izq.pack_propagate(False)

       
        titulo_panel = tk.Label(panel_izq, text="📝 Nueva Entrega", 
                               font=("Segoe UI", 18, "bold"), 
                               bg="#16213e", fg="#00d9ff")
        titulo_panel.pack(pady=20)

        
        form_frame = tk.Frame(panel_izq, bg="#16213e")
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        
        tk.Label(form_frame, text="Título", font=("Segoe UI", 11, "bold"),
                bg="#16213e", fg="#ffffff").pack(anchor="w", pady=(10, 5))
        self.titulo_entry = tk.Entry(form_frame, font=("Segoe UI", 11),
                                     bg="#0f3460", fg="white", 
                                     insertbackground="white",
                                     relief="flat", bd=0)
        self.titulo_entry.pack(fill="x", ipady=8)

        
        tk.Label(form_frame, text="Fecha de Entrega", font=("Segoe UI", 11, "bold"),
                bg="#16213e", fg="#ffffff").pack(anchor="w", pady=(15, 5))
        self.fecha_entry = DateEntry(form_frame, width=30, 
                                     background="#00d9ff", 
                                     foreground="white", 
                                     borderwidth=0,
                                     font=("Segoe UI", 10),
                                     date_pattern='dd/mm/yyyy')
        self.fecha_entry.pack(fill="x", ipady=5)

        
        tk.Label(form_frame, text="Hora (HH:MM)", font=("Segoe UI", 11, "bold"),
                bg="#16213e", fg="#ffffff").pack(anchor="w", pady=(15, 5))
        self.hora_entry = tk.Entry(form_frame, font=("Segoe UI", 11),
                                   bg="#0f3460", fg="white",
                                   insertbackground="white",
                                   relief="flat", bd=0)
        self.hora_entry.pack(fill="x", ipady=8)
        self.hora_entry.insert(0, "23:59")

        
        tk.Label(form_frame, text="Nivel de Importancia", font=("Segoe UI", 11, "bold"),
                bg="#16213e", fg="#ffffff").pack(anchor="w", pady=(15, 5))
        
        self.importancia_var = tk.StringVar()
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground="#0f3460", 
                       background="#00d9ff", foreground="white")
        
        self.importancia_combo = ttk.Combobox(form_frame, 
                                             textvariable=self.importancia_var,
                                             state="readonly",
                                             font=("Segoe UI", 10))
        self.importancia_combo['values'] = ("🔴 Alta", "🟠 Media", "🟢 Baja")
        self.importancia_combo.pack(fill="x", ipady=5)
        self.importancia_combo.current(1)

        
        tk.Label(form_frame, text="Descripción de la Tarea", font=("Segoe UI", 11, "bold"),
                bg="#16213e", fg="#ffffff").pack(anchor="w", pady=(15, 5))
        
        desc_frame = tk.Frame(form_frame, bg="#0f3460", bd=0)
        desc_frame.pack(fill="both", expand=True)
        
        self.descripcion_text = tk.Text(desc_frame, font=("Segoe UI", 10),
                                       bg="#0f3460", fg="white",
                                       insertbackground="white",
                                       relief="flat", bd=0,
                                       height=4, wrap="word")
        self.descripcion_text.pack(side="left", fill="both", expand=True)
        
        desc_scrollbar = tk.Scrollbar(desc_frame, command=self.descripcion_text.yview)
        desc_scrollbar.pack(side="right", fill="y")
        self.descripcion_text.config(yscrollcommand=desc_scrollbar.set)

        
        btn_frame = tk.Frame(form_frame, bg="#16213e")
        btn_frame.pack(pady=30)

        btn_agregar = tk.Button(btn_frame, text="➕ Agregar", 
                               command=self.agregar_entrega,
                               font=("Segoe UI", 12, "bold"),
                               bg="#00d9ff", fg="white",
                               activebackground="#00b8d4",
                               relief="flat", bd=0,
                               cursor="hand2",
                               padx=30, pady=10)
        btn_agregar.pack(pady=5, fill="x")

        btn_guardar = tk.Button(btn_frame, text="💾 Guardar Todo", 
                               command=self.guardar_datos,
                               font=("Segoe UI", 11, "bold"),
                               bg="#e94560", fg="white",
                               activebackground="#c73a50",
                               relief="flat", bd=0,
                               cursor="hand2",
                               padx=30, pady=8)
        btn_guardar.pack(pady=5, fill="x")

        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar Seleccionados", 
                                command=self.eliminar_seleccionados,
                                font=("Segoe UI", 11, "bold"),
                                bg="#533483", fg="white",
                                activebackground="#432870",
                                relief="flat", bd=0,
                                cursor="hand2",
                                padx=30, pady=8)
        btn_eliminar.pack(pady=5, fill="x")

        btn_eliminar_completadas = tk.Button(btn_frame, text="✓ Eliminar Completadas", 
                                            command=self.eliminar_completadas,
                                            font=("Segoe UI", 11, "bold"),
                                            bg="#7f8c8d", fg="white",
                                            activebackground="#6c7a7b",
                                            relief="flat", bd=0,
                                            cursor="hand2",
                                            padx=30, pady=8)
        btn_eliminar_completadas.pack(pady=5, fill="x")

       
        panel_der = tk.Frame(self.root, bg="#1a1a2e")
        panel_der.pack(side="right", fill="both", expand=True)

        
        self.notebook = ttk.Notebook(panel_der)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        
        style.configure('TNotebook', background="#1a1a2e", borderwidth=0)
        style.configure('TNotebook.Tab', background="#16213e", 
                       foreground="white", padding=[20, 10],
                       font=("Segoe UI", 10, "bold"))
        style.map('TNotebook.Tab', background=[('selected', '#00d9ff')],
                 foreground=[('selected', 'white')])

        
        self.tab_postits = tk.Frame(self.notebook, bg="#0f3460")
        self.notebook.add(self.tab_postits, text="📌 Post-its")

        
        canvas_frame = tk.Frame(self.tab_postits, bg="#0f3460")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar_y = tk.Scrollbar(canvas_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(canvas_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(canvas_frame, bg="#0f3460", 
                               highlightthickness=0,
                               yscrollcommand=scrollbar_y.set,
                               xscrollcommand=scrollbar_x.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar_y.config(command=self.canvas.yview)
        scrollbar_x.config(command=self.canvas.xview)

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        
        self.canvas.tag_bind("postit", "<ButtonPress-1>", self.iniciar_drag)
        self.canvas.tag_bind("postit", "<ButtonRelease-1>", self.finalizar_drag)
        self.canvas.tag_bind("postit", "<B1-Motion>", self.mover_postit)
        self.canvas.tag_bind("postit", "<Double-Button-1>", self.mostrar_detalle_postit)

        
        self.tab_lista = tk.Frame(self.notebook, bg="#0f3460")
        self.notebook.add(self.tab_lista, text="📋 Lista de Entregas")

        
        tree_frame = tk.Frame(self.tab_lista, bg="#0f3460")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        style.configure("Treeview", background="#16213e", 
                       foreground="white", fieldbackground="#16213e",
                       font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#00d9ff", 
                       foreground="white", font=("Segoe UI", 11, "bold"))
        style.map('Treeview', background=[('selected', '#00d9ff')])

        scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_tree.pack(side="right", fill="y")

        self.tree = ttk.Treeview(tree_frame, 
                                columns=("Sel", "Título", "Fecha", "Hora", "Importancia", "Estado"),
                                show="headings", 
                                height=20,
                                yscrollcommand=scrollbar_tree.set)
        
        scrollbar_tree.config(command=self.tree.yview)

        self.tree.heading("Sel", text="☑")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Importancia", text="Importancia")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("Sel", width=50, anchor="center")
        self.tree.column("Título", width=250)
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Hora", width=80, anchor="center")
        self.tree.column("Importancia", width=100, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Button-1>", self.toggle_seleccion)
        self.tree.bind("<Double-Button-1>", self.mostrar_detalle_tree)

    def agregar_entrega(self):
        titulo = self.titulo_entry.get().strip()
        fecha = self.fecha_entry.get_date()
        hora = self.hora_entry.get().strip()
        importancia = self.importancia_var.get()
        descripcion = self.descripcion_text.get("1.0", "end-1c").strip()

        if not titulo or not hora:
            messagebox.showwarning("Campos incompletos", 
                                  "Por favor ingresa un título y una hora.")
            return

        try:
            hora_valida = datetime.datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            messagebox.showerror("Formato inválido", 
                               "La hora debe estar en formato HH:MM (ejemplo: 14:30)")
            return

        entrega = {
            "titulo": titulo,
            "fecha": fecha,
            "hora": hora_valida,
            "importancia": importancia,
            "descripcion": descripcion,
            "completada": False,
            "seleccionada": False
        }
        self.entregas.append(entrega)

        self.titulo_entry.delete(0, tk.END)
        self.hora_entry.delete(0, tk.END)
        self.hora_entry.insert(0, "23:59")
        self.descripcion_text.delete("1.0", tk.END)

        self.actualizar_vista()
        self.mostrar_notificacion(f"✅ Entrega agregada:\n{titulo}", "#00d9ff")

    def actualizar_vista(self):
        
        self.canvas.delete("all")
        self.postits.clear()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        
        for idx, entrega in enumerate(self.entregas):
            self.crear_postit(entrega, idx)
            
            estado = "✓ Completa" if entrega["completada"] else "⏳ Pendiente"
            sel = "☑" if entrega.get("seleccionada", False) else "☐"
            
            self.tree.insert("", "end", values=(
                sel,
                entrega["titulo"],
                entrega["fecha"].strftime("%d/%m/%Y"),
                entrega["hora"].strftime("%H:%M"),
                entrega["importancia"],
                estado
            ))

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def crear_postit(self, entrega, idx):
        colores = {
            "🔴 Alta": "#ff6b6b",
            "🟠 Media": "#ffa500",
            "🟢 Baja": "#51cf66"
        }
        color = colores.get(entrega["importancia"], "#ffa500")

        x = 30 + (idx % 4) * 180
        y = 30 + (idx // 4) * 180

        
        shadow = self.canvas.create_rectangle(x+5, y+5, x+165, y+165,
                                             fill="#000000", outline="",
                                             tags=("postit", f"postit_{idx}"))

        
        rect = self.canvas.create_rectangle(x, y, x+160, y+160,
                                           fill="#fff9c4", outline="#f9a825",
                                           width=3, tags=("postit", f"postit_{idx}"))

        
        titulo_corto = entrega["titulo"][:20] + "..." if len(entrega["titulo"]) > 20 else entrega["titulo"]
        text = self.canvas.create_text(x+80, y+30, text=titulo_corto,
                                      tags=("postit", f"postit_{idx}"),
                                      font=("Segoe UI", 11, "bold"),
                                      width=140)

        
        fecha_texto = f"📅 {entrega['fecha'].strftime('%d/%m/%Y')}"
        fecha_label = self.canvas.create_text(x+80, y+70, text=fecha_texto,
                                             tags=("postit", f"postit_{idx}"),
                                             font=("Segoe UI", 9))

        
        hora_texto = f"🕐 {entrega['hora'].strftime('%H:%M')}"
        hora_label = self.canvas.create_text(x+80, y+95, text=hora_texto,
                                            tags=("postit", f"postit_{idx}"),
                                            font=("Segoe UI", 9))

        
        circ = self.canvas.create_oval(x+10, y+10, x+30, y+30,
                                       fill=color, outline="white", width=2,
                                       tags=("postit", f"postit_{idx}"))

        
        if entrega["completada"]:
            check = self.canvas.create_text(x+80, y+130, text="✓ COMPLETA",
                                          tags=("postit", f"postit_{idx}"),
                                          font=("Segoe UI", 10, "bold"),
                                          fill="#2ecc71")

        self.postits.append({
            "items": [shadow, rect, text, fecha_label, hora_label, circ],
            "entrega": entrega,
            "index": idx
        })

    def iniciar_drag(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        for postit in self.postits:
            if item in postit["items"]:
                self.drag_data["items"] = postit["items"]
                break
        
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def mover_postit(self, event):
        if self.drag_data["items"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            for item in self.drag_data["items"]:
                self.canvas.move(item, dx, dy)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def finalizar_drag(self, event):
        self.drag_data["items"] = None

    def mostrar_detalle_postit(self, event):
        item = self.canvas.find_closest(event.x, event.y)[0]
        for postit in self.postits:
            if item in postit["items"]:
                self.mostrar_popup_detalle(postit["entrega"], postit["index"])
                break

    def mostrar_detalle_tree(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            if item:
                idx = self.tree.index(item)
                if idx < len(self.entregas):
                    self.mostrar_popup_detalle(self.entregas[idx], idx)

    def mostrar_popup_detalle(self, entrega, idx):
        popup = tk.Toplevel(self.root)
        popup.title("Detalles de la Entrega")
        popup.geometry("500x550")
        popup.configure(bg="#16213e")
        popup.resizable(False, False)
        
        
        popup.transient(self.root)
        popup.grab_set()

        
        tk.Label(popup, text="📋 Detalles de la Entrega",
                font=("Segoe UI", 16, "bold"),
                bg="#16213e", fg="#00d9ff").pack(pady=20)

        
        detalle_frame = tk.Frame(popup, bg="#0f3460", relief="raised", bd=2)
        detalle_frame.pack(padx=30, pady=10, fill="both", expand=True)

        
        info = [
            ("📌 Título:", entrega["titulo"]),
            ("📅 Fecha:", entrega["fecha"].strftime("%d/%m/%Y")),
            ("🕐 Hora:", entrega["hora"].strftime("%H:%M")),
            ("⚠️ Importancia:", entrega["importancia"]),
            ("📊 Estado:", "✓ Completada" if entrega["completada"] else "⏳ Pendiente")
        ]

        for i, (label, valor) in enumerate(info):
            frame = tk.Frame(detalle_frame, bg="#0f3460")
            frame.pack(fill="x", padx=20, pady=8)

            tk.Label(frame, text=label, font=("Segoe UI", 11, "bold"),
                    bg="#0f3460", fg="#ffffff").pack(anchor="w")
            tk.Label(frame, text=valor, font=("Segoe UI", 11),
                    bg="#0f3460", fg="#cccccc").pack(anchor="w", padx=20)

        
        if entrega.get("descripcion"):
            desc_container = tk.Frame(detalle_frame, bg="#0f3460")
            desc_container.pack(fill="both", expand=True, padx=20, pady=8)
            
            tk.Label(desc_container, text="📝 Descripción:", font=("Segoe UI", 11, "bold"),
                    bg="#0f3460", fg="#ffffff").pack(anchor="w")
            
            desc_frame = tk.Frame(desc_container, bg="#16213e", relief="sunken", bd=1)
            desc_frame.pack(fill="both", expand=True, padx=20, pady=5)
            
            desc_text = tk.Text(desc_frame, font=("Segoe UI", 10),
                               bg="#16213e", fg="#cccccc",
                               wrap="word", height=6, relief="flat")
            desc_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            desc_text.insert("1.0", entrega["descripcion"])
            desc_text.config(state="disabled")
            
            desc_scroll = tk.Scrollbar(desc_frame, command=desc_text.yview)
            desc_scroll.pack(side="right", fill="y")
            desc_text.config(yscrollcommand=desc_scroll.set)

        # Botones
        btn_frame = tk.Frame(popup, bg="#16213e")
        btn_frame.pack(pady=20)

        if not entrega["completada"]:
            btn_completar = tk.Button(btn_frame, text="✓ Marcar como Completa",
                                     command=lambda: self.marcar_completa(idx, popup),
                                     font=("Segoe UI", 10, "bold"),
                                     bg="#2ecc71", fg="white",
                                     relief="flat", padx=20, pady=8,
                                     cursor="hand2")
            btn_completar.pack(side="left", padx=5)

        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar",
                                command=lambda: self.eliminar_una(idx, popup),
                                font=("Segoe UI", 10, "bold"),
                                bg="#e74c3c", fg="white",
                                relief="flat", padx=20, pady=8,
                                cursor="hand2")
        btn_eliminar.pack(side="left", padx=5)

        btn_cerrar = tk.Button(btn_frame, text="Cerrar",
                              command=popup.destroy,
                              font=("Segoe UI", 10),
                              bg="#95a5a6", fg="white",
                              relief="flat", padx=20, pady=8,
                              cursor="hand2")
        btn_cerrar.pack(side="left", padx=5)

    def marcar_completa(self, idx, popup):
        if idx < len(self.entregas):
            self.entregas[idx]["completada"] = True
            self.actualizar_vista()
            popup.destroy()
            self.mostrar_notificacion("✓ Entrega marcada como completa", "#2ecc71")

    def eliminar_una(self, idx, popup):
        if idx < len(self.entregas):
            titulo = self.entregas[idx]["titulo"]
            self.entregas.pop(idx)
            self.actualizar_vista()
            popup.destroy()
            self.mostrar_notificacion(f"🗑️ Eliminada:\n{titulo}", "#e74c3c")

    def toggle_seleccion(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#1":  # Columna de selección
                item = self.tree.identify_row(event.y)
                if item:
                    idx = self.tree.index(item)
                    if idx < len(self.entregas):
                        self.entregas[idx]["seleccionada"] = not self.entregas[idx].get("seleccionada", False)
                        self.actualizar_vista()

    def eliminar_seleccionados(self):
        seleccionados = [e for e in self.entregas if e.get("seleccionada", False)]
        
        if not seleccionados:
            messagebox.showinfo("Sin selección", 
                              "No hay entregas seleccionadas para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar eliminación",
                                       f"¿Eliminar {len(seleccionados)} entrega(s) seleccionada(s)?")
        
        if respuesta:
            self.entregas = [e for e in self.entregas if not e.get("seleccionada", False)]
            self.actualizar_vista()
            self.mostrar_notificacion(f"🗑️ {len(seleccionados)} entrega(s) eliminada(s)", "#e74c3c")

    def eliminar_completadas(self):
        completadas = [e for e in self.entregas if e["completada"]]
        
        if not completadas:
            messagebox.showinfo("Sin completadas", 
                              "No hay entregas completadas para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar eliminación",
                                       f"¿Eliminar {len(completadas)} entrega(s) completada(s)?")
        
        if respuesta:
            self.entregas = [e for e in self.entregas if not e["completada"]]
            self.actualizar_vista()
            self.mostrar_notificacion(f"✓ {len(completadas)} completada(s) eliminada(s)", "#2ecc71")

    def guardar_datos(self):
        try:
            datos = []
            for entrega in self.entregas:
                datos.append({
                    "titulo": entrega["titulo"],
                    "fecha": entrega["fecha"].strftime("%Y-%m-%d"),
                    "hora": entrega["hora"].strftime("%H:%M"),
                    "importancia": entrega["importancia"],
                    "descripcion": entrega.get("descripcion", ""),
                    "completada": entrega["completada"]
                })
            
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            self.mostrar_notificacion("💾 Datos guardados correctamente", "#2ecc71")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                for dato in datos:
                    entrega = {
                        "titulo": dato["titulo"],
                        "fecha": datetime.datetime.strptime(dato["fecha"], "%Y-%m-%d").date(),
                        "hora": datetime.datetime.strptime(dato["hora"], "%H:%M").time(),
                        "importancia": dato["importancia"],
                        "descripcion": dato.get("descripcion", ""),
                        "completada": dato["completada"],
                        "seleccionada": False
                    }
                    self.entregas.append(entrega)
            except Exception as e:
                print(f"Error al cargar datos: {e}")

    def mostrar_notificacion(self, mensaje, color="#00d9ff"):
        noti = tk.Toplevel(self.root)
        noti.overrideredirect(True)
        noti.attributes("-topmost", True)
        
        
        noti.configure(bg="#000000")
        
        ancho, alto = 350, 120
        x = self.root.winfo_screenwidth() - ancho - 30
        y = self.root.winfo_screenheight() - alto - 80
        noti.geometry(f"{ancho}x{alto}+{x}+{y}")

        
        main_frame = tk.Frame(noti, bg=color, bd=0)
        main_frame.place(x=3, y=3, width=ancho-6, height=alto-6)

        
        inner_frame = tk.Frame(main_frame, bg="#1a1a2e", bd=0)
        inner_frame.place(x=4, y=4, width=ancho-14, height=alto-14)

        
        top_bar = tk.Frame(inner_frame, bg=color, height=6)
        top_bar.pack(fill="x")

        
        content_frame = tk.Frame(inner_frame, bg="#1a1a2e")
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)

        
        iconos = {
            "#00d9ff": "ℹ️",
            "#2ecc71": "✅",
            "#e74c3c": "🗑️",
            "#ffa500": "⚠️"
        }
        icono = iconos.get(color, "📢")

        
        msg_frame = tk.Frame(content_frame, bg="#1a1a2e")
        msg_frame.pack(expand=True)

        tk.Label(msg_frame, text=icono, 
                font=("Segoe UI", 24),
                bg="#1a1a2e").pack(side="left", padx=(0, 15))

        tk.Label(msg_frame, text=mensaje, bg="#1a1a2e", fg="white",
                wraplength=250, justify="left",
                font=("Segoe UI", 11)).pack(side="left")

        
        progress_canvas = tk.Canvas(inner_frame, bg="#1a1a2e", 
                                    height=4, highlightthickness=0)
        progress_canvas.pack(fill="x", side="bottom")

        progress_bar = progress_canvas.create_rectangle(0, 0, ancho-14, 4, 
                                                        fill=color, outline="")

        
        x_final = x
        x_inicial = self.root.winfo_screenwidth()
        pasos = 20
        
        def animar_entrada(paso=0):
            if paso < pasos:
                x_actual = x_inicial - ((x_inicial - x_final) * paso / pasos)
                noti.geometry(f"{ancho}x{alto}+{int(x_actual)}+{y}")
                noti.after(10, lambda: animar_entrada(paso + 1))
        
        animar_entrada()

        
        duracion = 3000  
        pasos_progress = 60
        
        def actualizar_progress(paso=0):
            if paso < pasos_progress:
                ancho_actual = (ancho - 14) * (1 - paso / pasos_progress)
                progress_canvas.coords(progress_bar, 0, 0, ancho_actual, 4)
                noti.after(duracion // pasos_progress, 
                          lambda: actualizar_progress(paso + 1))
            else:
                animar_salida()
        
        
        def animar_salida(paso=0):
            if paso < pasos:
                x_actual = x_final + ((self.root.winfo_screenwidth() - x_final) * paso / pasos)
                noti.geometry(f"{ancho}x{alto}+{int(x_actual)}+{y}")
                noti.after(10, lambda: animar_salida(paso + 1))
            else:
                noti.destroy()
        
        noti.after(100, actualizar_progress)

        
        def cerrar(e):
            animar_salida()
        
        noti.bind("<Button-1>", cerrar)
        for widget in [main_frame, inner_frame, content_frame, msg_frame]:
            widget.bind("<Button-1>", cerrar)

    def verificar_alertas(self):
        ahora = datetime.datetime.now()
        for entrega in self.entregas:
            if not entrega["completada"]:
                fecha_hora = datetime.datetime.combine(entrega["fecha"], entrega["hora"])
                tiempo_restante = (fecha_hora - ahora).total_seconds()
                
                if 0 <= tiempo_restante <= 3600:
                    minutos = int(tiempo_restante / 60)
                    self.mostrar_notificacion(
                        f"⚠️ ¡Entrega pronta!\n{entrega['titulo']}\nFaltan {minutos} minutos",
                        "#e74c3c"
                    )
                    entrega["completada"] = True
                    self.actualizar_vista()
        
        self.root.after(60000, self.verificar_alertas)

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoCampus(root)
    root.mainloop()