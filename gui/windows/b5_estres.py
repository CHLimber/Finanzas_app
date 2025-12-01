"""
Archivo: gui/windows/b5_estres.py
Pestaña B5 - Estrés Financiero (Escenario Pesimista)
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.estres_financiero import EstresFinanciero


class B5EstresTab(ttk.Frame):
    """Pestaña B5 - Análisis de Estrés Financiero"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de B5"""
        
        canvas = tk.Canvas(self, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colors.BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo = tk.Label(
            scrollable_frame,
            text="B.5 ESTRÉS FINANCIERO - ESCENARIO PESIMISTA",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Subtítulo
        subtitulo = tk.Label(
            scrollable_frame,
            text="Simulación: Caída del 30% en Ingresos",
            font=Fonts.HEADER,
            bg=Colors.WARNING,
            fg="white",
            pady=8
        )
        subtitulo.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, pady=5)
        
        # Obtener datos del año 2
        income_data = self.app.income_data
        ingreso_servicios_y2 = income_data.ingresos_servicios_y2
        utilidad_neta_y2 = income_data.get_utilidad_neta(year=2)
        
        # Crear análisis
        analisis = EstresFinanciero(
            ingreso_actual=ingreso_servicios_y2,
            utilidad_neta_actual=utilidad_neta_y2,
            proporcion_gastos_fijos=0.40,
            proporcion_gastos_variables=0.60
        )
        
        # Aplicar escenario pesimista
        escenario = analisis.aplicar_escenario_pesimista(caida_ingresos=0.30)
    
        # Sección 1: Datos Base (Año 2)
        self._crear_datos_base(scrollable_frame, analisis)
        
        # Sección 2: Estructura de Costos
        self._crear_estructura_costos(scrollable_frame, analisis)
        
        # Sección 3: Escenario Pesimista
        self._crear_escenario_pesimista(scrollable_frame, analisis, escenario)
        
        # Sección 4: Punto de Equilibrio
        self._crear_punto_equilibrio(scrollable_frame, analisis)
        
        # Sección 5: Conclusión
        self._crear_conclusion(scrollable_frame, analisis, escenario)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def _crear_datos_base(self, parent, analisis):
        """Crea sección de datos base"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" 📊 Datos Base - Año 2 (Situación Actual) ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        metricas = analisis.resumen_metricas()
        
        datos = [
            ("Ingresos por Servicios", metricas['ingreso_actual'], Colors.INFO),
            ("Utilidad Neta", metricas['utilidad_neta_actual'], Colors.POSITIVE),
            ("Gastos Totales", metricas['gasto_total'], Colors.NEUTRAL)
        ]
        
        for nombre, valor, color in datos:
            fila = tk.Frame(frame, bg=Colors.BG_PRIMARY)
            fila.pack(fill=tk.X, pady=5)
            
            tk.Label(
                fila,
                text=nombre,
                font=Fonts.NORMAL_BOLD,
                bg=Colors.BG_PRIMARY,
                anchor="w",
                width=30
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                fila,
                text=NumberFormat.format(valor),
                font=Fonts.NORMAL_BOLD,
                bg=color,
                fg="white",
                padx=20,
                pady=5,
                relief="raised"
            ).pack(side=tk.RIGHT, padx=5)
    
    def _crear_estructura_costos(self, parent, analisis):
        """Crea sección de estructura de costos"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" 🔧 Estructura de Costos (Año 2) ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        metricas = analisis.resumen_metricas()
        
        # Gastos Fijos
        fila_fijos = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        fila_fijos.pack(fill=tk.X, pady=3)
        
        tk.Label(
            fila_fijos,
            text="Gastos Fijos (40%)",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            anchor="w",
            width=30
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            fila_fijos,
            text=NumberFormat.format(metricas['gasto_fijo']),
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            padx=15,
            pady=3
        ).pack(side=tk.RIGHT, padx=5)
        
        # Gastos Variables
        fila_variables = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        fila_variables.pack(fill=tk.X, pady=3)
        
        tk.Label(
            fila_variables,
            text="Gastos Variables (60%)",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            anchor="w",
            width=30
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            fila_variables,
            text=NumberFormat.format(metricas['gasto_variable']),
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            padx=15,
            pady=3
        ).pack(side=tk.RIGHT, padx=5)
        
        # Separador
        ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=10)
        
        # Margen de Contribución
        fila_margen = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        fila_margen.pack(fill=tk.X, pady=5)
        
        tk.Label(
            fila_margen,
            text="Margen de Contribución",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY,
            anchor="w",
            width=30
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            fila_margen,
            text=f"{metricas['margen_contribucion_pct']:.1f}%",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.INFO,
            fg="white",
            padx=20,
            pady=5,
            relief="raised"
        ).pack(side=tk.RIGHT, padx=5)
    
    def _crear_escenario_pesimista(self, parent, analisis, escenario):
        """Crea sección de escenario pesimista"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" ⚠️ Escenario Pesimista: -30% Ingresos ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Tabla comparativa
        datos = [
            ("Ingresos por Servicios", analisis.ingreso_actual, escenario['nuevo_ingreso']),
            ("Gastos Fijos", analisis.gasto_fijo, escenario['nuevo_gasto_fijo']),
            ("Gastos Variables", analisis.gasto_variable_total, escenario['nuevo_gasto_variable']),
            ("Gastos Totales", analisis.gasto_total, escenario['nuevo_gasto_total']),
            ("", None, None),  # Separador
            ("UTILIDAD NETA", analisis.utilidad_neta_actual, escenario['nueva_utilidad'])
        ]
        
        # Headers
        header_frame = tk.Frame(frame, bg=Colors.BG_SECONDARY)
        header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            header_frame,
            text="Concepto",
            font=Fonts.HEADER,
            bg=Colors.BG_SECONDARY,
            width=25,
            anchor="w"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            header_frame,
            text="Actual (Año 2)",
            font=Fonts.HEADER,
            bg=Colors.BG_SECONDARY,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            header_frame,
            text="Escenario -30%",
            font=Fonts.HEADER,
            bg=Colors.BG_SECONDARY,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            header_frame,
            text="Variación",
            font=Fonts.HEADER,
            bg=Colors.BG_SECONDARY,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Filas de datos
        for nombre, valor_actual, valor_nuevo in datos:
            if valor_actual is None:  # Separador
                ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=5)
                continue
            
            fila = tk.Frame(frame, bg=Colors.BG_PRIMARY)
            fila.pack(fill=tk.X, pady=2)
            
            es_total = nombre.isupper()
            font = Fonts.NORMAL_BOLD if es_total else Fonts.NORMAL
            
            # Concepto
            tk.Label(
                fila,
                text=nombre,
                font=font,
                bg=Colors.BG_PRIMARY,
                width=25,
                anchor="w"
            ).pack(side=tk.LEFT, padx=5)
            
            # Valor actual
            tk.Label(
                fila,
                text=NumberFormat.format(valor_actual),
                font=font,
                bg=Colors.BG_PRIMARY,
                width=15
            ).pack(side=tk.LEFT, padx=5)
            
            # Valor nuevo
            color_nuevo = Colors.BG_PRIMARY
            if es_total:
                color_nuevo = Colors.POSITIVE if valor_nuevo > 0 else Colors.DANGER
            
            tk.Label(
                fila,
                text=NumberFormat.format(valor_nuevo),
                font=font,
                fg="white" if es_total else "black",
                bg=color_nuevo,
                width=15
            ).pack(side=tk.LEFT, padx=5)
            
            # Variación
            if valor_actual != 0:
                variacion_pct = ((valor_nuevo - valor_actual) / abs(valor_actual)) * 100
            else:
                variacion_pct = 0
            
            tk.Label(
                fila,
                text=f"{variacion_pct:+.1f}%",
                font=font,
                fg=Colors.NEGATIVE if variacion_pct < 0 else Colors.POSITIVE,
                bg=Colors.BG_PRIMARY,
                width=12
            ).pack(side=tk.LEFT, padx=5)
        
        # Interpretación
        interp_frame = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        interp_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            interp_frame,
            text="📝 Interpretación:",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY,
            anchor="w"
        ).pack(anchor='w', pady=5)
        
        interpretacion = analisis.interpretar_nueva_utilidad(escenario['nueva_utilidad'])
        
        text_widget = tk.Text(
            interp_frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.X)
        text_widget.insert('1.0', interpretacion)
        text_widget.config(state='disabled')
    
    def _crear_punto_equilibrio(self, parent, analisis):
        """Crea sección de punto de equilibrio"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" 🎯 Punto de Equilibrio (Break-Even Point) ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        evaluacion = analisis.evaluar_punto_equilibrio()
        
        # Valor del punto de equilibrio
        fila_valor = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        fila_valor.pack(fill=tk.X, pady=5)
        
        tk.Label(
            fila_valor,
            text="Punto de Equilibrio (ingresos mínimos):",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY,
            anchor="w"
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            fila_valor,
            text=NumberFormat.format(analisis.punto_equilibrio),
            font=Fonts.LARGE,
            bg=Colors.INFO,
            fg="white",
            padx=20,
            pady=10,
            relief="raised"
        ).pack(side=tk.RIGHT, padx=5)
        
        # Porcentaje respecto a ingresos actuales
        fila_pct = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        fila_pct.pack(fill=tk.X, pady=5)
        
        tk.Label(
            fila_pct,
            text="Respecto a ingresos actuales:",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            anchor="w"
        ).pack(side=tk.LEFT, padx=5)
        
        nivel_colors = {
            'ÓPTIMO': Colors.SUCCESS,
            'ACEPTABLE': Colors.INFO,
            'RIESGOSO': Colors.WARNING,
            'CRÍTICO': Colors.DANGER
        }
        
        tk.Label(
            fila_pct,
            text=f"{evaluacion['porcentaje']:.1f}% - {evaluacion['estado']}",
            font=Fonts.NORMAL_BOLD,
            bg=nivel_colors.get(evaluacion['nivel'], Colors.NEUTRAL),
            fg="white",
            padx=15,
            pady=8,
            relief="raised"
        ).pack(side=tk.RIGHT, padx=5)
        
        # Interpretación
        ttk.Separator(frame, orient="horizontal").pack(fill=tk.X, pady=10)
        
        tk.Label(
            frame,
            text="📝 Evaluación:",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY,
            anchor="w"
        ).pack(anchor='w', pady=5)
        
        text_widget = tk.Text(
            frame,
            height=4,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.X)
        text_widget.insert('1.0', evaluacion['descripcion'])
        text_widget.config(state='disabled')
    
    def _crear_conclusion(self, parent, analisis, escenario):
        """Crea conclusión general"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" ✅ Conclusión del Análisis de Estrés ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        evaluacion_pe = analisis.evaluar_punto_equilibrio()
        
        # Generar conclusión
        if escenario['nueva_utilidad'] > 0 and evaluacion_pe['nivel'] in ['ÓPTIMO', 'ACEPTABLE']:
            conclusion = (
                f"✅ RESILIENCIA ALTA: La empresa demuestra solidez financiera. Incluso con una "
                f"caída del 30% en ingresos, mantiene utilidad positiva de "
                f"{NumberFormat.format(escenario['nueva_utilidad'])}. El punto de equilibrio "
                f"está en {evaluacion_pe['porcentaje']:.1f}% de los ingresos actuales, "
                f"lo que indica excelente margen de seguridad."
            )
            bg_color = Colors.SUCCESS
        elif escenario['nueva_utilidad'] >= 0 and evaluacion_pe['nivel'] == 'RIESGOSO':
            conclusion = (
                f"⚠️ RESILIENCIA MODERADA: La empresa sobrevive al escenario pesimista pero "
                f"con margen ajustado. La utilidad proyectada es "
                f"{NumberFormat.format(escenario['nueva_utilidad'])}. Se recomienda "
                f"reducir costos fijos y aumentar el margen de contribución."
            )
            bg_color = Colors.WARNING
        else:
            conclusion = (
                f"❌ VULNERABILIDAD ALTA: Una caída del 30% en ingresos genera pérdidas de "
                f"{NumberFormat.format(abs(escenario['nueva_utilidad']))}. La estructura "
                f"de costos actual no es sostenible. Se requiere reestructuración urgente."
            )
            bg_color = Colors.DANGER
        
        text_widget = tk.Text(
            frame,
            height=5,
            wrap='word',
            font=Fonts.NORMAL_BOLD,
            bg=bg_color,
            fg="white",
            relief='flat',
            padx=15,
            pady=15
        )
        text_widget.pack(fill=tk.X)
        text_widget.insert('1.0', conclusion)
        text_widget.config(state='disabled')