"""
Archivo: gui/windows/graficos.py
Ventana de Gráficos Financieros
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
from config import Colors, Fonts, Dimensions

# Importar funciones de gráficos
from graphics.graficas import grafico_analisis_financiero, grafico_analisis_economico


class GraficosWindow(ttk.Frame):
    """Ventana de Gráficos Financieros"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Guardar configuración original de matplotlib
        self.original_rcParams = mpl.rcParams.copy()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de gráficos"""
        # Notebook para los dos gráficos
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Análisis Financiero (Liquidez y Solvencia)
        self._crear_tab_analisis_financiero()
        
        # Tab 2: Análisis Económico (Rentabilidad)
        self._crear_tab_analisis_economico()
    
    def _crear_tab_analisis_financiero(self):
        """Crea la pestaña de Análisis Financiero"""
        # Frame para el gráfico
        tab_financiero = ttk.Frame(self.notebook)
        self.notebook.add(tab_financiero, text="Análisis Financiero - Liquidez y Solvencia")
        
        # Canvas con scrollbar
        canvas = tk.Canvas(tab_financiero, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(tab_financiero, orient="vertical", command=canvas.yview)
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
            text="GRÁFICOS DE ANÁLISIS FINANCIERO",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Preparar datos para el gráfico
        datos_año1 = self._preparar_datos_financieros(1)
        datos_año2 = self._preparar_datos_financieros(2)
        
        # Generar gráfico
        try:
            fig = grafico_analisis_financiero(datos_año1, datos_año2, "Año 1", "Año 2")
            
            # Integrar gráfico en tkinter
            canvas_grafico = FigureCanvasTkAgg(fig, master=scrollable_frame)
            canvas_grafico.draw()
            canvas_grafico.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Restaurar configuración de matplotlib
            mpl.rcParams.update(self.original_rcParams)
            
        except Exception as e:
            error_label = tk.Label(
                scrollable_frame,
                text=f"Error al generar gráfico: {str(e)}",
                font=Fonts.NORMAL,
                bg=Colors.BG_PRIMARY,
                fg=Colors.DANGER
            )
            error_label.pack(pady=20)
        
        # Descripción
        descripcion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Descripción del Gráfico ",
            padding=Dimensions.PADDING_LARGE
        )
        descripcion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        descripcion_text = tk.Text(
            descripcion_frame,
            height=6,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        descripcion_text.pack(fill=tk.X)
        descripcion_text.insert('1.0',
            'RATIOS DE LIQUIDEZ:\n'
            '• Liquidez General: Capacidad de pagar deudas de corto plazo con activos corrientes\n'
            '• Razón de Tesorería: Capacidad de pago inmediato con activos más líquidos\n'
            '• Razón de Disponibilidad: Efectivo disponible para cubrir pasivos corrientes\n\n'
            'RATIOS DE SOLVENCIA:\n'
            '• Ratio de Garantía: Respaldo total de activos frente a pasivos\n'
            '• Ratio de Autonomía: Independencia financiera (Patrimonio vs Pasivo)\n'
            '• Calidad de Deuda: Proporción de deuda de corto plazo en el total de pasivos'
        )
        descripcion_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_tab_analisis_economico(self):
        """Crea la pestaña de Análisis Económico"""
        # Frame para el gráfico
        tab_economico = ttk.Frame(self.notebook)
        self.notebook.add(tab_economico, text="Análisis Económico - Rentabilidad")
        
        # Canvas con scrollbar
        canvas = tk.Canvas(tab_economico, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(tab_economico, orient="vertical", command=canvas.yview)
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
            text="GRÁFICOS DE ANÁLISIS ECONÓMICO",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Preparar datos para el gráfico
        datos_año1 = self._preparar_datos_economicos(1)
        datos_año2 = self._preparar_datos_economicos(2)
        
        # Generar gráfico
        try:
            fig = grafico_analisis_economico(datos_año1, datos_año2, "Año 1", "Año 2")
            
            # Integrar gráfico en tkinter
            canvas_grafico = FigureCanvasTkAgg(fig, master=scrollable_frame)
            canvas_grafico.draw()
            canvas_grafico.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
            
            # Restaurar configuración de matplotlib
            mpl.rcParams.update(self.original_rcParams)
            
        except Exception as e:
            error_label = tk.Label(
                scrollable_frame,
                text=f"Error al generar gráfico: {str(e)}",
                font=Fonts.NORMAL,
                bg=Colors.BG_PRIMARY,
                fg=Colors.DANGER
            )
            error_label.pack(pady=20)
        
        # Descripción
        descripcion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Descripción del Gráfico ",
            padding=Dimensions.PADDING_LARGE
        )
        descripcion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                              pady=Dimensions.PADDING_MEDIUM)
        
        descripcion_text = tk.Text(
            descripcion_frame,
            height=8,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        descripcion_text.pack(fill=tk.X)
        descripcion_text.insert('1.0',
            'RENTABILIDAD ECONÓMICA Y FINANCIERA:\n'
            '• ROA (RAT): Rentabilidad del Activo Total - Eficiencia en uso de activos\n'
            '• ROE (RRP): Rentabilidad del Patrimonio - Retorno para accionistas\n\n'
            'ANÁLISIS DUPONT:\n'
            '• Rotación del Activo: Veces que el activo genera ventas\n'
            '• Apalancamiento Financiero: Activo Total / Patrimonio Neto\n\n'
            'MÁRGENES DE GANANCIA:\n'
            '• Margen Bruto: Ganancia sobre costos directos\n'
            '• Margen Operativo: Ganancia después de gastos operativos\n'
            '• Margen Neto: Ganancia final después de todos los gastos'
        )
        descripcion_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _preparar_datos_financieros(self, year):
        """
        Prepara los datos financieros para el gráfico
        
        Args:
            year: 1 o 2
            
        Returns:
            dict: Datos formateados para grafico_analisis_financiero
        """
        # Calcular ratios de liquidez
        ac = self.app.balance_data.get_total_corriente(year)
        pc = self.app.balance_data.get_total_pasivo_corriente(year)
        
        liquidez_general = (ac / pc) if pc != 0 else 0
        
        # Razón de Tesorería
        if year == 1:
            disponible = self.app.balance_data.caja_bancos_y1
            cxc = self.app.balance_data.clientes_cobrar_y1
        else:
            disponible = self.app.balance_data.caja_bancos_y2
            cxc = self.app.balance_data.clientes_cobrar_y2
        
        tesoreria = ((disponible + cxc) / pc) if pc != 0 else 0
        
        # Razón de Disponibilidad
        disponibilidad = (disponible / pc) if pc != 0 else 0
        
        # Ratios de Solvencia
        activo_total = self.app.balance_data.get_total_activos(year)
        pasivo_total = (self.app.balance_data.get_total_pasivo_corriente(year) + 
                       self.app.balance_data.get_total_pasivo_no_corriente(year))
        patrimonio = self.app.balance_data.get_total_patrimonio(year)
        
        garantia = (activo_total / pasivo_total) if pasivo_total != 0 else 0
        autonomia = (patrimonio / pasivo_total) if pasivo_total != 0 else 0
        calidad_deuda = (pc / pasivo_total) if pasivo_total != 0 else 0
        
        return {
            'liquidez_general': liquidez_general,
            'tesoreria': tesoreria,
            'disponibilidad': disponibilidad,
            'garantia': garantia,
            'autonomia': autonomia,
            'calidad_deuda': calidad_deuda
        }
    
    def _preparar_datos_economicos(self, year):
        """
        Prepara los datos económicos para el gráfico
        
        Args:
            year: 1 o 2
            
        Returns:
            dict: Datos formateados para grafico_analisis_economico
        """
        # ROA (RAT)
        baii = self.app.income_data.get_utilidad_operativa(year)
        activo_total = self.app.balance_data.get_total_activos(year)
        roa = (baii / activo_total * 100) if activo_total != 0 else 0
        
        # ROE (RRP)
        utilidad_neta = self.app.income_data.get_utilidad_neta(year)
        patrimonio = self.app.balance_data.get_total_patrimonio(year)
        roe = (utilidad_neta / patrimonio * 100) if patrimonio != 0 else 0
        
        # Margen Neto
        ventas = self.app.income_data.ingresos_servicios_y1 if year == 1 else self.app.income_data.ingresos_servicios_y2
        margen_neto = (utilidad_neta / ventas * 100) if ventas != 0 else 0
        
        # Rotación del Activo
        rotacion_activo = (ventas / activo_total) if activo_total != 0 else 0
        
        # Apalancamiento
        apalancamiento = (activo_total / patrimonio) if patrimonio != 0 else 0
        
        # Margen Bruto
        ganancia_bruta = self.app.income_data.get_ganancia_bruta(year)
        margen_bruto = (ganancia_bruta / ventas * 100) if ventas != 0 else 0
        
        # Margen Operativo
        margen_operativo = (baii / ventas * 100) if ventas != 0 else 0
        
        return {
            'roa': roa,
            'roe': roe,
            'margen_neto': margen_neto,
            'rotacion_activo': rotacion_activo,
            'apalancamiento': apalancamiento,
            'margen_bruto': margen_bruto,
            'margen_operativo': margen_operativo
        }