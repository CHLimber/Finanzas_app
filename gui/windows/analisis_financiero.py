"""
Archivo: gui/windows/analisis_financiero.py
Pestaña principal de Análisis Financiero con 5 sub-pestañas separadas
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts

# Importar las pestañas individuales
from gui.windows.b1_liquidez import B1LiquidezTab
from gui.windows.b2_solvencia import B2SolvenciaTab
from gui.windows.b3_comparativa import B3ComparativaTab
from gui.windows.b4_estructura import B4EstructuraTab
from gui.windows.b5_estres import B5EstresTab


class AnalisisFinancieroTab(ttk.Frame):
    """Pestaña principal de Análisis Financiero"""
    
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
            text="ANÁLISIS FINANCIERO",
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
        
        # Notebook para las 5 pestañas
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Crear las 5 pestañas separadas
        self.crear_pestanas()
        
        # Marcar como actualizado
        self.datos_desactualizados = False
        if self.label_estado:
            self.label_estado.pack_forget()
    
    def crear_pestanas(self):
        """Crea las 5 pestañas del análisis financiero"""
        
        # B1 - Ratios de Liquidez
        b1_tab = B1LiquidezTab(self.sub_notebook, self.app)
        self.sub_notebook.add(b1_tab, text="B1 - Liquidez")
        
        # B2 - Ratios de Solvencia
        b2_tab = B2SolvenciaTab(self.sub_notebook, self.app)
        self.sub_notebook.add(b2_tab, text="B2 - Solvencia")
        
        # B3 - Placeholder (implementar después)
        b3_tab = B3ComparativaTab(self.sub_notebook, self.app)
        self.sub_notebook.add(b3_tab, text="B3 - Comparativa")
        
        # B4 - Placeholder (implementar después)
        b4_tab = B4EstructuraTab(self.sub_notebook, self.app)
        self.sub_notebook.add(b4_tab, text="B4 - Estructura")
        
        # B5 - Placeholder (implementar después)
        b5_tab = B5EstresTab(self.sub_notebook, self.app)
        self.sub_notebook.add(b5_tab, text="B5 - Estrés Financiero")
    
    def _crear_placeholder(self, nombre):
        """Crea una pestaña placeholder"""
        tab = ttk.Frame(self.sub_notebook)
        ttk.Label(
            tab,
            text=f"{nombre}\n(En desarrollo)",
            font=Fonts.SUBTITLE
        ).pack(expand=True)
        return tab
    
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
            print("✅ Análisis Financiero actualizado")
        except Exception as e:
            print(f"❌ Error: {e}")