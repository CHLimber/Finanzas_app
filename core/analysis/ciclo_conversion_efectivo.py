"""
Archivo: core/analysis/ciclo_conversion_efectivo.py
Cálculo e interpretación del Ciclo de Conversión de Efectivo (CCE)
"""

class CicloConversionEfectivo:
    """
    Calcula el Ciclo de Conversión de Efectivo y sus componentes.
    
    CCE = Días de Inventario + Días de Clientes - Días de Proveedores
    
    Mide el tiempo que tarda la empresa en convertir sus inversiones 
    en inventario y cuentas por cobrar en efectivo.
    """
    
    def __init__(self, balance_model, estado_resultado_model):
        """
        Args:
            balance_model: Instancia de BalanceGeneral
            estado_resultado_model: Instancia de EstadoResultado
        """
        self.balance = balance_model
        self.estado = estado_resultado_model
    
    def dias_inventario(self, year):
        """
        Días de Inventario = 365 * (Existencias / Costo de servicio anual)
        
        Indica cuántos días permanece el inventario antes de ser vendido.
        """
        existencias = self.balance.existencias_y1 if year == 1 else self.balance.existencias_y2
        costo_servicio = self.estado.costo_servicios_y1 if year == 1 else self.estado.costo_servicios_y2
        
        if costo_servicio == 0:
            return 0
        
        return 0* 365 * (existencias / costo_servicio)
    
    def dias_clientes(self, year):
        """
        Días de Clientes = 365 * (Clientes por cobrar / Ingreso por servicios)
        
        Indica cuántos días tarda la empresa en cobrar a sus clientes.
        """
        clientes = self.balance.clientes_cobrar_y1 if year == 1 else self.balance.clientes_cobrar_y2
        ingresos = self.estado.ingresos_servicios_y1 if year == 1 else self.estado.ingresos_servicios_y2
        
        if ingresos == 0:
            return 0
        
        return 365 * (clientes / ingresos)
    
    def dias_proveedores(self, year):
        """
        Días de Proveedores = 365 * (Costo de servicio / Promedio de Proveedores)
        
        Promedio de Proveedores = (Proveedores Año 1 + Proveedores Año 2) / 2
        
        Indica cuántos días tarda la empresa en pagar a sus proveedores.
        """
        costo_servicio = self.estado.costo_servicios_y1 if year == 1 else self.estado.costo_servicios_y2
        
        # Promedio de proveedores entre ambos años
        promedio_proveedores = (self.balance.proveedores_y1 + self.balance.proveedores_y2) / 2
        
        if promedio_proveedores == 0:
            return 0
        
        return 365 * (promedio_proveedores / costo_servicio)
    
    def cce(self, year):
        """
        Ciclo de Conversión de Efectivo = DI + DC - DP
        
        Representa el número de días que la empresa necesita financiar
        entre el pago a proveedores y el cobro a clientes.
        """
        di = self.dias_inventario(year)
        dc = self.dias_clientes(year)
        dp = self.dias_proveedores(year)
        
        return di + dc - dp
    
    def interpretar_componente(self, nombre, valor, year):
        """
        Interpreta cada componente individual del CCE.
        
        Args:
            nombre: "DI", "DC" o "DP"
            valor: Valor en días
            year: Año analizado
        
        Returns:
            str: Interpretación del componente
        """
        if nombre == "DI":  # Días de Inventario
            if valor <= 30:
                return f"{valor:.1f} días: Rotación muy rápida. Excelente gestión de inventario."
            elif valor <= 60:
                return f"{valor:.1f} días: Rotación normal. Gestión adecuada."
            elif valor <= 90:
                return f"{valor:.1f} días: Rotación lenta. Revisar políticas de inventario."
            else:
                return f"{valor:.1f} días: Rotación muy lenta. Riesgo de obsolescencia o sobreinventario."
        
        elif nombre == "DC":  # Días de Clientes
            if valor <= 30:
                return f"{valor:.1f} días: Cobro muy rápido. Política de crédito restrictiva."
            elif valor <= 60:
                return f"{valor:.1f} días: Plazo de cobro normal. Gestión equilibrada."
            elif valor <= 90:
                return f"{valor:.1f} días: Plazo de cobro alto. Revisar política de crédito."
            else:
                return f"{valor:.1f} días: Plazo de cobro excesivo. Riesgo de incobrabilidad."
        
        elif nombre == "DP":  # Días de Proveedores
            if valor <= 30:
                return f"{valor:.1f} días: Pago muy rápido. Posible pérdida de financiamiento gratuito."
            elif valor <= 60:
                return f"{valor:.1f} días: Plazo de pago normal. Buena relación con proveedores."
            elif valor <= 90:
                return f"{valor:.1f} días: Plazo de pago amplio. Buen aprovechamiento del crédito."
            else:
                return f"{valor:.1f} días: Plazo de pago muy extenso. Posible riesgo de relación con proveedores."
        
        return f"{valor:.1f} días"
    
    def interpretar_cce(self, year, cce_value=None):
        """
        Interpreta el Ciclo de Conversión de Efectivo.
        
        Args:
            year: Año analizado
            cce_value: Valor del CCE (si no se proporciona, se calcula)
        
        Returns:
            str: Interpretación del CCE
        """
        cce_value = self.cce(year) if cce_value is None else cce_value
        
        if cce_value is None or (self.estado.costo_servicios_y1 == 0 and self.estado.costo_servicios_y2 == 0):
            return "No hay datos suficientes para calcular CCE."
        
        if cce_value <= 0:
            return (f"CCE = {cce_value:.1f} días: EXCELENTE. La empresa cobra antes de pagar, "
                   "generando financiamiento automático. Situación muy favorable.")
        elif cce_value <= 20:
            return (f"CCE = {cce_value:.1f} días: Muy eficiente y sostenible. "
                   "La empresa tiene una excelente gestión del capital de trabajo.")
        elif cce_value <= 40:
            return (f"CCE = {cce_value:.1f} días: Moderado y generalmente sostenible "
                   "si existe capital de trabajo suficiente.")
        elif cce_value <= 60:
            return (f"CCE = {cce_value:.1f} días: Preocupante. Requiere revisar "
                   "financiación de corto plazo y optimizar componentes.")
        else:
            return (f"CCE = {cce_value:.1f} días: Riesgo alto de iliquidez. "
                   "Necesita acciones urgentes: reducir DI/DC o aumentar DP/financiación.")
    
    def analisis_completo(self, year):
        """
        Genera análisis completo del CCE para un año.
        
        Returns:
            dict: Diccionario con todos los componentes y análisis
        """
        di = self.dias_inventario(year)
        dc = self.dias_clientes(year)
        dp = self.dias_proveedores(year)
        cce_val = self.cce(year)
        
        return {
            "dias_inventario": di,
            "dias_clientes": dc,
            "dias_proveedores": dp,
            "cce": cce_val,
            "interpretacion_di": self.interpretar_componente("DI", di, year),
            "interpretacion_dc": self.interpretar_componente("DC", dc, year),
            "interpretacion_dp": self.interpretar_componente("DP", dp, year),
            "interpretacion_cce": self.interpretar_cce(year, cce_val)
        }
    
    def analisis_dual(self):
        """
        Analiza el CCE para ambos años y genera comparación.
        
        Returns:
            dict: Análisis comparativo completo
        """
        analisis_y1 = self.analisis_completo(1)
        analisis_y2 = self.analisis_completo(2)
        
        # Calcular variaciones
        var_di = 0  #analisis_y2["dias_inventario"] - analisis_y1["dias_inventario"]
        var_dc = analisis_y2["dias_clientes"] - analisis_y1["dias_clientes"]
        var_dp = analisis_y2["dias_proveedores"] - analisis_y1["dias_proveedores"]
        var_cce = analisis_y2["cce"] - analisis_y1["cce"]
        
        # Interpretación de tendencia
        if var_cce < -5:
            tendencia = "MEJORA SIGNIFICATIVA: El CCE se redujo, mejorando la eficiencia del capital de trabajo."
        elif var_cce < 0:
            tendencia = "MEJORA LEVE: El CCE disminuyó ligeramente."
        elif var_cce <= 5:
            tendencia = "ESTABLE: El CCE se mantiene similar entre ambos años."
        else:
            tendencia = f"DETERIORO: El CCE aumentó en {var_cce:.1f} días, requiriendo más capital de trabajo."
        
        return {
            "year_1": analisis_y1,
            "year_2": analisis_y2,
            "variaciones": {
                "di": var_di,
                "dc": var_dc,
                "dp": var_dp,
                "cce": var_cce
            },
            "tendencia": tendencia
        }
    
    def recomendaciones(self, year):
        """
        Genera recomendaciones específicas basadas en el análisis.
        
        Returns:
            list: Lista de recomendaciones
        """
        analisis = self.analisis_completo(year)
        recomendaciones = []
        
        # Recomendaciones para Días de Inventario
        if analisis["dias_inventario"] > 90:
            recomendaciones.append(
                "📦 INVENTARIO: Reducir días de inventario implementando gestión JIT "
                "(Just-In-Time) o mejorando la rotación de stock."
            )
        
        # Recomendaciones para Días de Clientes
        if analisis["dias_clientes"] > 90:
            recomendaciones.append(
                "💰 COBRANZA: Mejorar políticas de crédito, implementar descuentos por pronto pago "
                "o reforzar procesos de cobranza."
            )
        elif analisis["dias_clientes"] < 15:
            recomendaciones.append(
                "💰 COBRANZA: Plazo muy corto. Considerar ampliar crédito a clientes confiables "
                "para aumentar ventas sin comprometer liquidez."
            )
        
        # Recomendaciones para Días de Proveedores
        if analisis["dias_proveedores"] < 30:
            recomendaciones.append(
                "🤝 PROVEEDORES: Negociar plazos de pago más largos para aprovechar "
                "financiamiento sin costo."
            )
        elif analisis["dias_proveedores"] > 120:
            recomendaciones.append(
                "🤝 PROVEEDORES: Plazo excesivo puede dañar relaciones comerciales. "
                "Considerar pago puntual para mantener buenas condiciones."
            )
        
        # Recomendaciones para CCE
        if analisis["cce"] > 60:
            recomendaciones.append(
                "⚠️ CCE ALTO: Urgente optimizar el ciclo. Considerar líneas de crédito, "
                "factoring o reestructuración del capital de trabajo."
            )
        elif analisis["cce"] < 0:
            recomendaciones.append(
                "✅ CCE NEGATIVO: Excelente. Mantener esta estrategia y considerar "
                "reinvertir el excedente de efectivo."
            )
        
        if not recomendaciones:
            recomendaciones.append(
                "✅ GESTIÓN ADECUADA: Los componentes del CCE están en rangos aceptables. "
                "Mantener monitoreo continuo."
            )
        
        return recomendaciones