"""
Archivo: gui/main_window.py
Ventana principal con sistema de pestañas y cierre correcto de matplotlib
"""

import tkinter as tk
from tkinter import ttk

from config import Colors, Fonts, Dimensions, Labels, WindowConfig
from core.models.balance import BalanceGeneral
from core.models.estado_resultado import EstadoResultado
from gui.windows.balance_window import BalanceTab
from gui.windows.estado_resultado_window import EstadoResultadoTab
from gui.windows.analisis_patrimonial import AnalisisPatrimonialTab
from gui.windows.analisis_financiero import AnalisisFinancieroTab
from gui.windows.analisis_economico import AnalisisEconomicoTab
from gui.windows.analisis_integral_diagnostico import AnalisisIntegralTab
from gui.windows.graficos import GraficosTab


class MainWindow(tk.Tk):
    """Ventana principal con pestañas y auto-actualización"""
    
    def __init__(self, app):
        super().__init__()
        
        self.app = app
        
        # Inicializar modelos
        if self.app.balance_data is None:
            self.app.balance_data = BalanceGeneral()
        if self.app.income_data is None:
            self.app.income_data = EstadoResultado()
        
        self.title(Labels.APP_TITLE)
        self.geometry(f"{Dimensions.WINDOW_WIDTH}x{Dimensions.WINDOW_HEIGHT}")
        self.configure(bg=Colors.BG_SECONDARY)
        
        # Configurar cierre correcto de la aplicación
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.crear_interfaz()
        WindowConfig.center_window(self)
        
        self.mainloop()
    
    def crear_interfaz(self):
        """Crea la interfaz con pestañas"""
        
        # Frame superior - Título
        header_frame = tk.Frame(
            self, 
            bg=Colors.BG_DARK, 
            height=Dimensions.HEADER_HEIGHT
        )
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=Labels.APP_TITLE,
            font=Fonts.LARGE,
            bg=Colors.BG_DARK,
            fg=Colors.TEXT_WHITE
        )
        title_label.pack(expand=True)
        
        # Notebook principal
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(
            fill=tk.BOTH, 
            expand=True, 
            padx=Dimensions.PADDING_MEDIUM, 
            pady=Dimensions.PADDING_MEDIUM
        )
        
        # Crear todas las pestañas
        self.crear_pestanas()
    
    def crear_pestanas(self):
        """Crea todas las pestañas del sistema"""
        
        # 1. Balance General
        balance_tab = BalanceTab(self.notebook, self.app.balance_data, self.actualizar_analisis)
        self.notebook.add(balance_tab, text=Labels.TAB_BALANCE)
        
        # 2. Estado de Resultados
        estado_tab = EstadoResultadoTab(self.notebook, self.app.income_data, self.actualizar_analisis)
        self.notebook.add(estado_tab, text=Labels.TAB_ESTADO)
        
        # 3. Análisis Patrimonial
        patrimonial_tab = AnalisisPatrimonialTab(self.notebook, self.app)
        self.notebook.add(patrimonial_tab, text=Labels.TAB_PATRIMONIAL)
        
        # 4. Análisis Financiero
        financiero_tab = AnalisisFinancieroTab(self.notebook, self.app)
        self.notebook.add(financiero_tab, text=Labels.TAB_FINANCIERO)
        
        # 5. Análisis Económico
        economico_tab = AnalisisEconomicoTab(self.notebook, self.app)
        self.notebook.add(economico_tab, text=Labels.TAB_ECONOMICO)
        
        # 6. Análisis Integral
        integral_tab = AnalisisIntegralTab(self.notebook, self.app)
        self.notebook.add(integral_tab, text=Labels.TAB_INTEGRAL)
        
        # 7. Gráficos
        graficos_tab = GraficosTab(self.notebook, self.app)
        self.notebook.add(graficos_tab, text=Labels.TAB_GRAFICOS)
    
    def actualizar_analisis(self):
        """
        Callback que se ejecuta cuando cambian los datos en Balance o Estado de Resultados.
        Notifica a todas las pestañas de análisis para que se actualicen.
        """
        if hasattr(self.app, 'notify_data_change'):
            self.app.notify_data_change()
    
    def on_closing(self):
        """
        Maneja el cierre correcto de la aplicación.
        Cierra todas las figuras de matplotlib antes de cerrar la ventana.
        """
        try:
            import matplotlib.pyplot as plt
            plt.close('all')  # Cerrar todas las figuras abiertas
        except Exception as e:
            print(f"Error al cerrar figuras de matplotlib: {e}")
        
        try:
            self.quit()      # Detener el mainloop de tkinter
            self.destroy()   # Destruir la ventana
        except Exception as e:
            print(f"Error al cerrar la ventana: {e}")