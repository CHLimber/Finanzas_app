"""
Archivo: core/analysis/diagnostico_patrimonial.py
Diagnóstico del Estado Patrimonial de la empresa
"""

class EstadoPatrimonial:
    """
    Calcula e interpreta el estado patrimonial de una empresa
    según: equilibrio total, normal, crisis o insolvencia.
    """

    def __init__(self, activo_corriente, pasivo_corriente,
                 patrimonio_neto, pasivo_total, activo_total=None):
        """
        Args:
            activo_corriente: AC del balance
            pasivo_corriente: PC del balance
            patrimonio_neto: Patrimonio
            pasivo_total: Pasivo total (corriente + no corriente)
            activo_total: Activo total (si no se pasa, se calcula)
        """
        self.ac = activo_corriente
        self.pc = pasivo_corriente
        self.pn = patrimonio_neto
        self.pt = pasivo_total

        # Si no pasan el activo total, lo calculamos
        # Nota: en tu código original había un error aquí
        if activo_total is not None:
            self.at = activo_total
        else:
            # Asumimos que falta el activo no corriente
            # AT = AC + ANC, donde ANC = PT + PN - AC (ecuación contable)
            self.at = self.pt + self.pn

    @property
    def fondo_maniobra(self):
        """Calcula el Fondo de Maniobra (FM = AC - PC)"""
        return self.ac - self.pc

    def determinar_estado(self):
        """
        Determina el estado patrimonial según las reglas:
        
        - INSOLVENCIA: AT < PT o PN < 0
        - CRISIS: FM < 0 (pero AT >= PT)
        - EQUILIBRIO TOTAL: FM >= 0 y PN > PT
        - EQUILIBRIO NORMAL: FM >= 0 y PN < PT
        
        Returns:
            str: Estado patrimonial
        """
        FM = self.fondo_maniobra

        # Insolvencia / Quiebra Técnica
        if self.at < self.pt or self.pn < 0:
            return "INSOLVENCIA"

        # Crisis Financiera
        if FM < 0:
            return "CRISIS"

        # Equilibrio Total (estructura muy sólida)
        if FM >= 0 and self.pn > self.pt:
            return "EQUILIBRIO TOTAL"

        # Equilibrio Normal (estructura estable con mayor deuda)
        if FM >= 0 and self.pn < self.pt:
            return "EQUILIBRIO NORMAL"

        return "NO CLASIFICADO"

    def interpretar(self):
        """
        Genera interpretación textual completa del estado patrimonial.
        
        Returns:
            str: Interpretación detallada
        """
        estado = self.determinar_estado()
        FM = self.fondo_maniobra

        if estado == "EQUILIBRIO TOTAL":
            return (
                f"Estado patrimonial: EQUILIBRIO TOTAL ✅\n\n"
                f"Fondo de Maniobra: {FM:,.2f} Bs. (positivo)\n\n"
                f"• El activo corriente cubre ampliamente las deudas a corto plazo.\n"
                f"• El patrimonio ({self.pn:,.2f}) es MAYOR que el pasivo total ({self.pt:,.2f}).\n"
                f"• Ratio Patrimonio/Pasivo: {(self.pn/self.pt if self.pt > 0 else 0):.2f}\n\n"
                f"→ La empresa posee una estructura financiera MUY SÓLIDA y ESTABLE.\n"
                f"→ Baja dependencia del endeudamiento externo.\n"
                f"→ Alta capacidad para absorber pérdidas o crisis temporales."
            )

        elif estado == "EQUILIBRIO NORMAL":
            ratio_endeudamiento = (self.pt / self.at * 100) if self.at > 0 else 0
            return (
                f"Estado patrimonial: EQUILIBRIO NORMAL ⚠️\n\n"
                f"Fondo de Maniobra: {FM:,.2f} Bs. (positivo)\n\n"
                f"• Liquidez buena, pero dependencia moderada del pasivo.\n"
                f"• El patrimonio ({self.pn:,.2f}) es MENOR que el pasivo total ({self.pt:,.2f}).\n"
                f"• Ratio de Endeudamiento: {ratio_endeudamiento:.1f}%\n\n"
                f"→ Empresa ESTABLE, pero depende más de deuda que de capital propio.\n"
                f"→ Estructura financiera común en empresas en crecimiento.\n"
                f"→ Requiere monitoreo del nivel de endeudamiento y capacidad de pago."
            )

        elif estado == "CRISIS":
            return (
                f"Estado patrimonial: CRISIS FINANCIERA 🚨\n\n"
                f"Fondo de Maniobra: {FM:,.2f} Bs. (NEGATIVO)\n\n"
                f"• El activo corriente NO cubre las deudas a corto plazo.\n"
                f"• Sin embargo, el activo total ({self.at:,.2f}) SÍ cubre el pasivo total ({self.pt:,.2f}).\n"
                f"• Déficit de liquidez: {abs(FM):,.2f} Bs.\n\n"
                f"→ RIESGO DE FALTA DE LIQUIDEZ para operaciones diarias.\n"
                f"→ La empresa NO está en quiebra técnica, pero tiene problemas de caja.\n"
                f"→ ACCIÓN REQUERIDA: Reestructurar deuda de CP a LP, mejorar cobranza, "
                f"o inyectar capital de trabajo."
            )

        elif estado == "INSOLVENCIA":
            deficit = self.pt - self.at if self.at < self.pt else 0
            return (
                f"Estado patrimonial: INSOLVENCIA / QUIEBRA TÉCNICA ❌\n\n"
                f"• El activo total ({self.at:,.2f}) es INSUFICIENTE para cubrir el pasivo ({self.pt:,.2f}).\n"
                f"• Patrimonio Neto: {self.pn:,.2f} Bs. {'(NEGATIVO)' if self.pn < 0 else ''}\n"
                f"• Déficit patrimonial: {deficit:,.2f} Bs.\n\n"
                f"→ La empresa NO puede cumplir sus obligaciones financieras.\n"
                f"→ RIESGO EXTREMO de quiebra o concurso de acreedores.\n"
                f"→ ACCIÓN URGENTE: Capitalización, reestructuración, o liquidación ordenada."
            )

        return "No se pudo determinar el estado patrimonial."

    def nivel_riesgo(self):
        """
        Determina el nivel de riesgo financiero.
        
        Returns:
            str: "BAJO", "MEDIO", "ALTO", "CRÍTICO"
        """
        estado = self.determinar_estado()
        
        if estado == "EQUILIBRIO TOTAL":
            return "BAJO"
        elif estado == "EQUILIBRIO NORMAL":
            # Depende del ratio de endeudamiento
            ratio_end = (self.pt / self.at * 100) if self.at > 0 else 100
            if ratio_end < 60:
                return "MEDIO"
            else:
                return "ALTO"
        elif estado == "CRISIS":
            return "ALTO"
        elif estado == "INSOLVENCIA":
            return "CRÍTICO"
        else:
            return "DESCONOCIDO"

    def recomendaciones(self):
        """
        Genera recomendaciones específicas según el estado.
        
        Returns:
            list: Lista de recomendaciones
        """
        estado = self.determinar_estado()
        recs = []

        if estado == "EQUILIBRIO TOTAL":
            recs.append("✅ Mantener la estructura financiera conservadora actual.")
            recs.append("💡 Evaluar oportunidades de apalancamiento moderado para acelerar crecimiento.")
            recs.append("📊 Considerar distribución de dividendos o recompra de acciones si hay exceso de capital.")

        elif estado == "EQUILIBRIO NORMAL":
            recs.append("⚠️ Monitorear el ratio de endeudamiento periódicamente.")
            recs.append("💰 Priorizar retención de utilidades para fortalecer el patrimonio.")
            recs.append("🔄 Evaluar refinanciación de deuda de corto a largo plazo.")
            recs.append("📈 Mantener flujo de caja positivo para cumplir obligaciones.")

        elif estado == "CRISIS":
            recs.append("🚨 URGENTE: Reestructurar deuda de corto plazo a largo plazo.")
            recs.append("💵 Implementar plan agresivo de cobranza y reducción de inventarios.")
            recs.append("💉 Considerar inyección de capital de trabajo (préstamos o aportes).")
            recs.append("✂️ Reducir gastos operativos no esenciales inmediatamente.")
            recs.append("🤝 Negociar con proveedores extensión de plazos de pago.")

        elif estado == "INSOLVENCIA":
            recs.append("❌ CRÍTICO: Convocar junta extraordinaria de accionistas.")
            recs.append("🏦 Explorar capitalización urgente o venta de activos no estratégicos.")
            recs.append("⚖️ Considerar asesoría legal para reestructuración o concurso de acreedores.")
            recs.append("📋 Evaluar viabilidad del negocio: reestructuración vs. liquidación ordenada.")
            recs.append("🛡️ Proteger activos críticos y preservar relaciones clave con stakeholders.")

        return recs

    def analisis_completo(self):
        """
        Genera un análisis completo con todos los datos.
        
        Returns:
            dict: Análisis completo
        """
        return {
            "activo_corriente": self.ac,
            "pasivo_corriente": self.pc,
            "activo_total": self.at,
            "pasivo_total": self.pt,
            "patrimonio_neto": self.pn,
            "fondo_maniobra": self.fondo_maniobra,
            "estado": self.determinar_estado(),
            "nivel_riesgo": self.nivel_riesgo(),
            "interpretacion": self.interpretar(),
            "recomendaciones": self.recomendaciones()
        }


class DiagnosticoPatrimonialDual:
    """
    Realiza diagnóstico patrimonial comparativo entre dos años.
    """
    
    def __init__(self, balance_model):
        """
        Args:
            balance_model: Instancia de BalanceGeneral
        """
        self.balance = balance_model
    
    def analizar_año(self, year):
        """
        Analiza el estado patrimonial de un año específico.
        
        Args:
            year: 1 o 2
        
        Returns:
            EstadoPatrimonial: Instancia con análisis del año
        """
        ac = self.balance.get_total_corriente(year)
        pc = self.balance.get_total_pasivo_corriente(year)
        pnc = self.balance.get_total_pasivo_no_corriente(year)
        pt = pc + pnc
        pn = self.balance.get_total_patrimonio(year)
        at = self.balance.get_total_activos(year)
        
        return EstadoPatrimonial(ac, pc, pn, pt, at)
    
    def analisis_dual(self):
        """
        Realiza análisis comparativo entre ambos años.
        
        Returns:
            dict: Análisis completo de ambos años
        """
        estado_y1 = self.analizar_año(1)
        estado_y2 = self.analizar_año(2)
        
        analisis_y1 = estado_y1.analisis_completo()
        analisis_y2 = estado_y2.analisis_completo()
        
        # Determinar evolución
        if analisis_y1["estado"] == analisis_y2["estado"]:
            evolucion = f"La empresa se mantiene en {analisis_y2['estado']} en ambos años."
        else:
            estados_orden = ["EQUILIBRIO TOTAL", "EQUILIBRIO NORMAL", "CRISIS", "INSOLVENCIA"]
            pos_y1 = estados_orden.index(analisis_y1["estado"]) if analisis_y1["estado"] in estados_orden else -1
            pos_y2 = estados_orden.index(analisis_y2["estado"]) if analisis_y2["estado"] in estados_orden else -1
            
            if pos_y2 < pos_y1:
                evolucion = f"✅ MEJORA: Pasó de {analisis_y1['estado']} a {analisis_y2['estado']}."
            elif pos_y2 > pos_y1:
                evolucion = f"🚨 DETERIORO: Pasó de {analisis_y1['estado']} a {analisis_y2['estado']}."
            else:
                evolucion = f"La situación cambió de {analisis_y1['estado']} a {analisis_y2['estado']}."
        
        return {
            "year_1": analisis_y1,
            "year_2": analisis_y2,
            "evolucion": evolucion
        }