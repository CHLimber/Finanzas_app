"""
Archivo: core/analysis/recomendaciones_estrategicas.py
Recomendaciones Estratégicas Fundamentadas Cuantitativamente
"""


class RecomendacionesEstrategicas:
    """Genera recomendaciones estratégicas fundamentadas en datos"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data
    
    def generar_recomendaciones_completas(self):
        """
        Genera las 3 recomendaciones estratégicas principales
        
        Returns:
            dict: Recomendaciones con fundamentos cuantitativos
        """
        return {
            'liquidez': self._generar_recomendaciones_liquidez(),
            'rentabilidad': self._generar_recomendaciones_rentabilidad(),
            'eficiencia_operativa': self._generar_recomendaciones_eficiencia()
        }
    
    def _generar_recomendaciones_liquidez(self):
        """Genera 3 recomendaciones para mejorar liquidez"""
        # Calcular métricas actuales
        ac_y2 = self.balance_data.get_total_corriente(2)
        pc_y2 = self.balance_data.get_total_pasivo_corriente(2)
        disponible_y2 = self.balance_data.caja_bancos_y2
        cxc_y2 = self.balance_data.clientes_cobrar_y2
        
        liquidez_actual = (ac_y2 / pc_y2) if pc_y2 != 0 else 0
        razon_disponibilidad = (disponible_y2 / pc_y2) if pc_y2 != 0 else 0
        
        # Calcular días de cobranza
        ventas_y2 = self.income_data.ingresos_servicios_y2
        dias_cobranza_actual = (cxc_y2 / ventas_y2 * 365) if ventas_y2 != 0 else 0
        
        recomendaciones = []
        
        # RECOMENDACIÓN 1: OPTIMIZAR CICLO DE CONVERSIÓN DE EFECTIVO
        dias_objetivo = 45
        mejora_dias = max(0, dias_cobranza_actual - dias_objetivo)
        efectivo_liberado = (mejora_dias / 365) * ventas_y2
        
        recom1 = {
            'numero': 1,
            'titulo': 'Optimizar Ciclo de Conversión de Efectivo',
            'fundamento_cuantitativo': (
                f"• Liquidez General: {liquidez_actual:.2f}\n"
                f"• Cuentas por Cobrar: ${cxc_y2:,.2f}\n"
                f"• Días de Cobranza: {dias_cobranza_actual:.0f} días\n"
                f"• Objetivo: {dias_objetivo} días\n"
                f"• Efectivo potencial liberado: ${efectivo_liberado:,.2f}"
            ),
            'analisis': (
                f"El período de cobranza actual de {dias_cobranza_actual:.0f} días excede el óptimo "
                f"del sector tecnológico (30-45 días). Reducir a {dias_objetivo} días liberaría "
                f"${efectivo_liberado:,.2f} en capital de trabajo."
            ),
            'acciones': [
                "Implementar descuentos por pronto pago (2% por pago en 10 días)",
                "Automatizar recordatorios de pago",
                "Establecer límites de crédito basados en historial",
                f"Considerar factoring para cuentas mayores a 60 días"
            ],
            'impacto': f"Mejora de liquidez: +${efectivo_liberado:,.2f} anuales"
        }
        recomendaciones.append(recom1)
        
        # RECOMENDACIÓN 2: REESTRUCTURAR DEUDA
        deuda_cp_y2 = self.balance_data.deuda_cp_y2
        monto_reestructurar = min(deuda_cp_y2 * 0.50, pc_y2 * 0.30)
        nuevo_pc = pc_y2 - monto_reestructurar
        nueva_liquidez = (ac_y2 / nuevo_pc) if nuevo_pc != 0 else 0
        
        recom2 = {
            'numero': 2,
            'titulo': 'Reestructurar Deuda de Corto a Largo Plazo',
            'fundamento_cuantitativo': (
                f"• Deuda Corto Plazo: ${deuda_cp_y2:,.2f}\n"
                f"• Pasivo Corriente: ${pc_y2:,.2f}\n"
                f"• Monto a reestructurar: ${monto_reestructurar:,.2f}\n"
                f"• Liquidez actual: {liquidez_actual:.2f}\n"
                f"• Liquidez proyectada: {nueva_liquidez:.2f}"
            ),
            'analisis': (
                f"Reestructurar ${monto_reestructurar:,.2f} de deuda CP a LP reduciría la presión "
                f"sobre el flujo de caja y mejoraría el ratio de liquidez de {liquidez_actual:.2f} "
                f"a {nueva_liquidez:.2f}."
            ),
            'acciones': [
                f"Negociar conversión de ${monto_reestructurar:,.2f} a LP",
                "Buscar tasas competitivas aprovechando buena posición crediticia",
                "Establecer vencimientos escalonados",
                "Evaluar opciones con múltiples instituciones"
            ],
            'impacto': f"Mejora de liquidez general: {liquidez_actual:.2f} → {nueva_liquidez:.2f}"
        }
        recomendaciones.append(recom2)
        
        # RECOMENDACIÓN 3: FONDO DE RESERVA
        gastos_operativos_mensuales = (
            self.income_data.gastos_admin_y2 +
            self.income_data.gastos_ventas_y2
        ) / 12
        
        # Validar gastos operativos
        if gastos_operativos_mensuales == 0:
            gastos_operativos_mensuales = 1  # Evitar división por cero
        
        cobertura_actual = disponible_y2 / gastos_operativos_mensuales
        reserva_objetivo = gastos_operativos_mensuales * 3
        brecha_reserva = max(0, reserva_objetivo - disponible_y2)
        
        recom3 = {
            'numero': 3,
            'titulo': 'Establecer Fondo de Reserva de Liquidez',
            'fundamento_cuantitativo': (
                f"• Gastos Operativos Mensuales: ${gastos_operativos_mensuales:,.2f}\n"
                f"• Disponible Actual: ${disponible_y2:,.2f}\n"
                f"• Cobertura Actual: {cobertura_actual:.1f} meses\n"
                f"• Reserva Objetivo (3 meses): ${reserva_objetivo:,.2f}\n"
                f"• Brecha: ${brecha_reserva:,.2f}"
            ),
            'analisis': (
                f"La cobertura actual de {cobertura_actual:.1f} meses es "
                f"{'inferior' if cobertura_actual < 3 else 'adecuada'} al objetivo de 3-6 meses recomendado para el sector tecnológico. "
                f"{'Se requiere incrementar reservas en ${:,.2f}.'.format(brecha_reserva) if brecha_reserva > 0 else 'Mantener nivel actual de reservas.'}"
            ),
            'acciones': [
                "Destinar 20% de utilidad neta trimestral a reserva",
                "Invertir reservas en instrumentos líquidos de bajo riesgo",
                "No utilizar reserva excepto para emergencias operativas",
                "Revisar objetivo de reserva anualmente"
            ],
            'impacto': f"Cobertura operativa: 3+ meses garantizados"
        }
        recomendaciones.append(recom3)
        
        return recomendaciones
    
    def _generar_recomendaciones_rentabilidad(self):
        """Genera 3 recomendaciones para mejorar rentabilidad"""
        ventas_y2 = self.income_data.ingresos_servicios_y2
        un_y2 = self.income_data.get_utilidad_neta(2)
        margen_neto_y2 = (un_y2 / ventas_y2 * 100) if ventas_y2 != 0 else 0
        pn_y2 = self.balance_data.get_total_patrimonio(2)
        rrp_y2 = (un_y2 / pn_y2 * 100) if pn_y2 != 0 else 0
        
        recomendaciones = []
        
        # RECOMENDACIÓN 1: OPTIMIZAR MIX DE PRODUCTOS
        incremento_margen_objetivo = 5
        nuevo_margen = margen_neto_y2 + incremento_margen_objetivo
        nueva_utilidad = ventas_y2 * (nuevo_margen / 100)
        incremento_utilidad = nueva_utilidad - un_y2
        nueva_rrp = (nueva_utilidad / pn_y2 * 100) if pn_y2 != 0 else 0
        
        recom1 = {
            'numero': 1,
            'titulo': 'Optimizar Mix de Productos/Servicios de Alto Margen',
            'fundamento_cuantitativo': (
                f"• Ingresos: ${ventas_y2:,.2f}\n"
                f"• Utilidad Neta: ${un_y2:,.2f}\n"
                f"• Margen Neto: {margen_neto_y2:.2f}%\n"
                f"• RRP: {rrp_y2:.2f}%\n"
                f"• Potencial incremento margen: +{incremento_margen_objetivo} p.p."
            ),
            'analisis': (
                f"Incrementar margen neto de {margen_neto_y2:.2f}% a {nuevo_margen:.2f}% mediante "
                f"enfoque en servicios premium aumentaría la utilidad en ${incremento_utilidad:,.2f} "
                f"y mejoraría RRP de {rrp_y2:.2f}% a {nueva_rrp:.2f}%."
            ),
            'acciones': [
                "Analizar rentabilidad por línea de producto/servicio",
                "Incrementar precios en servicios premium 10-15%",
                "Descontinuar servicios de bajo margen (<15%)",
                "Desarrollar ofertas de suscripción recurrente (SaaS)",
                "Implementar estrategia de upselling/cross-selling"
            ],
            'impacto': f"Incremento utilidad: +${incremento_utilidad:,.2f}" + (
                f" ({incremento_utilidad/un_y2*100:.1f}%)" if un_y2 != 0 else " (significativo)"
            )
        }
        recomendaciones.append(recom1)
        
        # RECOMENDACIÓN 2: REDUCIR GASTOS OPERATIVOS
        gastos_admin_y2 = self.income_data.gastos_admin_y2
        gastos_ventas_y2 = self.income_data.gastos_ventas_y2
        gastos_operativos_total = gastos_admin_y2 + gastos_ventas_y2
        
        reduccion_objetivo = gastos_operativos_total * 0.10
        impacto_margen_neto = reduccion_objetivo * 0.70
        nuevo_margen_neto = ((un_y2 + impacto_margen_neto) / ventas_y2 * 100) if ventas_y2 != 0 else 0
        
        recom2 = {
            'numero': 2,
            'titulo': 'Optimizar Estructura de Costos Operativos',
            'fundamento_cuantitativo': (
                f"• Gastos Operativos: ${gastos_operativos_total:,.2f}\n"
                f"• % de Ventas: {gastos_operativos_total/ventas_y2*100:.1f}%\n" if ventas_y2 != 0 else f"• % de Ventas: N/A\n"
                f"• Reducción objetivo (10%): ${reduccion_objetivo:,.2f}\n"
                f"• Impacto en utilidad neta: +${impacto_margen_neto:,.2f}\n"
                f"• Margen neto proyectado: {nuevo_margen_neto:.2f}%"
            ),
            'analisis': (
                f"Reducir gastos operativos en 10% (${reduccion_objetivo:,.2f}) mediante eficiencias "
                f"y renegociación de contratos aumentaría utilidad neta en ${impacto_margen_neto:,.2f}."
            ),
            'acciones': [
                "Auditar gastos y clasificar por criticidad",
                "Implementar presupuesto base cero",
                "Renegociar contratos (ahorro 15-20%)",
                "Automatizar procesos administrativos",
                "Migrar a servicios cloud escalables"
            ],
            'impacto': f"Ahorro anual: ${reduccion_objetivo:,.2f}" + (
                f", +{impacto_margen_neto/un_y2*100:.1f}% utilidad" if un_y2 != 0 else ", mejora significativa"
            )
        }
        recomendaciones.append(recom2)
        
        # RECOMENDACIÓN 3: ESTRATEGIA DE ESCALAMIENTO
        crecimiento_objetivo = 25
        ventas_objetivo = ventas_y2 * (1 + crecimiento_objetivo/100)
        incremento_ventas = ventas_objetivo - ventas_y2
        utilidad_incremental = incremento_ventas * (margen_neto_y2 / 100)
        inversion_requerida = incremento_ventas * 0.20
        roi = (utilidad_incremental / inversion_requerida * 100) if inversion_requerida != 0 else 0
        
        recom3 = {
            'numero': 3,
            'titulo': 'Implementar Estrategia de Escalamiento de Ingresos',
            'fundamento_cuantitativo': (
                f"• Ventas Actuales: ${ventas_y2:,.2f}\n"
                f"• Objetivo Crecimiento: {crecimiento_objetivo}%\n"
                f"• Ventas Proyectadas: ${ventas_objetivo:,.2f}\n"
                f"• Utilidad Incremental: ${utilidad_incremental:,.2f}\n"
                f"• Inversión Requerida: ${inversion_requerida:,.2f}\n"
                f"• ROI Estimado: {roi:.0f}%"
            ),
            'analisis': (
                f"Incrementar ventas {crecimiento_objetivo}% generaría ${utilidad_incremental:,.2f} "
                f"adicionales con inversión de ${inversion_requerida:,.2f} (ROI: {roi:.0f}%)."
            ),
            'acciones': [
                "Expandir canales de distribución digital",
                "Implementar marketing digital con ROI >300%",
                "Desarrollar programa de referidos",
                "Automatizar onboarding para escalar",
                "Establecer alianzas estratégicas"
            ],
            'impacto': f"Incremento ventas: ${incremento_ventas:,.2f}, Utilidad: +${utilidad_incremental:,.2f}"
        }
        recomendaciones.append(recom3)
        
        return recomendaciones
    
    def _generar_recomendaciones_eficiencia(self):
        """Genera 3 recomendaciones para mejorar eficiencia operativa"""
        ventas_y2 = self.income_data.ingresos_servicios_y2
        activo_y2 = self.balance_data.get_total_activos(2)
        rotacion_activos_y2 = (ventas_y2 / activo_y2) if activo_y2 != 0 else 0
        
        recomendaciones = []
        
        # RECOMENDACIÓN 1: INCREMENTAR ROTACIÓN DE ACTIVOS
        activo_optimizado = activo_y2 * 0.90
        nueva_rotacion = (ventas_y2 / activo_optimizado) if activo_optimizado != 0 else 0
        capital_liberado = activo_y2 - activo_optimizado
        
        recom1 = {
            'numero': 1,
            'titulo': 'Incrementar Rotación de Activos',
            'fundamento_cuantitativo': (
                f"• Activo Total: ${activo_y2:,.2f}\n"
                f"• Rotación Actual: {rotacion_activos_y2:.2f}x\n"
                f"• Activo Optimizado: ${activo_optimizado:,.2f}\n"
                f"• Nueva Rotación: {nueva_rotacion:.2f}x\n"
                f"• Capital Liberado: ${capital_liberado:,.2f}"
            ),
            'analisis': (
                f"Optimizar activos reduciendo 10% la base (${capital_liberado:,.2f}) mejoraría "
                f"rotación de {rotacion_activos_y2:.2f}x a {nueva_rotacion:.2f}x" +
                (f", incrementando eficiencia en {(nueva_rotacion/rotacion_activos_y2-1)*100:.1f}%." if rotacion_activos_y2 != 0 else ".")
            ),
            'acciones': [
                "Auditar activos subutilizados",
                "Vender equipos obsoletos",
                "Implementar arrendamiento operativo",
                "Migrar infraestructura a cloud",
                "Optimizar espacio físico"
            ],
            'impacto': (
                f"Mejora rotación: +{(nueva_rotacion/rotacion_activos_y2-1)*100:.1f}%, " if rotacion_activos_y2 != 0 else "Mejora rotación significativa, "
            ) + f"Capital liberado: ${capital_liberado:,.2f}"
        }
        recomendaciones.append(recom1)
        
        # RECOMENDACIÓN 2: AUTOMATIZACIÓN
        gastos_admin_y2 = self.income_data.gastos_admin_y2
        costo_procesos_manuales = gastos_admin_y2 * 0.30
        ahorro_automatizacion = costo_procesos_manuales * 0.50
        inversion_automatizacion = ahorro_automatizacion * 1.5
        
        # Validar ahorro para evitar división por cero
        if ahorro_automatizacion > 0:
            payback_meses = inversion_automatizacion / (ahorro_automatizacion/12)
        else:
            payback_meses = 0
        
        recom2 = {
            'numero': 2,
            'titulo': 'Automatizar Procesos Operativos Clave',
            'fundamento_cuantitativo': (
                f"• Costo Procesos Manuales: ${costo_procesos_manuales:,.2f}\n"
                f"• Ahorro Automatización (50%): ${ahorro_automatizacion:,.2f}\n"
                f"• Inversión Requerida: ${inversion_automatizacion:,.2f}\n"
                f"• Payback Period: {payback_meses:.1f} meses"
            ),
            'analisis': (
                f"Automatizar procesos clave puede ahorrar ${ahorro_automatizacion:,.2f} anuales "
                f"con inversión de ${inversion_automatizacion:,.2f} (recuperación en {payback_meses:.1f} meses)."
            ),
            'acciones': [
                "Implementar sistema ERP integrado",
                "Automatizar facturación y cobranza",
                "Implementar RPA para tareas repetitivas",
                "Digitalizar firma de documentos",
                "Automatizar reporteo financiero"
            ],
            'impacto': f"Ahorro anual: ${ahorro_automatizacion:,.2f}, Reducción tiempo: 50-70%"
        }
        recomendaciones.append(recom2)
        
        # RECOMENDACIÓN 3: OPTIMIZAR CAPITAL DE TRABAJO
        cxc_y2 = self.balance_data.clientes_cobrar_y2
        dias_cobranza = (cxc_y2 / ventas_y2 * 365) if ventas_y2 != 0 else 0
        
        inventarios_y2 = self.balance_data.existencias_y2
        dias_inventario = (inventarios_y2 / (ventas_y2/365)) if ventas_y2 != 0 else 0
        
        cxp_y2 = self.balance_data.proveedores_y2
        dias_pago = (cxp_y2 / (ventas_y2/365)) if ventas_y2 != 0 else 0
        
        ciclo_efectivo = dias_cobranza + dias_inventario - dias_pago
        reduccion_ciclo_objetivo = 15
        nuevo_ciclo = max(0, ciclo_efectivo - reduccion_ciclo_objetivo)
        capital_liberado = (reduccion_ciclo_objetivo/365) * ventas_y2
        
        recom3 = {
            'numero': 3,
            'titulo': 'Optimizar Ciclo de Capital de Trabajo',
            'fundamento_cuantitativo': (
                f"• Ciclo de Efectivo: {ciclo_efectivo:.0f} días\n"
                f"• Días Cobranza: {dias_cobranza:.0f}\n"
                f"• Días Inventario: {dias_inventario:.0f}\n"
                f"• Días Pago: {dias_pago:.0f}\n"
                f"• Reducción Objetivo: {reduccion_ciclo_objetivo} días\n"
                f"• Capital Liberado: ${capital_liberado:,.2f}"
            ),
            'analisis': (
                f"Reducir ciclo de {ciclo_efectivo:.0f} a {nuevo_ciclo:.0f} días liberaría "
                f"${capital_liberado:,.2f} de capital de trabajo, mejorando liquidez operativa."
            ),
            'acciones': [
                f"Reducir DSO a {max(30, dias_cobranza-10):.0f} días",
                "Optimizar inventarios (Just-in-Time)",
                f"Extender DPO a {dias_pago+7:.0f} días",
                "Implementar descuentos por pronto pago",
                "Automatizar facturación y cobranza"
            ],
            'impacto': f"Reducción ciclo: {reduccion_ciclo_objetivo} días, Capital liberado: ${capital_liberado:,.2f}"
        }
        recomendaciones.append(recom3)
        
        return recomendaciones