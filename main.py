"""
Archivo: main.py
Punto de entrada con sistema de actualización automática
"""

from gui.main_window import MainWindow


class FinancialAnalysisApp:
    """Aplicación principal de análisis financiero"""
    
    def __init__(self):
        # Modelos de datos compartidos
        self.balance_data = None
        self.income_data = None
        self.ratios_data = {}
        self.analisis_iniciado = False
        
        # Sistema de callbacks para notificar cambios de datos
        self.on_data_change_callbacks = []

        
    def start(self):
        """Inicia la aplicación con la ventana principal"""
        MainWindow(self)
    
    def notify_data_change(self):
        """
        Notifica a todas las pestañas registradas que los datos han cambiado.
        Esto permite la actualización automática de análisis.
        """
        for callback in self.on_data_change_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error al ejecutar callback de actualización: {e}")


if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.start()