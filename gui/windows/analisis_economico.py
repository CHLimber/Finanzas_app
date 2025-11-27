"""
Archivo: gui/windows/analisis_financiero.py
Pestaña de Análisis Financiero - Liquidez - Solvencia
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts

class AnalisisEconomicoTab(ttk.Frame):
    """Pestaña con subpestañas de Análisis Financiero"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.sub_notebook = None
        self.datos_desactualizados = False
        self.label_estado = None
        self.btn_actualizar = None
        
        self.crear_interfaz()
        
        # Suscribirse para marcar como desactualizado
        if hasattr(self.app, 'on_data_change_callbacks'):
            self.app.on_data_change_callbacks.append(self.marcar_desactualizado)
    
    def crear_interfaz(self):
        """Crea la interfaz con subpestañas"""
        
        # Limpiar contenido anterior
        for widget in self.winfo_children():
            widget.destroy()
        
        # Frame superior
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Título
        ttk.Label(
            titulo_frame,
            text="ANÁLISIS FINANCIERO",  # Cambiar según pestaña
            font=Fonts.TITLE
        ).pack(side=tk.LEFT, padx=10)
        
        # Indicador de estado
        self.label_estado = tk.Label(
            titulo_frame,
            text="⚠️ Datos modificados - Clic en Actualizar",
            font=Fonts.NORMAL,
            bg=Colors.WARNING,
            fg="white",
            padx=10,
            pady=5,
            relief="raised"
        )
        if self.datos_desactualizados:
            self.label_estado.pack(side=tk.LEFT, padx=10)
        
        # Botón actualizar
        self.btn_actualizar = tk.Button(
            titulo_frame,
            text="🔄 Actualizar",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.INFO,
            fg="white",
            cursor="hand2",
            command=self.actualizar_contenido
        )
        self.btn_actualizar.pack(side=tk.RIGHT, padx=10)
        
        # Notebook secundario
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Crear subpestañas (adaptar según cada análisis)
        self.crear_subpestana_c1_c2_c3()
        self.crear_subpestana_c4_c5()
        
        # Marcar como actualizado
        self.datos_desactualizados = False
        if self.label_estado:
            self.label_estado.pack_forget()
    
    def marcar_desactualizado(self):
        """Marca que hay datos nuevos"""
        self.datos_desactualizados = True
        if self.label_estado and self.label_estado.winfo_exists():
            self.label_estado.pack(side=tk.LEFT, padx=10)
            if self.btn_actualizar and self.btn_actualizar.winfo_exists():
                self.btn_actualizar.config(bg=Colors.SUCCESS)
                self.after(300, lambda: self.btn_actualizar.config(bg=Colors.INFO))
    
    def actualizar_contenido(self):
        """Actualiza manualmente"""
        try:
            import matplotlib.pyplot as plt
            plt.close('all')
            
            self.crear_interfaz()
            print("✅ Análisis actualizado")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def crear_subpestana_c1_c2_c3(self):
        """Subpestaña B1, B2 y B3"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="C1 - C2 - C3")
        
        content = ttk.Label(
            tab,
            text="C1, C2 y C3\n(Análisis de Liquidez)",
            font=("Arial", 12)
        )
        content.pack(expand=True)
    
    def crear_subpestana_c4_c5(self):
        """Subpestaña B4 y B5"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="C4 - C5")
        
        content = ttk.Label(
            tab,
            text="C4 y C5\n(Análisis de Económico)",
            font=("Arial", 12)
        )
        content.pack(expand=True)