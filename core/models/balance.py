"""
Archivo: core/models/balance.py
Modelo de datos para el Balance General
"""

class BalanceGeneral:
    """Modelo para almacenar datos del Balance General de 2 anos"""
    
    def __init__(self):
        # ACTIVO CORRIENTE - Ano 1 (2023)
        self.caja_bancos_y1 = 850.0
        self.clientes_cobrar_y1 = 1200.0
        self.inversion_cp_y1 = 300.0
        self.existencias_y1 = 450.0
        
        # ACTIVO CORRIENTE - Ano 2 (2024)
        self.caja_bancos_y2 = 1100.0
        self.clientes_cobrar_y2 = 1600.0
        self.inversion_cp_y2 = 500.0
        self.existencias_y2 = 600.0
        
        # ACTIVO NO CORRIENTE - Ano 1 (2023)
        self.inmuebles_planta_y1 = 1200.0
        self.depreciacion_acum_y1 = 400.0
        self.intangibles_y1 = 800.0
        self.depreciacion_intang_y1 = 150.0
        
        # ACTIVO NO CORRIENTE - Ano 2 (2024)
        self.inmuebles_planta_y2 = 1500.0
        self.depreciacion_acum_y2 = 550.0
        self.intangibles_y2 = 1200.0
        self.depreciacion_intang_y2 = 300.0
        
        # PASIVO CORRIENTE - Ano 1 (2023)
        self.proveedores_y1 = 300.0
        self.impuestos_pagar_y1 = 150.0
        self.deuda_cp_y1 = 100.0
        
        # PASIVO CORRIENTE - Ano 2 (2024)
        self.proveedores_y2 = 600.0
        self.impuestos_pagar_y2 = 200.0
        self.deuda_cp_y2 = 200.0
        
        # PASIVO NO CORRIENTE - Ano 1 (2023)
        self.prestamos_lp_y1 = 600.0
        self.provisiones_lp_y1 = 100.0
        
        # PASIVO NO CORRIENTE - Ano 2 (2024)
        self.prestamos_lp_y2 = 900.0
        self.provisiones_lp_y2 = 100.0
        
        # PATRIMONIO - Ano 1 (2023)
        self.capital_social_y1 = 1500.0
        self.reservas_legales_y1 = 400.0
        self.ganancias_acum_y1 = 1100.0
        
        # PATRIMONIO - Ano 2 (2024)
        self.capital_social_y2 = 1500.0
        self.reservas_legales_y2 = 500.0
        self.ganancias_acum_y2 = 1650.0
    
    # METODOS DE CALCULO AUTOMATICO
    
    def get_total_corriente(self, year):
        """Calcula Total Activo Corriente"""
        if year == 1:
            return (self.caja_bancos_y1 + self.clientes_cobrar_y1 + 
                    self.inversion_cp_y1 + self.existencias_y1)
        else:
            return (self.caja_bancos_y2 + self.clientes_cobrar_y2 + 
                    self.inversion_cp_y2 + self.existencias_y2)
    
    def get_total_no_corriente(self, year):
        """Calcula Total Activo No Corriente"""
        if year == 1:
            return (self.inmuebles_planta_y1 - self.depreciacion_acum_y1 + 
                    self.intangibles_y1 - self.depreciacion_intang_y1)
        else:
            return (self.inmuebles_planta_y2 - self.depreciacion_acum_y2 + 
                    self.intangibles_y2 - self.depreciacion_intang_y2)
    
    def get_total_activos(self, year):
        """Calcula Total Activos"""
        return self.get_total_corriente(year) + self.get_total_no_corriente(year)
    
    def get_total_pasivo_corriente(self, year):
        """Calcula Total Pasivo Corriente"""
        if year == 1:
            return (self.proveedores_y1 + self.impuestos_pagar_y1 + 
                    self.deuda_cp_y1)
        else:
            return (self.proveedores_y2 + self.impuestos_pagar_y2 + 
                    self.deuda_cp_y2)
    
    def get_total_pasivo_no_corriente(self, year):
        """Calcula Total Pasivo No Corriente"""
        if year == 1:
            return self.prestamos_lp_y1 + self.provisiones_lp_y1
        else:
            return self.prestamos_lp_y2 + self.provisiones_lp_y2
    
    def get_total_patrimonio(self, year):
        """Calcula Total Patrimonio"""
        if year == 1:
            return (self.capital_social_y1 + self.reservas_legales_y1 + 
                    self.ganancias_acum_y1)
        else:
            return (self.capital_social_y2 + self.reservas_legales_y2 + 
                    self.ganancias_acum_y2)
    
    def get_total_pasivo_patrimonio(self, year):
        """Calcula Total Pasivo + Patrimonio"""
        return (self.get_total_pasivo_corriente(year) + 
                self.get_total_pasivo_no_corriente(year) + 
                self.get_total_patrimonio(year))
    
    def validar_balance(self, year):
        """Verifica que Activos = Pasivos + Patrimonio"""
        activos = self.get_total_activos(year)
        pasivo_patrimonio = self.get_total_pasivo_patrimonio(year)
        diferencia = abs(activos - pasivo_patrimonio)
        return diferencia < 0.01  # Tolerancia de redondeo
