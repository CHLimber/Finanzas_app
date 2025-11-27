"""
Archivo: gui/windows/analisis_financiero.py
Pestaña de Análisis Financiero - Liquidez - Solvencia
"""

import tkinter as tk
from tkinter import ttk

class AnalisisFinancieroTab(ttk.Frame):
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
            text="ANÁLISIS FINANCIERO - LIQUIDEZ - SOLVENCIA",
            font=("Arial", 16, "bold")
        ).pack()
        
        # Notebook secundario
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Subpestañas
        self.crear_subpestana_b1_b2_b3()
        self.crear_subpestana_b4_b5()
    
    def crear_subpestana_b1_b2_b3(self):
        """Subpestaña B1, B2 y B3"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="B1 - B2 - B3")
        
        content = ttk.Label(
            tab,
            text="B1, B2 y B3\n(Análisis de Liquidez)",
            font=("Arial", 12)
        )
        content.pack(expand=True)
    
    def crear_subpestana_b4_b5(self):
        """Subpestaña B4 y B5"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="B4 - B5")
        
        content = ttk.Label(
            tab,
            text="B4 y B5\n(Análisis de Solvencia)",
            font=("Arial", 12)
        )
        content.pack(expand=True)