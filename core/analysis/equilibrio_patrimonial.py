"""
Archivo: core/analysis/equilibrio_patrimonial.py
Análisis de Equilibrio Patrimonial y Fondo de Maniobra para 2 años
"""

class EquilibrioPatrimonial:
    """
    Analiza el equilibrio patrimonial de un año específico.
    Determina si la estructura financiera es estable, inestable o nula.
    """
    
    def __init__(self, activo_corriente, activo_no_corriente,
                 pasivo_corriente, pasivo_no_corriente, patrimonio):
        """
        Args:
            activo_corriente: Activo corriente del año
            activo_no_corriente: Activo no corriente del año
            pasivo_corriente: Pasivo corriente del año
            pasivo_no_corriente: Pasivo no corriente del año
            patrimonio: Patrimonio neto del año
        """
        self.AC = activo_corriente
        self.ANC = activo_no_corriente
        self.PC = pasivo_corriente
        self.PNC = pasivo_no_corriente
        self.PAT = patrimonio
    
    def fondo_maniobra_absoluto(self):
        """
        Calcula el Fondo de Maniobra en valor absoluto.
        FM = Activo Corriente - Pasivo Corriente
        
        Returns:
            float: Fondo de Maniobra en unidades monetarias
        """
        return self.AC - self.PC
    
    def fondo_maniobra(self):
        """
        Calcula el Fondo de Maniobra como RATIO (para interpretación).
        FM Ratio = (AC - PC) / Activo Total
        
        IMPORTANTE: Este ratio es el que se usa para la interpretación
        con los rangos (0.10 - 0.30) del FinancialInterpreter.
        
        Returns:
            float: FM como ratio decimal
        """
        activo_total = self.AC + self.ANC
        if activo_total == 0:
            return 0
        return self.fondo_maniobra_absoluto() / activo_total
    
    def fondo_maniobra_ratio(self):
        """
        Alias de fondo_maniobra() para mantener compatibilidad.
        
        Returns:
            float: FM como ratio decimal
        """
        return self.fondo_maniobra()
    
    def financiacion_permanente(self):
        """
        Calcula la Financiación Permanente.
        FP = Patrimonio + Pasivo No Corriente
        
        Returns:
            float: Financiación Permanente
        """
        return self.PAT + self.PNC
    
    def financiacion_permanente(self):
        """
        Calcula la Financiación Permanente.
        FP = Patrimonio + Pasivo No Corriente
        
        Returns:
            float: Financiación Permanente
        """
        return self.PAT + self.PNC
    
    def tipo_equilibrio(self):
        """
        Determina el tipo de equilibrio patrimonial según la estructura financiera.
        
        Returns:
            str: Tipo de equilibrio ('estable', 'inestable', 'nulo')
        """
        fp = self.financiacion_permanente()
        
        if fp > self.ANC:
            return "estable"
        elif fp < self.ANC:
            return "inestable"
        else:
            return "nulo"
    
    def descripcion_equilibrio(self):
        """
        Devuelve una descripción detallada del equilibrio patrimonial.
        
        Returns:
            str: Descripción completa del tipo de equilibrio
        """
        tipo = self.tipo_equilibrio()
        fp = self.financiacion_permanente()
        
        descripciones = {
            "estable": f"Equilibrio patrimonial ESTABLE: La financiación permanente ({fp:,.2f}) es mayor que el activo no corriente ({self.ANC:,.2f}), lo que indica que la empresa financia sus activos fijos con recursos a largo plazo y tiene un fondo de maniobra positivo.",
            
            "inestable": f"Equilibrio patrimonial INESTABLE: La financiación permanente ({fp:,.2f}) es menor que el activo no corriente ({self.ANC:,.2f}), lo que significa que parte del activo no corriente se está financiando con pasivos a corto plazo. Esto representa un riesgo de liquidez.",
            
            "nulo": f"Equilibrio patrimonial NULO: La financiación permanente ({fp:,.2f}) es exactamente igual al activo no corriente ({self.ANC:,.2f}), lo que indica que todo el activo fijo está financiado con recursos permanentes, pero sin margen de seguridad (FM = 0)."
        }
        
        return descripciones[tipo]
    
    def tipo_equilibrio_por_fm(self):
        """
        Determina el equilibrio según el Fondo de Maniobra ABSOLUTO.
        
        Returns:
            str: Tipo de equilibrio basado en FM absoluto
        """
        fm_abs = self.fondo_maniobra_absoluto()
        
        if fm_abs > 0:
            return "Equilibrio patrimonial estable (FM > 0)"
        elif fm_abs < 0:
            return "Desequilibrio patrimonial inestable (FM < 0)"
        else:
            return "Equilibrio patrimonial nulo (FM = 0)"
    
    def analizar(self):
        """
        Devuelve análisis completo del equilibrio patrimonial.
        
        Returns:
            dict: Diccionario con todos los análisis
        """
        fm_abs = self.fondo_maniobra_absoluto()
        fm_ratio = self.fondo_maniobra()
        fp = self.financiacion_permanente()
        tipo = self.tipo_equilibrio()
        
        return {
            "fondo_maniobra_absoluto": fm_abs,
            "fondo_maniobra_ratio": fm_ratio,
            "financiacion_permanente": fp,
            "tipo_equilibrio": tipo,
            "descripcion_equilibrio": self.descripcion_equilibrio(),
            "tipo_equilibrio_fm": self.tipo_equilibrio_por_fm(),
            "activo_corriente": self.AC,
            "activo_no_corriente": self.ANC,
            "pasivo_corriente": self.PC,
            "pasivo_no_corriente": self.PNC,
            "patrimonio": self.PAT
        }
    
    def diagnostico_completo(self):
        """
        Genera un diagnóstico completo con recomendaciones.
        
        Returns:
            dict: Diagnóstico con interpretación y recomendaciones
        """
        fm_abs = self.fondo_maniobra_absoluto()
        fm_ratio = self.fondo_maniobra()
        tipo = self.tipo_equilibrio()
        
        # Interpretación según tipo
        interpretaciones = {
            "estable": "La empresa tiene una estructura financiera sólida. Los activos no corrientes están financiados con recursos permanentes y existe un colchón de seguridad para las operaciones diarias.",
            
            "inestable": "La empresa presenta riesgos de liquidez estructural. Parte de los activos fijos se financian con deuda de corto plazo, lo que puede generar problemas para renovar esos pasivos.",
            
            "nulo": "La empresa está en un punto crítico. Aunque los activos fijos están correctamente financiados, no existe margen de maniobra para imprevistos operativos."
        }
        
        # Recomendaciones según tipo
        recomendaciones = {
            "estable": "Mantener la estructura actual. Considerar optimizar el exceso de FM si existe para mejorar rentabilidad, pero sin comprometer la estabilidad.",
            
            "inestable": "URGENTE: Reestructurar la deuda a largo plazo o realizar una ampliación de capital. Reducir activos no corrientes o refinanciar pasivos corrientes a largo plazo.",
            
            "nulo": "Aumentar la financiación permanente mediante retención de beneficios, ampliación de capital o contratación de deuda a largo plazo para crear un colchón de seguridad."
        }
        
        return {
            "tipo_equilibrio": tipo,
            "fondo_maniobra_absoluto": fm_abs,
            "fondo_maniobra_ratio": fm_ratio,
            "interpretacion": interpretaciones[tipo],
            "recomendacion": recomendaciones[tipo],
            "nivel_riesgo": "bajo" if tipo == "estable" else ("critico" if tipo == "inestable" else "medio")
        }


class AnalisisFondoManiobraDual:
    """
    Analiza el Fondo de Maniobra comparativo entre dos años.
    Identifica evolución y cambios en el equilibrio patrimonial.
    """
    
    def __init__(self, fm_ano1, fm_ano2):
        """
        Args:
            fm_ano1: Fondo de Maniobra del Año 1
            fm_ano2: Fondo de Maniobra del Año 2
        """
        self.fm1 = fm_ano1
        self.fm2 = fm_ano2
    
    def tipo_equilibrio(self, valor):
        """
        Retorna el tipo de equilibrio patrimonial según el FM.
        
        Args:
            valor: Valor del Fondo de Maniobra
            
        Returns:
            str: Tipo de equilibrio
        """
        if valor > 0:
            return "Equilibrio patrimonial estable (FM > 0)"
        elif valor < 0:
            return "Desequilibrio patrimonial inestable (FM < 0)"
        else:
            return "Equilibrio patrimonial nulo (FM = 0)"
    
    def variacion_absoluta(self):
        """
        Calcula la variación absoluta del FM entre años.
        
        Returns:
            float: Diferencia en unidades monetarias
        """
        return self.fm2 - self.fm1
    
    def variacion_porcentual(self):
        """
        Calcula la variación porcentual del FM entre años.
        
        Returns:
            float: Variación en porcentaje
        """
        if self.fm1 == 0:
            return float('inf') if self.fm2 > 0 else float('-inf')
        return ((self.fm2 - self.fm1) / abs(self.fm1)) * 100
    
    def tendencia(self):
        """
        Determina la tendencia del FM (mejora, deterioro, estable).
        
        Returns:
            str: 'mejora', 'deterioro' o 'estable'
        """
        if self.fm2 > self.fm1:
            return "mejora"
        elif self.fm2 < self.fm1:
            return "deterioro"
        else:
            return "estable"
    
    def descripcion_evolucion(self):
        """
        Genera una descripción detallada de la evolución del FM.
        
        Returns:
            str: Descripción de la evolución
        """
        variacion = self.variacion_absoluta()
        var_pct = self.variacion_porcentual()
        tendencia = self.tendencia()
        
        if tendencia == "mejora":
            return f"El Fondo de Maniobra AUMENTÓ en {variacion:,.2f} unidades ({var_pct:+.2f}%), mostrando una mejora en la liquidez estructural. La empresa ha fortalecido su capacidad para financiar operaciones con recursos propios."
        
        elif tendencia == "deterioro":
            return f"El Fondo de Maniobra DISMINUYÓ en {abs(variacion):,.2f} unidades ({var_pct:.2f}%), indicando un deterioro en la liquidez estructural. Se requiere atención para evitar problemas de solvencia a corto plazo."
        
        else:
            return f"El Fondo de Maniobra se MANTUVO CONSTANTE en {self.fm1:,.2f} unidades entre ambos años, sin cambios significativos en la estructura de capital de trabajo."
    
    def cambio_situacion(self):
        """
        Identifica si hubo cambio en la situación de equilibrio entre años.
        
        Returns:
            dict: Información sobre cambios de situación
        """
        tipo1 = "positivo" if self.fm1 > 0 else ("negativo" if self.fm1 < 0 else "nulo")
        tipo2 = "positivo" if self.fm2 > 0 else ("negativo" if self.fm2 < 0 else "nulo")
        
        cambio = tipo1 != tipo2
        
        if cambio:
            if tipo1 == "negativo" and tipo2 == "positivo":
                mensaje = "¡MEJORA SIGNIFICATIVA! La empresa pasó de FM negativo a positivo, recuperando el equilibrio patrimonial."
            elif tipo1 == "positivo" and tipo2 == "negativo":
                mensaje = "¡ALERTA! La empresa pasó de FM positivo a negativo, entrando en desequilibrio patrimonial."
            elif tipo1 == "nulo":
                mensaje = f"La empresa salió de la situación límite (FM = 0) hacia un FM {tipo2}."
            else:
                mensaje = f"La empresa alcanzó un equilibrio límite (FM = 0) desde un FM {tipo1}."
        else:
            mensaje = f"La empresa mantiene su situación de FM {tipo1} en ambos años."
        
        return {
            "hubo_cambio": cambio,
            "situacion_ano1": tipo1,
            "situacion_ano2": tipo2,
            "mensaje": mensaje
        }
    
    def analizar(self):
        """
        Devuelve: evolución del FM y tipo de equilibrio patrimonial
        para cada año + conclusión.
        
        Returns:
            dict: Análisis completo comparativo
        """
        return {
            "fm_ano1": self.fm1,
            "fm_ano2": self.fm2,
            "tipo_equilibrio_ano1": self.tipo_equilibrio(self.fm1),
            "tipo_equilibrio_ano2": self.tipo_equilibrio(self.fm2),
            "variacion_absoluta": self.variacion_absoluta(),
            "variacion_porcentual": self.variacion_porcentual(),
            "tendencia": self.tendencia(),
            "evolucion": self.descripcion_evolucion(),
            "cambio_situacion": self.cambio_situacion()
        }
    
    def diagnostico_comparativo(self):
        """
        Genera un diagnóstico comparativo completo con recomendaciones.
        
        Returns:
            dict: Diagnóstico comparativo
        """
        tendencia = self.tendencia()
        cambio = self.cambio_situacion()
        
        # Nivel de alerta
        if tendencia == "deterioro" and self.fm2 < 0:
            nivel_alerta = "CRITICO"
            prioridad = "alta"
        elif tendencia == "deterioro":
            nivel_alerta = "ADVERTENCIA"
            prioridad = "media"
        elif tendencia == "mejora" and self.fm1 < 0 and self.fm2 > 0:
            nivel_alerta = "RECUPERACION"
            prioridad = "baja"
        else:
            nivel_alerta = "NORMAL"
            prioridad = "baja"
        
        # Recomendación
        if nivel_alerta == "CRITICO":
            recomendacion = "Acción inmediata requerida: Reestructurar deuda, ampliar capital o reducir activos no corrientes para restaurar el equilibrio."
        elif nivel_alerta == "ADVERTENCIA":
            recomendacion = "Monitorear de cerca la tendencia. Considerar medidas preventivas para evitar el deterioro continuo del FM."
        elif nivel_alerta == "RECUPERACION":
            recomendacion = "Excelente evolución. Mantener la disciplina financiera que permitió la recuperación del equilibrio."
        else:
            recomendacion = "Continuar con la gestión actual del capital de trabajo, manteniendo la estabilidad alcanzada."
        
        return {
            "nivel_alerta": nivel_alerta,
            "prioridad": prioridad,
            "tendencia": tendencia,
            "cambio_situacion": cambio["mensaje"],
            "recomendacion": recomendacion,
            "requiere_accion": prioridad in ["alta", "media"]
        }


class AnalisisPatrimonialCompleto:
    """
    Clase que integra el análisis completo de equilibrio patrimonial
    para ambos años usando los modelos de Balance.
    """
    
    def __init__(self, balance_model):
        """
        Args:
            balance_model: Instancia de BalanceGeneral
        """
        self.balance = balance_model
    
    def analizar_año(self, year):
        """
        Analiza el equilibrio patrimonial de un año específico.
        
        Args:
            year: 1 o 2
            
        Returns:
            EquilibrioPatrimonial: Instancia con el análisis del año
        """
        ac = self.balance.get_total_corriente(year)
        anc = self.balance.get_total_no_corriente(year)
        pc = self.balance.get_total_pasivo_corriente(year)
        pnc = self.balance.get_total_pasivo_no_corriente(year)
        pat = self.balance.get_total_patrimonio(year)
        
        return EquilibrioPatrimonial(ac, anc, pc, pnc, pat)
    
    def analisis_dual(self):
        """
        Realiza el análisis comparativo entre ambos años.
        
        Returns:
            dict: Análisis completo de ambos años y comparación
        """
        # Análisis individual de cada año
        eq_y1 = self.analizar_año(1)
        eq_y2 = self.analizar_año(2)
        
        analisis_y1 = eq_y1.analizar()
        analisis_y2 = eq_y2.analizar()
        
        # Análisis comparativo de FM
        fm_dual = AnalisisFondoManiobraDual(
            analisis_y1["fondo_maniobra_ratio"],
            analisis_y2["fondo_maniobra_ratio"]
        )
        
        comparacion = fm_dual.analizar()
        diagnostico = fm_dual.diagnostico_comparativo()
        
        return {
            "ano_1": analisis_y1,
            "ano_2": analisis_y2,
            "comparacion": comparacion,
            "diagnostico": diagnostico
        }