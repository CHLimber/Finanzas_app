"""
Archivo: core/analysis/margenes_analysis.py
Analisis de Margenes de Ganancia y Eficiencia en Costos
CORREGIDO: Nueva logica que evalua margenes por valor absoluto,
separa impuestos de gastos financieros, y considera evolucion temporal.
"""


class MargenesAnalysis:
    """Analisis completo de margenes de ganancia"""
    
    def __init__(self, income_data):
        self.income_data = income_data
    
    def calcular_margen_bruto(self, year):
        """
        Calcula Margen Bruto = (Ganancia Bruta / Ingresos) x 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Margen bruto en porcentaje
        """
        ganancia_bruta = self.income_data.get_ganancia_bruta(year)
        ingresos = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0.0
        
        return (ganancia_bruta / ingresos) * 100
    
    def calcular_margen_operativo(self, year):
        """
        Calcula Margen Operativo = (BAII / Ingresos) x 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Margen operativo en porcentaje
        """
        baii = self.income_data.get_utilidad_operativa(year)
        ingresos = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0.0
        
        return (baii / ingresos) * 100
    
    def calcular_margen_neto(self, year):
        """
        Calcula Margen Neto = (Utilidad Neta / Ingresos) x 100
        
        Args:
            year: 1 o 2
            
        Returns:
            float: Margen neto en porcentaje
        """
        utilidad_neta = self.income_data.get_utilidad_neta(year)
        ingresos = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0.0
        
        return (utilidad_neta / ingresos) * 100
    
    def analisis_dual_margenes(self):
        """
        Analisis completo de margenes para ambos años
        
        Returns:
            dict: Analisis completo con interpretaciones
        """
        # año 1
        margen_bruto_1 = self.calcular_margen_bruto(1)
        margen_operativo_1 = self.calcular_margen_operativo(1)
        margen_neto_1 = self.calcular_margen_neto(1)
        
        # año 2
        margen_bruto_2 = self.calcular_margen_bruto(2)
        margen_operativo_2 = self.calcular_margen_operativo(2)
        margen_neto_2 = self.calcular_margen_neto(2)
        
        # Interpretaciones individuales
        interp_bruto = self._interpretar_margen_bruto(margen_bruto_1, margen_bruto_2)
        interp_operativo = self._interpretar_margen_operativo(margen_operativo_1, margen_operativo_2)
        interp_neto = self._interpretar_margen_neto(margen_neto_1, margen_neto_2)
        
        # Interpretacion conjunta y eficiencia
        interp_eficiencia = self._interpretar_eficiencia_costos(
            margen_bruto_1, margen_operativo_1, margen_neto_1,
            margen_bruto_2, margen_operativo_2, margen_neto_2
        )
        
        return {
            'año_1': {
                'margen_bruto': margen_bruto_1,
                'margen_operativo': margen_operativo_1,
                'margen_neto': margen_neto_1
            },
            'año_2': {
                'margen_bruto': margen_bruto_2,
                'margen_operativo': margen_operativo_2,
                'margen_neto': margen_neto_2
            },
            'interpretaciones': {
                'margen_bruto': interp_bruto,
                'margen_operativo': interp_operativo,
                'margen_neto': interp_neto,
                'eficiencia_costos': interp_eficiencia
            }
        }
    
    def _interpretar_margen_bruto(self, mb1, mb2):
        """Interpreta el margen bruto"""
        # Evaluar nivel
        if mb2 >= 70:
            nivel = "muy alto"
            calidad = "excelente"
        elif mb2 >= 50:
            nivel = "alto"
            calidad = "buena"
        elif mb2 >= 30:
            nivel = "moderado"
            calidad = "aceptable"
        else:
            nivel = "bajo"
            calidad = "deficiente"
        
        # Tendencia
        if mb2 > mb1:
            tendencia = f"mejoro de {mb1:.2f}% a {mb2:.2f}%"
            evolucion = "positiva"
        elif mb2 < mb1:
            tendencia = f"disminuyo de {mb1:.2f}% a {mb2:.2f}%"
            evolucion = "negativa"
        else:
            tendencia = f"se mantuvo estable en {mb1:.2f}%"
            evolucion = "estable"
        
        texto = f"MARGEN BRUTO: {tendencia}.\n\n"
        texto += f"El margen bruto de {mb2:.2f}% es {nivel}, indicando una capacidad {calidad} de generar valor sobre los ingresos. "
        
        if mb2 >= 50:
            texto += "Esto muestra eficiencia en los costos directos del servicio, tipico de empresas de software donde "
            texto += "los costos de produccion son relativamente bajos en comparacion con los ingresos."
        elif mb2 >= 30:
            texto += "Aunque es aceptable, podria mejorarse optimizando los costos directos de produccion o servicio."
        else:
            texto += "Este margen es bajo, sugiriendo costos directos excesivos que requieren atencion inmediata."
        
        return texto
    
    def _interpretar_margen_operativo(self, mo1, mo2):
        """Interpreta el margen operativo"""
        # Evaluar nivel
        if mo2 >= 25:
            nivel = "excelente"
            control = "muy bueno"
        elif mo2 >= 15:
            nivel = "bueno"
            control = "adecuado"
        elif mo2 >= 8:
            nivel = "moderado"
            control = "aceptable"
        else:
            nivel = "bajo"
            control = "deficiente"
        
        # Tendencia
        if mo2 > mo1:
            tendencia = f"mejoro de {mo1:.2f}% a {mo2:.2f}%"
        elif mo2 < mo1:
            tendencia = f"disminuyo de {mo1:.2f}% a {mo2:.2f}%"
        else:
            tendencia = f"se mantuvo estable en {mo1:.2f}%"
        
        texto = f"MARGEN OPERATIVO: {tendencia}.\n\n"
        texto += f"El margen operativo de {mo2:.2f}% es {nivel}, confirmando un control {control} de los gastos administrativos, "
        texto += "de ventas y depreciaciones. "
        
        if mo2 >= 15:
            texto += "Esto indica que la empresa opera eficientemente, manteniendo los gastos operativos bajo control "
            texto += "y generando valor significativo de sus operaciones."
        elif mo2 >= 8:
            texto += "Aunque aceptable, hay margen para mejorar la eficiencia operativa reduciendo gastos administrativos o de ventas."
        else:
            texto += "Este margen bajo sugiere gastos operativos excesivos que erosionan la rentabilidad. "
            texto += "Se recomienda revisar la estructura de costos operativos."
        
        return texto
    
    def _interpretar_margen_neto(self, mn1, mn2):
        """Interpreta el margen neto"""
        # Evaluar nivel
        if mn2 >= 20:
            nivel = "muy saludable"
            rentabilidad = "excelente"
        elif mn2 >= 10:
            nivel = "saludable"
            rentabilidad = "buena"
        elif mn2 >= 5:
            nivel = "moderado"
            rentabilidad = "aceptable"
        else:
            nivel = "bajo"
            rentabilidad = "deficiente"
        
        # Tendencia
        if mn2 > mn1:
            tendencia = f"mejoro de {mn1:.2f}% a {mn2:.2f}%"
        elif mn2 < mn1:
            tendencia = f"disminuyo de {mn1:.2f}% a {mn2:.2f}%"
        else:
            tendencia = f"se mantuvo estable en {mn1:.2f}%"
        
        texto = f"MARGEN NETO: {tendencia}.\n\n"
        texto += f"El margen neto de {mn2:.2f}% es {nivel}, reflejando una rentabilidad final {rentabilidad}. "
        
        if mn2 >= 10:
            texto += "Esto indica que, despues de impuestos y gastos financieros, la empresa mantiene una rentabilidad solida, "
            texto += "generando valor consistente para los accionistas."
        elif mn2 >= 5:
            texto += "Aunque positivo, hay margen de mejora. Considerar optimizacion de gastos financieros o estructura tributaria."
        else:
            texto += "Este margen bajo sugiere que los gastos financieros o impuestos estan erosionando significativamente "
            texto += "la rentabilidad final. Revisar estructura de deuda y eficiencia fiscal."
        
        return texto
    
    def _interpretar_eficiencia_costos(self, mb1, mo1, mn1, mb2, mo2, mn2):
        """
        Interpreta la eficiencia en costos analizando los tres margenes en conjunto.
        
        LOGICA CORREGIDA:
        1. Evalua cada margen por su valor absoluto (no por caidas arbitrarias)
        2. Separa el impacto de impuestos (obligatorio) de gastos financieros (controlable)
        3. Considera la evolucion temporal (mejora = mayor eficiencia)
        4. Usa rangos mas universales
        """
        texto = "ANALISIS DE EFICIENCIA EN COSTOS\n\n"
        
        # ============================================================
        # 1. PRESENTAR EVOLUCION DE MARGENES
        # ============================================================
        texto += "EVOLUCION DE MARGENES:\n\n"
        texto += f"                    año 1      año 2     Variacion\n"
        texto += f"Margen Bruto:      {mb1:6.2f}%   {mb2:6.2f}%    {mb2-mb1:+.2f} p.p.\n"
        texto += f"Margen Operativo:  {mo1:6.2f}%   {mo2:6.2f}%    {mo2-mo1:+.2f} p.p.\n"
        texto += f"Margen Neto:       {mn1:6.2f}%   {mn2:6.2f}%    {mn2-mn1:+.2f} p.p.\n\n"
        
        # ============================================================
        # 2. EVALUAR CADA NIVEL DE MARGEN (año 2)
        # ============================================================
        texto += "EVALUACION POR NIVEL (año 2):\n\n"
        
        # --- MARGEN BRUTO (eficiencia en costos directos) ---
        texto += "1. MARGEN BRUTO (Eficiencia en Costos Directos):\n"
        if mb2 >= 60:
            eval_mb = "EXCELENTE"
            texto += f"   {mb2:.2f}% - {eval_mb}: Costos directos muy bajos respecto a ingresos.\n"
        elif mb2 >= 40:
            eval_mb = "BUENO"
            texto += f"   {mb2:.2f}% - {eval_mb}: Costos directos controlados adecuadamente.\n"
        elif mb2 >= 25:
            eval_mb = "ACEPTABLE"
            texto += f"   {mb2:.2f}% - {eval_mb}: Costos directos moderados, hay espacio de mejora.\n"
        else:
            eval_mb = "DEFICIENTE"
            texto += f"   {mb2:.2f}% - {eval_mb}: Costos directos muy elevados.\n"
        
        # --- MARGEN OPERATIVO (eficiencia en gastos operativos) ---
        texto += "\n2. MARGEN OPERATIVO (Eficiencia en Gastos Operativos):\n"
        # Calcular que porcentaje del margen bruto se conserva como operativo
        retencion_operativa = (mo2 / mb2 * 100) if mb2 > 0 else 0
        
        if mo2 >= 20:
            eval_mo = "EXCELENTE"
            texto += f"   {mo2:.2f}% - {eval_mo}: Gastos operativos muy bien controlados.\n"
        elif mo2 >= 12:
            eval_mo = "BUENO"
            texto += f"   {mo2:.2f}% - {eval_mo}: Gastos operativos en nivel adecuado.\n"
        elif mo2 >= 5:
            eval_mo = "ACEPTABLE"
            texto += f"   {mo2:.2f}% - {eval_mo}: Gastos operativos moderados.\n"
        else:
            eval_mo = "DEFICIENTE"
            texto += f"   {mo2:.2f}% - {eval_mo}: Gastos operativos excesivos.\n"
        
        texto += f"   Retencion del Margen Bruto: {retencion_operativa:.1f}% "
        if retencion_operativa >= 40:
            texto += "(eficiente)\n"
        elif retencion_operativa >= 25:
            texto += "(aceptable)\n"
        else:
            texto += "(baja - revisar gastos operativos)\n"
        
        # --- MARGEN NETO (rentabilidad final) ---
        texto += "\n3. MARGEN NETO (Rentabilidad Final):\n"
        # Calcular impacto de impuestos (aproximado como 25% de la utilidad antes de impuestos)
        # Si MN = UAI * 0.75 / Ingresos, entonces UAI/Ingresos = MN / 0.75
        margen_antes_imp = mn2 / 0.75 if mn2 > 0 else 0
        impacto_impuestos = margen_antes_imp - mn2
        impacto_gtos_fin = mo2 - margen_antes_imp
        
        if mn2 >= 15:
            eval_mn = "EXCELENTE"
            texto += f"   {mn2:.2f}% - {eval_mn}: Rentabilidad final muy solida.\n"
        elif mn2 >= 8:
            eval_mn = "BUENO"
            texto += f"   {mn2:.2f}% - {eval_mn}: Rentabilidad final adecuada.\n"
        elif mn2 >= 3:
            eval_mn = "ACEPTABLE"
            texto += f"   {mn2:.2f}% - {eval_mn}: Rentabilidad final ajustada.\n"
        else:
            eval_mn = "DEFICIENTE"
            texto += f"   {mn2:.2f}% - {eval_mn}: Rentabilidad final insuficiente.\n"
        
        # Desglose del impacto
        texto += f"\n   Desglose Operativo -> Neto:\n"
        texto += f"   - Gastos Financieros: -{impacto_gtos_fin:.2f} p.p. "
        if impacto_gtos_fin <= 2:
            texto += "(bajo/nulo)\n"
        elif impacto_gtos_fin <= 5:
            texto += "(moderado)\n"
        else:
            texto += "(ALTO - revisar estructura de deuda)\n"
        
        texto += f"   - Impuestos (25%):    -{impacto_impuestos:.2f} p.p. (obligatorio, no es ineficiencia)\n"
        
        # ============================================================
        # 3. ANALISIS DE TENDENCIA (mejora vs deterioro)
        # ============================================================
        texto += "\nTENDENCIA DE EFICIENCIA:\n\n"
        
        mejora_mb = mb2 - mb1
        mejora_mo = mo2 - mo1
        mejora_mn = mn2 - mn1
        
        mejoras = 0
        deterioros = 0
        
        if mejora_mb > 0.5:
            texto += f"   Margen Bruto: MEJORO +{mejora_mb:.2f} p.p. (mayor eficiencia en costos directos)\n"
            mejoras += 1
        elif mejora_mb < -0.5:
            texto += f"   Margen Bruto: EMPEORO {mejora_mb:.2f} p.p. (menor eficiencia en costos directos)\n"
            deterioros += 1
        else:
            texto += f"   Margen Bruto: ESTABLE ({mejora_mb:+.2f} p.p.)\n"
        
        if mejora_mo > 0.5:
            texto += f"   Margen Operativo: MEJORO +{mejora_mo:.2f} p.p. (mayor eficiencia operativa)\n"
            mejoras += 1
        elif mejora_mo < -0.5:
            texto += f"   Margen Operativo: EMPEORO {mejora_mo:.2f} p.p. (menor eficiencia operativa)\n"
            deterioros += 1
        else:
            texto += f"   Margen Operativo: ESTABLE ({mejora_mo:+.2f} p.p.)\n"
        
        if mejora_mn > 0.5:
            texto += f"   Margen Neto: MEJORO +{mejora_mn:.2f} p.p. (mayor rentabilidad final)\n"
            mejoras += 1
        elif mejora_mn < -0.5:
            texto += f"   Margen Neto: EMPEORO {mejora_mn:.2f} p.p. (menor rentabilidad final)\n"
            deterioros += 1
        else:
            texto += f"   Margen Neto: ESTABLE ({mejora_mn:+.2f} p.p.)\n"
        
        # ============================================================
        # 4. CONCLUSION FINAL
        # ============================================================
        texto += "\nCONCLUSION - EFICIENCIA EN COSTOS:\n\n"
        
        # Evaluar eficiencia por niveles de margen (valores absolutos)
        es_eficiente_bruto = mb2 >= 40
        es_eficiente_operativo = mo2 >= 12
        es_eficiente_neto = mn2 >= 8
        tendencia_positiva = mejoras > deterioros
        
        # Contar niveles eficientes
        niveles_eficientes = sum([es_eficiente_bruto, es_eficiente_operativo, es_eficiente_neto])
        
        if niveles_eficientes == 3:
            texto += "SI, LA EMPRESA ES EFICIENTE EN COSTOS.\n\n"
            texto += "Los tres margenes estan en niveles saludables:\n"
            texto += f"  - Margen Bruto {mb2:.2f}%: Control eficiente de costos directos\n"
            texto += f"  - Margen Operativo {mo2:.2f}%: Control eficiente de gastos operativos\n"
            texto += f"  - Margen Neto {mn2:.2f}%: Rentabilidad final solida\n"
            
            if tendencia_positiva:
                texto += "\nAdemas, la tendencia es POSITIVA con mejoras en los margenes respecto al año anterior."
            elif mejoras == deterioros == 0:
                texto += "\nLos margenes se mantienen estables respecto al año anterior."
        
        elif niveles_eficientes == 2:
            texto += "PARCIALMENTE EFICIENTE - Un area requiere atencion.\n\n"
            
            if not es_eficiente_bruto:
                texto += f"  - Margen Bruto {mb2:.2f}%: REQUIERE MEJORA en costos directos\n"
            else:
                texto += f"  - Margen Bruto {mb2:.2f}%: Adecuado\n"
            
            if not es_eficiente_operativo:
                texto += f"  - Margen Operativo {mo2:.2f}%: REQUIERE MEJORA en gastos operativos\n"
            else:
                texto += f"  - Margen Operativo {mo2:.2f}%: Adecuado\n"
            
            if not es_eficiente_neto:
                texto += f"  - Margen Neto {mn2:.2f}%: REQUIERE MEJORA (revisar gastos financieros)\n"
            else:
                texto += f"  - Margen Neto {mn2:.2f}%: Adecuado\n"
            
            if tendencia_positiva:
                texto += "\nLa tendencia es positiva, lo que indica mejora progresiva."
        
        elif niveles_eficientes == 1:
            texto += "BAJA EFICIENCIA - Dos areas requieren atencion urgente.\n\n"
            texto += "Se recomienda revisar:\n"
            if not es_eficiente_bruto:
                texto += "  - Costos directos de produccion/servicio\n"
            if not es_eficiente_operativo:
                texto += "  - Gastos administrativos, de ventas y depreciaciones\n"
            if not es_eficiente_neto:
                texto += "  - Estructura de financiamiento y carga de intereses\n"
        
        else:
            texto += "NO ES EFICIENTE EN COSTOS - Requiere revision integral.\n\n"
            texto += "Todos los margenes estan por debajo de los niveles recomendados.\n"
            texto += "Se requiere una revision completa de la estructura de costos:\n"
            texto += "  1. Optimizar costos directos de produccion/servicio\n"
            texto += "  2. Reducir gastos administrativos y de ventas\n"
            texto += "  3. Reestructurar deuda para reducir gastos financieros\n"
        
        return texto