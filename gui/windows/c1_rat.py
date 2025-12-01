"""
Archivo: gui/windows/c1_rat.py
Pestaña C1 - Rentabilidad del Activo Total (RAT)
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.rat_analysis import RATAnalysis


class C1RATTab(ttk.Frame):
    """Pestaña C1 - Rentabilidad del Activo Total"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de C1"""
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
            text="C.1 RENTABILIDAD DEL ACTIVO TOTAL (RAT)",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis = RATAnalysis(self.app.balance_data, self.app.income_data)
        resultado = analisis.analisis_dual()
        
        ano1 = resultado['ano_1']
        ano2 = resultado['ano_2']
        comparacion = resultado['comparacion']
        
        # FÓRMULA DEL RAT
        formula_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Fórmula ",
            padding=Dimensions.PADDING_LARGE
        )
        formula_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                          pady=Dimensions.PADDING_MEDIUM)
        
        formula_text = tk.Text(
            formula_frame,
            height=2,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        formula_text.pack(fill=tk.X)
        formula_text.insert('1.0', 'RAT = (BAII / Activo Total) × 100\n\nMide cuánto beneficio operativo genera cada peso invertido en activos.')
        formula_text.config(state='disabled')
        
        # TABLA: Datos y resultados lado a lado
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Comparativo ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        # Configurar grid
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(1, weight=1)
        tabla_frame.grid_columnconfigure(2, weight=0)  # Separador
        tabla_frame.grid_columnconfigure(3, weight=1)
        tabla_frame.grid_columnconfigure(4, weight=1)
        
        # Encabezados
        tk.Label(tabla_frame, text="", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        
        # Separador vertical
        ttk.Separator(tabla_frame, orient="vertical").grid(
            row=0, column=2, rowspan=10, sticky="ns", padx=15)
        
        tk.Label(tabla_frame, text="", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=3, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=4, padx=10, pady=5)
        
        # BAII
        tk.Label(tabla_frame, text="BAII (Utilidad Operativa)", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano1['baii']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=1, padx=10, pady=3)
        
        tk.Label(tabla_frame, text="BAII (Utilidad Operativa)", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=3, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano2['baii']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=4, padx=10, pady=3)
        
        # Activo Total
        tk.Label(tabla_frame, text="Activo Total", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano1['activo_total']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=1, padx=10, pady=3)
        
        tk.Label(tabla_frame, text="Activo Total", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=3, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano2['activo_total']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=4, padx=10, pady=3)
        
        # Separador
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=3, column=3, columnspan=2, sticky="ew", pady=8)
        
        # RAT con color de fondo según sostenibilidad
        rat_1 = ano1['rat']
        rat_2 = ano2['rat']
        
        tk.Label(tabla_frame, text="RAT (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        
        # Color para Año 1 (referencia)
        tk.Label(tabla_frame, 
                text=f"{rat_1:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="RAT (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=4, column=3, padx=10, pady=5, sticky="w")
        
        # Color para Año 2 según sostenibilidad
        sostenibilidad = comparacion['sostenible']
        if sostenibilidad == 'sostenible':
            color_rat2 = Colors.SUCCESS
        elif sostenibilidad == 'precaucion':
            color_rat2 = Colors.WARNING
        elif sostenibilidad == 'no_sostenible':
            color_rat2 = Colors.DANGER
        else:  # estable
            color_rat2 = Colors.INFO
        
        tk.Label(tabla_frame, 
                text=f"{rat_2:.2f}%",
                font=Fonts.LARGE,
                bg=color_rat2,
                fg="white",
                padx=10,
                pady=5).grid(row=4, column=4, padx=10, pady=5)
        
        # COMPARACIÓN
        comparacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Comparación Entre Períodos ",
            padding=Dimensions.PADDING_LARGE
        )
        comparacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        # Cambio absoluto
        delta = comparacion['delta_absoluto']
        tk.Label(comparacion_frame, text="Cambio Absoluto:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        
        color_delta = Colors.POSITIVE if delta > 0 else Colors.NEGATIVE if delta < 0 else Colors.NEUTRAL
        tk.Label(comparacion_frame, 
                text=f"{delta:+.2f} puntos porcentuales",
                font=Fonts.NORMAL,
                fg=color_delta,
                bg=Colors.BG_PRIMARY).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Cambio relativo
        crecimiento = comparacion['crecimiento_relativo']
        tk.Label(comparacion_frame, text="Cambio Relativo:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        
        color_crec = Colors.POSITIVE if crecimiento > 0 else Colors.NEGATIVE if crecimiento < 0 else Colors.NEUTRAL
        tk.Label(comparacion_frame, 
                text=f"{crecimiento:+.2f}%",
                font=Fonts.NORMAL,
                fg=color_crec,
                bg=Colors.BG_PRIMARY).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Estado de sostenibilidad
        tk.Label(comparacion_frame, text="Sostenibilidad:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        
        estado_texto = {
            'sostenible': 'SOSTENIBLE ✓',
            'precaucion': 'PRECAUCIÓN ⚠',
            'no_sostenible': 'NO SOSTENIBLE ✗',
            'estable': 'ESTABLE ='
        }
        
        tk.Label(comparacion_frame, 
                text=estado_texto.get(sostenibilidad, 'N/A'),
                font=Fonts.NORMAL_BOLD,
                fg="white",
                bg=color_rat2,
                padx=10,
                pady=3).grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        # INTERPRETACIÓN PROFESIONAL
        interpretacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación Profesional ",
            padding=Dimensions.PADDING_LARGE
        )
        interpretacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                 pady=Dimensions.PADDING_MEDIUM)
        
        interp_text = tk.Text(
            interpretacion_frame,
            height=8,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_text.pack(fill=tk.X)
        interp_text.insert('1.0', comparacion['interpretacion'])
        interp_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")