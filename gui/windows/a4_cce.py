"""
Archivo: gui/windows/a4_cce.py
Pestaña A4 - Ciclo de Conversión de Efectivo
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions
from core.analysis.ciclo_conversion_efectivo import CicloConversionEfectivo


class A4CCETab(ttk.Frame):
    """Pestaña A4 - Ciclo de Conversión de Efectivo"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):

        # Canvas con scroll
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
            text="A.4 CICLO DE CONVERSIÓN DE EFECTIVO (CCE)",
            font=Fonts.TITLE
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        # Descripción
        desc_frame = ttk.Frame(scrollable_frame)
        desc_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, pady=Dimensions.PADDING_MEDIUM)
        
        desc_text = (
            "El Ciclo de Conversión de Efectivo mide el tiempo (en días) que transcurre desde "
            "que la empresa paga a sus proveedores hasta que cobra de sus clientes.\n\n"
            "CCE = Días de Inventario + Días de Clientes - Días de Proveedores"
        )
        
        tk.Label(
            desc_frame,
            text=desc_text,
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            wraplength=800,
            justify="left",
            padx=15,
            pady=15,
            relief="solid",
            borderwidth=1
        ).pack(fill=tk.X)
        
        # Realizar análisis
        from core.analysis.ciclo_conversion_efectivo import CicloConversionEfectivo
        analisis_cce = CicloConversionEfectivo(self.app.balance_data, self.app.income_data)
        resultado = analisis_cce.analisis_dual()
        
        # ============================================================
        # selfLA: Componentes del CCE
        # ============================================================
        selfla_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Componentes del Ciclo de Conversión de Efectivo ",
            padding=Dimensions.PADDING_LARGE
        )
        selfla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        tree = ttk.Treeview(
            selfla_frame, 
            columns=("Concepto", "Año2"), 
            show="headings", 
            height=5
        )
        
        tree.heading("Concepto", text="Concepto")
        tree.heading("Año2", text="Año 2 (días)")
        
        tree.column("Concepto", width=300, anchor="w")
        tree.column("Año2", width=150, anchor="e")
        
        # Insertar datos
        y2 = resultado["year_2"]
        
        tree.insert("", "end", values=(
            "Días de Inventario (DI)",
            f"{y2['dias_inventario']:.1f}"
        ))
        
        tree.insert("", "end", values=(
            "Días de Clientes (DC)",
            f"{y2['dias_clientes']:.1f}"
        ))
        
        tree.insert("", "end", values=(
            "Días de Proveedores (DP)",
            f"{y2['dias_proveedores']:.1f}"
        ))
        
        tree.insert("", "end", values=(
            "CICLO DE CONVERSIÓN DE EFECTIVO",
            f"{y2['cce']:.1f}",

        ), tags=("total",))
        
        tree.tag_configure("total", background=Colors.INFO, foreground="white", font=Fonts.NORMAL_BOLD)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # ============================================================
        # INTERPRETACIÓN DE COMPONENTES - AÑO 2
        # ============================================================
        interp_comp_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación de Componentes - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_comp_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                            pady=Dimensions.PADDING_MEDIUM)
        
        # Días de Inventario
        ttk.Label(interp_comp_frame, text="📦 DÍAS DE INVENTARIO:", 
                font=Fonts.HEADER, foreground=Colors.ACTIVO).pack(anchor='w', pady=(0, 5))
        
        text_di = tk.Text(
            interp_comp_frame,
            height=2,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        text_di.pack(fill=tk.X, pady=(0, 10))
        text_di.insert('1.0', y2['interpretacion_di'])
        text_di.config(state='disabled')
        
        # Días de Clientes
        ttk.Label(interp_comp_frame, text="💰 DÍAS DE CLIENTES (COBRANZA):", 
                font=Fonts.HEADER, foreground=Colors.ACTIVO).pack(anchor='w', pady=(0, 5))
        
        text_dc = tk.Text(
            interp_comp_frame,
            height=2,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        text_dc.pack(fill=tk.X, pady=(0, 10))
        text_dc.insert('1.0', y2['interpretacion_dc'])
        text_dc.config(state='disabled')
        
        # Días de Proveedores
        ttk.Label(interp_comp_frame, text="🤝 DÍAS DE PROVEEDORES (PAGO):", 
                font=Fonts.HEADER, foreground=Colors.PASIVO).pack(anchor='w', pady=(0, 5))
        
        text_dp = tk.Text(
            interp_comp_frame,
            height=2,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        text_dp.pack(fill=tk.X)
        text_dp.insert('1.0', y2['interpretacion_dp'])
        text_dp.config(state='disabled')
        
        # ============================================================
        # INTERPRETACIÓN DEL CCE - AÑO 2
        # ============================================================
        interp_cce_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Interpretación del CCE - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        interp_cce_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                            pady=Dimensions.PADDING_MEDIUM)
        
        # Determinar color según CCE
        cce_y2 = y2['cce']
        if cce_y2 <= 20:
            bg_color = Colors.SUCCESS
        elif cce_y2 <= 40:
            bg_color = Colors.INFO
        elif cce_y2 <= 60:
            bg_color = Colors.WARNING
        else:
            bg_color = Colors.DANGER
        
        cce_label = tk.Label(
            interp_cce_frame,
            text=y2['interpretacion_cce'],
            font=Fonts.NORMAL_BOLD,
            bg=bg_color,
            fg="white",
            wraplength=700,
            justify="left",
            padx=15,
            pady=15,
            relief="raised",
            borderwidth=2
        )
        cce_label.pack(fill=tk.X)
        
        # ============================================================
        # TENDENCIA ENTRE AÑOS
        # ============================================================
        """
        tend_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Tendencia del CCE ",
            padding=Dimensions.PADDING_LARGE
        )
        tend_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                    pady=Dimensions.PADDING_MEDIUM)
        
        tendencia_label = tk.Label(
            tend_frame,
            text=resultado['tendencia'],
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            wraplength=700,
            justify="left",
            padx=15,
            pady=15,
            relief="flat"
        )
        tendencia_label.pack(fill=tk.X)
        """
        # ============================================================
        # RECOMENDACIONES
        # ============================================================
        rec_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Recomendaciones - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        rec_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                    pady=Dimensions.PADDING_MEDIUM)
        
        recomendaciones = analisis_cce.recomendaciones(2)
        
        for i, rec in enumerate(recomendaciones, 1):
            rec_label = tk.Label(
                rec_frame,
                text=f"{i}. {rec}",
                font=Fonts.NORMAL,
                bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY,
                wraplength=700,
                justify="left",
                padx=10,
                pady=8,
                anchor="w"
            )
            rec_label.pack(fill=tk.X, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")