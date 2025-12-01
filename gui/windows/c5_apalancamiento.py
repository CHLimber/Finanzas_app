"""
Archivo: gui/windows/c5_apalancamiento.py
Pestaña C5 - Apalancamiento Financiero
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.apalancamiento_analysis import ApalancamientoAnalysis


class C5ApalancamientoTab(ttk.Frame):
    """Pestaña C5 - Apalancamiento Financiero"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de C5"""
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
            text="C.5 APALANCAMIENTO FINANCIERO",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis = ApalancamientoAnalysis(self.app.balance_data, self.app.income_data)
        resultado = analisis.analisis_dual_apalancamiento()
        
        ano1 = resultado['ano_1']
        ano2 = resultado['ano_2']
        interpretaciones = resultado['interpretaciones']
        
        # a) COSTO PROMEDIO DE LA DEUDA
        costo_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" a) Costo Promedio de la Deuda (i) ",
            padding=Dimensions.PADDING_LARGE
        )
        costo_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        # Fórmula
        formula_costo = tk.Text(
            costo_frame,
            height=2,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        formula_costo.pack(fill=tk.X, pady=(0, 10))
        formula_costo.insert('1.0', 'i = Gastos Financieros / Deuda Total × 100\nDonde: Deuda Total = Préstamos LP + Deuda CP')
        formula_costo.config(state='disabled')
        
        # Tabla
        costo_grid = tk.Frame(costo_frame, bg=Colors.BG_PRIMARY)
        costo_grid.pack(fill=tk.X, pady=5)
        
        tk.Label(costo_grid, text="", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(costo_grid, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        tk.Label(costo_grid, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=2, padx=10, pady=5)
        
        tk.Label(costo_grid, text="Costo de Deuda (i):", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        
        tk.Label(costo_grid, 
                text=f"{ano1['i']:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=1, column=1, padx=10, pady=5)
        
        # Color según nivel
        i2 = ano2['i']
        if i2 <= 8:
            color_i = Colors.SUCCESS
        elif i2 <= 12:
            color_i = Colors.WARNING
        else:
            color_i = Colors.DANGER
        
        tk.Label(costo_grid, 
                text=f"{i2:.2f}%",
                font=Fonts.LARGE,
                bg=color_i,
                fg="white",
                padx=10,
                pady=5).grid(row=1, column=2, padx=10, pady=5)
        
        # Interpretación
        interp_costo_text = tk.Text(
            costo_frame,
            height=6,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_costo_text.pack(fill=tk.X, pady=(10, 0))
        interp_costo_text.insert('1.0', interpretaciones['costo_deuda'])
        interp_costo_text.config(state='disabled')
        
        # b) COMPARACIÓN RAT vs i
        comparacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" b) Comparación RAT vs Costo de Deuda (i) ",
            padding=Dimensions.PADDING_LARGE
        )
        comparacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        # Tabla comparativa (solo Año 2)
        comp_grid = tk.Frame(comparacion_frame, bg=Colors.BG_PRIMARY)
        comp_grid.pack(fill=tk.X, pady=5)
        
        tk.Label(comp_grid, text="Indicador", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(comp_grid, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        
        # RAT
        tk.Label(comp_grid, text="RAT (Rentabilidad Económica):", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(comp_grid, text=f"{ano2['rat']:.2f}%", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=1, padx=10, pady=3)
        
        # i
        tk.Label(comp_grid, text="i (Costo de Deuda):", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        tk.Label(comp_grid, text=f"{ano2['i']:.2f}%", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=2, column=1, padx=10, pady=3)
        
        # Diferencial
        diferencial = ano2['diferencial']
        tk.Label(comp_grid, text="Diferencial (RAT - i):", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        
        color_dif = Colors.SUCCESS if diferencial > 0 else Colors.DANGER if diferencial < 0 else Colors.INFO
        tk.Label(comp_grid, text=f"{diferencial:+.2f} p.p.", 
                 font=Fonts.LARGE, fg="white", bg=color_dif, padx=10, pady=3).grid(
            row=3, column=1, padx=10, pady=5)
        
        # Tipo de apalancamiento
        tk.Label(comp_grid, text="Tipo de Apalancamiento:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=4, column=0, padx=10, pady=5, sticky="w")
        
        if diferencial > 0:
            tipo_apal = "POSITIVO ✓"
            color_tipo = Colors.SUCCESS
        elif diferencial < 0:
            tipo_apal = "NEGATIVO ✗"
            color_tipo = Colors.DANGER
        else:
            tipo_apal = "NEUTRAL ="
            color_tipo = Colors.INFO
        
        tk.Label(comp_grid, text=tipo_apal, 
                 font=Fonts.LARGE, fg="white", bg=color_tipo, padx=10, pady=3).grid(
            row=4, column=1, padx=10, pady=5)
        
        # Interpretación
        interp_comp_text = tk.Text(
            comparacion_frame,
            height=8,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_comp_text.pack(fill=tk.X, pady=(10, 0))
        interp_comp_text.insert('1.0', interpretaciones['rat_vs_i'])
        interp_comp_text.config(state='disabled')
        
        # c) EFECTO APALANCAMIENTO
        efecto_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" c) Efecto Apalancamiento - Fórmula RRP ",
            padding=Dimensions.PADDING_LARGE
        )
        efecto_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                         pady=Dimensions.PADDING_MEDIUM)
        
        # Fórmula
        formula_efecto = tk.Text(
            efecto_frame,
            height=2,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        formula_efecto.pack(fill=tk.X, pady=(0, 10))
        formula_efecto.insert('1.0', 'RRP = RAT + (D/PN) × (RAT - i)\n\nDonde: D = Deuda Total, PN = Patrimonio Neto')
        formula_efecto.config(state='disabled')
        
        # Componentes (Año 2)
        comp_efecto_grid = tk.Frame(efecto_frame, bg=Colors.BG_PRIMARY)
        comp_efecto_grid.pack(fill=tk.X, pady=5)
        
        tk.Label(comp_efecto_grid, text="Componente", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(comp_efecto_grid, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        
        # D/PN
        tk.Label(comp_efecto_grid, text="D/PN (Apalancamiento):", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(comp_efecto_grid, text=f"{ano2['d_pn']:.2f} veces", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=1, padx=10, pady=3)
        
        # Efecto
        efecto_apal = ano2['efecto_apalancamiento']
        tk.Label(comp_efecto_grid, text="Efecto Apalancamiento:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        
        color_efecto = Colors.SUCCESS if efecto_apal > 0 else Colors.DANGER if efecto_apal < 0 else Colors.INFO
        tk.Label(comp_efecto_grid, text=f"{efecto_apal:+.2f} p.p.", 
                 font=Fonts.LARGE, fg="white", bg=color_efecto, padx=10, pady=3).grid(
            row=2, column=1, padx=10, pady=5)
        
        # RRP Calculado
        tk.Label(comp_efecto_grid, text="RRP (Calculado):", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(comp_efecto_grid, text=f"{ano2['rrp_calculado']:.2f}%", 
                 font=Fonts.LARGE, bg=Colors.INFO, fg="white", padx=10, pady=3).grid(
            row=3, column=1, padx=10, pady=5)
        
        # RRP Directo
        tk.Label(comp_efecto_grid, text="RRP (Directo):", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=4, column=0, padx=10, pady=3, sticky="w")
        tk.Label(comp_efecto_grid, text=f"{ano2['rrp_directo']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=4, column=1, padx=10, pady=3)
        
        # Interpretación
        interp_efecto_text = tk.Text(
            efecto_frame,
            height=8,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_efecto_text.pack(fill=tk.X, pady=(10, 0))
        interp_efecto_text.insert('1.0', interpretaciones['efecto_apalancamiento'])
        interp_efecto_text.config(state='disabled')
        
        # d) ¿CONVIENE AUMENTAR DEUDA?
        conveniencia_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" d) ¿Conviene Aumentar Deuda? ",
            padding=Dimensions.PADDING_LARGE
        )
        conveniencia_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                               pady=Dimensions.PADDING_MEDIUM)
        
        interp_conv_text = tk.Text(
            conveniencia_frame,
            height=14,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_conv_text.pack(fill=tk.X)
        interp_conv_text.insert('1.0', interpretaciones['conveniencia_deuda'])
        interp_conv_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")