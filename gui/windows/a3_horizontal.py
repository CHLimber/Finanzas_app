"""
Archivo: gui/windows/a3_horizontal.py
Pestaña A3 - Análisis Horizontal
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions


class A3HorizontalTab(ttk.Frame):
    """Pestaña A3 - Análisis Horizontal"""
    
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
        # TABLA: Variaciones del Pasivo Corriente (DESCOMPUESTO)
        # ============================================================
        tabla_pc_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Horizontal - PASIVO CORRIENTE (Detallado) ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_pc_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        tree_pc = ttk.Treeview(
            tabla_pc_frame, 
            columns=("Concepto", "Año1", "Año2", "VarAbs", "VarPct"), 
            show="headings", 
            height=5
        )
        
        tree_pc.heading("Concepto", text="Concepto")
        tree_pc.heading("Año1", text="Año 1")
        tree_pc.heading("Año2", text="Año 2")
        tree_pc.heading("VarAbs", text="Variación (Bs.)")
        tree_pc.heading("VarPct", text="Variación (%)")
        
        tree_pc.column("Concepto", width=250, anchor="w")
        tree_pc.column("Año1", width=120, anchor="e")
        tree_pc.column("Año2", width=120, anchor="e")
        tree_pc.column("VarAbs", width=120, anchor="e")
        tree_pc.column("VarPct", width=100, anchor="e")
        
        # Obtener datos descompuestos del Pasivo Corriente
        balance = self.app.balance_data
        
        # Proveedores
        prov_y1 = balance.proveedores_y1
        prov_y2 = balance.proveedores_y2
        var_prov = prov_y2 - prov_y1
        var_prov_pct = (var_prov / prov_y1 * 100) if prov_y1 != 0 else 0
        
        # Impuestos
        imp_y1 = balance.impuestos_pagar_y1
        imp_y2 = balance.impuestos_pagar_y2
        var_imp = imp_y2 - imp_y1
        var_imp_pct = (var_imp / imp_y1 * 100) if imp_y1 != 0 else 0
        
        # Deuda CP
        deuda_y1 = balance.deuda_cp_y1
        deuda_y2 = balance.deuda_cp_y2
        var_deuda = deuda_y2 - deuda_y1
        var_deuda_pct = (var_deuda / deuda_y1 * 100) if deuda_y1 != 0 else 0
        
        # Total PC
        pc_y1 = balance.get_total_pasivo_corriente(1)
        pc_y2 = balance.get_total_pasivo_corriente(2)
        var_pc = pc_y2 - pc_y1
        var_pc_pct = (var_pc / pc_y1 * 100) if pc_y1 != 0 else 0
        
        # Insertar en el tree
        tree_pc.insert("", "end", values=(
            "  Proveedores y gastos por pagar",
            f"{prov_y1:,.2f}",
            f"{prov_y2:,.2f}",
            f"{var_prov:+,.2f}",
            f"{var_prov_pct:+.2f}%"
        ))
        
        tree_pc.insert("", "end", values=(
            "  Impuestos por pagar",
            f"{imp_y1:,.2f}",
            f"{imp_y2:,.2f}",
            f"{var_imp:+,.2f}",
            f"{var_imp_pct:+.2f}%"
        ))
        
        tree_pc.insert("", "end", values=(
            "  Deuda a corto plazo bancaria",
            f"{deuda_y1:,.2f}",
            f"{deuda_y2:,.2f}",
            f"{var_deuda:+,.2f}",
            f"{var_deuda_pct:+.2f}%"
        ))
        
        tree_pc.insert("", "end", values=(
            "TOTAL PASIVO CORRIENTE",
            f"{pc_y1:,.2f}",
            f"{pc_y2:,.2f}",
            f"{var_pc:+,.2f}",
            f"{var_pc_pct:+.2f}%"
        ), tags=("total",))
        
        tree_pc.tag_configure("total", background=Colors.PASIVO, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree_pc.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # TABLA: Variaciones del Pasivo No Corriente (DESCOMPUESTO)
        # ============================================================
        tabla_pnc_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Horizontal - PASIVO NO CORRIENTE (Detallado) ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_pnc_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        tree_pnc = ttk.Treeview(
            tabla_pnc_frame, 
            columns=("Concepto", "Año1", "Año2", "VarAbs", "VarPct"), 
            show="headings", 
            height=4
        )
        
        tree_pnc.heading("Concepto", text="Concepto")
        tree_pnc.heading("Año1", text="Año 1")
        tree_pnc.heading("Año2", text="Año 2")
        tree_pnc.heading("VarAbs", text="Variación (Bs.)")
        tree_pnc.heading("VarPct", text="Variación (%)")
        
        tree_pnc.column("Concepto", width=250, anchor="w")
        tree_pnc.column("Año1", width=120, anchor="e")
        tree_pnc.column("Año2", width=120, anchor="e")
        tree_pnc.column("VarAbs", width=120, anchor="e")
        tree_pnc.column("VarPct", width=100, anchor="e")
        
        # Préstamos LP
        prest_y1 = balance.prestamos_lp_y1
        prest_y2 = balance.prestamos_lp_y2
        var_prest = prest_y2 - prest_y1
        var_prest_pct = (var_prest / prest_y1 * 100) if prest_y1 != 0 else 0
        
        # Provisiones LP
        prov_lp_y1 = balance.provisiones_lp_y1
        prov_lp_y2 = balance.provisiones_lp_y2
        var_prov_lp = prov_lp_y2 - prov_lp_y1
        var_prov_lp_pct = (var_prov_lp / prov_lp_y1 * 100) if prov_lp_y1 != 0 else 0
        
        # Total PNC
        pnc_y1 = balance.get_total_pasivo_no_corriente(1)
        pnc_y2 = balance.get_total_pasivo_no_corriente(2)
        var_pnc = pnc_y2 - pnc_y1
        var_pnc_pct = (var_pnc / pnc_y1 * 100) if pnc_y1 != 0 else 0
        
        tree_pnc.insert("", "end", values=(
            "  Préstamos a largo plazo (5% anual)",
            f"{prest_y1:,.2f}",
            f"{prest_y2:,.2f}",
            f"{var_prest:+,.2f}",
            f"{var_prest_pct:+.2f}%"
        ))
        
        tree_pnc.insert("", "end", values=(
            "  Provisiones a largo plazo",
            f"{prov_lp_y1:,.2f}",
            f"{prov_lp_y2:,.2f}",
            f"{var_prov_lp:+,.2f}",
            f"{var_prov_lp_pct:+.2f}%"
        ))
        
        tree_pnc.insert("", "end", values=(
            "TOTAL PASIVO NO CORRIENTE",
            f"{pnc_y1:,.2f}",
            f"{pnc_y2:,.2f}",
            f"{var_pnc:+,.2f}",
            f"{var_pnc_pct:+.2f}%"
        ), tags=("total",))
        
        tree_pnc.tag_configure("total", background=Colors.PASIVO, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree_pnc.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # TABLA: Variaciones del Patrimonio (DESCOMPUESTO)
        # ============================================================
        tabla_pat_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Análisis Horizontal - PATRIMONIO (Detallado) ",
            padding=Dimensions.PADDING_LARGE
        )
        tabla_pat_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        tree_pat = ttk.Treeview(
            tabla_pat_frame, 
            columns=("Concepto", "Año1", "Año2", "VarAbs", "VarPct"), 
            show="headings", 
            height=5
        )
        
        tree_pat.heading("Concepto", text="Concepto")
        tree_pat.heading("Año1", text="Año 1")
        tree_pat.heading("Año2", text="Año 2")
        tree_pat.heading("VarAbs", text="Variación (Bs.)")
        tree_pat.heading("VarPct", text="Variación (%)")
        
        tree_pat.column("Concepto", width=250, anchor="w")
        tree_pat.column("Año1", width=120, anchor="e")
        tree_pat.column("Año2", width=120, anchor="e")
        tree_pat.column("VarAbs", width=120, anchor="e")
        tree_pat.column("VarPct", width=100, anchor="e")
        
        # Capital Social
        cap_y1 = balance.capital_social_y1
        cap_y2 = balance.capital_social_y2
        var_cap = cap_y2 - cap_y1
        var_cap_pct = (var_cap / cap_y1 * 100) if cap_y1 != 0 else 0
        
        # Reservas Legales
        res_y1 = balance.reservas_legales_y1
        res_y2 = balance.reservas_legales_y2
        var_res = res_y2 - res_y1
        var_res_pct = (var_res / res_y1 * 100) if res_y1 != 0 else 0
        
        # Ganancias Acumuladas
        gan_y1 = balance.ganancias_acum_y1
        gan_y2 = balance.ganancias_acum_y2
        var_gan = gan_y2 - gan_y1
        var_gan_pct = (var_gan / gan_y1 * 100) if gan_y1 != 0 else 0
        
        # Total Patrimonio
        pat_y1 = balance.get_total_patrimonio(1)
        pat_y2 = balance.get_total_patrimonio(2)
        var_pat = pat_y2 - pat_y1
        var_pat_pct = (var_pat / pat_y1 * 100) if pat_y1 != 0 else 0
        
        tree_pat.insert("", "end", values=(
            "  Capital Social",
            f"{cap_y1:,.2f}",
            f"{cap_y2:,.2f}",
            f"{var_cap:+,.2f}",
            f"{var_cap_pct:+.2f}%"
        ))
        
        tree_pat.insert("", "end", values=(
            "  Reservas Legales",
            f"{res_y1:,.2f}",
            f"{res_y2:,.2f}",
            f"{var_res:+,.2f}",
            f"{var_res_pct:+.2f}%"
        ))
        
        tree_pat.insert("", "end", values=(
            "  Ganancias Acumuladas",
            f"{gan_y1:,.2f}",
            f"{gan_y2:,.2f}",
            f"{var_gan:+,.2f}",
            f"{var_gan_pct:+.2f}%"
        ))
        
        tree_pat.insert("", "end", values=(
            "TOTAL PATRIMONIO",
            f"{pat_y1:,.2f}",
            f"{pat_y2:,.2f}",
            f"{var_pat:+,.2f}",
            f"{var_pat_pct:+.2f}%"
        ), tags=("total",))
        
        tree_pat.tag_configure("total", background=Colors.PATRIMONIO, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree_pat.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # INTERPRETACIÓN MEJORADA
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
        
        # 2. ¿Cómo se financió el crecimiento? (CON DETALLES)
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
        
        # 3. Interpretación Detallada del Pasivo Corriente
        ttk.Label(interp_frame, text="3. DETALLE DEL PASIVO CORRIENTE", 
                font=Fonts.HEADER, foreground=Colors.PASIVO).pack(anchor='w', pady=(0, 5))
        
        # Generar interpretación específica del PC
        interpretacion_pc = f"""
    Proveedores: {'Aumentó' if var_prov > 0 else 'Disminuyó'} en {abs(var_prov):,.2f} Bs. ({abs(var_prov_pct):.2f}%). {'Esto indica mayor financiamiento de proveedores.' if var_prov > 0 else 'Indica pago a proveedores o reducción de compras a crédito.'}

    Impuestos por Pagar: {'Aumentó' if var_imp > 0 else 'Disminuyó'} en {abs(var_imp):,.2f} Bs. ({abs(var_imp_pct):.2f}%). {'Mayor actividad operativa genera más obligaciones tributarias.' if var_imp > 0 else 'Reducción en obligaciones fiscales.'}

    Deuda Bancaria CP: {'Aumentó' if var_deuda > 0 else 'Disminuyó'} en {abs(var_deuda):,.2f} Bs. ({abs(var_deuda_pct):.2f}%). {'Mayor dependencia de financiamiento bancario de corto plazo.' if var_deuda > 0 else 'Reducción de deuda bancaria, mejorando la salud financiera.'}
        """.strip()
        
        text_pc_det = tk.Text(
            interp_frame,
            height=6,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_pc_det.pack(fill=tk.X, pady=(0, 15))
        text_pc_det.insert('1.0', interpretacion_pc)
        text_pc_det.config(state='disabled')
        
        # 4. Interpretación Detallada del Patrimonio
        ttk.Label(interp_frame, text="4. DETALLE DEL PATRIMONIO", 
                font=Fonts.HEADER, foreground=Colors.PATRIMONIO).pack(anchor='w', pady=(0, 5))
        
        # Generar interpretación específica del Patrimonio
        interpretacion_pat = f"""
    Capital Social: {'Aumentó' if var_cap > 0 else 'Disminuyó' if var_cap < 0 else 'Se mantuvo'} en {abs(var_cap):,.2f} Bs. {'(Capitalización o nuevos aportes de socios)' if var_cap > 0 else '(Reducción de capital o retiro de socios)' if var_cap < 0 else '(Sin cambios en aportes)'}

    Reservas Legales: {'Aumentó' if var_res > 0 else 'Disminuyó' if var_res < 0 else 'Se mantuvo'} en {abs(var_res):,.2f} Bs. {'Retención de utilidades para cumplir requisitos legales.' if var_res > 0 else ''}

    Ganancias Acumuladas: {'Aumentó' if var_gan > 0 else 'Disminuyó' if var_gan < 0 else 'Se mantuvo'} en {abs(var_gan):,.2f} Bs. ({abs(var_gan_pct):.2f}%). {'Reinversión de utilidades en el negocio.' if var_gan > 0 else 'Distribución de dividendos o pérdidas del período.' if var_gan < 0 else 'Sin cambios significativos.'}

    CONCLUSIÓN: El patrimonio {'se fortaleció' if var_pat > 0 else 'se debilitó'} principalmente {'por retención de utilidades' if abs(var_gan) > abs(var_cap) and var_gan > 0 else 'por nuevos aportes de capital' if var_cap > 0 else 'por distribución de dividendos'}.
        """.strip()
        
        text_pat_det = tk.Text(
            interp_frame,
            height=7,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_pat_det.pack(fill=tk.X, pady=(0, 15))
        text_pat_det.insert('1.0', interpretacion_pat)
        text_pat_det.config(state='disabled')
        
        # 5. Conclusión General
        ttk.Label(interp_frame, text="5. CONCLUSIÓN GENERAL", 
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