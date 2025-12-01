"""
Archivo: core/analysis/dupont_analysis.py
Análisis DuPont para descomponer la Rentabilidad de Recursos Propios
"""


class DuPontAnalysis:
    """Análisis DuPont completo con descomposición de RRP"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data
    
    def calcular_margen_neto(self, year):
        """
        Calcula Margen Neto = Utilidad Neta / Ventas × 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Margen neto en porcentaje
        """
        utilidad_neta = self.income_data.get_utilidad_neta(year)
        ventas = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        
        if ventas == 0:
            return 0.0
        
        return (utilidad_neta / ventas) * 100
    
    def calcular_rotacion_activo(self, year):
        """
        Calcula Rotación del Activo = Ventas / Activo Total
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Rotación del activo (veces)
        """
        ventas = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        activo_total = self.balance_data.get_total_activos(year)
        
        if activo_total == 0:
            return 0.0
        
        return ventas / activo_total
    
    def calcular_apalancamiento(self, year):
        """
        Calcula Apalancamiento Financiero = Activo Total / Patrimonio Neto
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Apalancamiento (veces)
        """
        activo_total = self.balance_data.get_total_activos(year)
        patrimonio_neto = self.balance_data.get_total_patrimonio(year)
        
        if patrimonio_neto == 0:
            return 0.0
        
        return activo_total / patrimonio_neto
    
    def calcular_rrp_dupont(self, year):
        """
        Calcula RRP usando la fórmula DuPont:
        RRP = Margen Neto × Rotación Activo × Apalancamiento
        
        Args:
            year: 1 o 2
            
        Returns:
            float: RRP calculado mediante DuPont (%)
        """
        margen = self.calcular_margen_neto(year) / 100  # Convertir a decimal
        rotacion = self.calcular_rotacion_activo(year)
        apalancamiento = self.calcular_apalancamiento(year)
        
        return (margen * rotacion * apalancamiento) * 100
    
    def calcular_rrp_directo(self, year):
        """
        Calcula RRP directamente para verificación:
        RRP = Utilidad Neta / Patrimonio Neto × 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: RRP directo (%)
        """
        utilidad_neta = self.income_data.get_utilidad_neta(year)
        patrimonio_neto = self.balance_data.get_total_patrimonio(year)
        
        if patrimonio_neto == 0:
            return 0.0
        
        return (utilidad_neta / patrimonio_neto) * 100
    
    def analisis_dupont_dual(self):
        """
        Análisis DuPont completo para ambos años con verificación
        
        Returns:
            dict: Análisis completo con componentes y verificación
        """
        # Año 1
        margen_1 = self.calcular_margen_neto(1)
        rotacion_1 = self.calcular_rotacion_activo(1)
        apalancamiento_1 = self.calcular_apalancamiento(1)
        rrp_dupont_1 = self.calcular_rrp_dupont(1)
        rrp_directo_1 = self.calcular_rrp_directo(1)
        
        # Año 2
        margen_2 = self.calcular_margen_neto(2)
        rotacion_2 = self.calcular_rotacion_activo(2)
        apalancamiento_2 = self.calcular_apalancamiento(2)
        rrp_dupont_2 = self.calcular_rrp_dupont(2)
        rrp_directo_2 = self.calcular_rrp_directo(2)
        
        # Verificación (tolerancia de 0.01% por redondeos)
        verificacion_1 = abs(rrp_dupont_1 - rrp_directo_1) < 0.01
        verificacion_2 = abs(rrp_dupont_2 - rrp_directo_2) < 0.01
        
        # Interpretación
        interpretacion = self._interpretar_dupont(
            margen_1, margen_2,
            rotacion_1, rotacion_2,
            apalancamiento_1, apalancamiento_2,
            rrp_dupont_1, rrp_dupont_2
        )
        
        return {
            'ano_1': {
                'margen_neto': margen_1,
                'rotacion_activo': rotacion_1,
                'apalancamiento': apalancamiento_1,
                'rrp_dupont': rrp_dupont_1,
                'rrp_directo': rrp_directo_1,
                'verificacion': verificacion_1
            },
            'ano_2': {
                'margen_neto': margen_2,
                'rotacion_activo': rotacion_2,
                'apalancamiento': apalancamiento_2,
                'rrp_dupont': rrp_dupont_2,
                'rrp_directo': rrp_directo_2,
                'verificacion': verificacion_2
            },
            'interpretacion': interpretacion
        }
    
    def _interpretar_dupont(self, margen_1, margen_2, rotacion_1, rotacion_2,
                           apalancamiento_1, apalancamiento_2, rrp_1, rrp_2):
        """
        Genera interpretación del análisis DuPont
        
        Returns:
            str: Interpretación completa
        """
        texto = "ANÁLISIS DUPONT - DESCOMPOSICIÓN DEL RRP\n\n"
        
        # Evolución del RRP
        if rrp_2 > rrp_1:
            evol_rrp = f"aumentó de {rrp_1:.2f}% a {rrp_2:.2f}%"
            tendencia = "mejora"
        elif rrp_2 < rrp_1:
            evol_rrp = f"disminuyó de {rrp_1:.2f}% a {rrp_2:.2f}%"
            tendencia = "deterioro"
        else:
            evol_rrp = f"se mantuvo estable en {rrp_1:.2f}%"
            tendencia = "estabilidad"
        
        texto += f"La rentabilidad de los recursos propios {evol_rrp}, lo cual se explica por la evolución de sus tres componentes:\n\n"
        
        # Análisis del Margen Neto
        var_margen = ((margen_2 - margen_1) / margen_1 * 100) if margen_1 != 0 else 0
        texto += f"1. MARGEN NETO (Eficiencia Operativa):\n"
        texto += f"   - Año 1: {margen_1:.2f}%\n"
        texto += f"   - Año 2: {margen_2:.2f}%\n"
        
        if margen_2 > margen_1:
            texto += f"   ✓ Mejoró {abs(var_margen):.2f}%, indicando mayor eficiencia en convertir ventas en utilidad neta.\n"
        elif margen_2 < margen_1:
            texto += f"   ✗ Disminuyó {abs(var_margen):.2f}%, sugiriendo menores márgenes o mayores costos operativos.\n"
        else:
            texto += f"   = Se mantuvo estable, conservando la eficiencia operativa.\n"
        
        # Análisis de Rotación del Activo
        var_rotacion = ((rotacion_2 - rotacion_1) / rotacion_1 * 100) if rotacion_1 != 0 else 0
        texto += f"\n2. ROTACIÓN DEL ACTIVO (Eficiencia en el Uso de Activos):\n"
        texto += f"   - Año 1: {rotacion_1:.2f} veces\n"
        texto += f"   - Año 2: {rotacion_2:.2f} veces\n"
        
        if rotacion_2 > rotacion_1:
            texto += f"   ✓ Mejoró {abs(var_rotacion):.2f}%, indicando mejor aprovechamiento de los activos para generar ventas.\n"
        elif rotacion_2 < rotacion_1:
            texto += f"   ✗ Disminuyó {abs(var_rotacion):.2f}%, sugiriendo menor eficiencia o sobreinversión en activos.\n"
        else:
            texto += f"   = Se mantuvo estable, conservando la eficiencia en el uso de activos.\n"
        
        # Análisis del Apalancamiento
        var_apalancamiento = ((apalancamiento_2 - apalancamiento_1) / apalancamiento_1 * 100) if apalancamiento_1 != 0 else 0
        texto += f"\n3. APALANCAMIENTO FINANCIERO (Uso de Deuda):\n"
        texto += f"   - Año 1: {apalancamiento_1:.2f} veces\n"
        texto += f"   - Año 2: {apalancamiento_2:.2f} veces\n"
        
        if apalancamiento_2 > apalancamiento_1:
            texto += f"   ⚠ Aumentó {abs(var_apalancamiento):.2f}%, incrementando el uso de deuda para financiar activos.\n"
        elif apalancamiento_2 < apalancamiento_1:
            texto += f"   ✓ Disminuyó {abs(var_apalancamiento):.2f}%, reduciendo la dependencia de financiación externa.\n"
        else:
            texto += f"   = Se mantuvo estable en la estructura de capital.\n"
        
        # Conclusión
        texto += f"\n\nCONCLUSIÓN:\n"
        
        if tendencia == "mejora":
            # Identificar principal impulsor
            impulsores = []
            if var_margen > 5:
                impulsores.append("mejora en márgenes")
            if var_rotacion > 5:
                impulsores.append("mayor rotación de activos")
            if var_apalancamiento > 5:
                impulsores.append("incremento en apalancamiento")
            
            if impulsores:
                texto += f"La mejora del RRP se debe principalmente a: {', '.join(impulsores)}. "
            else:
                texto += "La mejora del RRP se debe a una combinación equilibrada de los tres factores. "
            
            texto += "Esto indica una gestión financiera efectiva que está maximizando el retorno para los accionistas."
        
        elif tendencia == "deterioro":
            # Identificar principal detractor
            detractores = []
            if var_margen < -5:
                detractores.append("reducción de márgenes")
            if var_rotacion < -5:
                detractores.append("menor rotación de activos")
            if var_apalancamiento < -5:
                detractores.append("desapalancamiento")
            
            if detractores:
                texto += f"El deterioro del RRP se explica por: {', '.join(detractores)}. "
            else:
                texto += "El deterioro del RRP se debe a un deterioro general en las tres componentes. "
            
            texto += "Se recomienda revisar la estrategia operativa y financiera para revertir esta tendencia."
        
        else:  # estabilidad
            texto += "El RRP se mantiene estable. Las variaciones en los componentes se compensan entre sí, "
            texto += "sugiriendo una gestión consistente aunque sin mejoras significativas."
        
        return texto