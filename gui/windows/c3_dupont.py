"""
Archivo: gui/windows/c3_dupont.py
Pestaña C3 - Análisis DuPont
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.dupont_analysis import DuPontAnalysis
from core.analysis.financial_interpreter import FinancialInterpreter


class C3DuPontTab(ttk.Frame):
    """Pestaña C3 - Análisis DuPont"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de C3"""
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
            text="C.3 ANÁLISIS DUPONT",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis = DuPontAnalysis(self.app.balance_data, self.app.income_data)
        resultado = analisis.analisis_dupont_dual()
        interpreter = FinancialInterpreter()
        
        ano1 = resultado['ano_1']
        ano2 = resultado['ano_2']
        
        # EXPLICACIÓN DEL MODELO DUPONT
        explicacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Modelo DuPont ",
            padding=Dimensions.PADDING_LARGE
        )
        explicacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        explicacion_text = tk.Text(
            explicacion_frame,
            height=5,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        explicacion_text.pack(fill=tk.X)
        explicacion_text.insert('1.0', 
            'El Análisis DuPont descompone la Rentabilidad de Recursos Propios (RRP) en tres componentes:\n\n'
            '  RRP = Margen Neto × Rotación del Activo × Apalancamiento Financiero\n\n'
            'Donde:\n'
            '  • Margen Neto = Utilidad Neta / Ventas (Eficiencia Operativa)\n'
            '  • Rotación del Activo = Ventas / Activo Total (Eficiencia en Uso de Activos)\n'
            '  • Apalancamiento = Activo Total / Patrimonio Neto (Uso de Deuda)')
        explicacion_text.config(state='disabled')
        
        # TABLA: Componentes DuPont lado a lado
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Componentes del Análisis DuPont ",
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
        tk.Label(tabla_frame, text="Componente", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        
        # Separador vertical
        ttk.Separator(tabla_frame, orient="vertical").grid(
            row=0, column=2, rowspan=15, sticky="ns", padx=15)
        
        tk.Label(tabla_frame, text="Componente", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=3, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=4, padx=10, pady=5)
        
        row = 1
        
        # 1. MARGEN NETO
        tk.Label(tabla_frame, text="1. Margen Neto (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text=f"{ano1['margen_neto']:.2f}%",
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=row, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="1. Margen Neto (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=3, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text=f"{ano2['margen_neto']:.2f}%",
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=row, column=4, padx=10, pady=5)
        row += 1
        
        # Interpretación Margen Neto
        interp_margen_1 = interpreter.get_interpretacion('margen_neto', ano1['margen_neto'])
        interp_margen_2 = interpreter.get_interpretacion('margen_neto', ano2['margen_neto'])
        
        tk.Label(tabla_frame, text="   Interpretación:", 
                 font=Fonts.SMALL, bg=Colors.BG_PRIMARY, fg=Colors.NEUTRAL).grid(
            row=row, column=0, padx=10, pady=2, sticky="w")
        
        text_margen_1 = tk.Text(tabla_frame, height=2, wrap='word', font=Fonts.SMALL,
                               bg=Colors.BG_SECONDARY, relief='flat', padx=5, pady=3)
        text_margen_1.grid(row=row, column=1, padx=10, pady=2, sticky="ew")
        text_margen_1.insert('1.0', interp_margen_1)
        text_margen_1.config(state='disabled')
        
        tk.Label(tabla_frame, text="   Interpretación:", 
                 font=Fonts.SMALL, bg=Colors.BG_PRIMARY, fg=Colors.NEUTRAL).grid(
            row=row, column=3, padx=10, pady=2, sticky="w")
        
        text_margen_2 = tk.Text(tabla_frame, height=2, wrap='word', font=Fonts.SMALL,
                               bg=Colors.BG_SECONDARY, relief='flat', padx=5, pady=3)
        text_margen_2.grid(row=row, column=4, padx=10, pady=2, sticky="ew")
        text_margen_2.insert('1.0', interp_margen_2)
        text_margen_2.config(state='disabled')
        row += 1
        
        # Separador
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=row, column=3, columnspan=2, sticky="ew", pady=8)
        row += 1
        
        # 2. ROTACIÓN DEL ACTIVO
        tk.Label(tabla_frame, text="2. Rotación del Activo (veces)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text=f"{ano1['rotacion_activo']:.2f}",
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=row, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="2. Rotación del Activo (veces)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=3, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text=f"{ano2['rotacion_activo']:.2f}",
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=row, column=4, padx=10, pady=5)
        row += 1
        
        # Interpretación Rotación
        interp_rotacion_1 = interpreter.get_interpretacion('rotacion_activos', ano1['rotacion_activo'])
        interp_rotacion_2 = interpreter.get_interpretacion('rotacion_activos', ano2['rotacion_activo'])
        
        tk.Label(tabla_frame, text="   Interpretación:", 
                 font=Fonts.SMALL, bg=Colors.BG_PRIMARY, fg=Colors.NEUTRAL).grid(
            row=row, column=0, padx=10, pady=2, sticky="w")
        
        text_rotacion_1 = tk.Text(tabla_frame, height=2, wrap='word', font=Fonts.SMALL,
                                 bg=Colors.BG_SECONDARY, relief='flat', padx=5, pady=3)
        text_rotacion_1.grid(row=row, column=1, padx=10, pady=2, sticky="ew")
        text_rotacion_1.insert('1.0', interp_rotacion_1)
        text_rotacion_1.config(state='disabled')
        
        tk.Label(tabla_frame, text="   Interpretación:", 
                 font=Fonts.SMALL, bg=Colors.BG_PRIMARY, fg=Colors.NEUTRAL).grid(
            row=row, column=3, padx=10, pady=2, sticky="w")
        
        text_rotacion_2 = tk.Text(tabla_frame, height=2, wrap='word', font=Fonts.SMALL,
                                 bg=Colors.BG_SECONDARY, relief='flat', padx=5, pady=3)
        text_rotacion_2.grid(row=row, column=4, padx=10, pady=2, sticky="ew")
        text_rotacion_2.insert('1.0', interp_rotacion_2)
        text_rotacion_2.config(state='disabled')
        row += 1
        
        # Separador
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=row, column=3, columnspan=2, sticky="ew", pady=8)
        row += 1
        
        # 3. APALANCAMIENTO FINANCIERO
        tk.Label(tabla_frame, text="3. Apalancamiento (veces)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text=f"{ano1['apalancamiento']:.2f}",
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=row, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="3. Apalancamiento (veces)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=3, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text=f"{ano2['apalancamiento']:.2f}",
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=row, column=4, padx=10, pady=5)
        row += 1
        
        # Interpretación Apalancamiento
        interp_apal_1 = interpreter.get_interpretacion('apalancamiento', ano1['apalancamiento'])
        interp_apal_2 = interpreter.get_interpretacion('apalancamiento', ano2['apalancamiento'])
        
        tk.Label(tabla_frame, text="   Interpretación:", 
                 font=Fonts.SMALL, bg=Colors.BG_PRIMARY, fg=Colors.NEUTRAL).grid(
            row=row, column=0, padx=10, pady=2, sticky="w")
        
        text_apal_1 = tk.Text(tabla_frame, height=2, wrap='word', font=Fonts.SMALL,
                             bg=Colors.BG_SECONDARY, relief='flat', padx=5, pady=3)
        text_apal_1.grid(row=row, column=1, padx=10, pady=2, sticky="ew")
        text_apal_1.insert('1.0', interp_apal_1)
        text_apal_1.config(state='disabled')
        
        tk.Label(tabla_frame, text="   Interpretación:", 
                 font=Fonts.SMALL, bg=Colors.BG_PRIMARY, fg=Colors.NEUTRAL).grid(
            row=row, column=3, padx=10, pady=2, sticky="w")
        
        text_apal_2 = tk.Text(tabla_frame, height=2, wrap='word', font=Fonts.SMALL,
                             bg=Colors.BG_SECONDARY, relief='flat', padx=5, pady=3)
        text_apal_2.grid(row=row, column=4, padx=10, pady=2, sticky="ew")
        text_apal_2.insert('1.0', interp_apal_2)
        text_apal_2.config(state='disabled')
        row += 1
        
        # Separador final
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=2, sticky="ew", pady=8)
        ttk.Separator(tabla_frame, orient="horizontal").grid(
            row=row, column=3, columnspan=2, sticky="ew", pady=8)
        row += 1
        
        # RESULTADO: RRP CALCULADO
        tk.Label(tabla_frame, text="RRP (DuPont) (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=0, padx=10, pady=5, sticky="w")
        
        tk.Label(tabla_frame, 
                text=f"{ano1['rrp_dupont']:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=row, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="RRP (DuPont) (%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=row, column=3, padx=10, pady=5, sticky="w")
        
        tk.Label(tabla_frame, 
                text=f"{ano2['rrp_dupont']:.2f}%",
                font=Fonts.LARGE,
                bg=Colors.INFO,
                fg="white",
                padx=10,
                pady=5).grid(row=row, column=4, padx=10, pady=5)
        row += 1
        
        # VERIFICACIÓN
        verificacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Verificación de Cálculo ",
            padding=Dimensions.PADDING_LARGE
        )
        verificacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                               pady=Dimensions.PADDING_MEDIUM)
        
        verif_grid = tk.Frame(verificacion_frame, bg=Colors.BG_PRIMARY)
        verif_grid.pack(fill=tk.X, pady=5)
        
        # Encabezados
        tk.Label(verif_grid, text="", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5)
        tk.Label(verif_grid, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        tk.Label(verif_grid, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=2, padx=10, pady=5)
        
        # RRP Directo
        tk.Label(verif_grid, text="RRP Directo (UN/PN):", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(verif_grid, text=f"{ano1['rrp_directo']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=1, padx=10, pady=3)
        tk.Label(verif_grid, text=f"{ano2['rrp_directo']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=2, padx=10, pady=3)
        
        # RRP DuPont
        tk.Label(verif_grid, text="RRP DuPont (M × R × A):", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        tk.Label(verif_grid, text=f"{ano1['rrp_dupont']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=1, padx=10, pady=3)
        tk.Label(verif_grid, text=f"{ano2['rrp_dupont']:.2f}%", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=2, padx=10, pady=3)
        
        # Verificación
        tk.Label(verif_grid, text="Verificación:", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=3, column=0, padx=10, pady=5, sticky="w")
        
        verif_1_text = "✓ CORRECTO" if ano1['verificacion'] else "✗ ERROR"
        verif_1_color = Colors.SUCCESS if ano1['verificacion'] else Colors.DANGER
        tk.Label(verif_grid, text=verif_1_text, 
                 font=Fonts.NORMAL_BOLD, fg="white", bg=verif_1_color, padx=5, pady=2).grid(
            row=3, column=1, padx=10, pady=5)
        
        verif_2_text = "✓ CORRECTO" if ano2['verificacion'] else "✗ ERROR"
        verif_2_color = Colors.SUCCESS if ano2['verificacion'] else Colors.DANGER
        tk.Label(verif_grid, text=verif_2_text, 
                 font=Fonts.NORMAL_BOLD, fg="white", bg=verif_2_color, padx=5, pady=2).grid(
            row=3, column=2, padx=10, pady=5)
        
        # INTERPRETACIÓN GLOBAL DUPONT
        interpretacion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación del Análisis DuPont ",
            padding=Dimensions.PADDING_LARGE
        )
        interpretacion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                                 pady=Dimensions.PADDING_MEDIUM)
        
        interp_text = tk.Text(
            interpretacion_frame,
            height=14,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        interp_text.pack(fill=tk.X)
        interp_text.insert('1.0', resultado['interpretacion'])
        interp_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")