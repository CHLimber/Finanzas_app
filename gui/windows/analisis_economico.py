"""
Archivo: gui/windows/analisis_financiero.py
Pestaña de Análisis Financiero - Liquidez - Solvencia
"""

import tkinter as tk
from tkinter import ttk

class AnalisisEconomicoTab(ttk.Frame):
    """Pestaña con subpestañas de Análisis Financiero"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz con subpestañas"""
        
        # Título superior
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            titulo_frame,
            text="ANÁLISIS ECONÓMICO - RENTABILIDAD ",
            font=("Arial", 16, "bold")
        ).pack()
        
        # Notebook secundario
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Subpestañas
        self.crear_subpestana_c1_c2_c3()
        self.crear_subpestana_c4_c5()
    
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