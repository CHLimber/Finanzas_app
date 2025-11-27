"""
Archivo: gui/windows/analisis_patrimonial.py
Pestaña de Análisis Patrimonial con SISTEMA HÍBRIDO de actualización
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
    """Pestaña con sistema híbrido: indicador + botón actualizar"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.sub_notebook = None
        self.titulo_frame = None
        self.datos_desactualizados = False
        self.label_estado = None
        self.btn_actualizar = None
        
        self.crear_interfaz()
        
        # Suscribirse para marcar como desactualizado cuando cambien datos
        if hasattr(self.app, 'on_data_change_callbacks'):
            self.app.on_data_change_callbacks.append(self.marcar_desactualizado)
    
    def crear_interfaz(self):
        """Crea la interfaz con subpestañas"""
        
        # Limpiar contenido anterior si existe
        for widget in self.winfo_children():
            widget.destroy()
        
        # Frame superior con título, indicador y botón
        self.titulo_frame = ttk.Frame(self)
        self.titulo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Título a la izquierda
        ttk.Label(
            self.titulo_frame,
            text="ANÁLISIS PATRIMONIAL",
            font=Fonts.TITLE
        ).pack(side=tk.LEFT, padx=10)
        
        # Indicador de estado (aparece cuando hay cambios)
        self.label_estado = tk.Label(
            self.titulo_frame,
            text="⚠️ Datos modificados - Clic en Actualizar",
            font=Fonts.NORMAL,
            bg=Colors.WARNING,
            fg="white",
            padx=10,
            pady=5,
            relief="raised"
        )
        if self.datos_desactualizados:
            self.label_estado.pack(side=tk.LEFT, padx=10)
        
        # Botón actualizar a la derecha
        self.btn_actualizar = tk.Button(
            self.titulo_frame,
            text="🔄 Actualizar Análisis",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.INFO,
            fg="white",
            activebackground="#138d75",
            activeforeground="white",
            cursor="hand2",
            relief="raised",
            borderwidth=2,
            padx=15,
            pady=5,
            command=self.actualizar_contenido
        )
        self.btn_actualizar.pack(side=tk.RIGHT, padx=10)
        
        # Notebook secundario para subpestañas
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Crear subpestañas
        self.crear_subpestana_a1()
        self.crear_subpestana_a2()
        self.crear_subpestana_a3()
        self.crear_subpestana_a4_a5()
        
        # Marcar como actualizado después de crear
        self.datos_desactualizados = False
        if self.label_estado:
            self.label_estado.pack_forget()
    
    def marcar_desactualizado(self):
        """
        Se llama automáticamente cuando se modifican datos en Balance/Estado.
        Muestra el indicador visual sin actualizar aún.
        """
        self.datos_desactualizados = True
        if self.label_estado and self.label_estado.winfo_exists():
            self.label_estado.pack(side=tk.LEFT, padx=10)
            # Hacer parpadear el botón actualizar
            if self.btn_actualizar and self.btn_actualizar.winfo_exists():
                self.btn_actualizar.config(bg=Colors.SUCCESS)
                self.after(300, lambda: self.btn_actualizar.config(bg=Colors.INFO))
    
    def actualizar_contenido(self):
        """
        Actualiza manualmente el contenido cuando el usuario hace clic.
        Cierra figuras de matplotlib antes de recrear.
        """
        try:
            # Cerrar todas las figuras de matplotlib para liberar memoria
            import matplotlib.pyplot as plt
            plt.close('all')
            
            # Recrear toda la interfaz con datos actualizados
            self.crear_interfaz()
            
            print("✅ Análisis patrimonial actualizado correctamente")
            
        except Exception as e:
            print(f"❌ Error al actualizar análisis patrimonial: {e}")
            # Mostrar error al usuario
            if hasattr(self, 'label_estado') and self.label_estado:
                self.label_estado.config(
                    text=f"❌ Error al actualizar: {str(e)[:50]}...",
                    bg=Colors.DANGER
                )
    
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
        
        # TABLA: Fondo de Maniobra
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Fondo de Maniobra ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                        pady=Dimensions.PADDING_MEDIUM)
        
        ttk.Label(tabla_frame, text="", font=Fonts.HEADER).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(tabla_frame, text="Año 1", font=Fonts.HEADER).grid(
            row=0, column=1, padx=10, pady=5)
        ttk.Label(tabla_frame, text="Año 2", font=Fonts.HEADER).grid(
            row=0, column=2, padx=10, pady=5)
        
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
        
        # GRÁFICO: Evolución
        grafico1_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Gráfico de Evolución ",
            padding=Dimensions.PADDING_LARGE
        )
        grafico1_frame.pack(fill=tk.BOTH, expand=True,
                           padx=Dimensions.PADDING_XLARGE,
                           pady=Dimensions.PADDING_MEDIUM)
        
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
    
    def crear_subpestana_a2(self):
        """Subpestaña A2 - Análisis Vertical"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A2 - Análisis Vertical")
        
        canvas = tk.Canvas(tab, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        ttk.Label(
            scrollable_frame,
            text="A.2 ANÁLISIS VERTICAL DEL BALANCE - AÑO 2",
            font=Fonts.TITLE
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        analisis = AnalisisVerticalBalance(self.app.balance_data, 2)
        
        # TABLA
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Vertical - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        tree = ttk.Treeview(tabla_frame, columns=("Concepto", "Valor", "Porcentaje"), 
                        show="headings", height=15)
        
        tree.heading("Concepto", text="Concepto")
        tree.heading("Valor", text="Valor (Bs.)")
        tree.heading("Porcentaje", text="% del Activo Total")
        
        tree.column("Concepto", width=300, anchor="w")
        tree.column("Valor", width=150, anchor="e")
        tree.column("Porcentaje", width=150, anchor="e")
        
        # ACTIVO
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
        
        tree.tag_configure("header", background=Colors.PRIMARY, foreground="white", font=Fonts.HEADER)
        tree.tag_configure("bold", font=Fonts.NORMAL_BOLD)
        tree.tag_configure("total", background=Colors.SUCCESS, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # INTERPRETACIÓN
        interp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación de la Estructura ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        resumen = analisis.resumen_completo()
        
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
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def crear_subpestana_a3(self):
        """Subpestaña A3 - Análisis Horizontal"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A3 - Análisis Horizontal")
        
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
            text="A.3 ANÁLISIS HORIZONTAL - EVOLUCIÓN AÑO 1 vs AÑO 2",
            font=Fonts.TITLE
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        # Realizar análisis horizontal
        from core.analysis.analisis_horizontal import AnalisisHorizontalBalance
        analisis = AnalisisHorizontalBalance(self.app.balance_data)
        datos_tabla = analisis.get_tabla_variaciones()
        
        # ============================================================
        # TABLA: Variaciones del Activo
        # ============================================================
        tabla_activo_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Horizontal - ACTIVOS ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_activo_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                            pady=Dimensions.PADDING_MEDIUM)
        
        tree_activo = ttk.Treeview(
            tabla_activo_frame, 
            columns=("Concepto", "Año1", "Año2", "VarAbs", "VarPct"), 
            show="headings", 
            height=10
        )
        
        tree_activo.heading("Concepto", text="Concepto")
        tree_activo.heading("Año1", text="Año 1")
        tree_activo.heading("Año2", text="Año 2")
        tree_activo.heading("VarAbs", text="Variación (Bs.)")
        tree_activo.heading("VarPct", text="Variación (%)")
        
        tree_activo.column("Concepto", width=250, anchor="w")
        tree_activo.column("Año1", width=120, anchor="e")
        tree_activo.column("Año2", width=120, anchor="e")
        tree_activo.column("VarAbs", width=120, anchor="e")
        tree_activo.column("VarPct", width=100, anchor="e")
        
        # Insertar datos de activos
        for concepto, y1, y2, var_abs, var_pct in datos_tabla['activos']:
            tag = ()
            if "TOTAL" in concepto:
                tag = ("total",)
            elif "Activo Corriente" == concepto or "Activo No Corriente" == concepto:
                tag = ("bold",)
            
            tree_activo.insert("", "end", values=(
                concepto,
                f"{y1:,.2f}",
                f"{y2:,.2f}",
                f"{var_abs:+,.2f}",
                f"{var_pct:+.2f}%"
            ), tags=tag)
        
        tree_activo.tag_configure("total", background=Colors.SUCCESS, foreground="white", font=Fonts.NORMAL_BOLD)
        tree_activo.tag_configure("bold", font=Fonts.NORMAL_BOLD)
        
        tree_activo.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # TABLA: Variaciones del Pasivo y Patrimonio
        # ============================================================
        tabla_pasivo_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Horizontal - PASIVO Y PATRIMONIO ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_pasivo_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                            pady=Dimensions.PADDING_MEDIUM)
        
        tree_pasivo = ttk.Treeview(
            tabla_pasivo_frame, 
            columns=("Concepto", "Año1", "Año2", "VarAbs", "VarPct"), 
            show="headings", 
            height=5
        )
        
        tree_pasivo.heading("Concepto", text="Concepto")
        tree_pasivo.heading("Año1", text="Año 1")
        tree_pasivo.heading("Año2", text="Año 2")
        tree_pasivo.heading("VarAbs", text="Variación (Bs.)")
        tree_pasivo.heading("VarPct", text="Variación (%)")
        
        tree_pasivo.column("Concepto", width=250, anchor="w")
        tree_pasivo.column("Año1", width=120, anchor="e")
        tree_pasivo.column("Año2", width=120, anchor="e")
        tree_pasivo.column("VarAbs", width=120, anchor="e")
        tree_pasivo.column("VarPct", width=100, anchor="e")
        
        # Insertar datos de pasivo y patrimonio
        for concepto, y1, y2, var_abs, var_pct in datos_tabla['pasivo_patrimonio']:
            tag = ()
            if "TOTAL" in concepto:
                tag = ("total",)
            
            tree_pasivo.insert("", "end", values=(
                concepto,
                f"{y1:,.2f}",
                f"{y2:,.2f}",
                f"{var_abs:+,.2f}",
                f"{var_pct:+.2f}%"
            ), tags=tag)
        
        tree_pasivo.tag_configure("total", background=Colors.SUCCESS, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree_pasivo.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # INTERPRETACIÓN
        # ============================================================
        interp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación del Análisis Horizontal ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        analisis_completo = analisis.analisis_completo()
        
        # 1. ¿Qué activos crecieron más?
        ttk.Label(interp_frame, text="1. ¿QUÉ ACTIVOS CRECIERON MÁS?", 
                font=Fonts.HEADER, foreground=Colors.ACTIVO).pack(anchor='w', pady=(0, 5))
        
        text_activos = tk.Text(
            interp_frame,
            height=5,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_activos.pack(fill=tk.X, pady=(0, 15))
        text_activos.insert('1.0', analisis_completo['interpretacion_activos'])
        text_activos.config(state='disabled')
        
        # 2. ¿Cómo se financió el crecimiento?
        ttk.Label(interp_frame, text="2. ¿CÓMO SE FINANCIÓ EL CRECIMIENTO?", 
                font=Fonts.HEADER, foreground=Colors.PASIVO).pack(anchor='w', pady=(0, 5))
        
        text_financiamiento = tk.Text(
            interp_frame,
            height=5,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_financiamiento.pack(fill=tk.X, pady=(0, 15))
        text_financiamiento.insert('1.0', analisis_completo['interpretacion_financiamiento'])
        text_financiamiento.config(state='disabled')
        
        # 3. Conclusión General
        ttk.Label(interp_frame, text="3. CONCLUSIÓN GENERAL", 
                font=Fonts.HEADER, foreground=Colors.PRIMARY).pack(anchor='w', pady=(0, 5))
        
        conclusion_label = tk.Label(
            interp_frame,
            text=analisis_completo['conclusion'],
            font=Fonts.NORMAL_BOLD,
            bg=Colors.INFO,
            fg="white",
            wraplength=700,
            justify="left",
            padx=15,
            pady=15,
            relief="raised",
            borderwidth=2
        )
        conclusion_label.pack(fill=tk.X)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_subpestana_a4_a5(self):
        """Subpestaña A4 y A5"""
        tab = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(tab, text="A4 - A5")
        
        content = ttk.Label(
            tab,
            text="A4 y A5\n(En desarrollo)",
            font=Fonts.SUBTITLE
        )
        content.pack(expand=True)