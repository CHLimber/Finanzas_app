"""
Archivo: core/analysis/rat_analysis.py
Análisis de Rentabilidad del Activo Total (RAT)
"""


class RATAnalysis:
    """Análisis completo de la Rentabilidad del Activo Total"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data
    
    def calcular_rat(self, year):
        """
        Calcula RAT = BAII / Activo Total × 100
        
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
    
    def analisis_dual(self):
        """
        Análisis comparativo de RAT entre Año 1 y Año 2
        
        Returns:
            dict: Análisis completo con interpretación
        """
        # Datos básicos
        baii_1 = self.income_data.get_utilidad_operativa(1)
        baii_2 = self.income_data.get_utilidad_operativa(2)
        activo_1 = self.balance_data.get_total_activos(1)
        activo_2 = self.balance_data.get_total_activos(2)
        
        # RAT por año
        rat_1 = self.calcular_rat(1)
        rat_2 = self.calcular_rat(2)
        
        # Comparación absoluta (puntos porcentuales)
        delta_rat = rat_2 - rat_1
        
        # Comparación relativa (crecimiento %)
        if rat_1 != 0:
            crecimiento_relativo = (delta_rat / rat_1) * 100
        else:
            crecimiento_relativo = 0.0
        
        # Análisis de sostenibilidad
        interpretacion = self._interpretar_sostenibilidad(
            rat_1, rat_2, baii_1, baii_2, activo_1, activo_2, 
            delta_rat, crecimiento_relativo
        )
        
        return {
            'ano_1': {
                'baii': baii_1,
                'activo_total': activo_1,
                'rat': rat_1
            },
            'ano_2': {
                'baii': baii_2,
                'activo_total': activo_2,
                'rat': rat_2
            },
            'comparacion': {
                'delta_absoluto': delta_rat,  # puntos porcentuales
                'crecimiento_relativo': crecimiento_relativo,  # porcentaje
                'interpretacion': interpretacion,
                'sostenible': self._evaluar_sostenibilidad(baii_1, baii_2, activo_1, activo_2, rat_2, rat_1)
            }
        }
    
    def _evaluar_sostenibilidad(self, baii_1, baii_2, activo_1, activo_2, rat_2, rat_1):
        """
        Evalúa si el cambio en RAT es sostenible
        
        Returns:
            str: 'sostenible', 'precaucion', 'no_sostenible'
        """
        # RAT aumenta y BAII crece más rápido que activo
        if rat_2 > rat_1 and baii_2 > baii_1:
            # Verificar que activo no creció demasiado (máximo 10% más que BAII)
            if activo_1 > 0:
                crecimiento_activo = ((activo_2 - activo_1) / activo_1) * 100
            else:
                crecimiento_activo = 0
            
            if baii_1 > 0:
                crecimiento_baii = ((baii_2 - baii_1) / baii_1) * 100
            else:
                crecimiento_baii = 100 if baii_2 > 0 else 0
            
            if crecimiento_baii >= crecimiento_activo:
                return 'sostenible'
            elif activo_2 <= activo_1 * 1.10:  # Activo creció máx 10%
                return 'sostenible'
            else:
                return 'precaucion'
        
        # RAT aumenta porque activo disminuye (precaución)
        elif rat_2 > rat_1 and activo_2 < activo_1:
            return 'precaucion'
        
        # RAT disminuye
        elif rat_2 < rat_1:
            return 'no_sostenible'
        
        # RAT se mantiene estable
        else:
            return 'estable'
    
    def _interpretar_sostenibilidad(self, rat_1, rat_2, baii_1, baii_2, 
                                    activo_1, activo_2, delta_rat, crecimiento_rel):
        """
        Genera interpretación profesional del análisis RAT
        
        Returns:
            str: Interpretación completa
        """
        # Determinar tendencia
        if rat_2 > rat_1:
            tendencia = "aumentó"
        elif rat_2 < rat_1:
            tendencia = "disminuyó"
        else:
            tendencia = "se mantuvo estable"
        
        # Calcular crecimientos
        if activo_1 > 0:
            var_activo = ((activo_2 - activo_1) / activo_1) * 100
        else:
            var_activo = 0
        
        if baii_1 > 0:
            var_baii = ((baii_2 - baii_1) / baii_1) * 100
        else:
            var_baii = 100 if baii_2 > 0 else 0
        
        # Texto base
        texto = f"La rentabilidad del activo {tendencia} de {rat_1:.2f}% en Año 1 a {rat_2:.2f}% en Año 2, "
        texto += f"lo que representa un cambio de {delta_rat:+.2f} puntos porcentuales "
        
        if rat_1 != 0:
            texto += f"y un {'incremento' if crecimiento_rel > 0 else 'decremento'} relativo del {abs(crecimiento_rel):.2f}%. "
        else:
            texto += ". "
        
        # Análisis de sostenibilidad
        sostenibilidad = self._evaluar_sostenibilidad(baii_1, baii_2, activo_1, activo_2, rat_2, rat_1)
        
        if sostenibilidad == 'sostenible':
            texto += f"\n\nEl cambio es SOSTENIBLE, ya que el BAII creció {var_baii:.2f}% mientras que el activo total creció {var_activo:.2f}%. "
            texto += "Esto indica que la empresa está mejorando su eficiencia operativa y su capacidad para generar resultados a partir de sus inversiones."
        
        elif sostenibilidad == 'precaucion':
            if activo_2 < activo_1:
                texto += f"\n\nSe debe tener PRECAUCIÓN, ya que aunque el RAT aumentó, el activo total disminuyó {abs(var_activo):.2f}%. "
                texto += "Esto puede indicar venta de activos o menor inversión, lo cual no es necesariamente sostenible a largo plazo."
            else:
                texto += f"\n\nSe debe tener PRECAUCIÓN, ya que el activo total creció {var_activo:.2f}% mientras el BAII solo creció {var_baii:.2f}%. "
                texto += "Esto sugiere que las nuevas inversiones aún no están generando la rentabilidad esperada."
        
        elif sostenibilidad == 'no_sostenible':
            texto += f"\n\nEl cambio NO ES SOSTENIBLE. El BAII varió {var_baii:+.2f}% y el activo total {var_activo:+.2f}%. "
            texto += "Esto indica que la empresa está perdiendo eficiencia operativa, lo cual requiere atención inmediata."
        
        else:  # estable
            texto += "\n\nEl RAT se mantiene estable, lo que sugiere una gestión consistente de los activos, aunque sin mejoras significativas en eficiencia."
        
        return texto