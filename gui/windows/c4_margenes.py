"""
Archivo: gui/windows/c4_margenes.py
Pestaña C4 - Márgenes de Ganancia
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.margenes_analysis import MargenesAnalysis


class C4MargenesTab(ttk.Frame):
    """Pestaña C4 - Márgenes de Ganancia"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de C4"""
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
            text="C.4 MÁRGENES DE GANANCIA Y EFICIENCIA EN COSTOS",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis = MargenesAnalysis(self.app.income_data)
        resultado = analisis.analisis_dual_margenes()
        
        ano1 = resultado['año_1']
        ano2 = resultado['año_2']
        interpretaciones = resultado['interpretaciones']
        
        # FÓRMULAS
        formulas_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Fórmulas de Márgenes ",
            padding=Dimensions.PADDING_LARGE
        )
        formulas_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                           pady=Dimensions.PADDING_MEDIUM)
        
        formulas_text = tk.Text(
            formulas_frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        formulas_text.pack(fill=tk.X)
        formulas_text.insert('1.0',
            'a) Margen Bruto = (Ganancia Bruta / Ingresos) × 100\n'
            'b) Margen Operativo = (BAII / Ingresos) × 100\n'
            'c) Margen Neto = (Utilidad Neta / Ingresos) × 100\n\n'
            'Estos márgenes miden la eficiencia en cada nivel: costos directos, operación y rentabilidad final.')
        formulas_text.config(state='disabled')
        
        # TABLA: Márgenes lado a lado
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis de Márgenes ",
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
        tk.Label(tabla_frame, text="Margen", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        
        # Separador vertical
        ttk.Separator(tabla_frame, orient="vertical").grid(
            row=0, column=2, rowspan=10, sticky="ns", padx=15)
        
        tk.Label(tabla_frame, text="Margen", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=3, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=4, padx=10, pady=5)
        
        # Margen Bruto
        tk.Label(tabla_frame, text="Margen Bruto", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        
        tk.Label(tabla_frame, 
                text=f"{ano1['margen_bruto']:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="Margen Bruto", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=3, padx=10, pady=5, sticky="w")
        
        # Color según nivel
        mb2 = ano2['margen_bruto']
        if mb2 >= 50:
            color_mb = Colors.SUCCESS
        elif mb2 >= 30:
            color_mb = Colors.WARNING
        else:
            color_mb = Colors.DANGER
        
        tk.Label(tabla_frame, 
                text=f"{mb2:.2f}%",
                font=Fonts.LARGE,
                bg=color_mb,
                fg="white",
                padx=10,
                pady=5).grid(row=1, column=4, padx=10, pady=5)
        
        # Margen Operativo
        tk.Label(tabla_frame, text="Margen Operativo", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        
        tk.Label(tabla_frame, 
                text=f"{ano1['margen_operativo']:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="Margen Operativo", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=2, column=3, padx=10, pady=5, sticky="w")
        
        # Color según nivel
        mo2 = ano2['margen_operativo']
        if mo2 >= 15:
            color_mo = Colors.SUCCESS
        elif mo2 >= 8:
            color_mo = Colors.WARNING
        else:
            color_mo = Colors.DANGER
        
        tk.Label(tabla_frame, 
                text=f"{mo2:.2f}%",
                font=Fonts.LARGE,
                bg=color_mo,
                fg="white",
                padx=10,
                pady=5).grid(row=2, column=4, padx=10, pady=5)
        
        # Margen Neto
        tk.Label(tabla_frame, text="Margen Neto", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        
        tk.Label(tabla_frame, 
                text=f"{ano1['margen_neto']:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=3, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="Margen Neto", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=3, column=3, padx=10, pady=5, sticky="w")
        
        # Color según nivel
        mn2 = ano2['margen_neto']
        if mn2 >= 10:
            color_mn = Colors.SUCCESS
        elif mn2 >= 5:
            color_mn = Colors.WARNING
        else:
            color_mn = Colors.DANGER
        
        tk.Label(tabla_frame, 
                text=f"{mn2:.2f}%",
                font=Fonts.LARGE,
                bg=color_mn,
                fg="white",
                padx=10,
                pady=5).grid(row=3, column=4, padx=10, pady=5)
        
        # INTERPRETACIÓN: Margen Bruto
        interp_bruto_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación: Margen Bruto ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_bruto_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                               pady=Dimensions.PADDING_MEDIUM)
        
        text_bruto = tk.Text(
            interp_bruto_frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_bruto.pack(fill=tk.X)
        text_bruto.insert('1.0', interpretaciones['margen_bruto'])
        text_bruto.config(state='disabled')
        
        # INTERPRETACIÓN: Margen Operativo
        interp_operativo_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación: Margen Operativo ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_operativo_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                    pady=Dimensions.PADDING_MEDIUM)
        
        text_operativo = tk.Text(
            interp_operativo_frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_operativo.pack(fill=tk.X)
        text_operativo.insert('1.0', interpretaciones['margen_operativo'])
        text_operativo.config(state='disabled')
        
        # INTERPRETACIÓN: Margen Neto
        interp_neto_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación: Margen Neto ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_neto_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        text_neto = tk.Text(
            interp_neto_frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_neto.pack(fill=tk.X)
        text_neto.insert('1.0', interpretaciones['margen_neto'])
        text_neto.config(state='disabled')
        
        # INTERPRETACIÓN: Eficiencia en Costos (Conjunta)
        interp_eficiencia_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" ¿La Empresa es Eficiente en Costos? ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_eficiencia_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                    pady=Dimensions.PADDING_MEDIUM)
        
        text_eficiencia = tk.Text(
            interp_eficiencia_frame,
            height=18,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_eficiencia.pack(fill=tk.X)
        text_eficiencia.insert('1.0', interpretaciones['eficiencia_costos'])
        text_eficiencia.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")