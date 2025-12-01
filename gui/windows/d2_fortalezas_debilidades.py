"""
Archivo: gui/windows/d2_fortalezas_debilidades.py
Pestaña D2 - Fortalezas y Debilidades
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.matriz_ratios import MatrizRatios
from core.analysis.fortalezas_debilidades import FortalezasDebilidadesAnalysis


class D2FortalezasDebilidadesTab(ttk.Frame):
    """Pestaña D2 - Fortalezas y Debilidades"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de D2"""
        canvas = tk.Canvas(self, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colors.BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo = tk.Label(
            scrollable_frame,
            text="D.2 FORTALEZAS Y DEBILIDADES FINANCIERAS",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Subtítulo
        subtitulo = tk.Label(
            scrollable_frame,
            text="Identificación Cuantitativa de las 3 Principales Fortalezas y 3 Principales Debilidades",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            fg=Colors.NEUTRAL
        )
        subtitulo.pack(pady=(0, Dimensions.PADDING_MEDIUM))
        
        # Obtener análisis
        matriz_analisis = MatrizRatios(self.app.balance_data, self.app.income_data)
        matriz = matriz_analisis.generar_matriz_completa()
        
        analisis = FortalezasDebilidadesAnalysis(matriz)
        resultado = analisis.identificar_fortalezas_debilidades()
        
        # FORTALEZAS
        fortalezas_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" ✓ FORTALEZAS FINANCIERAS ",
            padding=Dimensions.PADDING_LARGE
        )
        fortalezas_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                             pady=Dimensions.PADDING_MEDIUM)
        
        for fortaleza in resultado['fortalezas']:
            self._crear_card_fortaleza(fortalezas_frame, fortaleza)
        
        # DEBILIDADES
        debilidades_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" ✗ DEBILIDADES FINANCIERAS ",
            padding=Dimensions.PADDING_LARGE
        )
        debilidades_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                               pady=Dimensions.PADDING_MEDIUM)
        
        for debilidad in resultado['debilidades']:
            self._crear_card_debilidad(debilidades_frame, debilidad)
        
        # DIAGNÓSTICO INTEGRAL
        diagnostico_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" 📊 DIAGNÓSTICO INTEGRAL ",
            padding=Dimensions.PADDING_LARGE
        )
        diagnostico_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        diagnostico_text = tk.Text(
            diagnostico_frame,
            height=12,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        diagnostico_text.pack(fill=tk.X)
        diagnostico_text.insert('1.0', resultado['interpretacion_global'])
        diagnostico_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_card_fortaleza(self, parent, fortaleza):
        """Crea una card para mostrar una fortaleza"""
        # Frame contenedor
        card_frame = tk.Frame(parent, bg=Colors.SUCCESS, relief='solid', borderwidth=1)
        card_frame.pack(fill=tk.X, pady=Dimensions.PADDING_MEDIUM)
        
        # Padding interno
        inner_frame = tk.Frame(card_frame, bg=Colors.SUCCESS)
        inner_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Header con título y badge
        header_frame = tk.Frame(inner_frame, bg=Colors.SUCCESS)
        header_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Título
        titulo_label = tk.Label(
            header_frame,
            text=f"FORTALEZA #{fortaleza['posicion']}",
            font=Fonts.HEADER,
            bg=Colors.SUCCESS,
            fg="white"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Badge de categoría
        badge = tk.Label(
            header_frame,
            text=fortaleza['categoria'],
            font=Fonts.SMALL,
            bg="white",
            fg=Colors.SUCCESS,
            padx=8,
            pady=2
        )
        badge.pack(side=tk.RIGHT)
        
        # Nombre del ratio
        nombre_label = tk.Label(
            inner_frame,
            text=fortaleza['ratio'],
            font=Fonts.LARGE,
            bg=Colors.SUCCESS,
            fg="white"
        )
        nombre_label.pack(anchor="w", pady=(0, 10))
        
        # Datos cuantitativos en grid
        datos_frame = tk.Frame(inner_frame, bg="white")
        datos_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid 2x2
        tk.Label(datos_frame, text="Año 1:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(datos_frame, text=self._formatear_valor(fortaleza['ano_1'], fortaleza['unidad']), 
                 font=Fonts.NORMAL_BOLD, bg="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(datos_frame, text="Año 2:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tk.Label(datos_frame, text=self._formatear_valor(fortaleza['ano_2'], fortaleza['unidad']), 
                 font=Fonts.NORMAL_BOLD, bg="white", fg=Colors.SUCCESS).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        tk.Label(datos_frame, text="Cambio:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        cambio_color = Colors.SUCCESS if fortaleza['cambio_pct'] > 0 else Colors.DANGER
        tk.Label(datos_frame, text=f"{fortaleza['cambio_pct']:+.1f}%", 
                 font=Fonts.NORMAL_BOLD, bg="white", fg=cambio_color).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(datos_frame, text="Estado:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(datos_frame, text=fortaleza['estado'].upper(), 
                 font=Fonts.NORMAL_BOLD, bg="white", fg=Colors.SUCCESS).grid(row=1, column=3, padx=10, pady=5, sticky="w")
        
        # Análisis completo
        analisis_text = tk.Text(
            inner_frame,
            height=10,
            wrap='word',
            font=Fonts.SMALL,
            bg="white",
            relief='flat',
            padx=10,
            pady=10
        )
        analisis_text.pack(fill=tk.X)
        analisis_text.insert('1.0', fortaleza['analisis'])
        analisis_text.config(state='disabled')
    
    def _crear_card_debilidad(self, parent, debilidad):
        """Crea una card para mostrar una debilidad"""
        # Frame contenedor
        card_frame = tk.Frame(parent, bg=Colors.DANGER, relief='solid', borderwidth=1)
        card_frame.pack(fill=tk.X, pady=Dimensions.PADDING_MEDIUM)
        
        # Padding interno
        inner_frame = tk.Frame(card_frame, bg=Colors.DANGER)
        inner_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Header con título y badge
        header_frame = tk.Frame(inner_frame, bg=Colors.DANGER)
        header_frame.pack(fill=tk.X, pady=(0, 8))
        
        # Título
        titulo_label = tk.Label(
            header_frame,
            text=f"DEBILIDAD #{debilidad['posicion']}",
            font=Fonts.HEADER,
            bg=Colors.DANGER,
            fg="white"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Badge de categoría
        badge = tk.Label(
            header_frame,
            text=debilidad['categoria'],
            font=Fonts.SMALL,
            bg="white",
            fg=Colors.DANGER,
            padx=8,
            pady=2
        )
        badge.pack(side=tk.RIGHT)
        
        # Nombre del ratio
        nombre_label = tk.Label(
            inner_frame,
            text=debilidad['ratio'],
            font=Fonts.LARGE,
            bg=Colors.DANGER,
            fg="white"
        )
        nombre_label.pack(anchor="w", pady=(0, 10))
        
        # Datos cuantitativos en grid
        datos_frame = tk.Frame(inner_frame, bg="white")
        datos_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid 2x2
        tk.Label(datos_frame, text="Año 1:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(datos_frame, text=self._formatear_valor(debilidad['ano_1'], debilidad['unidad']), 
                 font=Fonts.NORMAL_BOLD, bg="white").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(datos_frame, text="Año 2:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        tk.Label(datos_frame, text=self._formatear_valor(debilidad['ano_2'], debilidad['unidad']), 
                 font=Fonts.NORMAL_BOLD, bg="white", fg=Colors.DANGER).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        tk.Label(datos_frame, text="Cambio:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        cambio_color = Colors.SUCCESS if debilidad['cambio_pct'] > 0 else Colors.DANGER
        tk.Label(datos_frame, text=f"{debilidad['cambio_pct']:+.1f}%", 
                 font=Fonts.NORMAL_BOLD, bg="white", fg=cambio_color).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(datos_frame, text="Estado:", font=Fonts.SMALL, 
                 bg="white", fg=Colors.NEUTRAL).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        tk.Label(datos_frame, text=debilidad['estado'].upper(), 
                 font=Fonts.NORMAL_BOLD, bg="white", fg=Colors.DANGER).grid(row=1, column=3, padx=10, pady=5, sticky="w")
        
        # Análisis completo
        analisis_text = tk.Text(
            inner_frame,
            height=11,
            wrap='word',
            font=Fonts.SMALL,
            bg="white",
            relief='flat',
            padx=10,
            pady=10
        )
        analisis_text.pack(fill=tk.X)
        analisis_text.insert('1.0', debilidad['analisis'])
        analisis_text.config(state='disabled')
    
    def _formatear_valor(self, valor, unidad):
        """Formatea un valor según su unidad"""
        if unidad == 'porcentaje':
            return f"{valor:.2f}%"
        elif unidad == 'veces':
            return f"{valor:.2f}x"
        else:  # ratio
            return f"{valor:.2f}"