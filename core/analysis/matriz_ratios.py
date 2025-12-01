"""
Archivo: core/analysis/matriz_ratios.py
Matriz de Ratios Comparativos - Analisis Integral
CORREGIDO: La direccion (mejora/deterioro) ahora se evalua respecto
al rango optimo, no simplemente si el valor subio o bajo.
"""


class MatrizRatios:
    """Matriz comparativa de los principales ratios financieros"""
    
    def __init__(self, balance_data, income_data):
        self.balance_data = balance_data
        self.income_data = income_data

    def _get_total_pasivos(self, year):
        """Helper: Calcula Pasivo Total = PC + PNC"""
        return (self.balance_data.get_total_pasivo_corriente(year) + 
                self.balance_data.get_total_pasivo_no_corriente(year))

    def calcular_fondo_maniobra(self, year):
        """Calcula Fondo de Maniobra"""
        activo_corriente = self.balance_data.get_total_corriente(year)
        pasivo_corriente = self.balance_data.get_total_pasivo_corriente(year)
        return activo_corriente - pasivo_corriente
    
    def calcular_ratio_fm(self, year):
        """Calcula Ratio FM = FM / Activo Total"""
        fm = self.calcular_fondo_maniobra(year)
        activo_total = self.balance_data.get_total_activos(year)
        return (fm / activo_total) if activo_total != 0 else 0
    
    def calcular_liquidez_general(self, year):
        """Calcula Liquidez General = AC / PC"""
        ac = self.balance_data.get_total_corriente(year)
        pc = self.balance_data.get_total_pasivo_corriente(year)
        return (ac / pc) if pc != 0 else 0
    
    def calcular_razon_tesoreria(self, year):
        """Calcula Razon de Tesoreria"""
        if year == 1:
            disponible = self.balance_data.caja_bancos_y1
            cxc = self.balance_data.clientes_cobrar_y1
        else:
            disponible = self.balance_data.caja_bancos_y2
            cxc = self.balance_data.clientes_cobrar_y2
        
        pc = self.balance_data.get_total_pasivo_corriente(year)
        return ((disponible + cxc) / pc) if pc != 0 else 0
    
    def calcular_razon_disponibilidad(self, year):
        """Calcula Razon de Disponibilidad"""
        disponible = self.balance_data.caja_bancos_y1 if year == 1 else self.balance_data.caja_bancos_y2
        pc = self.balance_data.get_total_pasivo_corriente(year)
        return (disponible / pc) if pc != 0 else 0
    
    def calcular_ratio_garantia(self, year):
        activo = self.balance_data.get_total_activos(year)
        pasivo = self._get_total_pasivos(year) 
        return (activo / pasivo) if pasivo != 0 else 0
    
    def calcular_ratio_autonomia(self, year):
        """Calcula Ratio de Autonomia = Patrimonio / Pasivo"""
        patrimonio = self.balance_data.get_total_patrimonio(year)
        pasivo = self._get_total_pasivos(year)
        return (patrimonio / pasivo) if pasivo != 0 else 0
    
    def calcular_ratio_calidad_deuda(self, year):
        """Calcula Calidad de Deuda = PC / Pasivo Total"""
        pc = self.balance_data.get_total_pasivo_corriente(year)
        pasivo = self._get_total_pasivos(year)
        return (pc / pasivo) if pasivo != 0 else 0
    
    def calcular_rat(self, year):
        """Calcula RAT = BAII / Activo Total x 100"""
        baii = self.income_data.get_utilidad_operativa(year)
        activo = self.balance_data.get_total_activos(year)
        return (baii / activo * 100) if activo != 0 else 0
    
    def calcular_rrp(self, year):
        """Calcula RRP = UN / PN x 100"""
        un = self.income_data.get_utilidad_neta(year)
        pn = self.balance_data.get_total_patrimonio(year)
        return (un / pn * 100) if pn != 0 else 0
    
    def calcular_margen_neto(self, year):
        """Calcula Margen Neto = UN / Ventas x 100"""
        un = self.income_data.get_utilidad_neta(year)
        ventas = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        return (un / ventas * 100) if ventas != 0 else 0
    
    def calcular_rotacion_activos(self, year):
        """Calcula Rotacion de Activos = Ventas / Activo"""
        ventas = self.income_data.ingresos_servicios_y1 if year == 1 else self.income_data.ingresos_servicios_y2
        activo = self.balance_data.get_total_activos(year)
        return (ventas / activo) if activo != 0 else 0
    
    def calcular_apalancamiento(self, year):
        """Calcula Apalancamiento = Activo / PN"""
        activo = self.balance_data.get_total_activos(year)
        pn = self.balance_data.get_total_patrimonio(year)
        return (activo / pn) if pn != 0 else 0
    
    def _calcular_distancia_al_optimo(self, valor, rango_min, rango_max):
        """
        Calcula la distancia de un valor al rango optimo.
        
        Returns:
            float: 0 si esta dentro del rango, distancia positiva si esta fuera
        """
        if valor < rango_min:
            return rango_min - valor
        elif valor > rango_max:
            return valor - rango_max
        else:
            return 0  # Esta dentro del rango optimo
    
    def _determinar_estado(self, valor, rango_min, rango_max):
        """Determina si el valor esta bajo, optimo o alto"""
        if valor < rango_min:
            return "bajo"
        elif valor > rango_max:
            return "alto"
        else:
            return "optimo"
    
    def _evaluar_direccion_vs_optimo(self, ano1, ano2, rango_min, rango_max):
        """
        Evalua la direccion del cambio respecto al rango optimo.
        
        LOGICA CORREGIDA:
        - Si se ACERCA al rango optimo -> mejora
        - Si se ALEJA del rango optimo -> deterioro
        - Si ambos en optimo o distancia similar -> estable
        
        Returns:
            tuple: (direccion, simbolo)
        """
        estado_y1 = self._determinar_estado(ano1, rango_min, rango_max)
        estado_y2 = self._determinar_estado(ano2, rango_min, rango_max)
        
        dist_y1 = self._calcular_distancia_al_optimo(ano1, rango_min, rango_max)
        dist_y2 = self._calcular_distancia_al_optimo(ano2, rango_min, rango_max)
        
        # Umbral para considerar cambio significativo (5% del rango)
        rango_amplitud = rango_max - rango_min
        umbral = rango_amplitud * 0.1 if rango_amplitud > 0 else 0.05
        
        # CASO 1: Ambos en rango optimo
        if estado_y1 == "optimo" and estado_y2 == "optimo":
            return ("estable", "=")
        
        # CASO 2: Entro al rango optimo
        if estado_y1 != "optimo" and estado_y2 == "optimo":
            return ("mejora", "^")
        
        # CASO 3: Salio del rango optimo
        if estado_y1 == "optimo" and estado_y2 != "optimo":
            return ("deterioro", "v")
        
        # CASO 4: Ambos fuera del optimo - comparar distancias
        diferencia = dist_y1 - dist_y2  # Positivo si mejoro (se acerco)
        
        if diferencia > umbral:
            return ("mejora", "^")
        elif diferencia < -umbral:
            return ("deterioro", "v")
        else:
            return ("estable", "=")
    
    def generar_matriz_completa(self):
        """
        Genera la matriz completa de ratios comparativos
        
        Returns:
            dict: Matriz con todos los ratios y analisis de cambios
        """
        ratios = {
            # ANALISIS PATRIMONIAL
            'fondo_maniobra': {
                'nombre': 'Fondo de Maniobra (Ratio)',
                'categoria': 'Patrimonial',
                'unidad': 'ratio',
                'ano_1': self.calcular_ratio_fm(1),
                'ano_2': self.calcular_ratio_fm(2),
                'rango_optimo': (0.10, 0.30),
                'sector': 'tecnologia'
            },
            'liquidez_general': {
                'nombre': 'Liquidez General',
                'categoria': 'Patrimonial',
                'unidad': 'ratio',
                'ano_1': self.calcular_liquidez_general(1),
                'ano_2': self.calcular_liquidez_general(2),
                'rango_optimo': (1.5, 2.5),
                'sector': 'tecnologia'
            },
            'razon_tesoreria': {
                'nombre': 'Razon de Tesoreria',
                'categoria': 'Patrimonial',
                'unidad': 'ratio',
                'ano_1': self.calcular_razon_tesoreria(1),
                'ano_2': self.calcular_razon_tesoreria(2),
                'rango_optimo': (1.0, 1.5),
                'sector': 'tecnologia'
            },
            'razon_disponibilidad': {
                'nombre': 'Razon de Disponibilidad',
                'categoria': 'Patrimonial',
                'unidad': 'ratio',
                'ano_1': self.calcular_razon_disponibilidad(1),
                'ano_2': self.calcular_razon_disponibilidad(2),
                'rango_optimo': (0.20, 0.50),
                'sector': 'tecnologia'
            },
            
            # ANALISIS FINANCIERO (SOLVENCIA)
            'ratio_garantia': {
                'nombre': 'Ratio de Garantia',
                'categoria': 'Financiero',
                'unidad': 'ratio',
                'ano_1': self.calcular_ratio_garantia(1),
                'ano_2': self.calcular_ratio_garantia(2),
                'rango_optimo': (1.5, 2.5),
                'sector': 'tecnologia'
            },
            'ratio_autonomia': {
                'nombre': 'Ratio de Autonomia',
                'categoria': 'Financiero',
                'unidad': 'ratio',
                'ano_1': self.calcular_ratio_autonomia(1),
                'ano_2': self.calcular_ratio_autonomia(2),
                'rango_optimo': (0.8, 1.5),
                'sector': 'tecnologia'
            },
            'ratio_calidad_deuda': {
                'nombre': 'Calidad de Deuda',
                'categoria': 'Financiero',
                'unidad': 'ratio',
                'ano_1': self.calcular_ratio_calidad_deuda(1),
                'ano_2': self.calcular_ratio_calidad_deuda(2),
                'rango_optimo': (0.30, 0.50),
                'sector': 'tecnologia'
            },
            
            # ANALISIS Económico (RENTABILIDAD)
            'rat': {
                'nombre': 'RAT (Rent. Activos)',
                'categoria': 'Económico',
                'unidad': 'porcentaje',
                'ano_1': self.calcular_rat(1),
                'ano_2': self.calcular_rat(2),
                'rango_optimo': (10, 20),
                'sector': 'tecnologia'
            },
            'rrp': {
                'nombre': 'RRP (Rent. Patrimonio)',
                'categoria': 'Económico',
                'unidad': 'porcentaje',
                'ano_1': self.calcular_rrp(1),
                'ano_2': self.calcular_rrp(2),
                'rango_optimo': (15, 30),
                'sector': 'tecnologia'
            },
            'margen_neto': {
                'nombre': 'Margen Neto',
                'categoria': 'Económico',
                'unidad': 'porcentaje',
                'ano_1': self.calcular_margen_neto(1),
                'ano_2': self.calcular_margen_neto(2),
                'rango_optimo': (15, 25),
                'sector': 'tecnologia'
            },
            'rotacion_activos': {
                'nombre': 'Rotacion de Activos',
                'categoria': 'Económico',
                'unidad': 'veces',
                'ano_1': self.calcular_rotacion_activos(1),
                'ano_2': self.calcular_rotacion_activos(2),
                'rango_optimo': (0.8, 1.5),
                'sector': 'tecnologia'
            },
            'apalancamiento': {
                'nombre': 'Apalancamiento Financiero',
                'categoria': 'Económico',
                'unidad': 'veces',
                'ano_1': self.calcular_apalancamiento(1),
                'ano_2': self.calcular_apalancamiento(2),
                'rango_optimo': (1.3, 2.0),
                'sector': 'tecnologia'
            }
        }
        
        # Calcular cambios e interpretaciones
        for key, data in ratios.items():
            ano1 = data['ano_1']
            ano2 = data['ano_2']
            rango_min, rango_max = data['rango_optimo']
            
            # Cambio absoluto
            cambio_absoluto = ano2 - ano1
            
            # Cambio porcentual
            if ano1 != 0:
                cambio_porcentual = ((ano2 - ano1) / abs(ano1)) * 100
            else:
                cambio_porcentual = 0
            
            # Estado en Ano 2 (respecto al rango optimo)
            estado = self._determinar_estado(ano2, rango_min, rango_max)
            
            # Estado en Ano 1 (para comparacion)
            estado_y1 = self._determinar_estado(ano1, rango_min, rango_max)
            
            # DIRECCION CORREGIDA: basada en proximidad al optimo
            direccion, simbolo = self._evaluar_direccion_vs_optimo(
                ano1, ano2, rango_min, rango_max
            )
            
            # Interpretacion del cambio (ahora considera el optimo)
            interpretacion = self._interpretar_cambio(
                key, ano1, ano2, cambio_absoluto, cambio_porcentual, 
                direccion, estado, estado_y1, data['rango_optimo'], data['sector']
            )
            
            # Anadir datos calculados
            data.update({
                'cambio_absoluto': cambio_absoluto,
                'cambio_porcentual': cambio_porcentual,
                'direccion': direccion,
                'simbolo': simbolo,
                'estado': estado,
                'estado_y1': estado_y1,
                'interpretacion': interpretacion
            })
        
        return ratios
    
    def _interpretar_cambio(self, ratio_key, ano1, ano2, cambio_abs, cambio_pct, 
                           direccion, estado, estado_y1, rango_optimo, sector):
        """
        Interpreta el cambio de cada ratio considerando el rango optimo
        """
        rango_min, rango_max = rango_optimo
        
        # Texto base segun direccion y estados
        if direccion == "mejora":
            if estado == "optimo" and estado_y1 != "optimo":
                base = f"MEJORA: Entro al rango optimo ({rango_min:.2f}-{rango_max:.2f})"
            elif estado != "optimo":
                base = f"MEJORA: Se acerca al rango optimo ({rango_min:.2f}-{rango_max:.2f})"
            else:
                base = "Se mantiene en rango optimo"
        elif direccion == "deterioro":
            if estado != "optimo" and estado_y1 == "optimo":
                base = f"DETERIORO: Salio del rango optimo ({rango_min:.2f}-{rango_max:.2f})"
            elif estado != "optimo":
                base = f"DETERIORO: Se aleja del rango optimo ({rango_min:.2f}-{rango_max:.2f})"
            else:
                base = "Deterioro dentro del rango optimo"
        else:
            if estado == "optimo":
                base = "ESTABLE en rango optimo"
            else:
                base = f"ESTABLE fuera del optimo (estado: {estado})"
        
        # Agregar contexto especifico por ratio
        contexto = self._contexto_ratio(ratio_key, ano2, estado, sector)
        
        return f"{base}. {contexto}"
    
    def _contexto_ratio(self, ratio_key, valor, estado, sector):
        """Genera contexto especifico para cada ratio"""
        
        contextos = {
            'fondo_maniobra': {
                'optimo': "Capacidad adecuada para financiar operaciones corrientes.",
                'bajo': "Riesgo de liquidez estructural.",
                'alto': "Exceso de recursos corrientes, posible ineficiencia."
            },
            'liquidez_general': {
                'optimo': "Equilibrio entre liquidez y eficiencia.",
                'bajo': "Riesgo de no poder cubrir obligaciones CP.",
                'alto': "Capital ocioso que podria reinvertirse."
            },
            'razon_tesoreria': {
                'optimo': "Capacidad de pago inmediato adecuada.",
                'bajo': "Dependencia de inventarios para cubrir deudas.",
                'alto': "Exceso de activos liquidos."
            },
            'razon_disponibilidad': {
                'optimo': "Efectivo suficiente para operaciones.",
                'bajo': "Podria tener dificultades de caja.",
                'alto': "Acumulacion de efectivo, comun en tech exitosas."
            },
            'ratio_garantia': {
                'optimo': "Solvencia solida ante acreedores.",
                'bajo': "Riesgo de insolvencia.",
                'alto': "Estructura muy conservadora."
            },
            'ratio_autonomia': {
                'optimo': "Equilibrio entre deuda y patrimonio.",
                'bajo': "Alta dependencia de financiacion externa.",
                'alto': "Posible subaprovechamiento del apalancamiento."
            },
            'ratio_calidad_deuda': {
                'optimo': "Estructura de vencimientos equilibrada.",
                'bajo': "Deuda concentrada en largo plazo.",
                'alto': "Presion de pagos a corto plazo."
            },
            'rat': {
                'optimo': f"Rentabilidad economica saludable ({valor:.1f}%).",
                'bajo': f"Baja eficiencia en uso de activos ({valor:.1f}%).",
                'alto': f"Excelente rentabilidad ({valor:.1f}%), verificar sostenibilidad."
            },
            'rrp': {
                'optimo': f"Retorno atractivo para accionistas ({valor:.1f}%).",
                'bajo': f"Rentabilidad insuficiente ({valor:.1f}%).",
                'alto': f"Rentabilidad excepcional ({valor:.1f}%), tipica de tech exitosa."
            },
            'margen_neto': {
                'optimo': f"Margen saludable ({valor:.1f}%).",
                'bajo': f"Margen ajustado ({valor:.1f}%), revisar eficiencia.",
                'alto': f"Margen excelente ({valor:.1f}%), tipico de SaaS."
            },
            'rotacion_activos': {
                'optimo': f"Uso eficiente de activos ({valor:.2f}x).",
                'bajo': f"Activos subutilizados ({valor:.2f}x).",
                'alto': f"Alta rotacion ({valor:.2f}x), verificar capacidad."
            },
            'apalancamiento': {
                'optimo': "Uso equilibrado del apalancamiento.",
                'bajo': "Estructura conservadora, menor ROE potencial.",
                'alto': "Alto riesgo financiero."
            }
        }
        
        if ratio_key in contextos:
            return contextos[ratio_key].get(estado, f"Estado: {estado}")
        
        return f"Valor: {valor:.2f}, Estado: {estado}"