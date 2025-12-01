"""
Archivo: gui/windows/c2_rrp.py
Pestaña C2 - Rentabilidad de Recursos Propios (RRP)
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.rrp_analysis import RRPAnalysis


class C2RRPTab(ttk.Frame):
    """Pestaña C2 - Rentabilidad de Recursos Propios"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de C2"""
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
            text="C.2 RENTABILIDAD DE RECURSOS PROPIOS (RRP)",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis = RRPAnalysis(self.app.balance_data, self.app.income_data)
        resultado_rrp = analisis.analisis_dual_rrp()
        resultado_comparativo = analisis.analisis_comparativo_rat_rrp()
        
        ano1_rrp = resultado_rrp['ano_1']
        ano2_rrp = resultado_rrp['ano_2']
        comparacion_rrp = resultado_rrp['comparacion']
        
        ano1_comp = resultado_comparativo['ano_1']
        ano2_comp = resultado_comparativo['ano_2']
        
        # FÓRMULA DEL RRP
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
        formula_text.insert('1.0', 'RRP = (Utilidad Neta / Patrimonio Neto) × 100\n\nMide la rentabilidad que obtienen los accionistas sobre su inversión en el patrimonio.')
        formula_text.config(state='disabled')
        
        # TABLA: Análisis RRP lado a lado
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis de RRP ",
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
        
        # Utilidad Neta
        tk.Label(tabla_frame, text="Utilidad Neta", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano1_rrp['utilidad_neta']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=1, padx=10, pady=3)
        
        tk.Label(tabla_frame, text="Utilidad Neta", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=3, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano2_rrp['utilidad_neta']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=4, padx=10, pady=3)
        
        # Patrimonio Neto
        tk.Label(tabla_frame, text="Patrimonio Neto", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano1_rrp['patrimonio_neto']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=1, padx=10, pady=3)
        
        tk.Label(tabla_frame, text="Patrimonio Neto", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=3, padx=10, pady=3, sticky="w")
        tk.Label(tabla_frame, text=NumberFormat.format(ano2_rrp['patrimonio_neto']),
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=4, padx=10, pady=3)
        
        # Separador
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=3, column=3, columnspan=2, sticky="ew", pady=8)
        
        # RRP
        rrp_1 = ano1_rrp['rrp']
        rrp_2 = ano2_rrp['rrp']
        
        tk.Label(tabla_frame, text="RRP (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        
        tk.Label(tabla_frame, 
                text=f"{rrp_1:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="RRP (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=4, column=3, padx=10, pady=5, sticky="w")
        
        # Color según comparación con Año 1
        if rrp_2 > rrp_1:
            color_rrp2 = Colors.SUCCESS
        elif rrp_2 < rrp_1:
            color_rrp2 = Colors.DANGER
        else:
            color_rrp2 = Colors.INFO
        
        tk.Label(tabla_frame, 
                text=f"{rrp_2:.2f}%",
                font=Fonts.LARGE,
                bg=color_rrp2,
                fg="white",
                padx=10,
                pady=5).grid(row=4, column=4, padx=10, pady=5)
        
        # COMPARACIÓN RRP
        comparacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Comparación RRP Entre Períodos ",
            padding=Dimensions.PADDING_LARGE
        )
        comparacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        # Cambio absoluto
        delta = comparacion_rrp['delta_absoluto']
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
        crecimiento = comparacion_rrp['crecimiento_relativo']
        tk.Label(comparacion_frame, text="Cambio Relativo:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        
        color_crec = Colors.POSITIVE if crecimiento > 0 else Colors.NEGATIVE if crecimiento < 0 else Colors.NEUTRAL
        tk.Label(comparacion_frame, 
                text=f"{crecimiento:+.2f}%",
                font=Fonts.NORMAL,
                fg=color_crec,
                bg=Colors.BG_PRIMARY).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # INTERPRETACIÓN RRP
        interpretacion_rrp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación RRP ",
            padding=Dimensions.PADDING_LARGE
        )
        interpretacion_rrp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                     pady=Dimensions.PADDING_MEDIUM)
        
        interp_rrp_text = tk.Text(
            interpretacion_rrp_frame,
            height=6,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_rrp_text.pack(fill=tk.X)
        interp_rrp_text.insert('1.0', comparacion_rrp['interpretacion'])
        interp_rrp_text.config(state='disabled')
        
        # COMPARACIÓN RAT vs RRP
        comparacion_rat_rrp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Comparación RAT vs RRP (Apalancamiento Financiero) ",
            padding=Dimensions.PADDING_LARGE
        )
        comparacion_rat_rrp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                       pady=Dimensions.PADDING_MEDIUM)
        
        # Tabla comparativa
        comp_grid = tk.Frame(comparacion_rat_rrp_frame, bg=Colors.BG_PRIMARY)
        comp_grid.pack(fill=tk.X, pady=5)
        
        # Encabezados
        tk.Label(comp_grid, text="", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(comp_grid, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        tk.Label(comp_grid, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=2, padx=10, pady=5)
        
        # RAT
        tk.Label(comp_grid, text="RAT (%)", font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(comp_grid, text=f"{ano1_comp['rat']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=1, padx=10, pady=3)
        tk.Label(comp_grid, text=f"{ano2_comp['rat']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=2, padx=10, pady=3)
        
        # RRP
        tk.Label(comp_grid, text="RRP (%)", font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        tk.Label(comp_grid, text=f"{ano1_comp['rrp']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=1, padx=10, pady=3)
        tk.Label(comp_grid, text=f"{ano2_comp['rrp']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=2, padx=10, pady=3)
        
        # Apalancamiento
        tk.Label(comp_grid, text="Apalancamiento", font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        
        # Color Año 1
        apal_1 = ano1_comp['apalancamiento']
        color_apal_1 = Colors.SUCCESS if apal_1 == "positivo" else Colors.DANGER if apal_1 == "negativo" else Colors.INFO
        tk.Label(comp_grid, text=apal_1.upper(), 
                 font=Fonts.NORMAL_BOLD, fg="white", bg=color_apal_1, padx=5, pady=2).grid(
            row=3, column=1, padx=10, pady=5)
        
        # Color Año 2
        apal_2 = ano2_comp['apalancamiento']
        color_apal_2 = Colors.SUCCESS if apal_2 == "positivo" else Colors.DANGER if apal_2 == "negativo" else Colors.INFO
        tk.Label(comp_grid, text=apal_2.upper(), 
                 font=Fonts.NORMAL_BOLD, fg="white", bg=color_apal_2, padx=5, pady=2).grid(
            row=3, column=2, padx=10, pady=5)
        
        # INTERPRETACIÓN COMPARATIVA
        interpretacion_comp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación del Apalancamiento Financiero ",
            padding=Dimensions.PADDING_LARGE
        )
        interpretacion_comp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                      pady=Dimensions.PADDING_MEDIUM)
        
        interp_comp_text = tk.Text(
            interpretacion_comp_frame,
            height=12,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_comp_text.pack(fill=tk.X)
        interp_comp_text.insert('1.0', resultado_comparativo['interpretacion_completa'])
        interp_comp_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")