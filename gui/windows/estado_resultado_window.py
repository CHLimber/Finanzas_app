"""
Archivo: gui/windows/estado_resultado_window.py
Pestaña del Estado de Resultados con cálculo automático
"""

import tkinter as tk
from tkinter import ttk

class EstadoResultadoTab(ttk.Frame):
    """Pestaña para el Estado de Resultados con cálculo automático"""
    
    def __init__(self, parent, estado_modelo, callback_actualizar=None):
        super().__init__(parent)
        self.estado_modelo = estado_modelo
        self.callback_actualizar = callback_actualizar
        
        self.entries = {}
        self.calculated_labels = {}
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def crear_interfaz(self):
        """Crea la interfaz del estado de resultados"""
        
        # Canvas con scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo = ttk.Label(scrollable_frame, 
                          text="ESTADO DE RESULTADOS (en miles de Bs.)", 
                          font=("Arial", 18, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=15)
        
        # Encabezados
        ttk.Label(scrollable_frame, text="Concepto", font=("Arial", 11, "bold")).grid(
            row=1, column=0, padx=15, pady=8, sticky="w")
        ttk.Label(scrollable_frame, text="Año 1", font=("Arial", 11, "bold")).grid(
            row=1, column=1, padx=15, pady=8)
        ttk.Label(scrollable_frame, text="Año 2", font=("Arial", 11, "bold")).grid(
            row=1, column=2, padx=15, pady=8)
        
        row = 2
        
        # INGRESOS Y COSTOS
        row = self.campo_entrada(scrollable_frame, "Ingresos por servicios", 
                                "ingresos_servicios_y1", "ingresos_servicios_y2", row)
        row = self.campo_entrada(scrollable_frame, "Costo de servicios", 
                                "costo_servicios_y1", "costo_servicios_y2", row)
        row = self.campo_calculado(scrollable_frame, "GANANCIA BRUTA", 
                                   "ganancia_bruta", row, bold=True)
        
        # Separador
        ttk.Separator(scrollable_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=8)
        row += 1
        
        # GASTOS OPERATIVOS
        row = self.campo_entrada(scrollable_frame, "Gastos de administración", 
                                "gastos_admin_y1", "gastos_admin_y2", row)
        row = self.campo_entrada(scrollable_frame, "Gastos de ventas", 
                                "gastos_ventas_y1", "gastos_ventas_y2", row)
        row = self.campo_entrada(scrollable_frame, "Depreciación y amortización", 
                                "depreciacion_amort_y1", "depreciacion_amort_y2", row)
        row = self.campo_calculado(scrollable_frame, "UTILIDAD OPERATIVA (BAII)", 
                                   "utilidad_operativa", row, bold=True)
        
        # Separador
        ttk.Separator(scrollable_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=8)
        row += 1
        
        # OTROS INGRESOS Y GASTOS
        row = self.campo_entrada(scrollable_frame, "Gastos financieros", 
                                "gastos_financieros_y1", "gastos_financieros_y2", row)
        row = self.campo_entrada(scrollable_frame, "Otros ingresos", 
                                "otros_ingresos_y1", "otros_ingresos_y2", row)
        row = self.campo_calculado(scrollable_frame, "UTILIDAD ANTES DE IMPUESTOS", 
                                   "utilidad_antes_impuestos", row, bold=True)
        
        # Separador
        ttk.Separator(scrollable_frame, orient="horizontal").grid(
            row=row, column=0, columnspan=3, sticky="ew", pady=8)
        row += 1
        
        # IMPUESTOS Y UTILIDAD NETA
        row = self.campo_calculado(scrollable_frame, "Impuestos a la renta (25%)", 
                                   "impuestos_renta", row)
        row = self.campo_calculado(scrollable_frame, "UTILIDAD NETA", 
                                   "utilidad_neta", row, bold=True, color="darkblue", size=12)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def campo_entrada(self, parent, label, field_y1, field_y2, row):
        """Campo de entrada con cálculo automático"""
        ttk.Label(parent, text=label, font=("Arial", 10)).grid(
            row=row, column=0, sticky="w", padx=30, pady=3)
        
        # Entry Año 1
        entry_y1 = ttk.Entry(parent, width=18, justify="right", font=("Arial", 10))
        entry_y1.grid(row=row, column=1, padx=15, pady=3)
        entry_y1.insert(0, "0.00")
        entry_y1.bind("<KeyRelease>", lambda e: self.calcular_automatico())
        self.entries[field_y1] = entry_y1
        
        # Entry Año 2
        entry_y2 = ttk.Entry(parent, width=18, justify="right", font=("Arial", 10))
        entry_y2.grid(row=row, column=2, padx=15, pady=3)
        entry_y2.insert(0, "0.00")
        entry_y2.bind("<KeyRelease>", lambda e: self.calcular_automatico())
        self.entries[field_y2] = entry_y2
        
        return row + 1
    
    def campo_calculado(self, parent, label, field_name, row, 
                       bold=False, color="darkgreen", size=10):
        """Campo calculado automáticamente"""
        font = ("Arial", size, "bold") if bold else ("Arial", size)
        
        ttk.Label(parent, text=label, font=font).grid(
            row=row, column=0, sticky="w", padx=30, pady=3)
        
        # Label Año 1
        label_y1 = tk.Label(parent, text="0.00", font=font, 
                           foreground=color, bg="white", width=18, anchor="e")
        label_y1.grid(row=row, column=1, padx=15, pady=3)
        self.calculated_labels[f"{field_name}_y1"] = label_y1
        
        # Label Año 2
        label_y2 = tk.Label(parent, text="0.00", font=font, 
                           foreground=color, bg="white", width=18, anchor="e")
        label_y2.grid(row=row, column=2, padx=15, pady=3)
        self.calculated_labels[f"{field_name}_y2"] = label_y2
        
        return row + 1
    
    def calcular_automatico(self):
        """Calcula automáticamente todos los resultados"""
        try:
            # Guardar datos en el modelo
            for field_name, entry in self.entries.items():
                try:
                    value = float(entry.get().replace(",", ""))
                    setattr(self.estado_modelo, field_name, value)
                except:
                    setattr(self.estado_modelo, field_name, 0.0)
            
            # Actualizar campos calculados para Año 1
            self.actualizar_label("ganancia_bruta_y1", 
                                 self.estado_modelo.get_ganancia_bruta(1))
            self.actualizar_label("utilidad_operativa_y1", 
                                 self.estado_modelo.get_utilidad_operativa(1))
            self.actualizar_label("utilidad_antes_impuestos_y1", 
                                 self.estado_modelo.get_utilidad_antes_impuestos(1))
            self.actualizar_label("impuestos_renta_y1", 
                                 self.estado_modelo.get_impuestos_renta(1))
            self.actualizar_label("utilidad_neta_y1", 
                                 self.estado_modelo.get_utilidad_neta(1))
            
            # Actualizar campos calculados para Año 2
            self.actualizar_label("ganancia_bruta_y2", 
                                 self.estado_modelo.get_ganancia_bruta(2))
            self.actualizar_label("utilidad_operativa_y2", 
                                 self.estado_modelo.get_utilidad_operativa(2))
            self.actualizar_label("utilidad_antes_impuestos_y2", 
                                 self.estado_modelo.get_utilidad_antes_impuestos(2))
            self.actualizar_label("impuestos_renta_y2", 
                                 self.estado_modelo.get_impuestos_renta(2))
            self.actualizar_label("utilidad_neta_y2", 
                                 self.estado_modelo.get_utilidad_neta(2))
            
            # Llamar callback para actualizar análisis
            if self.callback_actualizar:
                self.callback_actualizar()
                
        except Exception as e:
            pass  # Ignorar errores durante la escritura
    
    def actualizar_label(self, field_name, value):
        """Actualiza un label calculado"""
        if field_name in self.calculated_labels:
            self.calculated_labels[field_name].config(text=f"{value:,.2f}")
    
    def cargar_datos(self):
        """Carga datos del modelo"""
        for field_name, entry in self.entries.items():
            value = getattr(self.estado_modelo, field_name, 0.0)
            entry.delete(0, tk.END)
            entry.insert(0, f"{value:.2f}")
        
        self.calcular_automatico()