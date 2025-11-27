import tkinter as tk
from gui.main_window import MainWindow

class FinancialAnalysisApp:
    """Aplicación principal de análisis financiero"""
    
    def __init__(self):
        # Modelos de datos compartidos
        self.balance_data = None
        self.income_data = None
        self.ratios_data = {}
        self.analisis_iniciado = False
        
    def start(self):
        """Inicia la aplicación con la ventana principal"""
        MainWindow(self)


if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.start()