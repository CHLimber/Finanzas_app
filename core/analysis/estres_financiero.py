"""
Archivo: core/analysis/estres_financiero.py
Análisis de estrés financiero y punto de equilibrio
"""

class EstresFinanciero:
    """
    Analiza el impacto de una caída en ingresos y calcula el punto de equilibrio.
    Útil para evaluar la resiliencia financiera ante escenarios adversos.
    """
    
    def __init__(self, ingreso_actual, utilidad_neta_actual, 
                 proporcion_gastos_fijos=0.40, proporcion_gastos_variables=0.60):
        """
        Args:
            ingreso_actual: Ingresos por servicios del año base
            utilidad_neta_actual: Utilidad neta del año base
            proporcion_gastos_fijos: Proporción de gastos fijos (default 40%)
            proporcion_gastos_variables: Proporción de gastos variables (default 60%)
        """
        self.ingreso_actual = ingreso_actual
        self.utilidad_neta_actual = utilidad_neta_actual
        
        # Cálculo de gastos totales
        self.gasto_total = ingreso_actual - utilidad_neta_actual
        
        # Distribución de gastos
        self.gasto_fijo = self.gasto_total * proporcion_gastos_fijos
        self.gasto_variable_total = self.gasto_total * proporcion_gastos_variables
        
        # Margen de contribución
        if ingreso_actual > 0:
            self.margen_contribucion = 1 - (self.gasto_variable_total / ingreso_actual)
        else:
            self.margen_contribucion = 0
        
        # Punto de equilibrio
        if self.margen_contribucion > 0:
            self.punto_equilibrio = self.gasto_fijo / self.margen_contribucion
        else:
            self.punto_equilibrio = float('inf')
    
    def aplicar_escenario_pesimista(self, caida_ingresos=0.30):
        """
        Aplica un escenario de caída en ingresos.
        
        Args:
            caida_ingresos: Porcentaje de caída (0.30 = 30%)
        
        Returns:
            dict con resultados del escenario
        """
        # Nuevo ingreso (caída del X%)
        nuevo_ingreso = self.ingreso_actual * (1 - caida_ingresos)
        
        # Gastos variables se reducen proporcionalmente
        nuevo_gasto_variable = self.gasto_variable_total * (1 - caida_ingresos)
        
        # Gastos fijos se mantienen
        nuevo_gasto_fijo = self.gasto_fijo
        
        # Nuevo gasto total
        nuevo_gasto_total = nuevo_gasto_fijo + nuevo_gasto_variable
        
        # Nueva utilidad neta
        nueva_utilidad = nuevo_ingreso - nuevo_gasto_total
        
        return {
            'nuevo_ingreso': nuevo_ingreso,
            'nuevo_gasto_variable': nuevo_gasto_variable,
            'nuevo_gasto_fijo': nuevo_gasto_fijo,
            'nuevo_gasto_total': nuevo_gasto_total,
            'nueva_utilidad': nueva_utilidad,
            'caida_ingresos_pct': caida_ingresos * 100,
            'impacto_utilidad': self.utilidad_neta_actual - nueva_utilidad
        }
    
    def evaluar_punto_equilibrio(self):
        """
        Evalúa el punto de equilibrio en relación a los ingresos actuales.
        
        Returns:
            dict con estado y descripción
        """
        if self.ingreso_actual == 0:
            return {
                'nivel': 'NO_EVALUABLE',
                'porcentaje': 0,
                'estado': 'Sin ingresos para evaluar',
                'descripcion': 'No se puede evaluar el punto de equilibrio sin ingresos.'  # ✅ AÑADIR
            }
        
        porcentaje_equilibrio = (self.punto_equilibrio / self.ingreso_actual) * 100
        
        if porcentaje_equilibrio < 50:
            return {
                'nivel': 'ÓPTIMO',
                'porcentaje': porcentaje_equilibrio,
                'estado': 'Excelente',
                'descripcion': (
                    'La empresa recupera costos rápidamente y tiene alto margen de contribución. '
                    'Estructura muy saludable, típica de empresas SaaS rentables.'
                )
            }
        elif porcentaje_equilibrio < 70:
            return {
                'nivel': 'ACEPTABLE',
                'porcentaje': porcentaje_equilibrio,
                'estado': 'Saludable',
                'descripcion': (
                    'Aún hay margen de seguridad, pero los costos fijos empiezan a ser importantes. '
                    'Se recomienda monitorear y optimizar gastos fijos.'
                )
            }
        elif porcentaje_equilibrio < 90:
            return {
                'nivel': 'RIESGOSO',
                'porcentaje': porcentaje_equilibrio,
                'estado': 'Riesgoso',
                'descripcion': (
                    'La empresa depende demasiado de mantener ingresos altos. '
                    'Cualquier caída significativa puede generar pérdidas. Se requiere acción correctiva.'
                )
            }
        else:
            return {
                'nivel': 'CRÍTICO',
                'porcentaje': porcentaje_equilibrio,
                'estado': 'Crítico',
                'descripcion': (
                    'Un pequeño descenso de ingresos provoca pérdidas. '
                    'No es viable para un software rentable. Se requiere reestructuración urgente.'
                )
            }
    
    def interpretar_nueva_utilidad(self, nueva_utilidad):
        """
        Interpreta el impacto en la utilidad neta bajo el escenario pesimista.
        
        Args:
            nueva_utilidad: Utilidad neta proyectada
        
        Returns:
            str con interpretación
        """
        if nueva_utilidad > 0:
            reduccion_pct = ((self.utilidad_neta_actual - nueva_utilidad) / self.utilidad_neta_actual) * 100
            return (
                f"A pesar de la caída del 30% en ingresos, la empresa mantiene utilidad positiva "
                f"de ${nueva_utilidad:,.0f}, aunque reducida en {reduccion_pct:.1f}%. "
                f"Esto demuestra cierta resiliencia en la estructura de costos."
            )
        elif nueva_utilidad == 0:
            return (
                "La caída del 30% en ingresos lleva a la empresa al punto de equilibrio. "
                "No hay utilidades pero tampoco pérdidas. La situación es delicada y requiere "
                "atención inmediata."
            )
        else:
            return (
                f"La caída del 30% en ingresos genera pérdidas de ${abs(nueva_utilidad):,.0f}. "
                f"Esto indica alta vulnerabilidad financiera. Se requieren medidas urgentes "
                f"para reducir costos fijos o aumentar márgenes."
            )
    
    def resumen_metricas(self):
        """
        Retorna un resumen de todas las métricas clave.
        """
        return {
            'ingreso_actual': self.ingreso_actual,
            'utilidad_neta_actual': self.utilidad_neta_actual,
            'gasto_total': self.gasto_total,
            'gasto_fijo': self.gasto_fijo,
            'gasto_variable': self.gasto_variable_total,
            'margen_contribucion': self.margen_contribucion,
            'margen_contribucion_pct': self.margen_contribucion * 100,
            'punto_equilibrio': self.punto_equilibrio
        }