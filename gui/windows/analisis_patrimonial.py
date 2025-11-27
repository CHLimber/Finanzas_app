"""
Archivo: gui/windows/analisis_patrimonial.py
Pestaña de Análisis Patrimonial con subpestañas A1, A2, A3, A4 y A5
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.equilibrio_patrimonial import AnalisisPatrimonialCompleto
from graphics.fondo_maniobra import grafico_barras_con_variacion
from graphics.grafico_balance import grafico_balance
from core.analysis.analisis_vertical import AnalisisVerticalBalance

class AnalisisPatrimonialTab(ttk.Frame):
    """Pestaña con subpestañas de Análisis Patrimonial"""
    
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
            text="ANÁLISIS PATRIMONIAL",
            font=Fonts.TITLE
        ).pack()
        
        # Notebook secundario para subpestañas
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Crear subpestañas
        self.crear_subpestana_a1()
        self.crear_subpestana_a2()
        self.crear_subpestana_a3()
        self.crear_subpestana_a4_a5()
    
    def crear_subpestana_a1(self):
        """Subpestaña A1 - Fondo de Maniobra"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A1 - Fondo de Maniobra")
        
        # Canvas principal con scroll
        canvas = tk.Canvas(tab, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título de la sección
        titulo = ttk.Label(
            scrollable_frame,
            text="A.1 FONDO DE MANIOBRA",
            font=Fonts.TITLE
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener análisis
        analisis_completo = AnalisisPatrimonialCompleto(self.app.balance_data)
        resultado = analisis_completo.analisis_dual()
        
        ano1 = resultado['ano_1']
        ano2 = resultado['ano_2']
        comparacion = resultado['comparacion']
        
        # ============================================================
        # TABLA: Fondo de Maniobra
        # ============================================================
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Fondo de Maniobra ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                        pady=Dimensions.PADDING_MEDIUM)
        
        # Encabezados
        ttk.Label(tabla_frame, text="", font=Fonts.HEADER).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(tabla_frame, text="Año 1", font=Fonts.HEADER).grid(
            row=0, column=1, padx=10, pady=5)
        ttk.Label(tabla_frame, text="Año 2", font=Fonts.HEADER).grid(
            row=0, column=2, padx=10, pady=5)
        
        # Valores
        ttk.Label(tabla_frame, text="Fondo de Maniobra", 
                 font=Fonts.NORMAL_BOLD).grid(
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
        
        # ============================================================
        # DESCRIPCIÓN DE EVOLUCIÓN
        # ============================================================
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
        
        # ============================================================
        # DESCRIPCIÓN DE EQUILIBRIO
        # ============================================================
        eq_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Equilibrio Patrimonial ",
            padding=Dimensions.PADDING_LARGE
        )
        eq_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                     pady=Dimensions.PADDING_MEDIUM)
        
        # Año 1
        ttk.Label(eq_frame, text="Año 1:", font=Fonts.NORMAL_BOLD).pack(
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
        
        # Año 2
        ttk.Label(eq_frame, text="Año 2:", font=Fonts.NORMAL_BOLD).pack(
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
        
        # ============================================================
        # GRÁFICO: Evolución del Fondo de Maniobra
        # ============================================================
        grafico1_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Gráfico de Evolución ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico1_frame.pack(fill=tk.BOTH, expand=True,
                           padx=Dimensions.PADDING_XLARGE,
                           pady=Dimensions.PADDING_MEDIUM)
        
        # Crear gráfico de barras con variación
        fig1 = grafico_barras_con_variacion(fm1, fm2, "Año 1", "Año 2")
        
        canvas1 = FigureCanvasTkAgg(fig1, master=grafico1_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # GRÁFICO: Balance Año 1
        # ============================================================
        grafico2_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Representación Balance - Año 1 ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico2_frame.pack(fill=tk.BOTH, expand=True,
                           padx=Dimensions.PADDING_XLARGE,
                           pady=Dimensions.PADDING_MEDIUM)
        
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
        
        # ============================================================
        # GRÁFICO: Balance Año 2
        # ============================================================
        grafico3_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Representación Balance - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico3_frame.pack(fill=tk.BOTH, expand=True,
                           padx=Dimensions.PADDING_XLARGE,
                           pady=Dimensions.PADDING_MEDIUM)
        
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
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_subpestana_a2(self):
        
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A2 - Análisis Vertical")
        
        # Canvas con scroll
        canvas = tk.Canvas(tab, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        ttk.Label(
            scrollable_frame,
            text="A.2 ANÁLISIS VERTICAL DEL BALANCE - AÑO 2",
            font=Fonts.TITLE
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        # Realizar análisis vertical
        from core.analysis.analisis_vertical import AnalisisVerticalBalance
        analisis = AnalisisVerticalBalance(self.app.balance_data, 2)
        datos_tabla = analisis.get_tabla_analisis_vertical()
        
        # ============================================================
        # TABLA: Análisis Vertical
        # ============================================================
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Vertical - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        # Crear tabla con Treeview
        tree = ttk.Treeview(tabla_frame, columns=("Concepto", "Valor", "Porcentaje"), 
                        show="headings", height=15)
        
        tree.heading("Concepto", text="Concepto")
        tree.heading("Valor", text="Valor (Bs.)")
        tree.heading("Porcentaje", text="% del Activo Total")
        
        tree.column("Concepto", width=300, anchor="w")
        tree.column("Valor", width=150, anchor="e")
        tree.column("Porcentaje", width=150, anchor="e")
        
        # Insertar datos - ACTIVO
        tree.insert("", "end", values=("ACTIVO", "", ""), tags=("header",))
        tree.insert("", "end", values=(
            "  Activo Corriente",
            f"{analisis.activo_corriente:,.2f}",
            f"{analisis.pct_activo_corriente:.2f}%"
        ), tags=("bold",))
        tree.insert("", "end", values=(
            "    Caja y Bancos",
            f"{getattr(analisis.balance, f'caja_bancos_y2'):,.2f}",
            f"{analisis.pct_caja_bancos:.2f}%"
        ))
        tree.insert("", "end", values=(
            "    Clientes por Cobrar",
            f"{getattr(analisis.balance, f'clientes_cobrar_y2'):,.2f}",
            f"{analisis.pct_clientes:.2f}%"
        ))
        tree.insert("", "end", values=(
            "    Inversiones CP",
            f"{getattr(analisis.balance, f'inversion_cp_y2'):,.2f}",
            f"{analisis.pct_inversiones_cp:.2f}%"
        ))
        tree.insert("", "end", values=(
            "    Existencias",
            f"{getattr(analisis.balance, f'existencias_y2'):,.2f}",
            f"{analisis.pct_existencias:.2f}%"
        ))
        
        tree.insert("", "end", values=(
            "  Activo No Corriente",
            f"{analisis.activo_no_corriente:,.2f}",
            f"{analisis.pct_activo_no_corriente:.2f}%"
        ), tags=("bold",))
        
        tree.insert("", "end", values=(
            "TOTAL ACTIVO",
            f"{analisis.activo_total:,.2f}",
            "100.00%"
        ), tags=("total",))
        
        # Separador
        tree.insert("", "end", values=("", "", ""))
        
        # PASIVO Y PATRIMONIO
        tree.insert("", "end", values=("PASIVO Y PATRIMONIO", "", ""), tags=("header",))
        tree.insert("", "end", values=(
            "  Pasivo Corriente",
            f"{analisis.pasivo_corriente:,.2f}",
            f"{analisis.pct_pasivo_corriente:.2f}%"
        ), tags=("bold",))
        tree.insert("", "end", values=(
            "  Pasivo No Corriente",
            f"{analisis.pasivo_no_corriente:,.2f}",
            f"{analisis.pct_pasivo_no_corriente:.2f}%"
        ), tags=("bold",))
        tree.insert("", "end", values=(
            "  Patrimonio",
            f"{analisis.patrimonio:,.2f}",
            f"{analisis.pct_patrimonio:.2f}%"
        ), tags=("bold",))
        tree.insert("", "end", values=(
            "TOTAL PASIVO + PATRIMONIO",
            f"{analisis.pasivo_corriente + analisis.pasivo_no_corriente + analisis.patrimonio:,.2f}",
            "100.00%"
        ), tags=("total",))
        
        # Estilos de tags
        tree.tag_configure("header", background=Colors.PRIMARY, foreground="white", font=Fonts.HEADER)
        tree.tag_configure("bold", font=Fonts.NORMAL_BOLD)
        tree.tag_configure("total", background=Colors.SUCCESS, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # INTERPRETACIÓN
        # ============================================================
        interp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación de la Estructura ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        resumen = analisis.resumen_completo()
        
        # Estructura Económica
        ttk.Label(interp_frame, text="ESTRUCTURA ECONÓMICA:", 
                font=Fonts.HEADER, foreground=Colors.ACTIVO).pack(anchor='w', pady=(0, 5))
        
        text_economica = tk.Text(
            interp_frame,
            height=6,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_economica.pack(fill=tk.X, pady=(0, 15))
        text_economica.insert('1.0', resumen['estructura_economica'])
        text_economica.config(state='disabled')
        
        # Estructura Financiera
        ttk.Label(interp_frame, text="ESTRUCTURA FINANCIERA:", 
                font=Fonts.HEADER, foreground=Colors.PASIVO).pack(anchor='w', pady=(0, 5))
        
        text_financiera = tk.Text(
            interp_frame,
            height=6,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_financiera.pack(fill=tk.X)
        text_financiera.insert('1.0', resumen['estructura_financiera'])
        text_financiera.config(state='disabled')
        
        # Empaquetar canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    
    def crear_subpestana_a3(self):
        """Subpestaña A2 y A3"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A2 - A3")
        
        # Contenido placeholder
        content = ttk.Label(
            tab,
            text="A2 y A3\n(En desarrollo)",
            font=Fonts.SUBTITLE
        )
        content.pack(expand=True)
    
    def crear_subpestana_a4_a5(self):
        """Subpestaña A4 y A5"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A4 - A5")
        
        # Contenido placeholder
        content = ttk.Label(
            tab,
            text="A4 y A5\n(En desarrollo)",
            font=Fonts.SUBTITLE
        )
        content.pack(expand=True)