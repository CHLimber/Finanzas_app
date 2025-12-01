"""
Archivo: core/analysis/resumen_integral.py
Resumen Integral de todos los Ratios Financieros
"""

from core.analysis.financial_interpreter import FinancialInterpreter


class ResumenIntegralRatios:
    """Genera resumen completo con interpretaciones de todos los ratios"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data
        self.interpreter = FinancialInterpreter()
    
    def _get_total_pasivos(self, year):
        """Helper: Calcula Pasivo Total = PC + PNC"""
        return (self.balance_data.get_total_pasivo_corriente(year) + 
                self.balance_data.get_total_pasivo_no_corriente(year))
    
    def generar_resumen_completo(self):
        """
        Genera resumen completo de todos los ratios con interpretación, causa y recomendación
        
        Returns:
            dict: Resumen completo por categorías
        """
        # Calcular todos los ratios
        ratios = {
            # ANÁLISIS PATRIMONIAL
            'fondo_maniobra': self._calcular_ratio_fm(2),
            'razon_liquidez': self._calcular_liquidez_general(2),
            'razon_tesoreria': self._calcular_razon_tesoreria(2),
            'razon_disponibilidad': self._calcular_razon_disponibilidad(2),
            
            # ANÁLISIS FINANCIERO
            'ratio_garantia': self._calcular_ratio_garantia(2),
            'ratio_autonomia': self._calcular_ratio_autonomia(2),
            'ratio_calidad_deuda': self._calcular_ratio_calidad_deuda(2),
            # ratio_endeudamiento no está en financial_interpreter - removido
            
            # ANÁLISIS ECONÓMICO
            'rrp': self._calcular_rrp(2),
            'margen_neto': self._calcular_margen_neto(2),
            'rotacion_activos': self._calcular_rotacion_activos(2),
            'apalancamiento': self._calcular_apalancamiento(2)
        }
        
        # Generar análisis completo para cada ratio
        resumen = {
            'patrimonial': [],
            'financiero': [],
            'economico': []
        }
        
        # PATRIMONIAL
        for ratio_key in ['fondo_maniobra', 'razon_liquidez', 'razon_tesoreria', 'razon_disponibilidad']:
            if ratio_key in ratios:
                analisis = self.interpreter.evaluate_ratio(ratio_key, ratios[ratio_key])
                # Solo agregar si no hay error
                if 'error' not in analisis:
                    resumen['patrimonial'].append({
                        'ratio_key': ratio_key,
                        'valor': ratios[ratio_key],
                        'analisis': analisis
                    })
        
        # FINANCIERO
        for ratio_key in ['ratio_garantia', 'ratio_autonomia', 'ratio_calidad_deuda']:
            if ratio_key in ratios:
                analisis = self.interpreter.evaluate_ratio(ratio_key, ratios[ratio_key])
                # Solo agregar si no hay error
                if 'error' not in analisis:
                    resumen['financiero'].append({
                        'ratio_key': ratio_key,
                        'valor': ratios[ratio_key],
                        'analisis': analisis
                    })
        
        # ECONÓMICO
        for ratio_key in ['rrp', 'margen_neto', 'rotacion_activos', 'apalancamiento']:
            if ratio_key in ratios:
                analisis = self.interpreter.evaluate_ratio(ratio_key, ratios[ratio_key])
                # Solo agregar si no hay error
                if 'error' not in analisis:
                    resumen['economico'].append({
                        'ratio_key': ratio_key,
                        'valor': ratios[ratio_key],
                        'analisis': analisis
                    })
        
        # Generar conclusión global
        resumen['conclusion_global'] = self._generar_conclusion_global(resumen)
        
        return resumen
    
    def _calcular_ratio_fm(self, year):
        """Calcula Ratio FM = FM / Activo Total"""
        ac = self.balance_data.get_total_corriente(year)
        pc = self.balance_data.get_total_pasivo_corriente(year)
        fm = ac - pc
        activo = self.balance_data.get_total_activos(year)
        return (fm / activo) if activo != 0 else 0
    
    def _calcular_liquidez_general(self, year):
        """Calcula Liquidez General = AC / PC"""
        ac = self.balance_data.get_total_corriente(year)
        pc = self.balance_data.get_total_pasivo_corriente(year)
        return (ac / pc) if pc != 0 else 0
    
    def _calcular_razon_tesoreria(self, year):
        """Calcula Razón de Tesorería"""
        if year == 1:
            disponible = self.balance_data.caja_bancos_y1
            cxc = self.balance_data.clientes_cobrar_y1
        else:
            disponible = self.balance_data.caja_bancos_y2
            cxc = self.balance_data.clientes_cobrar_y2
        
        pc = self.balance_data.get_total_pasivo_corriente(year)
        return ((disponible + cxc) / pc) if pc != 0 else 0
    
    def _calcular_razon_disponibilidad(self, year):
        """Calcula Razón de Disponibilidad"""
        disponible = self.balance_data.caja_bancos_y1 if year == 1 else self.balance_data.caja_bancos_y2
        pc = self.balance_data.get_total_pasivo_corriente(year)
        return (disponible / pc) if pc != 0 else 0
    
    def _calcular_ratio_garantia(self, year):
        """Calcula Ratio de Garantía"""
        activo = self.balance_data.get_total_activos(year)
        pasivo = self._get_total_pasivos(year)
        return (activo / pasivo) if pasivo != 0 else 0
    
    def _calcular_ratio_autonomia(self, year):
        """Calcula Ratio de Autonomía"""
        patrimonio = self.balance_data.get_total_patrimonio(year)
        pasivo = self._get_total_pasivos(year)
        return (patrimonio / pasivo) if pasivo != 0 else 0
    
    def _calcular_ratio_calidad_deuda(self, year):
        """Calcula Calidad de Deuda"""
        pc = self.balance_data.get_total_pasivo_corriente(year)
        pasivo = self._get_total_pasivos(year)
        return (pc / pasivo) if pasivo != 0 else 0
    
    def _calcular_ratio_endeudamiento(self, year):
        """Calcula Ratio de Endeudamiento"""
        pasivo = self._get_total_pasivos(year)
        activo = self.balance_data.get_total_activos(year)
        return (pasivo / activo) if activo != 0 else 0
    
    def _calcular_rrp(self, year):
        """Calcula RRP"""
        un = self.income_data.get_utilidad_neta(year)
        pn = self.balance_data.get_total_patrimonio(year)
        return ((un / pn) * 100) if pn != 0 else 0
    
    def _calcular_margen_neto(self, year):
        """Calcula Margen Neto"""
        un = self.income_data.get_utilidad_neta(year)
        ventas = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        return ((un / ventas) * 100) if ventas != 0 else 0
    
    def _calcular_rotacion_activos(self, year):
        """Calcula Rotación de Activos"""
        ventas = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        activo = self.balance_data.get_total_activos(year)
        return (ventas / activo) if activo != 0 else 0
    
    def _calcular_apalancamiento(self, year):
        """Calcula Apalancamiento"""
        activo = self.balance_data.get_total_activos(year)
        pn = self.balance_data.get_total_patrimonio(year)
        return (activo / pn) if pn != 0 else 0
    
    def _generar_conclusion_global(self, resumen):
        """Genera conclusión global del análisis"""
        # Contar estados
        total_ratios = 0
        optimos = 0
        problematicos = 0
        
        for categoria in ['patrimonial', 'financiero', 'economico']:
            for ratio_data in resumen[categoria]:
                total_ratios += 1
                estado = ratio_data['analisis']['estado']
                if estado == 'optimo':
                    optimos += 1
                else:
                    problematicos += 1
        
        pct_optimos = (optimos / total_ratios * 100) if total_ratios > 0 else 0
        
        texto = "CONCLUSIÓN GLOBAL DEL ANÁLISIS FINANCIERO\n\n"
        
        texto += f"De {total_ratios} ratios analizados:\n"
        texto += f"• {optimos} ratios en rango ÓPTIMO ({pct_optimos:.1f}%)\n"
        texto += f"• {problematicos} ratios requieren ATENCIÓN ({100-pct_optimos:.1f}%)\n\n"
        
        if pct_optimos >= 75:
            texto += "✓ DIAGNÓSTICO: EXCELENTE SALUD FINANCIERA\n\n"
            texto += "La empresa presenta una situación financiera sólida y equilibrada. "
            texto += "La mayoría de los indicadores se encuentran en rangos óptimos, lo que demuestra "
            texto += "una gestión financiera efectiva en las tres dimensiones: patrimonial, financiera y económica.\n\n"
            texto += "Recomendación: Mantener las políticas actuales y continuar monitoreando los ratios "
            texto += "para asegurar la sostenibilidad de esta posición favorable."
        
        elif pct_optimos >= 50:
            texto += "✓ DIAGNÓSTICO: SALUD FINANCIERA ACEPTABLE\n\n"
            texto += "La empresa muestra indicadores financieros mayormente favorables, aunque existen "
            texto += "áreas de mejora identificadas. La situación es estable pero requiere atención "
            texto += "en los ratios que están fuera del rango óptimo.\n\n"
            texto += "Recomendación: Implementar planes de acción específicos para mejorar los ratios "
            texto += "problemáticos, priorizando aquellos que tienen mayor impacto en la operación."
        
        else:
            texto += "⚠ DIAGNÓSTICO: REQUIERE MEJORA\n\n"
            texto += "La empresa enfrenta desafíos financieros significativos que requieren atención inmediata. "
            texto += "Más de la mitad de los indicadores están fuera de rangos óptimos, lo que sugiere "
            texto += "necesidad de reestructuración o ajustes estratégicos importantes.\n\n"
            texto += "Recomendación: Desarrollar un plan de acción integral que aborde las debilidades "
            texto += "identificadas, priorizando la mejora de liquidez, solvencia y/o rentabilidad según "
            texto += "las áreas más críticas."
        
        return texto