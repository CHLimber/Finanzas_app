"""
Archivo: gui/windows/graficos.py
Pestaña de Gráficos (sin subpestañas)
"""

import tkinter as tk
from tkinter import ttk

class GraficosTab(ttk.Frame):
    """Pestaña de Gráficos sin subpestañas"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de gráficos"""
        
        # Título
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, padx=10, pady=20)
        
        ttk.Label(
            titulo_frame,
            text="GRÁFICOS Y VISUALIZACIONES",
            font=("Arial", 18, "bold")
        ).pack()
        
        # Frame central
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Grid de botones para diferentes gráficos
        buttons = [
            ("📊 Gráfico de Barras", self.grafico_barras),
            ("📈 Gráfico de Líneas", self.grafico_lineas),
            ("🥧 Gráfico Circular", self.grafico_circular),
            ("📉 Evolución Temporal", self.grafico_evolucion),
            ("🔄 Comparativas", self.grafico_comparativas),
            ("📌 Ratios Financieros", self.grafico_ratios)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(
                content_frame,
                text=text,
                command=command
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew", ipadx=20, ipady=15)
        
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
    
    def grafico_barras(self):
        """Placeholder para gráfico de barras"""
        print("Gráfico de barras")
    
    def grafico_lineas(self):
        """Placeholder para gráfico de líneas"""
        print("Gráfico de líneas")
    
    def grafico_circular(self):
        """Placeholder para gráfico circular"""
        print("Gráfico circular")
    
    def grafico_evolucion(self):
        """Placeholder para evolución temporal"""
        print("Evolución temporal")
    
    def grafico_comparativas(self):
        """Placeholder para comparativas"""
        print("Comparativas")
    
    def grafico_ratios(self):
        """Placeholder para ratios"""
        print("Ratios financieros")