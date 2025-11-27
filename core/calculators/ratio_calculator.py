"""
Archivo: core/calculators/ratio_calculator.py
Calculadora de ratios financieros a partir de Balance y Estado de Resultados
"""

class RatioCalculator:
    """
    Calcula todos los ratios financieros a partir de los modelos
    de Balance General y Estado de Resultados
    """
    
    def __init__(self, balance_model, estado_resultado_model):
        """
        Args:
            balance_model: Instancia de BalanceGeneral
            estado_resultado_model: Instancia de EstadoResultado
        """
        self.balance = balance_model
        self.estado = estado_resultado_model
    
    # ============================================================
    # RATIOS PATRIMONIALES
    # ============================================================
    
    def calcular_fondo_maniobra(self, year):
        """
        Fondo de Maniobra como RATIO (para interpretación con rangos).
        FM Ratio = (Activo Corriente - Pasivo Corriente) / Activo Total
        
        IMPORTANTE: Este ratio decimal (0.10 - 0.30) se usa para comparar 
        con los rangos del FinancialInterpreter.
        """
        activo_corriente = self.balance.get_total_corriente(year)
        pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        activo_total = self.balance.get_total_activos(year)
        
        if activo_total == 0:
            return 0
        
        return (activo_corriente - pasivo_corriente) / activo_total
    
    def calcular_fondo_maniobra_absoluto(self, year):
        """
        Fondo de Maniobra en valor absoluto (unidades monetarias).
        FM = Activo Corriente - Pasivo Corriente
        
        Este valor se usa para análisis de equilibrio patrimonial.
        """
        activo_corriente = self.balance.get_total_corriente(year)
        pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        
        return activo_corriente - pasivo_corriente
    
    # ============================================================
    # RATIOS DE LIQUIDEZ
    # ============================================================
    
    def calcular_razon_liquidez(self, year):
        """
        Razón de Liquidez = Activo Corriente / Pasivo Corriente
        """
        activo_corriente = self.balance.get_total_corriente(year)
        pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        
        if pasivo_corriente == 0:
            return float('inf')
        
        return activo_corriente / pasivo_corriente
    
    def calcular_razon_tesoreria(self, year):
        """
        Razón de Tesorería = (Activo Corriente - Existencias) / Pasivo Corriente
        """
        activo_corriente = self.balance.get_total_corriente(year)
        existencias = self.balance.existencias_y1 if year == 1 else self.balance.existencias_y2
        pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        
        if pasivo_corriente == 0:
            return float('inf')
        
        return (activo_corriente - existencias) / pasivo_corriente
    
    def calcular_razon_disponibilidad(self, year):
        """
        Razón de Disponibilidad = Caja y Bancos / Pasivo Corriente
        """
        caja_bancos = self.balance.caja_bancos_y1 if year == 1 else self.balance.caja_bancos_y2
        pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        
        if pasivo_corriente == 0:
            return float('inf')
        
        return caja_bancos / pasivo_corriente
    
    # ============================================================
    # RATIOS DE SOLVENCIA
    # ============================================================
    
    def calcular_ratio_garantia(self, year):
        """
        Ratio de Garantía = Activo Total / Pasivo Total
        """
        activo_total = self.balance.get_total_activos(year)
        pasivo_total = (self.balance.get_total_pasivo_corriente(year) + 
                       self.balance.get_total_pasivo_no_corriente(year))
        
        if pasivo_total == 0:
            return float('inf')
        
        return activo_total / pasivo_total
    
    def calcular_ratio_autonomia(self, year):
        """
        Ratio de Autonomía = Patrimonio / Pasivo Total
        """
        patrimonio = self.balance.get_total_patrimonio(year)
        pasivo_total = (self.balance.get_total_pasivo_corriente(year) + 
                       self.balance.get_total_pasivo_no_corriente(year))
        
        if pasivo_total == 0:
            return float('inf')
        
        return patrimonio / pasivo_total
    
    def calcular_ratio_calidad_deuda(self, year):
        """
        Ratio de Calidad de Deuda = Pasivo Corriente / Pasivo Total
        """
        pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        pasivo_total = (self.balance.get_total_pasivo_corriente(year) + 
                       self.balance.get_total_pasivo_no_corriente(year))
        
        if pasivo_total == 0:
            return 0
        
        return pasivo_corriente / pasivo_total
    
    # ============================================================
    # RATIOS DE RENTABILIDAD
    # ============================================================
    
    def calcular_rat(self, year):
        """
        RAT (Rentabilidad sobre Activos Totales) = Utilidad Neta / Activo Total
        """
        utilidad_neta = self.estado.get_utilidad_neta(year)
        activo_total = self.balance.get_total_activos(year)
        
        if activo_total == 0:
            return 0
        
        return utilidad_neta / activo_total
    
    def calcular_rpp(self, year):
        """
        RPP (Rentabilidad sobre Patrimonio) = Utilidad Neta / Patrimonio
        También conocido como ROE
        """
        utilidad_neta = self.estado.get_utilidad_neta(year)
        patrimonio = self.balance.get_total_patrimonio(year)
        
        if patrimonio == 0:
            return 0
        
        return utilidad_neta / patrimonio
    
    def calcular_margen_neto(self, year):
        """
        Margen Neto = Utilidad Neta / Ingresos
        """
        utilidad_neta = self.estado.get_utilidad_neta(year)
        ingresos = self.estado.ingresos_servicios_y1 if year == 1 else self.estado.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0
        
        return utilidad_neta / ingresos
    
    def calcular_rotacion_activos(self, year):
        """
        Rotación de Activos = Ingresos / Activo Total
        """
        ingresos = self.estado.ingresos_servicios_y1 if year == 1 else self.estado.ingresos_servicios_y2
        activo_total = self.balance.get_total_activos(year)
        
        if activo_total == 0:
            return 0
        
        return ingresos / activo_total
    
    def calcular_apalancamiento(self, year):
        """
        Apalancamiento Financiero = Activo Total / Patrimonio
        """
        activo_total = self.balance.get_total_activos(year)
        patrimonio = self.balance.get_total_patrimonio(year)
        
        if patrimonio == 0:
            return float('inf')
        
        return activo_total / patrimonio
    
    def calcular_margen_bruto(self, year):
        """
        Margen Bruto = Ganancia Bruta / Ingresos
        """
        ganancia_bruta = self.estado.get_ganancia_bruta(year)
        ingresos = self.estado.ingresos_servicios_y1 if year == 1 else self.estado.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0
        
        return ganancia_bruta / ingresos
    
    def calcular_margen_operativo(self, year):
        """
        Margen Operativo = Utilidad Operativa / Ingresos
        """
        utilidad_operativa = self.estado.get_utilidad_operativa(year)
        ingresos = self.estado.ingresos_servicios_y1 if year == 1 else self.estado.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0
        
        return utilidad_operativa / ingresos
    
    # ============================================================
    # MÉTODO PARA CALCULAR TODOS LOS RATIOS
    # ============================================================
    
    def calcular_todos_ratios(self, year):
        """
        Calcula todos los ratios financieros para un año específico.
        
        Args:
            year: 1 o 2
            
        Returns:
            dict: Diccionario con todos los ratios calculados
        """
        return {
            # Patrimoniales
            "fondo_maniobra": self.calcular_fondo_maniobra(year),
            
            # Liquidez
            "razon_liquidez": self.calcular_razon_liquidez(year),
            "razon_tesoreria": self.calcular_razon_tesoreria(year),
            "razon_disponibilidad": self.calcular_razon_disponibilidad(year),
            
            # Solvencia
            "ratio_garantia": self.calcular_ratio_garantia(year),
            "ratio_autonomia": self.calcular_ratio_autonomia(year),
            "ratio_calidad_deuda": self.calcular_ratio_calidad_deuda(year),
            
            # Rentabilidad
            "rat": self.calcular_rat(year),
            "rpp": self.calcular_rpp(year),
            "margen_neto": self.calcular_margen_neto(year),
            "rotacion_activos": self.calcular_rotacion_activos(year),
            "apalancamiento": self.calcular_apalancamiento(year),
            "margen_bruto": self.calcular_margen_bruto(year),
            "margen_operativo": self.calcular_margen_operativo(year)
        }
    
    def calcular_ambos_años(self):
        """
        Calcula todos los ratios para ambos años.
        
        Returns:
            dict: Diccionario con ratios de año 1 y año 2
        """
        return {
            "year_1": self.calcular_todos_ratios(1),
            "year_2": self.calcular_todos_ratios(2)
        }