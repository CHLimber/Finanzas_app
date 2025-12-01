"""
Archivo: core/analysis/estructura_financiera.py
Análisis de Estructura Financiera con interpretación por sector
"""

class EstructuraFinanciera:
    """
    Analiza la composición del financiamiento de la empresa:
    - Pasivo Corriente (corto plazo)
    - Pasivo No Corriente (largo plazo)
    - Patrimonio Neto (recursos propios)
    """
    
    # Rangos óptimos para sector tecnológico/software
    RANGOS_TECNOLOGIA = {
        'patrimonio': {
            'optimo_min': 0.50,
            'optimo_max': 0.75,
            'minimo_aceptable': 0.40
        },
        'deuda_total': {
            'maximo_aceptable': 0.50,
            'maximo_conservador': 0.35
        },
        'pasivo_corriente': {
            'maximo_aceptable': 0.30,
            'maximo_conservador': 0.20
        },
        'pasivo_no_corriente': {
            'maximo_aceptable': 0.30,
            'maximo_conservador': 0.20
        }
    }
    
    def __init__(self, pasivo_corriente, pasivo_no_corriente, patrimonio, sector='tecnologia'):
        self.pc = pasivo_corriente
        self.pnc = pasivo_no_corriente
        self.pn = patrimonio
        self.sector = sector
        
        self.total_financiamiento = self.pc + self.pnc + self.pn
        
        # Cálculo porcentual
        if self.total_financiamiento > 0:
            self.pct_pc = self.pc / self.total_financiamiento
            self.pct_pnc = self.pnc / self.total_financiamiento
            self.pct_pn = self.pn / self.total_financiamiento
        else:
            self.pct_pc = 0
            self.pct_pnc = 0
            self.pct_pn = 0
        
        self.pct_deuda_total = self.pct_pc + self.pct_pnc
    
    def porcentajes(self):
        """Devuelve los porcentajes en formato numérico."""
        return {
            "pct_pc": self.pct_pc,
            "pct_pnc": self.pct_pnc,
            "pct_pn": self.pct_pn,
            "pct_deuda_total": self.pct_deuda_total
        }
    
    def evaluar_componente(self, componente):
        """
        Evalúa un componente específico y retorna estado.
        Retorna: 'optimo', 'aceptable', 'riesgoso'
        """
        rangos = self.RANGOS_TECNOLOGIA
        
        if componente == 'patrimonio':
            if self.pct_pn >= rangos['patrimonio']['optimo_min']:
                return 'optimo'
            elif self.pct_pn >= rangos['patrimonio']['minimo_aceptable']:
                return 'aceptable'
            else:
                return 'riesgoso'
        
        elif componente == 'deuda_total':
            if self.pct_deuda_total <= rangos['deuda_total']['maximo_conservador']:
                return 'optimo'
            elif self.pct_deuda_total <= rangos['deuda_total']['maximo_aceptable']:
                return 'aceptable'
            else:
                return 'riesgoso'
        
        elif componente == 'pasivo_corriente':
            if self.pct_pc <= rangos['pasivo_corriente']['maximo_conservador']:
                return 'optimo'
            elif self.pct_pc <= rangos['pasivo_corriente']['maximo_aceptable']:
                return 'aceptable'
            else:
                return 'riesgoso'
        
        elif componente == 'pasivo_no_corriente':
            if self.pct_pnc <= rangos['pasivo_no_corriente']['maximo_conservador']:
                return 'optimo'
            elif self.pct_pnc <= rangos['pasivo_no_corriente']['maximo_aceptable']:
                return 'aceptable'
            else:
                return 'riesgoso'
        
        return 'no_evaluado'
    
    def interpretar_patrimonio(self):
        """Interpretación del nivel de recursos propios"""
        if self.pct_pn >= 0.65:
            return (
                "Excelente nivel de recursos propios (≥65%). La empresa muestra "
                "alta autonomía financiera, característica ideal para el sector "
                "tecnológico que requiere flexibilidad y bajo riesgo financiero."
            )
        elif self.pct_pn >= 0.50:
            return (
                "Buen nivel de recursos propios (50-65%). Estructura equilibrada "
                "con predominio de financiamiento propio, adecuada para empresas "
                "de software."
            )
        elif self.pct_pn >= 0.40:
            return (
                "Nivel aceptable de recursos propios (40-50%). Se recomienda "
                "aumentar el patrimonio para reducir dependencia de terceros."
            )
        else:
            return (
                "Nivel bajo de recursos propios (<40%). La empresa depende "
                "excesivamente del endeudamiento, situación riesgosa para el "
                "sector tecnológico."
            )
    
    def interpretar_deuda_total(self):
        """Interpretación del nivel total de endeudamiento"""
        if self.pct_deuda_total <= 0.35:
            return (
                "Endeudamiento bajo (≤35%). Estructura conservadora que otorga "
                "alta solvencia y capacidad de maniobra."
            )
        elif self.pct_deuda_total <= 0.50:
            return (
                "Endeudamiento moderado (35-50%). Nivel aceptable que equilibra "
                "financiamiento propio y de terceros."
            )
        else:
            return (
                "Endeudamiento alto (>50%). Situación que puede comprometer la "
                "flexibilidad financiera y aumentar el riesgo."
            )
    
    def interpretar_pasivo_corriente(self):
        """Interpretación de la deuda de corto plazo"""
        if self.pct_pc <= 0.20:
            return (
                "Deuda de corto plazo baja (≤20%). Excelente, reduce presión "
                "sobre la liquidez y permite enfocarse en crecimiento."
            )
        elif self.pct_pc <= 0.30:
            return (
                "Deuda de corto plazo moderada (20-30%). Nivel manejable que "
                "requiere atención constante a la liquidez."
            )
        else:
            return (
                "Deuda de corto plazo alta (>30%). Presión significativa sobre "
                "la liquidez que puede limitar la capacidad operativa."
            )
    
    def interpretar_pasivo_no_corriente(self):
        """Interpretación de la deuda de largo plazo"""
        if self.pct_pnc <= 0.20:
            return (
                "Deuda de largo plazo baja (≤20%). Estructura conservadora con "
                "bajo compromiso de largo plazo."
            )
        elif self.pct_pnc <= 0.30:
            return (
                "Deuda de largo plazo moderada (20-30%). Nivel razonable para "
                "financiar activos no corrientes."
            )
        else:
            return (
                "Deuda de largo plazo alta (>30%). Puede indicar dependencia "
                "excesiva de financiamiento externo de largo plazo."
            )
    
    def interpretar(self):
        """
        Devuelve una interpretación completa de la estructura financiera.
        """
        return {
            'patrimonio': self.interpretar_patrimonio(),
            'deuda_total': self.interpretar_deuda_total(),
            'pasivo_corriente': self.interpretar_pasivo_corriente(),
            'pasivo_no_corriente': self.interpretar_pasivo_no_corriente()
        }
    
    def diagnostico(self):
        """
        Devuelve un diagnóstico final: equilibrada, conservadora o riesgosa.
        """
        estado_patrimonio = self.evaluar_componente('patrimonio')
        estado_deuda = self.evaluar_componente('deuda_total')
        estado_pc = self.evaluar_componente('pasivo_corriente')
        
        # Estructura óptima
        if estado_patrimonio == 'optimo' and estado_deuda == 'optimo':
            return {
                'nivel': 'ÓPTIMA',
                'descripcion': 'Estructura altamente equilibrada y conservadora. Ideal para el sector software.'
            }
        
        # Estructura equilibrada
        if estado_patrimonio in ['optimo', 'aceptable'] and estado_deuda in ['optimo', 'aceptable']:
            return {
                'nivel': 'EQUILIBRADA',
                'descripcion': 'Estructura financiera sólida con balance adecuado entre recursos propios y deuda.'
            }
        
        # Estructura con advertencias
        if estado_patrimonio == 'riesgoso' or estado_deuda == 'riesgoso':
            return {
                'nivel': 'RIESGOSA',
                'descripcion': 'Estructura con exceso de deuda. Se requieren medidas correctivas urgentes.'
            }
        
        return {
            'nivel': 'ACEPTABLE',
            'descripcion': 'Estructura funcional pero con margen de mejora.'
        }
    
    def rangos_optimos_sector(self):
        """Retorna los rangos óptimos para el sector tecnológico"""
        return {
            'Patrimonio Neto': '50% - 75%',
            'Deuda Total': '≤ 35% (conservador) | ≤ 50% (aceptable)',
            'Pasivo Corriente': '≤ 20% (conservador) | ≤ 30% (aceptable)',
            'Pasivo No Corriente': '≤ 20% (conservador) | ≤ 30% (aceptable)'
        }