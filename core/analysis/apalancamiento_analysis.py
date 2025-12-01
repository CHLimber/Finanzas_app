"""
Archivo: core/analysis/apalancamiento_analysis.py
Análisis de Apalancamiento Financiero
"""


class ApalancamientoAnalysis:
    """Análisis completo del apalancamiento financiero"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data
    
    def calcular_costo_deuda(self, year):
        """
        Calcula el costo promedio de la deuda:
        i = Gastos Financieros / Deuda Total × 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Costo de deuda en porcentaje
        """
        gastos_financieros = self.income_data.gastos_financieros_y1 if year == 1 else self.income_data.gastos_financieros_y2
        
        # Deuda Total = Préstamos LP + Deuda CP
        if year == 1:
            deuda_total = self.balance_data.prestamos_lp_y1 + self.balance_data.proveedores_y1
        else:
            deuda_total = self.balance_data.prestamos_lp_y2 + self.balance_data.proveedores_y2
        
        if deuda_total == 0:
            return 0.0
        
        return (gastos_financieros / deuda_total) * 100
    
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
    
    def calcular_efecto_apalancamiento(self, year):
        """
        Calcula el efecto apalancamiento mediante la fórmula:
        RRP = RAT + (D/PN) × (RAT - i)
        
        Args:
            year: 1 o 2
            
        Returns:
            dict: Componentes del efecto apalancamiento
        """
        rat = self.calcular_rat(year)
        i = self.calcular_costo_deuda(year)
        rrp_directo = self.calcular_rrp(year)
        
        # Deuda Total
        if year == 1:
            deuda = self.balance_data.prestamos_lp_y1 + self.balance_data.deuda_cp_y1
        else:
            deuda = self.balance_data.prestamos_lp_y2 + self.balance_data.deuda_cp_y2
        
        patrimonio = self.balance_data.get_total_patrimonio(year)
        
        if patrimonio == 0:
            d_pn = 0
        else:
            d_pn = deuda / patrimonio
        
        # Efecto apalancamiento
        diferencial = rat - i
        efecto = d_pn * diferencial
        rrp_calculado = rat + efecto
        
        return {
            'rat': rat,
            'i': i,
            'deuda': deuda,
            'patrimonio': patrimonio,
            'd_pn': d_pn,
            'diferencial': diferencial,
            'efecto_apalancamiento': efecto,
            'rrp_calculado': rrp_calculado,
            'rrp_directo': rrp_directo
        }
    
    def analisis_dual_apalancamiento(self):
        """
        Análisis completo del apalancamiento financiero para ambos años
        
        Returns:
            dict: Análisis completo con interpretaciones
        """
        # Año 1
        efecto_1 = self.calcular_efecto_apalancamiento(1)
        
        # Año 2
        efecto_2 = self.calcular_efecto_apalancamiento(2)
        
        # Interpretaciones
        interp_costo = self._interpretar_costo_deuda(efecto_1['i'], efecto_2['i'])
        interp_comparacion = self._interpretar_rat_vs_i(efecto_2['rat'], efecto_2['i'])
        interp_efecto = self._interpretar_efecto_apalancamiento(efecto_2)
        interp_recomendacion = self._interpretar_conveniencia_deuda(efecto_2)
        
        return {
            'ano_1': efecto_1,
            'ano_2': efecto_2,
            'interpretaciones': {
                'costo_deuda': interp_costo,
                'rat_vs_i': interp_comparacion,
                'efecto_apalancamiento': interp_efecto,
                'conveniencia_deuda': interp_recomendacion
            }
        }
    
    def _interpretar_costo_deuda(self, i1, i2):
        """Interpreta el costo de la deuda"""
        texto = f"COSTO PROMEDIO DE LA DEUDA\n\n"
        texto += f"Año 1: {i1:.2f}%\n"
        texto += f"Año 2: {i2:.2f}%\n\n"
        
        # Evaluar nivel del costo (Año 2)
        if i2 <= 5:
            nivel = "muy favorable"
            evaluacion = "excelente"
        elif i2 <= 8:
            nivel = "favorable"
            evaluacion = "buena"
        elif i2 <= 12:
            nivel = "moderado"
            evaluacion = "aceptable"
        else:
            nivel = "elevado"
            evaluacion = "preocupante"
        
        texto += f"El costo de la deuda del {i2:.2f}% en el Año 2 es {nivel}, indicando condiciones de financiamiento {evaluacion}. "
        
        if i2 <= 8:
            texto += "La empresa tiene acceso a financiamiento a tasas competitivas, lo cual es positivo para aprovechar el apalancamiento."
        elif i2 <= 12:
            texto += "El costo es razonable pero podría optimizarse mediante negociación de tasas o reestructuración de deuda."
        else:
            texto += "El costo es elevado, lo que reduce significativamente los beneficios del apalancamiento y puede estar erosionando la rentabilidad."
        
        # Tendencia
        if i2 < i1:
            texto += f"\n\nPositivamente, el costo de la deuda disminuyó {abs(i2-i1):.2f} puntos porcentuales respecto al Año 1, "
            texto += "indicando mejora en las condiciones de financiamiento."
        elif i2 > i1:
            texto += f"\n\nEl costo de la deuda aumentó {abs(i2-i1):.2f} puntos porcentuales respecto al Año 1, "
            texto += "lo cual puede indicar endurecimiento de condiciones crediticias o mayor riesgo percibido."
        else:
            texto += "\n\nEl costo de la deuda se mantuvo estable entre períodos."
        
        return texto
    
    def _interpretar_rat_vs_i(self, rat, i):
        """Interpreta la comparación RAT vs i"""
        diferencial = rat - i
        
        texto = f"COMPARACIÓN: RAT vs COSTO DE DEUDA (i)\n\n"
        texto += f"RAT (Rentabilidad Económica): {rat:.2f}%\n"
        texto += f"i (Costo de Deuda): {i:.2f}%\n"
        texto += f"Diferencial (RAT - i): {diferencial:+.2f} puntos porcentuales\n\n"
        
        if diferencial > 0:
            texto += f"✓ APALANCAMIENTO POSITIVO\n\n"
            texto += f"La rentabilidad económica (RAT = {rat:.2f}%) es superior al costo de la deuda (i = {i:.2f}%), "
            texto += f"generando un diferencial positivo de {diferencial:.2f} puntos porcentuales. "
            texto += "Esto significa que la empresa está generando más rentabilidad con sus activos de lo que paga por financiarse, "
            texto += "por lo cual el apalancamiento es POSITIVO y la deuda está aumentando la rentabilidad del patrimonio.\n\n"
            
            if diferencial >= 10:
                texto += "El diferencial es significativo, indicando un apalancamiento muy favorable que amplifica considerablemente "
                texto += "la rentabilidad para los accionistas."
            elif diferencial >= 5:
                texto += "El diferencial es moderado pero positivo, generando valor adicional para los accionistas mediante el uso de deuda."
            else:
                texto += "El diferencial es positivo pero ajustado. Aunque favorable, cambios en las condiciones (tasas o rentabilidad) "
                texto += "podrían reducir o eliminar este beneficio."
        
        elif diferencial < 0:
            texto += f"✗ APALANCAMIENTO NEGATIVO\n\n"
            texto += f"La rentabilidad económica (RAT = {rat:.2f}%) es inferior al costo de la deuda (i = {i:.2f}%), "
            texto += f"generando un diferencial negativo de {diferencial:.2f} puntos porcentuales. "
            texto += "Esto significa que la deuda resulta más costosa que la rentabilidad generada por los activos, "
            texto += "por lo que el apalancamiento es NEGATIVO y la deuda está destruyendo valor para los accionistas.\n\n"
            texto += "En esta situación, la empresa paga más por su financiamiento de lo que genera con sus operaciones, "
            texto += "reduciendo la rentabilidad del patrimonio."
        
        else:
            texto += f"= APALANCAMIENTO NEUTRAL\n\n"
            texto += f"La rentabilidad económica (RAT = {rat:.2f}%) es igual al costo de la deuda (i = {i:.2f}%). "
            texto += "En este caso, el apalancamiento es NEUTRAL y la deuda no mejora ni empeora la rentabilidad del patrimonio."
        
        return texto
    
    def _interpretar_efecto_apalancamiento(self, efecto):
        """Interpreta el efecto apalancamiento mediante la fórmula"""
        rat = efecto['rat']
        i = efecto['i']
        d_pn = efecto['d_pn']
        diferencial = efecto['diferencial']
        efecto_apal = efecto['efecto_apalancamiento']
        rrp_calc = efecto['rrp_calculado']
        rrp_directo = efecto['rrp_directo']
        
        texto = f"EFECTO APALANCAMIENTO - FÓRMULA\n\n"
        texto += f"RRP = RAT + (D/PN) × (RAT - i)\n\n"
        texto += f"Donde:\n"
        texto += f"• RAT = {rat:.2f}%\n"
        texto += f"• i = {i:.2f}%\n"
        texto += f"• D/PN = {d_pn:.2f} veces\n"
        texto += f"• (RAT - i) = {diferencial:.2f} p.p.\n\n"
        
        texto += f"Cálculo:\n"
        texto += f"RRP = {rat:.2f}% + ({d_pn:.2f} × {diferencial:.2f}%)\n"
        texto += f"RRP = {rat:.2f}% + {efecto_apal:.2f}%\n"
        texto += f"RRP = {rrp_calc:.2f}%\n\n"
        
        texto += f"Verificación (RRP directo): {rrp_directo:.2f}%\n\n"
        
        # Interpretación
        if efecto_apal > 0:
            texto += f"✓ EFECTO POSITIVO: +{efecto_apal:.2f} puntos porcentuales\n\n"
            texto += f"El apalancamiento financiero está añadiendo {efecto_apal:.2f} p.p. a la rentabilidad del patrimonio. "
            texto += f"Esto significa que, gracias al uso de deuda, la rentabilidad de los accionistas (RRP = {rrp_directo:.2f}%) "
            texto += f"es superior a la rentabilidad económica pura (RAT = {rat:.2f}%).\n\n"
            texto += "La deuda está MEJORANDO la rentabilidad del patrimonio al permitir financiar más activos sin diluir "
            texto += "el capital de los accionistas."
        
        elif efecto_apal < 0:
            texto += f"✗ EFECTO NEGATIVO: {efecto_apal:.2f} puntos porcentuales\n\n"
            texto += f"El apalancamiento financiero está REDUCIENDO {abs(efecto_apal):.2f} p.p. la rentabilidad del patrimonio. "
            texto += f"Esto significa que la deuda está PERJUDICANDO a los accionistas, reduciendo su rentabilidad "
            texto += f"desde {rat:.2f}% (RAT) hasta {rrp_directo:.2f}% (RRP).\n\n"
            texto += "La deuda está destruyendo valor porque su costo supera la rentabilidad que genera."
        
        else:
            texto += f"= EFECTO NEUTRAL\n\n"
            texto += "El apalancamiento no afecta la rentabilidad del patrimonio. RRP = RAT."
        
        return texto
    
    def _interpretar_conveniencia_deuda(self, efecto):
        """Interpreta si conviene aumentar deuda"""
        rat = efecto['rat']
        i = efecto['i']
        diferencial = efecto['diferencial']
        d_pn = efecto['d_pn']
        
        texto = f"¿CONVIENE AUMENTAR DEUDA?\n\n"
        
        # Condición 1: RAT vs i
        condicion_1 = rat > i
        
        # Condición 2: Nivel de apalancamiento actual
        if d_pn < 0.5:
            nivel_apal = "bajo"
            riesgo = "bajo"
        elif d_pn < 1.0:
            nivel_apal = "moderado"
            riesgo = "moderado"
        elif d_pn < 2.0:
            nivel_apal = "alto"
            riesgo = "elevado"
        else:
            nivel_apal = "muy alto"
            riesgo = "muy elevado"
        
        condicion_2 = d_pn < 1.5  # No sobre-apalancado
        
        # Decisión
        if condicion_1 and condicion_2:
            texto += f"✓ SÍ, CONVIENE AUMENTAR DEUDA\n\n"
            texto += f"Razones:\n"
            texto += f"1. RAT ({rat:.2f}%) > i ({i:.2f}%) → Apalancamiento POSITIVO con diferencial de {diferencial:.2f} p.p.\n"
            texto += f"2. Nivel de apalancamiento actual: {nivel_apal} (D/PN = {d_pn:.2f}), con margen para crecer.\n"
            texto += f"3. La deuda está generando valor y amplificando las ganancias de los accionistas.\n\n"
            texto += f"La empresa puede considerar aumentar su nivel de endeudamiento de forma prudente, ya que:\n"
            texto += f"• Cada peso adicional de deuda genera valor neto de {diferencial:.2f}% anual\n"
            texto += f"• El riesgo financiero actual es {riesgo}\n"
            texto += f"• Hay capacidad para asumir más deuda sin comprometer la solvencia\n\n"
            texto += f"Recomendación: Evaluar oportunidades de inversión que generen retornos superiores al {i:.2f}% "
            texto += f"para maximizar el beneficio del apalancamiento."
        
        elif condicion_1 and not condicion_2:
            texto += f"⚠ PRECAUCIÓN AL AUMENTAR DEUDA\n\n"
            texto += f"Situación mixta:\n"
            texto += f"• ✓ RAT ({rat:.2f}%) > i ({i:.2f}%) → Apalancamiento POSITIVO\n"
            texto += f"• ✗ Apalancamiento actual {nivel_apal} (D/PN = {d_pn:.2f}) → Riesgo {riesgo}\n\n"
            texto += f"Aunque el apalancamiento es positivo y genera valor, el nivel de endeudamiento actual ya es {nivel_apal}. "
            texto += f"Aumentar más deuda incrementaría significativamente el riesgo financiero y la vulnerabilidad ante:\n"
            texto += f"• Cambios en tasas de interés\n"
            texto += f"• Caídas en rentabilidad operativa\n"
            texto += f"• Problemas de liquidez\n\n"
            texto += f"Recomendación: Mantener nivel de deuda actual o aumentar solo moderadamente con proyectos "
            texto += f"de muy alta rentabilidad (>>{i:.2f}%)."
        
        else:  # No condicion_1
            texto += f"✗ NO CONVIENE AUMENTAR DEUDA\n\n"
            texto += f"Razones:\n"
            texto += f"• RAT ({rat:.2f}%) {'<' if rat < i else '='} i ({i:.2f}%) → Apalancamiento {'NEGATIVO' if rat < i else 'NEUTRAL'}\n"
            texto += f"• La deuda está {'DESTRUYENDO' if rat < i else 'sin afectar'} valor para los accionistas\n"
            texto += f"• Cada peso de deuda {'reduce' if rat < i else 'no mejora'} la rentabilidad del patrimonio\n\n"
            
            if rat < i:
                texto += f"La empresa paga más por su financiamiento ({i:.2f}%) de lo que genera con sus activos ({rat:.2f}%). "
                texto += f"En esta situación, aumentar deuda solo empeoraría la rentabilidad de los accionistas.\n\n"
                texto += f"Recomendaciones:\n"
                texto += f"1. Priorizar reducción de deuda o renegociación de tasas\n"
                texto += f"2. Mejorar rentabilidad operativa (RAT) antes de considerar más financiamiento\n"
                texto += f"3. Evaluar venta de activos improductivos para reducir pasivos\n"
                texto += f"4. Fortalecer patrimonio mediante retención de utilidades o aportes de capital"
            else:
                texto += f"Como el apalancamiento es neutral, aumentar deuda no generaría valor adicional. "
                texto += f"Es preferible mantener la estructura actual o buscar mejorar la rentabilidad operativa primero."
        
        return texto