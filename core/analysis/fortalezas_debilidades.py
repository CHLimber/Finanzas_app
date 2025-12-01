"""
Archivo: core/analysis/fortalezas_debilidades.py
Análisis de Fortalezas y Debilidades Financieras
"""


class FortalezasDebilidadesAnalysis:
    """Identifica las principales fortalezas y debilidades financieras"""
    
    def __init__(self, matriz_ratios):
        """
        Args:
            matriz_ratios: Diccionario con la matriz de ratios del análisis D1
        """
        self.matriz = matriz_ratios
    
    def identificar_fortalezas_debilidades(self):
        """
        Identifica las 3 principales fortalezas y 3 principales debilidades
        
        Returns:
            dict: Fortalezas y debilidades con análisis cuantitativo
        """
        # Preparar ratios para ranking
        ratios_ranking = []
        
        for key, data in self.matriz.items():
            # Calcular score compuesto
            score = self._calcular_score(data)
            
            ratios_ranking.append({
                'key': key,
                'nombre': data['nombre'],
                'categoria': data['categoria'],
                'ano_1': data['ano_1'],
                'ano_2': data['ano_2'],
                'cambio_porcentual': data['cambio_porcentual'],
                'estado': data['estado'],
                'direccion': data['direccion'],
                'unidad': data['unidad'],
                'rango_optimo': data['rango_optimo'],
                'score': score,
                'interpretacion': data['interpretacion']
            })
        
        # Ordenar por score (mayor a menor)
        ratios_ordenados = sorted(ratios_ranking, key=lambda x: x['score'], reverse=True)
        
        # Top 3 fortalezas (scores más altos)
        fortalezas = ratios_ordenados[:3]
        
        # Top 3 debilidades (scores más bajos)
        debilidades = ratios_ordenados[-3:]
        debilidades.reverse()  # Ordenar de peor a menos peor
        
        # Generar análisis cuantitativo
        fortalezas_con_analisis = [
            self._analizar_fortaleza(f, i+1) for i, f in enumerate(fortalezas)
        ]
        
        debilidades_con_analisis = [
            self._analizar_debilidad(d, i+1) for i, d in enumerate(debilidades)
        ]
        
        # Generar interpretación global
        interpretacion_global = self._generar_interpretacion_global(
            fortalezas_con_analisis, debilidades_con_analisis
        )
        
        return {
            'fortalezas': fortalezas_con_analisis,
            'debilidades': debilidades_con_analisis,
            'interpretacion_global': interpretacion_global
        }
    
    def _calcular_score(self, data):
        """
        Calcula un score compuesto para ranking:
        - Estado óptimo = +100
        - Estado bajo = -100
        - Estado alto = -50
        - Mejora = +50
        - Deterioro = -50
        - Bonus si está muy dentro del rango óptimo
        - Penalty si está muy fuera del rango óptimo
        """
        score = 0
        
        # Score base por estado
        if data['estado'] == 'optimo':
            score += 100
            # Bonus adicional: qué tan centrado está en el rango
            rango_min, rango_max = data['rango_optimo']
            centro = (rango_min + rango_max) / 2
            ancho = rango_max - rango_min
            desviacion = abs(data['ano_2'] - centro) / ancho
            score += (1 - desviacion) * 20  # Hasta +20 si está en el centro
        
        elif data['estado'] == 'bajo':
            score -= 100
            # Penalty adicional: qué tan lejos está del rango
            rango_min, rango_max = data['rango_optimo']
            if data['ano_2'] < rango_min:
                distancia_rel = (rango_min - data['ano_2']) / rango_min
                score -= min(distancia_rel * 50, 50)  # Hasta -50 adicional
        
        else:  # alto
            score -= 50
            # Penalty adicional: qué tan lejos está del rango
            rango_min, rango_max = data['rango_optimo']
            if data['ano_2'] > rango_max:
                distancia_rel = (data['ano_2'] - rango_max) / rango_max
                score -= min(distancia_rel * 30, 30)  # Hasta -30 adicional
        
        # Score por tendencia
        if data['direccion'] == 'mejora':
            score += 50
            # Bonus si la mejora es significativa (>20%)
            if abs(data['cambio_porcentual']) > 20:
                score += 20
        elif data['direccion'] == 'deterioro':
            score -= 50
            # Penalty si el deterioro es significativo (>20%)
            if abs(data['cambio_porcentual']) > 20:
                score -= 20
        
        return score
    
    def _analizar_fortaleza(self, fortaleza, posicion):
        """Genera análisis cuantitativo de una fortaleza"""
        nombre = fortaleza['nombre']
        ano1 = fortaleza['ano_1']
        ano2 = fortaleza['ano_2']
        cambio_pct = fortaleza['cambio_porcentual']
        unidad = fortaleza['unidad']
        rango_min, rango_max = fortaleza['rango_optimo']
        
        # Formatear valores
        valor1 = self._formatear_valor(ano1, unidad)
        valor2 = self._formatear_valor(ano2, unidad)
        
        # Análisis cuantitativo
        analisis = f"FORTALEZA #{posicion}: {nombre}\n\n"
        
        # Datos cuantitativos
        analisis += f"📊 DATOS CUANTITATIVOS:\n"
        analisis += f"   • Año 1: {valor1}\n"
        analisis += f"   • Año 2: {valor2}\n"
        analisis += f"   • Cambio: {cambio_pct:+.1f}%\n"
        analisis += f"   • Rango Óptimo: {self._formatear_valor(rango_min, unidad)} - {self._formatear_valor(rango_max, unidad)}\n\n"
        
        # Por qué es fortaleza
        analisis += f"✓ POR QUÉ ES UNA FORTALEZA:\n"
        
        if fortaleza['estado'] == 'optimo' and fortaleza['direccion'] == 'mejora':
            analisis += f"   1. Se encuentra en rango óptimo ({valor2})\n"
            analisis += f"   2. Mejoró {abs(cambio_pct):.1f}% respecto al año anterior\n"
            analisis += f"   3. Muestra tendencia positiva y sostenible\n"
        
        elif fortaleza['estado'] == 'optimo':
            analisis += f"   1. Se mantiene sólidamente en rango óptimo ({valor2})\n"
            analisis += f"   2. Demuestra estabilidad financiera\n"
            analisis += f"   3. Supera estándares del sector tecnológico\n"
        
        elif fortaleza['direccion'] == 'mejora':
            analisis += f"   1. Mejora significativa de {abs(cambio_pct):.1f}%\n"
            analisis += f"   2. Tendencia positiva hacia el rango óptimo\n"
            analisis += f"   3. Demuestra gestión financiera efectiva\n"
        
        analisis += f"\n"
        
        # Impacto en el negocio
        analisis += self._interpretar_impacto_fortaleza(fortaleza)
        
        return {
            'posicion': posicion,
            'ratio': nombre,
            'categoria': fortaleza['categoria'],
            'ano_1': ano1,
            'ano_2': ano2,
            'cambio_pct': cambio_pct,
            'unidad': unidad,
            'estado': fortaleza['estado'],
            'rango_optimo': fortaleza['rango_optimo'],
            'analisis': analisis,
            'score': fortaleza['score']
        }
    
    def _analizar_debilidad(self, debilidad, posicion):
        """Genera análisis cuantitativo de una debilidad"""
        nombre = debilidad['nombre']
        ano1 = debilidad['ano_1']
        ano2 = debilidad['ano_2']
        cambio_pct = debilidad['cambio_porcentual']
        unidad = debilidad['unidad']
        rango_min, rango_max = debilidad['rango_optimo']
        
        # Formatear valores
        valor1 = self._formatear_valor(ano1, unidad)
        valor2 = self._formatear_valor(ano2, unidad)
        
        # Análisis cuantitativo
        analisis = f"DEBILIDAD #{posicion}: {nombre}\n\n"
        
        # Datos cuantitativos
        analisis += f"📊 DATOS CUANTITATIVOS:\n"
        analisis += f"   • Año 1: {valor1}\n"
        analisis += f"   • Año 2: {valor2}\n"
        analisis += f"   • Cambio: {cambio_pct:+.1f}%\n"
        analisis += f"   • Rango Óptimo: {self._formatear_valor(rango_min, unidad)} - {self._formatear_valor(rango_max, unidad)}\n"
        
        # Calcular brecha con rango óptimo
        if debilidad['estado'] == 'bajo':
            brecha = rango_min - ano2
            brecha_pct = (brecha / rango_min) * 100
            analisis += f"   • Brecha con óptimo: {abs(brecha_pct):.1f}% por debajo\n\n"
        elif debilidad['estado'] == 'alto':
            brecha = ano2 - rango_max
            brecha_pct = (brecha / rango_max) * 100
            analisis += f"   • Brecha con óptimo: {abs(brecha_pct):.1f}% por encima\n\n"
        else:
            analisis += "\n"
        
        # Por qué es debilidad
        analisis += f"✗ POR QUÉ ES UNA DEBILIDAD:\n"
        
        if debilidad['estado'] == 'bajo' and debilidad['direccion'] == 'deterioro':
            analisis += f"   1. Está {abs(brecha_pct):.1f}% por debajo del rango óptimo\n"
            analisis += f"   2. Se deterioró {abs(cambio_pct):.1f}% respecto al año anterior\n"
            analisis += f"   3. Muestra tendencia negativa preocupante\n"
        
        elif debilidad['estado'] == 'bajo':
            analisis += f"   1. Está por debajo del rango óptimo ({valor2} < {self._formatear_valor(rango_min, unidad)})\n"
            analisis += f"   2. No alcanza estándares del sector tecnológico\n"
            analisis += f"   3. Requiere acciones correctivas inmediatas\n"
        
        elif debilidad['direccion'] == 'deterioro':
            analisis += f"   1. Deterioro significativo de {abs(cambio_pct):.1f}%\n"
            analisis += f"   2. Tendencia negativa que requiere atención\n"
            analisis += f"   3. Puede comprometer competitividad\n"
        
        elif debilidad['estado'] == 'alto':
            analisis += f"   1. Excede el rango óptimo, indicando ineficiencia\n"
            analisis += f"   2. Posible sobreinversión o recursos subutilizados\n"
            analisis += f"   3. Oportunidad de optimización\n"
        
        analisis += f"\n"
        
        # Impacto y recomendaciones
        analisis += self._interpretar_impacto_debilidad(debilidad)
        
        return {
            'posicion': posicion,
            'ratio': nombre,
            'categoria': debilidad['categoria'],
            'ano_1': ano1,
            'ano_2': ano2,
            'cambio_pct': cambio_pct,
            'unidad': unidad,
            'estado': debilidad['estado'],
            'rango_optimo': debilidad['rango_optimo'],
            'analisis': analisis,
            'score': debilidad['score']
        }
    
    def _interpretar_impacto_fortaleza(self, fortaleza):
        """Interpreta el impacto de una fortaleza en el negocio"""
        key = fortaleza['key']
        
        impactos = {
            'liquidez_general': "💼 IMPACTO: Alta capacidad para afrontar obligaciones corrientes sin comprometer operaciones. Esto permite invertir en I+D y oportunidades de crecimiento sin restricciones de liquidez.",
            
            'razon_tesoreria': "💼 IMPACTO: Excelente posición de efectivo para aprovechar oportunidades estratégicas (M&A, contrataciones clave) sin depender de financiamiento externo.",
            
            'rat': "💼 IMPACTO: Alta rentabilidad económica demuestra eficiencia operativa superior. En tech, RAT elevado indica escalabilidad exitosa y ventaja competitiva sostenible.",
            
            'rrp': "💼 IMPACTO: Rentabilidad excepcional para accionistas. Justifica el riesgo de inversión en sector tecnológico y atrae capital para expansión.",
            
            'margen_neto': "💼 IMPACTO: Márgenes elevados típicos de SaaS/software exitoso. Indica poder de fijación de precios y eficiencia operativa tras alcanzar escala.",
            
            'ratio_garantia': "💼 IMPACTO: Sólida solvencia facilita acceso a financiamiento para proyectos de expansión a tasas favorables.",
            
            'ratio_autonomia': "💼 IMPACTO: Independencia financiera que permite tomar decisiones estratégicas sin presión de acreedores.",
            
            'fondo_maniobra': "💼 IMPACTO: Capital de trabajo saludable asegura continuidad operativa y capacidad de inversión en innovación.",
            
            'razon_disponibilidad': "💼 IMPACTO: Reservas de efectivo permiten capitalizar oportunidades emergentes y resistir períodos de volatilidad típicos del sector.",
            
            'rotacion_activos': "💼 IMPACTO: Uso eficiente de activos maximiza retorno. En tech, indica que inversiones en talento e infraestructura generan valor.",
            
            'apalancamiento': "💼 IMPACTO: Estructura de capital óptima que amplifica retornos sin comprometer estabilidad financiera.",
            
            'ratio_calidad_deuda': "💼 IMPACTO: Estructura de deuda equilibrada reduce riesgo de refinanciamiento y mantiene flexibilidad financiera."
        }
        
        return impactos.get(key, "💼 IMPACTO: Fortalece la posición financiera general de la empresa.")
    
    def _interpretar_impacto_debilidad(self, debilidad):
        """Interpreta el impacto de una debilidad y recomienda acciones"""
        key = debilidad['key']
        
        impactos = {
            'liquidez_general': "⚠️ IMPACTO: Riesgo de dificultades para cumplir obligaciones corrientes. En tech, puede limitar inversión en I+D crítico.\n\n📋 RECOMENDACIÓN: Mejorar gestión de cobros, negociar plazos con proveedores o considerar líneas de crédito.",
            
            'razon_tesoreria': "⚠️ IMPACTO: Vulnerabilidad ante gastos imprevistos o caídas temporales de ingresos.\n\n📋 RECOMENDACIÓN: Incrementar reservas de efectivo, acelerar cobranza o establecer línea de crédito de respaldo.",
            
            'rat': "⚠️ IMPACTO: Baja rentabilidad económica indica problemas de eficiencia operativa o márgenes comprimidos.\n\n📋 RECOMENDACIÓN: Optimizar costos operativos, revisar pricing, mejorar mix de productos/servicios de mayor margen.",
            
            'rrp': "⚠️ IMPACTO: Retorno insuficiente no justifica riesgo. Puede dificultar atracción de inversores.\n\n📋 RECOMENDACIÓN: Mejorar rentabilidad operativa, optimizar estructura de capital, reducir gastos financieros.",
            
            'margen_neto': "⚠️ IMPACTO: Márgenes bajos indican presión competitiva o ineficiencias operativas.\n\n📋 RECOMENDACIÓN: Revisar estructura de costos, optimizar pricing, enfocarse en segmentos de mayor valor.",
            
            'ratio_garantia': "⚠️ IMPACTO: Solvencia comprometida dificulta acceso a financiamiento y aumenta costo de capital.\n\n📋 RECOMENDACIÓN: Reducir deuda, retener utilidades o considerar capitalización mediante nuevos aportes.",
            
            'ratio_autonomia': "⚠️ IMPACTO: Alta dependencia de financiamiento externo limita autonomía estratégica.\n\n📋 RECOMENDACIÓN: Fortalecer patrimonio mediante retención de utilidades o aportes de capital.",
            
            'fondo_maniobra': "⚠️ IMPACTO: Capital de trabajo insuficiente compromete operación diaria y limita inversión.\n\n📋 RECOMENDACIÓN: Reestructurar deuda a LP, mejorar ciclo de conversión de efectivo.",
            
            'razon_disponibilidad': "⚠️ IMPACTO: Bajo efectivo limita capacidad de reacción ante oportunidades o crisis.\n\n📋 RECOMENDACIÓN: Incrementar generación de caja operativa, reducir capital de trabajo innecesario.",
            
            'rotacion_activos': "⚠️ IMPACTO: Subutilización de activos reduce retorno sobre inversión.\n\n📋 RECOMENDACIÓN: Optimizar uso de activos, vender activos improductivos, mejorar eficiencia operativa.",
            
            'apalancamiento': "⚠️ IMPACTO: Estructura de capital subóptima no maximiza retorno o genera riesgo excesivo.\n\n📋 RECOMENDACIÓN: Ajustar proporción deuda/equity según costo de capital y perfil de riesgo.",
            
            'ratio_calidad_deuda': "⚠️ IMPACTO: Estructura de deuda desequilibrada aumenta riesgo de refinanciamiento.\n\n📋 RECOMENDACIÓN: Reestructurar deuda hacia plazos más largos o reducir deuda CP."
        }
        
        return impactos.get(key, "⚠️ IMPACTO: Área que requiere atención y mejora.\n\n📋 RECOMENDACIÓN: Desarrollar plan de acción para corregir esta debilidad.")
    
    def _generar_interpretacion_global(self, fortalezas, debilidades):
        """Genera interpretación global del análisis"""
        texto = "DIAGNÓSTICO FINANCIERO INTEGRAL\n\n"
        
        # Resumen de fortalezas
        texto += "FORTALEZAS PRINCIPALES:\n"
        for f in fortalezas:
            texto += f"✓ {f['ratio']} ({f['categoria']}): {self._formatear_valor(f['ano_2'], f['unidad'])}\n"
        
        texto += "\nDEBILIDADES PRINCIPALES:\n"
        for d in debilidades:
            texto += f"✗ {d['ratio']} ({d['categoria']}): {self._formatear_valor(d['ano_2'], d['unidad'])}\n"
        
        texto += "\n" + "="*60 + "\n\n"
        
        # Análisis por categoría
        categorias_fortalezas = [f['categoria'] for f in fortalezas]
        categorias_debilidades = [d['categoria'] for d in debilidades]
        
        if categorias_fortalezas.count('Económico') >= 2:
            texto += "💪 FORTALEZA CLAVE: Rentabilidad y eficiencia económica destacadas.\n"
        elif categorias_fortalezas.count('Patrimonial') >= 2:
            texto += "💪 FORTALEZA CLAVE: Solidez patrimonial y liquidez robusta.\n"
        elif categorias_fortalezas.count('Financiero') >= 2:
            texto += "💪 FORTALEZA CLAVE: Solvencia y estructura financiera sólida.\n"
        
        if categorias_debilidades.count('Económico') >= 2:
            texto += "⚠️ ÁREA CRÍTICA: Rentabilidad y eficiencia operativa requieren mejora urgente.\n"
        elif categorias_debilidades.count('Patrimonial') >= 2:
            texto += "⚠️ ÁREA CRÍTICA: Liquidez y capital de trabajo comprometen operaciones.\n"
        elif categorias_debilidades.count('Financiero') >= 2:
            texto += "⚠️ ÁREA CRÍTICA: Solvencia y estructura de deuda requieren reestructuración.\n"
        
        texto += "\nCONCLUSIÓN: "
        
        if len([f for f in fortalezas if f['categoria'] == 'Económico']) >= 2:
            texto += "La empresa presenta sólida rentabilidad, lo cual es fundamental en el sector tecnológico. "
            texto += "Las debilidades identificadas son manejables y pueden corregirse sin comprometer el crecimiento. "
            texto += "Priorizar: fortalecimiento de áreas débiles manteniendo el impulso en rentabilidad."
        else:
            texto += "La empresa enfrenta desafíos financieros que requieren atención estratégica. "
            texto += "Es crítico capitalizar las fortalezas existentes mientras se implementan acciones correctivas "
            texto += "en las áreas débiles. Priorizar: mejora de rentabilidad operativa y optimización de estructura financiera."
        
        return texto
    
    def _formatear_valor(self, valor, unidad):
        """Formatea un valor según su unidad"""
        if unidad == 'porcentaje':
            return f"{valor:.2f}%"
        elif unidad == 'veces':
            return f"{valor:.2f}x"
        else:  # ratio
            return f"{valor:.2f}"