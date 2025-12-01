"""
Archivo: core/analysis/rrp_analysis.py
Análisis de Rentabilidad de Recursos Propios (RRP)
"""


class RRPAnalysis:
    """Análisis completo de la Rentabilidad de Recursos Propios"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data
    
    def calcular_rrp(self, year):
        """
        Calcula RRP = Utilidad Neta / Patrimonio Neto × 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: RRP en porcentaje
        """
        utilidad_neta = self.income_data.get_utilidad_neta(year)
        patrimonio_neto = self.balance_data.get_total_patrimonio(year)
        
        if patrimonio_neto == 0:
            return 0.0
        
        return (utilidad_neta / patrimonio_neto) * 100
    
    def calcular_rat(self, year):
        """
        Calcula RAT = BAII / Activo Total × 100
        (Reutilizado para comparación)
        
        Args:
            year: 1 o 2
            
        Returns:
            float: RAT en porcentaje
        """
        baii = self.income_data.get_utilidad_operativa(year)
        activo_total = self.balance_data.get_total_activos(year)
        
        if activo_total == 0:
            return 0.0
        
        return (baii / activo_total) * 100
    
    def analisis_dual_rrp(self):
        """
        Análisis comparativo de RRP entre Año 1 y Año 2
        
        Returns:
            dict: Análisis completo RRP con interpretación
        """
        # Datos básicos
        utilidad_1 = self.income_data.get_utilidad_neta(1)
        utilidad_2 = self.income_data.get_utilidad_neta(2)
        patrimonio_1 = self.balance_data.get_total_patrimonio(1)
        patrimonio_2 = self.balance_data.get_total_patrimonio(2)
        
        # RRP por año
        rrp_1 = self.calcular_rrp(1)
        rrp_2 = self.calcular_rrp(2)
        
        # Comparación absoluta (puntos porcentuales)
        delta_rrp = rrp_2 - rrp_1
        
        # Comparación relativa (crecimiento %)
        if rrp_1 != 0:
            crecimiento_relativo = (delta_rrp / rrp_1) * 100
        else:
            crecimiento_relativo = 0.0
        
        # Interpretación
        interpretacion_rrp = self._interpretar_rrp(
            rrp_1, rrp_2, utilidad_1, utilidad_2, 
            patrimonio_1, patrimonio_2, delta_rrp, crecimiento_relativo
        )
        
        return {
            'ano_1': {
                'utilidad_neta': utilidad_1,
                'patrimonio_neto': patrimonio_1,
                'rrp': rrp_1
            },
            'ano_2': {
                'utilidad_neta': utilidad_2,
                'patrimonio_neto': patrimonio_2,
                'rrp': rrp_2
            },
            'comparacion': {
                'delta_absoluto': delta_rrp,
                'crecimiento_relativo': crecimiento_relativo,
                'interpretacion': interpretacion_rrp
            }
        }
    
    def analisis_comparativo_rat_rrp(self):
        """
        Análisis comparativo entre RAT y RRP (apalancamiento financiero)
        
        Returns:
            dict: Comparación RAT vs RRP con análisis de apalancamiento
        """
        # Calcular RAT
        rat_1 = self.calcular_rat(1)
        rat_2 = self.calcular_rat(2)
        
        # Calcular RRP
        rrp_1 = self.calcular_rrp(1)
        rrp_2 = self.calcular_rrp(2)
        
        # Análisis de apalancamiento para Año 1
        if rrp_1 > rat_1:
            apalancamiento_1 = "positivo"
            interpretacion_1 = "Apalancamiento positivo: la deuda amplifica la rentabilidad del patrimonio."
        elif rrp_1 < rat_1:
            apalancamiento_1 = "negativo"
            interpretacion_1 = "Apalancamiento negativo: la deuda reduce la rentabilidad para los dueños."
        else:
            apalancamiento_1 = "neutral"
            interpretacion_1 = "Apalancamiento neutral: ambas rentabilidades son similares."
        
        # Análisis de apalancamiento para Año 2
        if rrp_2 > rat_2:
            apalancamiento_2 = "positivo"
            interpretacion_2 = "Apalancamiento positivo: la deuda amplifica la rentabilidad del patrimonio."
        elif rrp_2 < rat_2:
            apalancamiento_2 = "negativo"
            interpretacion_2 = "Apalancamiento negativo: la deuda reduce la rentabilidad para los dueños."
        else:
            apalancamiento_2 = "neutral"
            interpretacion_2 = "Apalancamiento neutral: ambas rentabilidades son similares."
        
        # Interpretación completa
        interpretacion_completa = self._interpretar_apalancamiento(
            rat_1, rat_2, rrp_1, rrp_2, 
            apalancamiento_1, apalancamiento_2
        )
        
        return {
            'ano_1': {
                'rat': rat_1,
                'rrp': rrp_1,
                'apalancamiento': apalancamiento_1,
                'interpretacion': interpretacion_1
            },
            'ano_2': {
                'rat': rat_2,
                'rrp': rrp_2,
                'apalancamiento': apalancamiento_2,
                'interpretacion': interpretacion_2
            },
            'interpretacion_completa': interpretacion_completa
        }
    
    def _interpretar_rrp(self, rrp_1, rrp_2, utilidad_1, utilidad_2,
                        patrimonio_1, patrimonio_2, delta_rrp, crecimiento_rel):
        """
        Genera interpretación del RRP
        
        Returns:
            str: Interpretación completa
        """
        # Determinar tendencia
        if rrp_2 > rrp_1:
            tendencia = "aumentó"
        elif rrp_2 < rrp_1:
            tendencia = "disminuyó"
        else:
            tendencia = "se mantuvo estable"
        
        # Calcular variaciones
        if patrimonio_1 > 0:
            var_patrimonio = ((patrimonio_2 - patrimonio_1) / patrimonio_1) * 100
        else:
            var_patrimonio = 0
        
        if utilidad_1 > 0:
            var_utilidad = ((utilidad_2 - utilidad_1) / utilidad_1) * 100
        else:
            var_utilidad = 100 if utilidad_2 > 0 else 0
        
        # Texto base
        texto = f"La rentabilidad de los recursos propios {tendencia} de {rrp_1:.2f}% en Año 1 a {rrp_2:.2f}% en Año 2, "
        texto += f"lo que representa un cambio de {delta_rrp:+.2f} puntos porcentuales"
        
        if rrp_1 != 0:
            texto += f" y un {'incremento' if crecimiento_rel > 0 else 'decremento'} relativo del {abs(crecimiento_rel):.2f}%."
        else:
            texto += "."
        
        # Análisis detallado
        texto += f"\n\nLa utilidad neta varió {var_utilidad:+.2f}% mientras que el patrimonio neto varió {var_patrimonio:+.2f}%. "
        
        if rrp_2 > rrp_1:
            texto += "Esto indica que la empresa está generando mejores retornos para sus accionistas, "
            texto += "incrementando la rentabilidad del capital invertido por los propietarios."
        elif rrp_2 < rrp_1:
            texto += "Esto sugiere una disminución en la capacidad de generar beneficios para los accionistas, "
            texto += "lo cual puede requerir revisión de la estrategia financiera."
        else:
            texto += "La rentabilidad se mantiene estable, indicando una gestión consistente del patrimonio."
        
        return texto
    
    def _interpretar_apalancamiento(self, rat_1, rat_2, rrp_1, rrp_2,
                                   apalancamiento_1, apalancamiento_2):
        """
        Genera interpretación del apalancamiento financiero
        
        Returns:
            str: Interpretación completa
        """
        # Evolución del RAT
        if rat_2 > rat_1:
            evol_rat = f"aumentó de {rat_1:.2f}% a {rat_2:.2f}%"
        elif rat_2 < rat_1:
            evol_rat = f"disminuyó de {rat_1:.2f}% a {rat_2:.2f}%"
        else:
            evol_rat = f"se mantuvo estable en {rat_1:.2f}%"
        
        # Evolución del RRP
        if rrp_2 > rrp_1:
            evol_rrp = f"aumentó de {rrp_1:.2f}% a {rrp_2:.2f}%"
        elif rrp_2 < rrp_1:
            evol_rrp = f"disminuyó de {rrp_1:.2f}% a {rrp_2:.2f}%"
        else:
            evol_rrp = f"se mantuvo estable en {rrp_1:.2f}%"
        
        texto = f"ANÁLISIS DE APALANCAMIENTO FINANCIERO\n\n"
        texto += f"En el Año 1, la RAT fue {rat_1:.2f}% y la RRP fue {rrp_1:.2f}%, "
        texto += f"presentando un apalancamiento {apalancamiento_1}.\n\n"
        
        texto += f"En el Año 2, la RAT {evol_rat} y la RRP {evol_rrp}, "
        texto += f"resultando en un apalancamiento {apalancamiento_2}.\n\n"
        
        # Análisis específico del Año 2
        if apalancamiento_2 == "positivo":
            diferencia = rrp_2 - rat_2
            texto += f"El apalancamiento positivo ({rrp_2:.2f}% vs {rat_2:.2f}%) indica que la empresa está utilizando "
            texto += f"deuda de forma eficiente para aumentar la rentabilidad del patrimonio en {diferencia:.2f} puntos porcentuales. "
            texto += "Esto significa que el costo de la deuda es menor que la rentabilidad generada, beneficiando a los accionistas."
        
        elif apalancamiento_2 == "negativo":
            diferencia = rat_2 - rrp_2
            texto += f"El apalancamiento negativo ({rrp_2:.2f}% vs {rat_2:.2f}%) sugiere que el costo de la deuda está "
            texto += f"reduciendo la rentabilidad del patrimonio en {diferencia:.2f} puntos porcentuales. "
            texto += "Esto indica que la empresa podría estar sobre-endeudada o pagando tasas de interés excesivas."
        
        else:  # neutral
            texto += f"El apalancamiento neutral indica que la deuda no está afectando significativamente la rentabilidad "
            texto += "del patrimonio, lo cual puede ser apropiado para una estructura financiera conservadora."
        
        # Recomendación
        if apalancamiento_1 == "positivo" and apalancamiento_2 == "positivo":
            texto += "\n\n✓ RECOMENDACIÓN: Mantener la estrategia de apalancamiento, ya que está generando valor para los accionistas."
        elif apalancamiento_1 == "negativo" and apalancamiento_2 == "positivo":
            texto += "\n\n✓ RECOMENDACIÓN: La mejora en el apalancamiento es positiva. Continuar optimizando la estructura de capital."
        elif apalancamiento_1 == "positivo" and apalancamiento_2 == "negativo":
            texto += "\n\n⚠ RECOMENDACIÓN: Revisar la estructura de deuda, ya que el apalancamiento se volvió negativo."
        elif apalancamiento_1 == "negativo" and apalancamiento_2 == "negativo":
            texto += "\n\n⚠ RECOMENDACIÓN: Considerar reducir deuda o negociar mejores tasas para mejorar la rentabilidad patrimonial."
        
        return texto