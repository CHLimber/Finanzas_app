"""
Archivo: gui/windows/balance_window.py
Pestaña del Balance General con estilos centralizados
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, Labels, NumberFormat

class BalanceTab(ttk.Frame):
    """Pestaña para el Balance General con cálculo automático"""
    
    def __init__(self, parent, balance_model, callback_actualizar=None):
        super().__init__(parent)
        self.balance_model = balance_model
        self.callback_actualizar = callback_actualizar
        
        self.entries = {}
        self.calculated_labels = {}
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea la interfaz del balance"""
        
        # Canvas con scrollbar
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
        titulo = ttk.Label(
            scrollable_frame, 
            text="BALANCE GENERAL",
            font=Fonts.TITLE
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=Dimensions.PADDING_LARGE)
        
        # Encabezados
        ttk.Label(
            scrollable_frame, 
            text=Labels.COL_CUENTA, 
            font=Fonts.HEADER
        ).grid(row=1, column=0, padx=Dimensions.PADDING_LARGE, 
               pady=Dimensions.PADDING_MEDIUM, sticky="w")
        
        ttk.Label(
            scrollable_frame, 
            text=Labels.COL_YEAR_1, 
            font=Fonts.HEADER
        ).grid(row=1, column=1, padx=Dimensions.PADDING_LARGE, 
               pady=Dimensions.PADDING_MEDIUM)
        
        ttk.Label(
            scrollable_frame, 
            text=Labels.COL_YEAR_2, 
            font=Fonts.HEADER
        ).grid(row=1, column=2, padx=Dimensions.PADDING_LARGE, 
               pady=Dimensions.PADDING_MEDIUM)
        
        row = 2
        
        # ACTIVO CORRIENTE
        row = self.seccion_titulo(scrollable_frame, "ACTIVO CORRIENTE", row, Colors.ACTIVO)
        row = self.campo_entrada(scrollable_frame, "Caja y Bancos", 
                                "caja_bancos_y1", "caja_bancos_y2", row)
        row = self.campo_entrada(scrollable_frame, "Clientes por cobrar", 
                                "clientes_cobrar_y1", "clientes_cobrar_y2", row)
        row = self.campo_entrada(scrollable_frame, "Inversión a corto plazo", 
                                "inversion_cp_y1", "inversion_cp_y2", row)
        row = self.campo_entrada(scrollable_frame, "Existencias y servicios en preparación", 
                                "existencias_y1", "existencias_y2", row)
        row = self.campo_calculado(scrollable_frame, "TOTAL CORRIENTE", 
                                   "total_corriente", row, bold=True)
        
        # ACTIVO NO CORRIENTE
        row = self.seccion_titulo(scrollable_frame, "ACTIVO NO CORRIENTE", row, Colors.ACTIVO)
        row = self.campo_entrada(scrollable_frame, "Inmuebles, planta y equipo", 
                                "inmuebles_planta_y1", "inmuebles_planta_y2", row)
        row = self.campo_entrada(scrollable_frame, "Depreciación acumulada", 
                                "depreciacion_acum_y1", "depreciacion_acum_y2", row)
        row = self.campo_entrada(scrollable_frame, "Intangibles (software desarrollado)", 
                                "intangibles_y1", "intangibles_y2", row)
        row = self.campo_entrada(scrollable_frame, "Depreciación intangibles", 
                                "depreciacion_intang_y1", "depreciacion_intang_y2", row)
        row = self.campo_calculado(scrollable_frame, "TOTAL ACTIVO NO CORRIENTE", 
                                   "total_no_corriente", row, bold=True)
        row = self.campo_calculado(scrollable_frame, "TOTAL ACTIVOS", 
                                   "total_activos", row, bold=True, size=Fonts.SIZE_HEADER)
        
        # PASIVO CORRIENTE
        row = self.seccion_titulo(scrollable_frame, "PASIVO CORRIENTE", row, Colors.PASIVO)
        row = self.campo_entrada(scrollable_frame, "Proveedores y gastos por pagar", 
                                "proveedores_y1", "proveedores_y2", row)
        row = self.campo_entrada(scrollable_frame, "Impuestos por pagar", 
                                "impuestos_pagar_y1", "impuestos_pagar_y2", row)
        row = self.campo_entrada(scrollable_frame, "Deuda a corto plazo bancaria", 
                                "deuda_cp_y1", "deuda_cp_y2", row)
        row = self.campo_calculado(scrollable_frame, "TOTAL PASIVO CORRIENTE", 
                                   "total_pasivo_corriente", row, bold=True)
        
        # PASIVO NO CORRIENTE
        row = self.seccion_titulo(scrollable_frame, "PASIVO NO CORRIENTE", row, Colors.PASIVO)
        row = self.campo_entrada(scrollable_frame, "Préstamos a largo plazo (5% anual)", 
                                "prestamos_lp_y1", "prestamos_lp_y2", row)
        row = self.campo_entrada(scrollable_frame, "Provisiones a largo plazo", 
                                "provisiones_lp_y1", "provisiones_lp_y2", row)
        row = self.campo_calculado(scrollable_frame, "TOTAL PASIVO NO CORRIENTE", 
                                   "total_pasivo_no_corriente", row, bold=True)
        
        # PATRIMONIO
        row = self.seccion_titulo(scrollable_frame, "PATRIMONIO", row, Colors.PATRIMONIO)
        row = self.campo_entrada(scrollable_frame, "Capital Social", 
                                "capital_social_y1", "capital_social_y2", row)
        row = self.campo_entrada(scrollable_frame, "Reservas legales", 
                                "reservas_legales_y1", "reservas_legales_y2", row)
        row = self.campo_entrada(scrollable_frame, "Ganancias acumuladas", 
                                "ganancias_acum_y1", "ganancias_acum_y2", row)
        row = self.campo_calculado(scrollable_frame, "TOTAL PATRIMONIO", 
                                   "total_patrimonio", row, bold=True)
        row = self.campo_calculado(scrollable_frame, "TOTAL PASIVO + PATRIMONIO", 
                                   "total_pasivo_patrimonio", row, bold=True, 
                                   size=Fonts.SIZE_HEADER)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def seccion_titulo(self, parent, texto, row, color):
        """Título de sección"""
        ttk.Label(
            parent, 
            text=texto, 
            font=Fonts.HEADER,
            foreground=color
        ).grid(row=row, column=0, columnspan=3, sticky="w", 
               padx=Dimensions.PADDING_LARGE, 
               pady=(Dimensions.PADDING_LARGE, Dimensions.PADDING_SMALL))
        return row + 1
    
    def campo_entrada(self, parent, label, field_y1, field_y2, row):
        """Campo de entrada con cálculo automático"""
        ttk.Label(
            parent, 
            text=label, 
            font=Fonts.NORMAL
        ).grid(row=row, column=0, sticky="w", 
               padx=Dimensions.PADDING_XLARGE, 
               pady=Dimensions.PADDING_SMALL)
        
        # Entry Año 1
        entry_y1 = ttk.Entry(
            parent, 
            width=Dimensions.ENTRY_WIDTH, 
            justify="right", 
            font=Fonts.NORMAL
        )
        entry_y1.grid(row=row, column=1, 
                     padx=Dimensions.PADDING_LARGE, 
                     pady=Dimensions.PADDING_SMALL)
        entry_y1.insert(0, "0.00")
        entry_y1.bind("<KeyRelease>", lambda e: self.calcular_automatico())
        self.entries[field_y1] = entry_y1
        
        # Entry Año 2
        entry_y2 = ttk.Entry(
            parent, 
            width=Dimensions.ENTRY_WIDTH, 
            justify="right", 
            font=Fonts.NORMAL
        )
        entry_y2.grid(row=row, column=2, 
                     padx=Dimensions.PADDING_LARGE, 
                     pady=Dimensions.PADDING_SMALL)
        entry_y2.insert(0, "0.00")
        entry_y2.bind("<KeyRelease>", lambda e: self.calcular_automatico())
        self.entries[field_y2] = entry_y2
        
        return row + 1
    
    def campo_calculado(self, parent, label, field_name, row, bold=False, size=Fonts.SIZE_NORMAL):
        """Campo calculado automáticamente"""
        font = (Fonts.FAMILY, size, "bold") if bold else (Fonts.FAMILY, size)
        
        ttk.Label(
            parent, 
            text=label, 
            font=font
        ).grid(row=row, column=0, sticky="w", 
               padx=Dimensions.PADDING_XLARGE, 
               pady=Dimensions.PADDING_SMALL)
        
        # Label Año 1
        label_y1 = tk.Label(
            parent, 
            text="0.00", 
            font=font,
            foreground=Colors.CALCULATED, 
            bg=Colors.BG_PRIMARY, 
            width=Dimensions.LABEL_WIDTH, 
            anchor="e"
        )
        label_y1.grid(row=row, column=1, 
                     padx=Dimensions.PADDING_LARGE, 
                     pady=Dimensions.PADDING_SMALL)
        self.calculated_labels[f"{field_name}_y1"] = label_y1
        
        # Label Año 2
        label_y2 = tk.Label(
            parent, 
            text="0.00", 
            font=font,
            foreground=Colors.CALCULATED, 
            bg=Colors.BG_PRIMARY, 
            width=Dimensions.LABEL_WIDTH, 
            anchor="e"
        )
        label_y2.grid(row=row, column=2, 
                     padx=Dimensions.PADDING_LARGE, 
                     pady=Dimensions.PADDING_SMALL)
        self.calculated_labels[f"{field_name}_y2"] = label_y2
        
        return row + 1
    
    def calcular_automatico(self):
        """Calcula automáticamente todos los totales"""
        try:
            for field_name, entry in self.entries.items():
                try:
                    value = NumberFormat.parse(entry.get())
                    setattr(self.balance_model, field_name, value)
                except:
                    setattr(self.balance_model, field_name, 0.0)
            
            # Actualizar campos calculados
            self.actualizar_label("total_corriente_y1", 
                                 self.balance_model.get_total_corriente(1))
            self.actualizar_label("total_corriente_y2", 
                                 self.balance_model.get_total_corriente(2))
            self.actualizar_label("total_no_corriente_y1", 
                                 self.balance_model.get_total_no_corriente(1))
            self.actualizar_label("total_no_corriente_y2", 
                                 self.balance_model.get_total_no_corriente(2))
            self.actualizar_label("total_activos_y1", 
                                 self.balance_model.get_total_activos(1))
            self.actualizar_label("total_activos_y2", 
                                 self.balance_model.get_total_activos(2))
            self.actualizar_label("total_pasivo_corriente_y1", 
                                 self.balance_model.get_total_pasivo_corriente(1))
            self.actualizar_label("total_pasivo_corriente_y2", 
                                 self.balance_model.get_total_pasivo_corriente(2))
            self.actualizar_label("total_pasivo_no_corriente_y1", 
                                 self.balance_model.get_total_pasivo_no_corriente(1))
            self.actualizar_label("total_pasivo_no_corriente_y2", 
                                 self.balance_model.get_total_pasivo_no_corriente(2))
            self.actualizar_label("total_patrimonio_y1", 
                                 self.balance_model.get_total_patrimonio(1))
            self.actualizar_label("total_patrimonio_y2", 
                                 self.balance_model.get_total_patrimonio(2))
            self.actualizar_label("total_pasivo_patrimonio_y1", 
                                 self.balance_model.get_total_pasivo_patrimonio(1))
            self.actualizar_label("total_pasivo_patrimonio_y2", 
                                 self.balance_model.get_total_pasivo_patrimonio(2))
            
            if self.callback_actualizar:
                self.callback_actualizar()
                
        except Exception as e:
            pass
    
    def actualizar_label(self, field_name, value):
        """Actualiza un label calculado"""
        if field_name in self.calculated_labels:
            self.calculated_labels[field_name].config(text=NumberFormat.format(value))
    
    def cargar_datos(self):
        """Carga datos del modelo"""
        for field_name, entry in self.entries.items():
            value = getattr(self.balance_model, field_name, 0.0)
            entry.delete(0, tk.END)
            entry.insert(0, NumberFormat.format(value))
        
        self.calcular_automatico()