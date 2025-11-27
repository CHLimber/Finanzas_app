"""
Archivo: core/models/estado_resultado.py
Modelo de datos para el Estado de Resultados
"""

class EstadoResultado:
    """Modelo para almacenar datos del Estado de Resultados de 2 años"""
    
    def __init__(self):
        # DATOS INGRESADOS MANUALMENTE
        self.ingresos_servicios_y1 = 0.0
        self.ingresos_servicios_y2 = 0.0
        
        self.costo_servicios_y1 = 0.0
        self.costo_servicios_y2 = 0.0
        
        self.gastos_admin_y1 = 0.0
        self.gastos_admin_y2 = 0.0
        
        self.gastos_ventas_y1 = 0.0
        self.gastos_ventas_y2 = 0.0
        
        self.depreciacion_amort_y1 = 0.0
        self.depreciacion_amort_y2 = 0.0
        
        self.gastos_financieros_y1 = 0.0
        self.gastos_financieros_y2 = 0.0
        
        self.otros_ingresos_y1 = 0.0
        self.otros_ingresos_y2 = 0.0
    
    # MÉTODOS DE CÁLCULO AUTOMÁTICO
    
    def get_ganancia_bruta(self, year):
        """Calcula Ganancia Bruta"""
        if year == 1:
            return self.ingresos_servicios_y1 - self.costo_servicios_y1
        else:
            return self.ingresos_servicios_y2 - self.costo_servicios_y2
    
    def get_utilidad_operativa(self, year):
        """Calcula Utilidad Operativa (BAII)"""
        ganancia_bruta = self.get_ganancia_bruta(year)
        
        if year == 1:
            return (ganancia_bruta - self.gastos_admin_y1 - 
                    self.gastos_ventas_y1 - self.depreciacion_amort_y1)
        else:
            return (ganancia_bruta - self.gastos_admin_y2 - 
                    self.gastos_ventas_y2 - self.depreciacion_amort_y2)
    
    def get_utilidad_antes_impuestos(self, year):
        """Calcula Utilidad Antes de Impuestos"""
        utilidad_operativa = self.get_utilidad_operativa(year)
        
        if year == 1:
            return (utilidad_operativa - self.gastos_financieros_y1 + 
                    self.otros_ingresos_y1)
        else:
            return (utilidad_operativa - self.gastos_financieros_y2 + 
                    self.otros_ingresos_y2)
    
    def get_impuestos_renta(self, year):
        """Calcula Impuestos a la Renta (25%)"""
        utilidad_antes_impuestos = self.get_utilidad_antes_impuestos(year)
        return max(0, utilidad_antes_impuestos * 0.25)  # Solo si hay ganancia
    
    def get_utilidad_neta(self, year):
        """Calcula Utilidad Neta"""
        utilidad_antes_impuestos = self.get_utilidad_antes_impuestos(year)
        impuestos = self.get_impuestos_renta(year)
        return utilidad_antes_impuestos - impuestos
    
    def get_margen_bruto(self, year):
        """Calcula Margen Bruto %"""
        ingresos = self.ingresos_servicios_y1 if year == 1 else self.ingresos_servicios_y2
        if ingresos == 0:
            return 0
        return (self.get_ganancia_bruta(year) / ingresos) * 100
    
    def get_margen_operativo(self, year):
        """Calcula Margen Operativo %"""
        ingresos = self.ingresos_servicios_y1 if year == 1 else self.ingresos_servicios_y2
        if ingresos == 0:
            return 0
        return (self.get_utilidad_operativa(year) / ingresos) * 100
    
    def get_margen_neto(self, year):
        """Calcula Margen Neto %"""
        ingresos = self.ingresos_servicios_y1 if year == 1 else self.ingresos_servicios_y2
        if ingresos == 0:
            return 0
        return (self.get_utilidad_neta(year) / ingresos) * 100