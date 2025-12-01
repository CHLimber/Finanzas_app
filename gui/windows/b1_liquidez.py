"""
Archivo: gui/windows/b1_liquidez.py
Pestaña B1 - Ratios de Liquidez
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions


class B1LiquidezTab(ttk.Frame):
    """Pestaña B1 - Ratios de Liquidez"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de B1"""
        
        # Canvas con scroll
        canvas = tk.Canvas(self, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        ttk.Label(
            scrollable_frame,
            text="B.1 RATIOS DE LIQUIDEZ",
            font=Fonts.TITLE,
            foreground=Colors.PRIMARY
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        # Descripción breve
        desc = "Miden la capacidad de la empresa para cumplir obligaciones de corto plazo."
        ttk.Label(
            scrollable_frame,
            text=desc,
            font=Fonts.NORMAL,
            foreground=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 15))
        
        # Calcular ratios
        from core.calculators.ratio_calculator import RatioCalculator
        from core.analysis.financial_interpreter import FinancialInterpreter
        
        calculator = RatioCalculator(self.app.balance_data, self.app.income_data)
        interpreter = FinancialInterpreter()
        
        # Ratios
        ratios_info = [
            ("Razón de Liquidez General", "razon_liquidez"),
            ("Razón de Tesorería", "razon_tesoreria"),
            ("Razón de Disponibilidad", "razon_disponibilidad")
        ]
        
        # Crear análisis para cada ratio
        for nombre, key in ratios_info:
            self._crear_analisis_ratio(
                scrollable_frame,
                nombre,
                key,
                calculator,
                interpreter
            )
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_analisis_ratio(self, parent, nombre, key, calculator, interpreter):
        """Crea el análisis de un ratio con diseño lado a lado"""
        
        # Frame principal del ratio
        ratio_frame = ttk.LabelFrame(
            parent,
            text=f" {nombre} ",
            padding=15
        )
        ratio_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Calcular valores
        valor_y1 = getattr(calculator, f'calcular_{key}')(1)
        valor_y2 = getattr(calculator, f'calcular_{key}')(2)
        
        # Análisis
        analisis_y1 = interpreter.evaluate_ratio(key, valor_y1)
        analisis_y2 = interpreter.evaluate_ratio(key, valor_y2)
        
        # ==========================================
        # DISEÑO LADO A LADO
        # ==========================================
        
        # Frame contenedor horizontal
        container = ttk.Frame(ratio_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # ============ COLUMNA AÑO 1 ============
        col_y1 = ttk.Frame(container)
        col_y1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self._crear_columna_analisis(col_y1, "AÑO 1", valor_y1, analisis_y1)
        
        # Separador vertical
        separator = ttk.Separator(container, orient='vertical')
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # ============ COLUMNA AÑO 2 ============
        col_y2 = ttk.Frame(container)
        col_y2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self._crear_columna_analisis(col_y2, "AÑO 2", valor_y2, analisis_y2)
    
    def _crear_columna_analisis(self, parent, titulo, valor, analisis):
        """Crea una columna con el análisis de un año"""
        
        # Título del año
        ttk.Label(
            parent,
            text=titulo,
            font=Fonts.HEADER,
            foreground=Colors.PRIMARY
        ).pack(pady=(0, 10))
        
        # Valor con semáforo
        valor_frame = tk.Frame(
            parent,
            bg=self._get_color_semaforo(analisis['estado']),
            relief='raised',
            borderwidth=2
        )
        valor_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            valor_frame,
            text=f"{valor:.4f}",
            font=Fonts.LARGE,
            bg=self._get_color_semaforo(analisis['estado']),
            fg="white",
            pady=15
        ).pack()
        
        # Estado
        estado_text = self._traducir_estado(analisis['estado']).upper()
        tk.Label(
            parent,
            text=f"Estado: {estado_text}",
            font=Fonts.NORMAL_BOLD,
            fg=self._get_color_semaforo(analisis['estado'])
        ).pack(pady=(0, 5))
        
        # Rango óptimo
        rango = analisis['rango_optimo']
        tk.Label(
            parent,
            text=f"Rango Óptimo: {rango[0]:.2f} - {rango[1]:.2f}",
            font=Fonts.SMALL,
            fg=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 10))
        
        # Interpretación
        ttk.Label(
            parent,
            text="📊 Interpretación:",
            font=Fonts.NORMAL_BOLD
        ).pack(anchor='w', pady=(5, 3))
        
        interp_text = tk.Text(
            parent,
            height=3,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=8,
            pady=5
        )
        interp_text.pack(fill=tk.X, pady=(0, 10))
        interp_text.insert('1.0', analisis['interpretacion'])
        interp_text.config(state='disabled')
        
        # Causa
        ttk.Label(
            parent,
            text="🔍 Causa:",
            font=Fonts.NORMAL_BOLD
        ).pack(anchor='w', pady=(5, 3))
        
        causa_text = tk.Text(
            parent,
            height=2,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=8,
            pady=5
        )
        causa_text.pack(fill=tk.X)
        causa_text.insert('1.0', analisis['causa'])
        causa_text.config(state='disabled')
    
    def _get_color_semaforo(self, estado):
        """Retorna color semáforo según el estado"""
        colores = {
            "optimo": Colors.SUCCESS,    # Verde
            "bajo": Colors.DANGER,        # Rojo
            "alto": Colors.WARNING        # Naranja
        }
        return colores.get(estado, Colors.NEUTRAL)
    
    def _traducir_estado(self, estado):
        """Traduce el estado a español"""
        traducciones = {
            "optimo": "Óptimo",
            "bajo": "Bajo",
            "alto": "Alto"
        }
        return traducciones.get(estado, estado)