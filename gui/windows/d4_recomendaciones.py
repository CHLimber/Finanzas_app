"""
Archivo: gui/windows/d4_recomendaciones.py
Pestaña D4 - Recomendaciones Estratégicas
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions
from core.analysis.recomendaciones_estrategicas import RecomendacionesEstrategicas


class D4RecomendacionesTab(ttk.Frame):
    """Pestaña D4 - Recomendaciones Estratégicas"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de D4"""
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
            text="D.4 RECOMENDACIONES ESTRATÉGICAS",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Subtítulo
        subtitulo = tk.Label(
            scrollable_frame,
            text="3 Recomendaciones Fundamentadas Cuantitativamente por Área Crítica",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            fg=Colors.NEUTRAL
        )
        subtitulo.pack(pady=(0, Dimensions.PADDING_MEDIUM))
        
        # Obtener análisis
        analisis = RecomendacionesEstrategicas(self.app.balance_data, self.app.income_data)
        resultado = analisis.generar_recomendaciones_completas()
        
        # a) LIQUIDEZ
        self._crear_seccion_recomendaciones(
            scrollable_frame,
            "a) RECOMENDACIONES PARA MEJORAR LIQUIDEZ",
            Colors.INFO,
            resultado['liquidez']
        )
        
        # b) RENTABILIDAD
        self._crear_seccion_recomendaciones(
            scrollable_frame,
            "b) RECOMENDACIONES PARA MEJORAR RENTABILIDAD",
            Colors.SUCCESS,
            resultado['rentabilidad']
        )
        
        # c) EFICIENCIA OPERATIVA
        self._crear_seccion_recomendaciones(
            scrollable_frame,
            "c) RECOMENDACIONES PARA MEJORAR EFICIENCIA OPERATIVA",
            Colors.WARNING,
            resultado['eficiencia_operativa']
        )
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_seccion_recomendaciones(self, parent, titulo, color, recomendaciones):
        """Crea una sección con las 3 recomendaciones"""
        # Frame de la sección
        seccion_frame = ttk.LabelFrame(
            parent,
            text=f" {titulo} ",
            padding=Dimensions.PADDING_LARGE
        )
        seccion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                          pady=Dimensions.PADDING_MEDIUM)
        
        # Crear cards para cada recomendación
        for recom in recomendaciones:
            self._crear_card_recomendacion(seccion_frame, recom, color)
    
    def _crear_card_recomendacion(self, parent, recom, color):
        """Crea una card para mostrar una recomendación"""
        # Frame contenedor con borde de color
        card_frame = tk.Frame(parent, bg=color, relief='solid', borderwidth=2)
        card_frame.pack(fill=tk.X, pady=Dimensions.PADDING_MEDIUM)
        
        # Frame interno
        inner_frame = tk.Frame(card_frame, bg=Colors.BG_PRIMARY)
        inner_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # HEADER
        header_frame = tk.Frame(inner_frame, bg=color)
        header_frame.pack(fill=tk.X)
        
        # Título con número
        titulo_container = tk.Frame(header_frame, bg=color)
        titulo_container.pack(fill=tk.X, padx=15, pady=12)
        
        # Badge de número
        numero_badge = tk.Label(
            titulo_container,
            text=f"#{recom['numero']}",
            font=("Arial", 16, "bold"),
            bg="white",
            fg=color,
            padx=10,
            pady=5
        )
        numero_badge.pack(side=tk.LEFT, padx=(0, 10))
        
        # Título
        titulo_label = tk.Label(
            titulo_container,
            text=recom['titulo'],
            font=Fonts.LARGE,
            bg=color,
            fg="white"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # CUERPO
        body_frame = tk.Frame(inner_frame, bg=Colors.BG_PRIMARY)
        body_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # FUNDAMENTO CUANTITATIVO
        fund_frame = tk.Frame(body_frame, bg=Colors.BG_SECONDARY, relief='solid', borderwidth=1)
        fund_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            fund_frame,
            text="📊 FUNDAMENTO CUANTITATIVO",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_SECONDARY,
            fg=color
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        fund_text = tk.Text(
            fund_frame,
            height=5,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        fund_text.pack(fill=tk.X, padx=5, pady=(0, 10))
        fund_text.insert('1.0', recom['fundamento_cuantitativo'])
        fund_text.config(state='disabled')
        
        # ANÁLISIS
        analisis_frame = tk.Frame(body_frame, bg=Colors.BG_SECONDARY, relief='solid', borderwidth=1)
        analisis_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            analisis_frame,
            text="🔍 ANÁLISIS",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_SECONDARY,
            fg=color
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        analisis_label = tk.Label(
            analisis_frame,
            text=recom['analisis'],
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            wraplength=900,
            justify="left"
        )
        analisis_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # ACCIONES ESPECÍFICAS
        acciones_frame = tk.Frame(body_frame, bg=Colors.BG_SECONDARY, relief='solid', borderwidth=1)
        acciones_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            acciones_frame,
            text="✓ ACCIONES ESPECÍFICAS",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_SECONDARY,
            fg=color
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        for i, accion in enumerate(recom['acciones'], 1):
            accion_label = tk.Label(
                acciones_frame,
                text=f"  • {accion}",
                font=Fonts.NORMAL,
                bg=Colors.BG_SECONDARY,
                wraplength=880,
                justify="left"
            )
            accion_label.pack(anchor="w", padx=10, pady=2)
        
        tk.Label(acciones_frame, text="", bg=Colors.BG_SECONDARY).pack(pady=5)
        
        # IMPACTO PROYECTADO
        impacto_frame = tk.Frame(body_frame, bg=color, relief='solid', borderwidth=1)
        impacto_frame.pack(fill=tk.X)
        
        tk.Label(
            impacto_frame,
            text="💡 IMPACTO PROYECTADO",
            font=Fonts.NORMAL_BOLD,
            bg=color,
            fg="white"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        impacto_label = tk.Label(
            impacto_frame,
            text=recom['impacto'],
            font=("Arial", 11, "bold"),
            bg=color,
            fg="white",
            wraplength=900,
            justify="left"
        )
        impacto_label.pack(anchor="w", padx=10, pady=(0, 10))