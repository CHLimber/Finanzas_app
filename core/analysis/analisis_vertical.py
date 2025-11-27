"""
Archivo: core/analysis/analisis_vertical.py
Análisis Vertical del Balance General e interpretación de estructura
"""

class AnalisisVerticalBalance:
    """
    Clase para realizar análisis vertical del balance e interpretar
    la estructura económica y financiera de la empresa.
    """

    def __init__(self, balance_model, year):
        """
        Args:
            balance_model: Instancia de BalanceGeneral
            year: Año a analizar (1 o 2)
        """
        self.balance = balance_model
        self.year = year
        
        # Calcular totales
        self.activo_total = self.balance.get_total_activos(year)
        self.activo_corriente = self.balance.get_total_corriente(year)
        self.activo_no_corriente = self.balance.get_total_no_corriente(year)
        self.pasivo_corriente = self.balance.get_total_pasivo_corriente(year)
        self.pasivo_no_corriente = self.balance.get_total_pasivo_no_corriente(year)
        self.patrimonio = self.balance.get_total_patrimonio(year)
        
        # Calcular porcentajes
        self.calcular_porcentajes()
    
    def calcular_porcentajes(self):
        """Calcula todos los porcentajes respecto al Activo Total"""
        if self.activo_total == 0:
            # Si no hay datos, todos los porcentajes son 0
            self.pct_activo_corriente = 0
            self.pct_activo_no_corriente = 0
            self.pct_pasivo_corriente = 0
            self.pct_pasivo_no_corriente = 0
            self.pct_patrimonio = 0
            self.pct_caja_bancos = 0
            self.pct_clientes = 0
            self.pct_inversiones_cp = 0
            self.pct_existencias = 0
            self.pct_inmuebles = 0
            self.pct_intangibles = 0
            self.pct_proveedores = 0
            self.pct_impuestos = 0
            self.pct_deuda_cp = 0
            self.pct_prestamos_lp = 0
            self.pct_provisiones_lp = 0
            self.pct_capital = 0
            self.pct_reservas = 0
            self.pct_ganancias_acum = 0
            return
        
        # Porcentajes principales
        self.pct_activo_corriente = (self.activo_corriente / self.activo_total) * 100
        self.pct_activo_no_corriente = (self.activo_no_corriente / self.activo_total) * 100
        self.pct_pasivo_corriente = (self.pasivo_corriente / self.activo_total) * 100
        self.pct_pasivo_no_corriente = (self.pasivo_no_corriente / self.activo_total) * 100
        self.pct_patrimonio = (self.patrimonio / self.activo_total) * 100
        
        # Porcentajes detallados del Activo Corriente
        if self.year == 1:
            self.pct_caja_bancos = (self.balance.caja_bancos_y1 / self.activo_total) * 100
            self.pct_clientes = (self.balance.clientes_cobrar_y1 / self.activo_total) * 100
            self.pct_inversiones_cp = (self.balance.inversion_cp_y1 / self.activo_total) * 100
            self.pct_existencias = (self.balance.existencias_y1 / self.activo_total) * 100
            
            # Activo No Corriente (neto)
            inmuebles_neto = self.balance.inmuebles_planta_y1 - self.balance.depreciacion_acum_y1
            intangibles_neto = self.balance.intangibles_y1 - self.balance.depreciacion_intang_y1
            self.pct_inmuebles = (inmuebles_neto / self.activo_total) * 100
            self.pct_intangibles = (intangibles_neto / self.activo_total) * 100
            
            # Pasivo y Patrimonio
            self.pct_proveedores = (self.balance.proveedores_y1 / self.activo_total) * 100
            self.pct_impuestos = (self.balance.impuestos_pagar_y1 / self.activo_total) * 100
            self.pct_deuda_cp = (self.balance.deuda_cp_y1 / self.activo_total) * 100
            self.pct_prestamos_lp = (self.balance.prestamos_lp_y1 / self.activo_total) * 100
            self.pct_provisiones_lp = (self.balance.provisiones_lp_y1 / self.activo_total) * 100
            self.pct_capital = (self.balance.capital_social_y1 / self.activo_total) * 100
            self.pct_reservas = (self.balance.reservas_legales_y1 / self.activo_total) * 100
            self.pct_ganancias_acum = (self.balance.ganancias_acum_y1 / self.activo_total) * 100
        else:
            self.pct_caja_bancos = (self.balance.caja_bancos_y2 / self.activo_total) * 100
            self.pct_clientes = (self.balance.clientes_cobrar_y2 / self.activo_total) * 100
            self.pct_inversiones_cp = (self.balance.inversion_cp_y2 / self.activo_total) * 100
            self.pct_existencias = (self.balance.existencias_y2 / self.activo_total) * 100
            
            inmuebles_neto = self.balance.inmuebles_planta_y2 - self.balance.depreciacion_acum_y2
            intangibles_neto = self.balance.intangibles_y2 - self.balance.depreciacion_intang_y2
            self.pct_inmuebles = (inmuebles_neto / self.activo_total) * 100
            self.pct_intangibles = (intangibles_neto / self.activo_total) * 100
            
            self.pct_proveedores = (self.balance.proveedores_y2 / self.activo_total) * 100
            self.pct_impuestos = (self.balance.impuestos_pagar_y2 / self.activo_total) * 100
            self.pct_deuda_cp = (self.balance.deuda_cp_y2 / self.activo_total) * 100
            self.pct_prestamos_lp = (self.balance.prestamos_lp_y2 / self.activo_total) * 100
            self.pct_provisiones_lp = (self.balance.provisiones_lp_y2 / self.activo_total) * 100
            self.pct_capital = (self.balance.capital_social_y2 / self.activo_total) * 100
            self.pct_reservas = (self.balance.reservas_legales_y2 / self.activo_total) * 100
            self.pct_ganancias_acum = (self.balance.ganancias_acum_y2 / self.activo_total) * 100
    
    def interpretar_estructura_economica(self):
        """Interpreta la estructura económica (Activos)"""
        texto = []
        
        # Análisis general
        texto.append(f"El Activo Corriente representa el {self.pct_activo_corriente:.2f}%, "
                     f"mientras que el Activo No Corriente representa el {self.pct_activo_no_corriente:.2f}%.")
        
        # Perfil económico basado en AC
        if self.pct_activo_corriente > 60:
            texto.append("La empresa posee una estructura económica muy líquida y orientada al corto plazo, "
                        "lo que le proporciona flexibilidad operativa pero requiere una gestión eficiente del capital de trabajo.")
        elif 40 <= self.pct_activo_corriente <= 60:
            texto.append("La empresa presenta una estructura económica balanceada entre liquidez y activos fijos, "
                        "mostrando un equilibrio entre operaciones corrientes e inversiones a largo plazo.")
        else:
            texto.append("La empresa es intensiva en activos fijos y depende menos del ciclo operativo, "
                        "característica de empresas industriales o con alto componente tecnológico.")
        
        # Composición interna del AC
        if self.pct_caja_bancos > 15:
            texto.append(f"El efectivo ({self.pct_caja_bancos:.2f}%) es significativo, "
                        "indicando buena liquidez pero posible subutilización de recursos.")
        
        if self.pct_clientes > 20:
            texto.append(f"Las cuentas por cobrar ({self.pct_clientes:.2f}%) tienen un peso importante, "
                        "lo que implica dependencia del crédito otorgado a clientes.")
        
        if self.pct_existencias > 25:
            texto.append(f"Los inventarios ({self.pct_existencias:.2f}%) son elevados, "
                        "sugiriendo una política de stocks robusta o posible sobre-inventario.")
        
        # Composición del ANC
        if self.pct_inmuebles > 30:
            texto.append(f"Los activos fijos tangibles ({self.pct_inmuebles:.2f}%) dominan la estructura, "
                        "caracterizando a la empresa como capital-intensiva.")
        
        if self.pct_intangibles > 10:
            texto.append(f"Los intangibles ({self.pct_intangibles:.2f}%) tienen presencia relevante, "
                        "indicando inversión en tecnología o desarrollo de software.")
        
        return " ".join(texto)
    
    def interpretar_estructura_financiera(self):
        """Interpreta la estructura financiera (Pasivo + Patrimonio)"""
        texto = []
        
        total_pasivo = self.pct_pasivo_corriente + self.pct_pasivo_no_corriente
        
        texto.append(f"El financiamiento se divide en {total_pasivo:.2f}% de pasivos y "
                     f"{self.pct_patrimonio:.2f}% de patrimonio.")
        
        # Nivel de endeudamiento
        if total_pasivo > 70:
            texto.append("La empresa está altamente apalancada y depende fuertemente de la deuda, "
                        "lo que incrementa el riesgo financiero pero puede potenciar la rentabilidad.")
        elif 50 <= total_pasivo <= 70:
            texto.append("La empresa mantiene un apalancamiento medio, "
                        "equilibrando entre el uso de deuda y recursos propios.")
        else:
            texto.append("La empresa posee bajo nivel de endeudamiento y alta solidez patrimonial, "
                        "reflejando una estructura financiera conservadora.")
        
        # Análisis del Pasivo Corriente
        ratio_pc_sobre_pasivo = (self.pct_pasivo_corriente / total_pasivo * 100) if total_pasivo > 0 else 0
        
        if self.pct_pasivo_corriente > 30:
            texto.append(f"Existe presión de liquidez debido al alto peso del pasivo corriente ({self.pct_pasivo_corriente:.2f}%), "
                        "requiriendo una gestión cuidadosa del flujo de caja.")
        elif self.pct_pasivo_no_corriente > self.pct_pasivo_corriente:
            texto.append("La estructura de deuda se concentra más en el largo plazo, "
                        "lo cual reduce la presión inmediata de pago y mejora la estabilidad financiera.")
        
        # Capitalización
        if self.pct_patrimonio > 50:
            texto.append(f"Con un {self.pct_patrimonio:.2f}% de patrimonio, "
                        "la empresa muestra sólida capitalización y capacidad de absorber pérdidas.")
        elif self.pct_patrimonio < 30:
            texto.append(f"El patrimonio ({self.pct_patrimonio:.2f}%) es relativamente bajo, "
                        "indicando alta dependencia de financiación externa.")
        
        return " ".join(texto)
    
    def resumen_completo(self):
        """Retorna el resumen completo de ambas estructuras"""
        return {
            "estructura_economica": self.interpretar_estructura_economica(),
            "estructura_financiera": self.interpretar_estructura_financiera()
        }
    
    def get_tabla_analisis_vertical(self):
        """Retorna los datos para la tabla de análisis vertical"""
        return {
            "ACTIVO": {
                "Activo Corriente": {
                    "valor": self.activo_corriente,
                    "porcentaje": self.pct_activo_corriente,
                    "detalle": {
                        "Caja y Bancos": (getattr(self.balance, f'caja_bancos_y{self.year}'), self.pct_caja_bancos),
                        "Clientes por Cobrar": (getattr(self.balance, f'clientes_cobrar_y{self.year}'), self.pct_clientes),
                        "Inversiones CP": (getattr(self.balance, f'inversion_cp_y{self.year}'), self.pct_inversiones_cp),
                        "Existencias": (getattr(self.balance, f'existencias_y{self.year}'), self.pct_existencias)
                    }
                },
                "Activo No Corriente": {
                    "valor": self.activo_no_corriente,
                    "porcentaje": self.pct_activo_no_corriente,
                    "detalle": {
                        "Inmuebles, Planta y Equipo (neto)": (self.activo_no_corriente - (getattr(self.balance, f'intangibles_y{self.year}') - getattr(self.balance, f'depreciacion_intang_y{self.year}')), self.pct_inmuebles),
                        "Intangibles (neto)": (getattr(self.balance, f'intangibles_y{self.year}') - getattr(self.balance, f'depreciacion_intang_y{self.year}'), self.pct_intangibles)
                    }
                },
                "TOTAL ACTIVO": {
                    "valor": self.activo_total,
                    "porcentaje": 100.0
                }
            },
            "PASIVO Y PATRIMONIO": {
                "Pasivo Corriente": {
                    "valor": self.pasivo_corriente,
                    "porcentaje": self.pct_pasivo_corriente
                },
                "Pasivo No Corriente": {
                    "valor": self.pasivo_no_corriente,
                    "porcentaje": self.pct_pasivo_no_corriente
                },
                "Patrimonio": {
                    "valor": self.patrimonio,
                    "porcentaje": self.pct_patrimonio
                },
                "TOTAL PASIVO + PATRIMONIO": {
                    "valor": self.pasivo_corriente + self.pasivo_no_corriente + self.patrimonio,
                    "porcentaje": 100.0
                }
            }
        }