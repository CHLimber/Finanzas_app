"""
Archivo: gui/windows/a2_vertical.py
Pestana A2 - Analisis Vertical con desglose completo
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions
from core.analysis.analisis_vertical import AnalisisVerticalBalance


class A2VerticalTab(ttk.Frame):
    """Pestana A2 - Analisis Vertical"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        canvas = tk.Canvas(self, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        ttk.Label(
            scrollable_frame,
            text="A.2 ANALISIS VERTICAL DEL BALANCE",
            font=Fonts.TITLE
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener analisis de ambos anos
        analisis_y1 = AnalisisVerticalBalance(self.app.balance_data, 1)
        analisis_y2 = AnalisisVerticalBalance(self.app.balance_data, 2)
        
        # TABLA COMPARATIVA
        tabla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Analisis Vertical Comparativo ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        # Crear Treeview con 5 columnas
        tree = ttk.Treeview(
            tabla_frame, 
            columns=("Concepto", "Valor_Y1", "Pct_Y1", "Valor_Y2", "Pct_Y2"), 
            show="headings", 
            height=28
        )
        
        tree.heading("Concepto", text="Concepto")
        tree.heading("Valor_Y1", text="Ano 1 (Bs.)")
        tree.heading("Pct_Y1", text="% Ano 1")
        tree.heading("Valor_Y2", text="Ano 2 (Bs.)")
        tree.heading("Pct_Y2", text="% Ano 2")
        
        tree.column("Concepto", width=280, anchor="w")
        tree.column("Valor_Y1", width=120, anchor="e")
        tree.column("Pct_Y1", width=80, anchor="e")
        tree.column("Valor_Y2", width=120, anchor="e")
        tree.column("Pct_Y2", width=80, anchor="e")
        
        # ==================== ACTIVO ====================
        tree.insert("", "end", values=("ACTIVO", "", "", "", ""), tags=("header",))
        
        # Activo Corriente - Titulo
        tree.insert("", "end", values=(
            "  Activo Corriente",
            f"{analisis_y1.activo_corriente:,.2f}",
            f"{analisis_y1.pct_activo_corriente:.2f}%",
            f"{analisis_y2.activo_corriente:,.2f}",
            f"{analisis_y2.pct_activo_corriente:.2f}%"
        ), tags=("subtotal",))
        
        # Desglose Activo Corriente
        tree.insert("", "end", values=(
            "      Caja y Bancos",
            f"{self.app.balance_data.caja_bancos_y1:,.2f}",
            f"{analisis_y1.pct_caja_bancos:.2f}%",
            f"{self.app.balance_data.caja_bancos_y2:,.2f}",
            f"{analisis_y2.pct_caja_bancos:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Clientes por Cobrar",
            f"{self.app.balance_data.clientes_cobrar_y1:,.2f}",
            f"{analisis_y1.pct_clientes:.2f}%",
            f"{self.app.balance_data.clientes_cobrar_y2:,.2f}",
            f"{analisis_y2.pct_clientes:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Inversiones CP",
            f"{self.app.balance_data.inversion_cp_y1:,.2f}",
            f"{analisis_y1.pct_inversiones_cp:.2f}%",
            f"{self.app.balance_data.inversion_cp_y2:,.2f}",
            f"{analisis_y2.pct_inversiones_cp:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Existencias",
            f"{self.app.balance_data.existencias_y1:,.2f}",
            f"{analisis_y1.pct_existencias:.2f}%",
            f"{self.app.balance_data.existencias_y2:,.2f}",
            f"{analisis_y2.pct_existencias:.2f}%"
        ))
        
        # Activo No Corriente - Titulo
        tree.insert("", "end", values=(
            "  Activo No Corriente",
            f"{analisis_y1.activo_no_corriente:,.2f}",
            f"{analisis_y1.pct_activo_no_corriente:.2f}%",
            f"{analisis_y2.activo_no_corriente:,.2f}",
            f"{analisis_y2.pct_activo_no_corriente:.2f}%"
        ), tags=("subtotal",))
        
        # Desglose Activo No Corriente (valores netos)
        inmuebles_neto_y1 = self.app.balance_data.inmuebles_planta_y1 - self.app.balance_data.depreciacion_acum_y1
        inmuebles_neto_y2 = self.app.balance_data.inmuebles_planta_y2 - self.app.balance_data.depreciacion_acum_y2
        intangibles_neto_y1 = self.app.balance_data.intangibles_y1 - self.app.balance_data.depreciacion_intang_y1
        intangibles_neto_y2 = self.app.balance_data.intangibles_y2 - self.app.balance_data.depreciacion_intang_y2
        
        tree.insert("", "end", values=(
            "      Inmuebles, Planta y Eq. (neto)",
            f"{inmuebles_neto_y1:,.2f}",
            f"{analisis_y1.pct_inmuebles:.2f}%",
            f"{inmuebles_neto_y2:,.2f}",
            f"{analisis_y2.pct_inmuebles:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Intangibles (neto)",
            f"{intangibles_neto_y1:,.2f}",
            f"{analisis_y1.pct_intangibles:.2f}%",
            f"{intangibles_neto_y2:,.2f}",
            f"{analisis_y2.pct_intangibles:.2f}%"
        ))
        
        # TOTAL ACTIVO
        tree.insert("", "end", values=(
            "TOTAL ACTIVO",
            f"{analisis_y1.activo_total:,.2f}",
            "100.00%",
            f"{analisis_y2.activo_total:,.2f}",
            "100.00%"
        ), tags=("total",))
        
        # Linea en blanco
        tree.insert("", "end", values=("", "", "", "", ""))
        
        # ==================== PASIVO Y PATRIMONIO ====================
        tree.insert("", "end", values=("PASIVO Y PATRIMONIO", "", "", "", ""), tags=("header",))
        
        # Pasivo Corriente - Titulo
        tree.insert("", "end", values=(
            "  Pasivo Corriente",
            f"{analisis_y1.pasivo_corriente:,.2f}",
            f"{analisis_y1.pct_pasivo_corriente:.2f}%",
            f"{analisis_y2.pasivo_corriente:,.2f}",
            f"{analisis_y2.pct_pasivo_corriente:.2f}%"
        ), tags=("subtotal",))
        
        # Desglose Pasivo Corriente
        tree.insert("", "end", values=(
            "      Proveedores y Gastos por Pagar",
            f"{self.app.balance_data.proveedores_y1:,.2f}",
            f"{analisis_y1.pct_proveedores:.2f}%",
            f"{self.app.balance_data.proveedores_y2:,.2f}",
            f"{analisis_y2.pct_proveedores:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Impuestos por Pagar",
            f"{self.app.balance_data.impuestos_pagar_y1:,.2f}",
            f"{analisis_y1.pct_impuestos:.2f}%",
            f"{self.app.balance_data.impuestos_pagar_y2:,.2f}",
            f"{analisis_y2.pct_impuestos:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Deuda CP Bancaria",
            f"{self.app.balance_data.deuda_cp_y1:,.2f}",
            f"{analisis_y1.pct_deuda_cp:.2f}%",
            f"{self.app.balance_data.deuda_cp_y2:,.2f}",
            f"{analisis_y2.pct_deuda_cp:.2f}%"
        ))
        
        # Pasivo No Corriente - Titulo
        tree.insert("", "end", values=(
            "  Pasivo No Corriente",
            f"{analisis_y1.pasivo_no_corriente:,.2f}",
            f"{analisis_y1.pct_pasivo_no_corriente:.2f}%",
            f"{analisis_y2.pasivo_no_corriente:,.2f}",
            f"{analisis_y2.pct_pasivo_no_corriente:.2f}%"
        ), tags=("subtotal",))
        
        # Desglose Pasivo No Corriente
        tree.insert("", "end", values=(
            "      Prestamos LP (5% anual)",
            f"{self.app.balance_data.prestamos_lp_y1:,.2f}",
            f"{analisis_y1.pct_prestamos_lp:.2f}%",
            f"{self.app.balance_data.prestamos_lp_y2:,.2f}",
            f"{analisis_y2.pct_prestamos_lp:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Provisiones LP",
            f"{self.app.balance_data.provisiones_lp_y1:,.2f}",
            f"{analisis_y1.pct_provisiones_lp:.2f}%",
            f"{self.app.balance_data.provisiones_lp_y2:,.2f}",
            f"{analisis_y2.pct_provisiones_lp:.2f}%"
        ))
        
        # Patrimonio - Titulo
        tree.insert("", "end", values=(
            "  Patrimonio",
            f"{analisis_y1.patrimonio:,.2f}",
            f"{analisis_y1.pct_patrimonio:.2f}%",
            f"{analisis_y2.patrimonio:,.2f}",
            f"{analisis_y2.pct_patrimonio:.2f}%"
        ), tags=("subtotal",))
        
        # Desglose Patrimonio
        tree.insert("", "end", values=(
            "      Capital Social",
            f"{self.app.balance_data.capital_social_y1:,.2f}",
            f"{analisis_y1.pct_capital:.2f}%",
            f"{self.app.balance_data.capital_social_y2:,.2f}",
            f"{analisis_y2.pct_capital:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Reservas Legales",
            f"{self.app.balance_data.reservas_legales_y1:,.2f}",
            f"{analisis_y1.pct_reservas:.2f}%",
            f"{self.app.balance_data.reservas_legales_y2:,.2f}",
            f"{analisis_y2.pct_reservas:.2f}%"
        ))
        tree.insert("", "end", values=(
            "      Ganancias Acumuladas",
            f"{self.app.balance_data.ganancias_acum_y1:,.2f}",
            f"{analisis_y1.pct_ganancias_acum:.2f}%",
            f"{self.app.balance_data.ganancias_acum_y2:,.2f}",
            f"{analisis_y2.pct_ganancias_acum:.2f}%"
        ))
        
        # TOTAL PASIVO + PATRIMONIO
        total_pp_y1 = analisis_y1.pasivo_corriente + analisis_y1.pasivo_no_corriente + analisis_y1.patrimonio
        total_pp_y2 = analisis_y2.pasivo_corriente + analisis_y2.pasivo_no_corriente + analisis_y2.patrimonio
        
        tree.insert("", "end", values=(
            "TOTAL PASIVO + PATRIMONIO",
            f"{total_pp_y1:,.2f}",
            "100.00%",
            f"{total_pp_y2:,.2f}",
            "100.00%"
        ), tags=("total",))
        
        # Configurar estilos de las filas
        tree.tag_configure("header", background=Colors.PRIMARY, foreground="white", font=Fonts.HEADER)
        tree.tag_configure("subtotal", font=Fonts.NORMAL_BOLD, background="#e8e8e8")
        tree.tag_configure("total", background=Colors.SUCCESS, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # INTERPRETACION
        interp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretacion de la Estructura (Ano 2) ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        resumen = analisis_y2.resumen_completo()
        
        ttk.Label(interp_frame, text="ESTRUCTURA ECONOMICA:", 
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