"""
Archivo: gui/windows/a1_fondo_maniobra.py
Pestaña A1 - Fondo de Maniobra
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')  # ✅ Forzar backend TkAgg
matplotlib.rcParams['font.size'] = 10  # ✅ Tamaño de fuente matplotlib

from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.equilibrio_patrimonial import AnalisisPatrimonialCompleto
from graphics.fondo_maniobra import grafico_barras_con_variacion
from graphics.grafico_balance import grafico_balance


class A1FondoManiobraTab(ttk.Frame):
    """Pestaña A1 - Fondo de Maniobra"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        canvas = tk.Canvas(self, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colors.BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título de la sección
        titulo = tk.Label(
            scrollable_frame,
            text="A.1 FONDO DE MANIOBRA",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis_completo = AnalisisPatrimonialCompleto(self.app.balance_data)
        resultado = analisis_completo.analisis_dual()
        
        ano1 = resultado['ano_1']
        ano2 = resultado['ano_2']
        comparacion = resultado['comparacion']
        
        # TABLA: Fondo de Maniobra
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Fondo de Maniobra ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                        pady=Dimensions.PADDING_MEDIUM)
        
        tk.Label(tabla_frame, text="", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(tabla_frame, text="Año 1", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=1, padx=10, pady=5)
        tk.Label(tabla_frame, text="Año 2", font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=2, padx=10, pady=5)
        
        tk.Label(tabla_frame, text="Fondo de Maniobra", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        
        fm1 = ano1['fondo_maniobra_absoluto']
        fm2 = ano2['fondo_maniobra_absoluto']
        
        tk.Label(tabla_frame, 
                text=NumberFormat.format(fm1),
                font=Fonts.NORMAL,
                fg=Colors.POSITIVE if fm1 > 0 else Colors.NEGATIVE,
                bg=Colors.BG_PRIMARY).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(tabla_frame,
                text=NumberFormat.format(fm2),
                font=Fonts.NORMAL,
                fg=Colors.POSITIVE if fm2 > 0 else Colors.NEGATIVE,
                bg=Colors.BG_PRIMARY).grid(row=1, column=2, padx=10, pady=5)
        
        # DESCRIPCIÓN DE EVOLUCIÓN
        evol_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Evolución del Fondo de Maniobra ",
            padding=Dimensions.PADDING_LARGE
        )
        evol_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                       pady=Dimensions.PADDING_MEDIUM)
        
        evol_text = tk.Text(
            evol_frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        evol_text.pack(fill=tk.X)
        evol_text.insert('1.0', comparacion['evolucion'])
        evol_text.config(state='disabled')
        
        # DESCRIPCIÓN DE EQUILIBRIO
        eq_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Equilibrio Patrimonial ",
            padding=Dimensions.PADDING_LARGE
        )
        eq_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                     pady=Dimensions.PADDING_MEDIUM)
        
        tk.Label(eq_frame, text="Año 1:", font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).pack(
            anchor='w', pady=(0, 5))
        
        eq1_text = tk.Text(
            eq_frame,
            height=3,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        eq1_text.pack(fill=tk.X, pady=(0, 10))
        eq1_text.insert('1.0', ano1['descripcion_equilibrio'])
        eq1_text.config(state='disabled')
        
        tk.Label(eq_frame, text="Año 2:", font=Fonts.NORMAL_BOLD, bg=Colors.BG_PRIMARY).pack(
            anchor='w', pady=(0, 5))
        
        eq2_text = tk.Text(
            eq_frame,
            height=3,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        eq2_text.pack(fill=tk.X)
        eq2_text.insert('1.0', ano2['descripcion_equilibrio'])
        eq2_text.config(state='disabled')
        
        # GRÁFICO: Evolución
        grafico1_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Gráfico de Evolución ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico1_frame.pack(fill=tk.BOTH, expand=True,
                           padx=Dimensions.PADDING_XLARGE,
                           pady=Dimensions.PADDING_MEDIUM)
        
        import matplotlib.pyplot as plt
        with plt.rc_context({'font.size': 10}):  # Contexto local
            fig1 = grafico_barras_con_variacion(fm1, fm2, "Año 1", "Año 2")
            canvas1 = FigureCanvasTkAgg(fig1, master=grafico1_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # GRÁFICO: Balance Año 1
        grafico2_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Representación Balance - Año 1 ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico2_frame.pack(fill=tk.BOTH, expand=True,
                        padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        # GRÁFICO: Balance Año 1
        grafico2_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Representación Balance - Año 1 ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico2_frame.pack(fill=tk.BOTH, expand=True,
                        padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        with plt.rc_context({'font.size': 10}):
            fig2 = grafico_balance(
                activo_nc=ano1['activo_no_corriente'],
                activo_c=ano1['activo_corriente'],
                patrimonio=ano1['patrimonio'],
                pasivo_nc=ano1['pasivo_no_corriente'],
                pasivo_c=ano1['pasivo_corriente'],
                anio=1
            )
            canvas2 = FigureCanvasTkAgg(fig2, master=grafico2_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # GRÁFICO: Balance Año 2
        grafico3_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Representación Balance - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico3_frame.pack(fill=tk.BOTH, expand=True,
                        padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
    
        with plt.rc_context({'font.size': 10}):
            fig3 = grafico_balance(
                activo_nc=ano2['activo_no_corriente'],
                activo_c=ano2['activo_corriente'],
                patrimonio=ano2['patrimonio'],
                pasivo_nc=ano2['pasivo_no_corriente'],
                pasivo_c=ano2['pasivo_corriente'],
                anio=2
            )
            canvas3 = FigureCanvasTkAgg(fig3, master=grafico3_frame)
            canvas3.draw()
            canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")