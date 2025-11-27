"""
Archivo: core/analysis/analisis_horizontal.py
Análisis Horizontal del Balance General (comparación entre años)
"""

class AnalisisHorizontalBalance:
    """
    Analiza la evolución del Balance entre dos años.
    Responde: ¿Qué activos crecieron más? ¿Cómo se financió el crecimiento?
    """
    
    def __init__(self, balance_model):
        """
        Args:
            balance_model: Instancia de BalanceGeneral con datos de ambos años
        """
        self.balance = balance_model
        
        # Obtener totales de ambos años
        self.calcular_variaciones()
    
    def calcular_variaciones(self):
        """Calcula todas las variaciones entre año 1 y año 2"""
        
        # ACTIVOS
        self.caja_y1 = self.balance.caja_bancos_y1
        self.caja_y2 = self.balance.caja_bancos_y2
        self.var_caja = self.caja_y2 - self.caja_y1
        self.var_caja_pct = (self.var_caja / self.caja_y1 * 100) if self.caja_y1 != 0 else 0
        
        self.clientes_y1 = self.balance.clientes_cobrar_y1
        self.clientes_y2 = self.balance.clientes_cobrar_y2
        self.var_clientes = self.clientes_y2 - self.clientes_y1
        self.var_clientes_pct = (self.var_clientes / self.clientes_y1 * 100) if self.clientes_y1 != 0 else 0
        
        self.inversiones_y1 = self.balance.inversion_cp_y1
        self.inversiones_y2 = self.balance.inversion_cp_y2
        self.var_inversiones = self.inversiones_y2 - self.inversiones_y1
        self.var_inversiones_pct = (self.var_inversiones / self.inversiones_y1 * 100) if self.inversiones_y1 != 0 else 0
        
        self.existencias_y1 = self.balance.existencias_y1
        self.existencias_y2 = self.balance.existencias_y2
        self.var_existencias = self.existencias_y2 - self.existencias_y1
        self.var_existencias_pct = (self.var_existencias / self.existencias_y1 * 100) if self.existencias_y1 != 0 else 0
        
        self.ac_y1 = self.balance.get_total_corriente(1)
        self.ac_y2 = self.balance.get_total_corriente(2)
        self.var_ac = self.ac_y2 - self.ac_y1
        self.var_ac_pct = (self.var_ac / self.ac_y1 * 100) if self.ac_y1 != 0 else 0
        
        # Activo No Corriente (neto)
        self.ppe_y1 = self.balance.inmuebles_planta_y1 - self.balance.depreciacion_acum_y1
        self.ppe_y2 = self.balance.inmuebles_planta_y2 - self.balance.depreciacion_acum_y2
        self.var_ppe = self.ppe_y2 - self.ppe_y1
        self.var_ppe_pct = (self.var_ppe / self.ppe_y1 * 100) if self.ppe_y1 != 0 else 0
        
        self.intangibles_y1 = self.balance.intangibles_y1 - self.balance.depreciacion_intang_y1
        self.intangibles_y2 = self.balance.intangibles_y2 - self.balance.depreciacion_intang_y2
        self.var_intangibles = self.intangibles_y2 - self.intangibles_y1
        self.var_intangibles_pct = (self.var_intangibles / self.intangibles_y1 * 100) if self.intangibles_y1 != 0 else 0
        
        self.anc_y1 = self.balance.get_total_no_corriente(1)
        self.anc_y2 = self.balance.get_total_no_corriente(2)
        self.var_anc = self.anc_y2 - self.anc_y1
        self.var_anc_pct = (self.var_anc / self.anc_y1 * 100) if self.anc_y1 != 0 else 0
        
        self.activo_total_y1 = self.balance.get_total_activos(1)
        self.activo_total_y2 = self.balance.get_total_activos(2)
        self.var_activo_total = self.activo_total_y2 - self.activo_total_y1
        self.var_activo_total_pct = (self.var_activo_total / self.activo_total_y1 * 100) if self.activo_total_y1 != 0 else 0
        
        # PASIVOS Y PATRIMONIO
        self.pc_y1 = self.balance.get_total_pasivo_corriente(1)
        self.pc_y2 = self.balance.get_total_pasivo_corriente(2)
        self.var_pc = self.pc_y2 - self.pc_y1
        self.var_pc_pct = (self.var_pc / self.pc_y1 * 100) if self.pc_y1 != 0 else 0
        
        self.pnc_y1 = self.balance.get_total_pasivo_no_corriente(1)
        self.pnc_y2 = self.balance.get_total_pasivo_no_corriente(2)
        self.var_pnc = self.pnc_y2 - self.pnc_y1
        self.var_pnc_pct = (self.var_pnc / self.pnc_y1 * 100) if self.pnc_y1 != 0 else 0
        
        self.pasivo_total_y1 = self.pc_y1 + self.pnc_y1
        self.pasivo_total_y2 = self.pc_y2 + self.pnc_y2
        self.var_pasivo_total = self.pasivo_total_y2 - self.pasivo_total_y1
        self.var_pasivo_total_pct = (self.var_pasivo_total / self.pasivo_total_y1 * 100) if self.pasivo_total_y1 != 0 else 0
        
        self.patrimonio_y1 = self.balance.get_total_patrimonio(1)
        self.patrimonio_y2 = self.balance.get_total_patrimonio(2)
        self.var_patrimonio = self.patrimonio_y2 - self.patrimonio_y1
        self.var_patrimonio_pct = (self.var_patrimonio / self.patrimonio_y1 * 100) if self.patrimonio_y1 != 0 else 0
    
    def get_activo_mayor_crecimiento_absoluto(self):
        """Identifica el rubro del activo con mayor crecimiento absoluto"""
        variaciones = {
            "Caja y Bancos": self.var_caja,
            "Clientes por Cobrar": self.var_clientes,
            "Inversiones CP": self.var_inversiones,
            "Existencias": self.var_existencias,
            "Inmuebles, Planta y Equipo": self.var_ppe,
            "Intangibles": self.var_intangibles
        }
        
        max_rubro = max(variaciones.items(), key=lambda x: abs(x[1]))
        return {
            "rubro": max_rubro[0],
            "variacion": max_rubro[1],
            "direccion": "aumento" if max_rubro[1] > 0 else "disminución"
        }
    
    def get_activo_mayor_crecimiento_relativo(self):
        """Identifica el rubro con mayor crecimiento porcentual"""
        variaciones_pct = {
            "Caja y Bancos": self.var_caja_pct,
            "Clientes por Cobrar": self.var_clientes_pct,
            "Inversiones CP": self.var_inversiones_pct,
            "Existencias": self.var_existencias_pct,
            "Inmuebles, Planta y Equipo": self.var_ppe_pct,
            "Intangibles": self.var_intangibles_pct
        }
        
        max_rubro = max(variaciones_pct.items(), key=lambda x: abs(x[1]))
        return {
            "rubro": max_rubro[0],
            "porcentaje": max_rubro[1],
            "direccion": "aumento" if max_rubro[1] > 0 else "disminución"
        }
    
    def interpretar_crecimiento_activos(self):
        """Genera interpretación del crecimiento de activos"""
        texto = []
        
        # Variación total
        texto.append(f"El Activo Total {'aumentó' if self.var_activo_total > 0 else 'disminuyó'} "
                    f"en {abs(self.var_activo_total):,.2f} Bs., equivalente al {abs(self.var_activo_total_pct):.2f}%.")
        
        # Mayor crecimiento absoluto
        max_abs = self.get_activo_mayor_crecimiento_absoluto()
        if abs(max_abs['variacion']) > 0:
            texto.append(f"El rubro que más {'creció' if max_abs['variacion'] > 0 else 'decreció'} "
                        f"en términos absolutos fue {max_abs['rubro']}, "
                        f"con un {'incremento' if max_abs['variacion'] > 0 else 'decremento'} "
                        f"de {abs(max_abs['variacion']):,.2f} Bs.")
        
        # Mayor crecimiento relativo
        max_rel = self.get_activo_mayor_crecimiento_relativo()
        if abs(max_rel['porcentaje']) > 0:
            texto.append(f"En términos relativos (%), el crecimiento más significativo fue "
                        f"{max_rel['rubro']}, con un crecimiento de {abs(max_rel['porcentaje']):.2f}%.")
        
        # Interpretación específica
        if self.var_ac > self.var_anc:
            texto.append("Esto indica que la empresa aumentó su liquidez y capacidad operativa "
                        "mediante mayor efectivo, cartera o inventarios.")
        elif self.var_anc > self.var_ac:
            texto.append("Esto indica que la empresa realizó inversiones en activos fijos o intangibles, "
                        "orientándose hacia el crecimiento a largo plazo.")
        
        return " ".join(texto)
    
    def interpretar_financiamiento(self):
        """Analiza cómo se financió el crecimiento del activo"""
        texto = []
        
        # Variaciones de financiamiento
        texto.append(f"El Pasivo Total (corto + largo plazo) "
                    f"{'aumentó' if self.var_pasivo_total > 0 else 'disminuyó'} "
                    f"en {abs(self.var_pasivo_total):,.2f} Bs. ")
        
        texto.append(f"El Patrimonio "
                    f"{'aumentó' if self.var_patrimonio > 0 else 'disminuyó'} "
                    f"en {abs(self.var_patrimonio):,.2f} Bs.")
        
        # Determinar tipo de financiamiento
        if abs(self.var_pasivo_total) > abs(self.var_patrimonio) and self.var_pasivo_total > 0:
            texto.append("El crecimiento del activo fue financiado principalmente con DEUDA. ")
            
            if self.var_pc > self.var_pnc:
                texto.append("En particular, se utilizó deuda de CORTO PLAZO, "
                            "lo cual aumenta la presión de liquidez y el riesgo financiero a corto plazo.")
            else:
                texto.append("En particular, se utilizó deuda de LARGO PLAZO, "
                            "lo cual es más sostenible y reduce la presión inmediata de pago.")
        
        elif abs(self.var_patrimonio) > abs(self.var_pasivo_total) and self.var_patrimonio > 0:
            texto.append("El aumento del activo se financió casi en su totalidad con RECURSOS PROPIOS "
                        "(patrimonio), lo que demuestra que la empresa tuvo reinversión de utilidades "
                        "y/o aportes de socios, sin depender de endeudamiento.")
        
        elif self.var_pasivo_total > 0 and self.var_patrimonio > 0:
            ratio_deuda = abs(self.var_pasivo_total) / (abs(self.var_pasivo_total) + abs(self.var_patrimonio)) * 100
            texto.append(f"El financiamiento fue MIXTO: {ratio_deuda:.1f}% con deuda y "
                        f"{100-ratio_deuda:.1f}% con patrimonio, "
                        "lo que muestra un equilibrio entre recursos externos e internos.")
        
        else:
            texto.append("La empresa no experimentó un crecimiento significativo del activo, "
                        "o bien redujo su tamaño mediante desinversión.")
        
        return " ".join(texto)
    
    def conclusion_general(self):
        """Genera una conclusión sobre la evolución patrimonial"""
        
        if self.var_activo_total > 0:
            # La empresa creció
            if abs(self.var_patrimonio) > abs(self.var_pasivo_total) and self.var_patrimonio > 0:
                return "La empresa creció de forma SALUDABLE con bajo endeudamiento y fortalecimiento patrimonial."
            
            elif self.var_pc > 0 and abs(self.var_pc) > abs(self.var_patrimonio):
                return "La empresa está invirtiendo agresivamente, pero aumentó su dependencia de deuda a corto plazo, lo que incrementa el riesgo de liquidez."
            
            elif self.var_anc > self.var_ac:
                return "La empresa está invirtiendo agresivamente en activos fijos para crecimiento a largo plazo."
            
            else:
                return "La empresa está ampliando su capacidad operativa, pero debe monitorear su estructura de financiamiento."
        
        else:
            # La empresa decreció o se mantuvo
            return "La empresa redujo su tamaño, posiblemente por desinversión, pago de deudas o reparto de dividendos."
    
    def analisis_completo(self):
        """Genera el análisis horizontal completo"""
        return {
            "interpretacion_activos": self.interpretar_crecimiento_activos(),
            "interpretacion_financiamiento": self.interpretar_financiamiento(),
            "conclusion": self.conclusion_general()
        }
    
    def get_tabla_variaciones(self):
        """Retorna los datos para la tabla de variaciones"""
        return {
            "activos": [
                ("Caja y Bancos", self.caja_y1, self.caja_y2, self.var_caja, self.var_caja_pct),
                ("Clientes por Cobrar", self.clientes_y1, self.clientes_y2, self.var_clientes, self.var_clientes_pct),
                ("Inversiones CP", self.inversiones_y1, self.inversiones_y2, self.var_inversiones, self.var_inversiones_pct),
                ("Existencias", self.existencias_y1, self.existencias_y2, self.var_existencias, self.var_existencias_pct),
                ("Activo Corriente", self.ac_y1, self.ac_y2, self.var_ac, self.var_ac_pct),
                ("Inmuebles, Planta y Equipo", self.ppe_y1, self.ppe_y2, self.var_ppe, self.var_ppe_pct),
                ("Intangibles", self.intangibles_y1, self.intangibles_y2, self.var_intangibles, self.var_intangibles_pct),
                ("Activo No Corriente", self.anc_y1, self.anc_y2, self.var_anc, self.var_anc_pct),
                ("TOTAL ACTIVO", self.activo_total_y1, self.activo_total_y2, self.var_activo_total, self.var_activo_total_pct),
            ],
            "pasivo_patrimonio": [
                ("Pasivo Corriente", self.pc_y1, self.pc_y2, self.var_pc, self.var_pc_pct),
                ("Pasivo No Corriente", self.pnc_y1, self.pnc_y2, self.var_pnc, self.var_pnc_pct),
                ("TOTAL PASIVO", self.pasivo_total_y1, self.pasivo_total_y2, self.var_pasivo_total, self.var_pasivo_total_pct),
                ("Patrimonio", self.patrimonio_y1, self.patrimonio_y2, self.var_patrimonio, self.var_patrimonio_pct),
            ]
        }