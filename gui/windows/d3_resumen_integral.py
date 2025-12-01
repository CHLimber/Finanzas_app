"""
Archivo: gui/windows/d3_resumen_integral.py
Pestaña D3 - Resumen Integral de Ratios
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.resumen_integral import ResumenIntegralRatios


class D3ResumenIntegralTab(ttk.Frame):
    """Pestaña D3 - Resumen Integral de Ratios"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de D3"""
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
            text="D.3 RESUMEN INTEGRAL DE RATIOS FINANCIEROS",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Subtítulo
        subtitulo = tk.Label(
            scrollable_frame,
            text="Interpretación, Causa y Recomendación Completa de Todos los Ratios (Año 2)",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            fg=Colors.NEUTRAL
        )
        subtitulo.pack(pady=(0, Dimensions.PADDING_MEDIUM))
        
        # Obtener análisis
        analisis = ResumenIntegralRatios(self.app.balance_data, self.app.income_data)
        resumen = analisis.generar_resumen_completo()
        
        # ANÁLISIS PATRIMONIAL
        self._crear_seccion_categoria(
            scrollable_frame,
            "ANÁLISIS PATRIMONIAL",
            "Ratios de Liquidez y Capital de Trabajo",
            resumen['patrimonial']
        )
        
        # ANÁLISIS FINANCIERO
        self._crear_seccion_categoria(
            scrollable_frame,
            "ANÁLISIS FINANCIERO",
            "Ratios de Solvencia y Estructura de Capital",
            resumen['financiero']
        )
        
        # ANÁLISIS ECONÓMICO
        self._crear_seccion_categoria(
            scrollable_frame,
            "ANÁLISIS ECONÓMICO",
            "Ratios de Rentabilidad y Eficiencia",
            resumen['economico']
        )
        
        # CONCLUSIÓN GLOBAL
        conclusion_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" 📊 CONCLUSIÓN GLOBAL DEL ANÁLISIS ",
            padding=Dimensions.PADDING_LARGE
        )
        conclusion_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                             pady=Dimensions.PADDING_MEDIUM)
        
        conclusion_text = tk.Text(
            conclusion_frame,
            height=10,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        conclusion_text.pack(fill=tk.X)
        conclusion_text.insert('1.0', resumen['conclusion_global'])
        conclusion_text.config(state='disabled')
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_seccion_categoria(self, parent, titulo, subtitulo, ratios):
        """Crea una sección para una categoría de ratios"""
        # Frame de la categoría
        categoria_frame = ttk.LabelFrame(
            parent,
            text=f" {titulo} ",
            padding=Dimensions.PADDING_LARGE
        )
        categoria_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                            pady=Dimensions.PADDING_MEDIUM)
        
        # Subtítulo
        subtitulo_label = tk.Label(
            categoria_frame,
            text=subtitulo,
            font=Fonts.SMALL,
            bg=Colors.BG_PRIMARY,
            fg=Colors.NEUTRAL
        )
        subtitulo_label.pack(anchor="w", pady=(0, 10))
        
        # Crear cards para cada ratio
        for ratio_data in ratios:
            self._crear_card_ratio(categoria_frame, ratio_data)
    
    def _crear_card_ratio(self, parent, ratio_data):
        """Crea una card para mostrar un ratio con su análisis completo"""
        analisis = ratio_data['analisis']
        valor = ratio_data['valor']
        
        # Determinar color según estado
        if analisis['estado'] == 'optimo':
            color_borde = Colors.SUCCESS
            color_header = Colors.SUCCESS
        elif analisis['estado'] == 'bajo':
            color_borde = Colors.DANGER
            color_header = Colors.DANGER
        else:  # alto
            color_borde = Colors.WARNING
            color_header = Colors.WARNING
        
        # Frame contenedor con borde
        card_frame = tk.Frame(parent, bg=color_borde, relief='solid', borderwidth=2)
        card_frame.pack(fill=tk.X, pady=Dimensions.PADDING_MEDIUM)
        
        # Frame interno
        inner_frame = tk.Frame(card_frame, bg=Colors.BG_PRIMARY)
        inner_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # HEADER
        header_frame = tk.Frame(inner_frame, bg=color_header)
        header_frame.pack(fill=tk.X)
        
        # Título y valor
        titulo_container = tk.Frame(header_frame, bg=color_header)
        titulo_container.pack(fill=tk.X, padx=15, pady=10)
        
        nombre_label = tk.Label(
            titulo_container,
            text=analisis['nombre'],
            font=Fonts.LARGE,
            bg=color_header,
            fg="white"
        )
        nombre_label.pack(side=tk.LEFT)
        
        # Valor y badge de estado
        valor_container = tk.Frame(titulo_container, bg=color_header)
        valor_container.pack(side=tk.RIGHT)
        
        # Formatear valor
        if analisis.get('unidad') == 'porcentaje':
            valor_texto = f"{valor:.2f}%"
        elif analisis.get('unidad') == 'veces':
            valor_texto = f"{valor:.2f}x"
        else:
            valor_texto = f"{valor:.2f}"
        
        valor_label = tk.Label(
            valor_container,
            text=valor_texto,
            font=("Arial", 18, "bold"),
            bg=color_header,
            fg="white"
        )
        valor_label.pack(side=tk.LEFT, padx=(0, 10))
        
        estado_badge = tk.Label(
            valor_container,
            text=analisis['estado'].upper(),
            font=Fonts.SMALL,
            bg="white",
            fg=color_header,
            padx=8,
            pady=3
        )
        estado_badge.pack(side=tk.LEFT)
        
        # CUERPO - Grid de 3 columnas
        body_frame = tk.Frame(inner_frame, bg=Colors.BG_PRIMARY)
        body_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Configurar grid
        body_frame.grid_columnconfigure(0, weight=1)
        body_frame.grid_columnconfigure(1, weight=1)
        body_frame.grid_columnconfigure(2, weight=1)
        
        # INTERPRETACIÓN
        interp_frame = tk.Frame(body_frame, bg=Colors.BG_SECONDARY, relief='solid', borderwidth=1)
        interp_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        tk.Label(
            interp_frame,
            text="📊 INTERPRETACIÓN",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_SECONDARY,
            fg=Colors.PRIMARY
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        interp_text = tk.Text(
            interp_frame,
            height=6,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        interp_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        interp_text.insert('1.0', analisis['interpretacion'])
        interp_text.config(state='disabled')
        
        # CAUSA
        causa_frame = tk.Frame(body_frame, bg=Colors.BG_SECONDARY, relief='solid', borderwidth=1)
        causa_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        
        tk.Label(
            causa_frame,
            text="🔍 CAUSA",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_SECONDARY,
            fg=Colors.PRIMARY
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        causa_text = tk.Text(
            causa_frame,
            height=6,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        causa_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        causa_text.insert('1.0', analisis['causa'])
        causa_text.config(state='disabled')
        
        # RECOMENDACIÓN
        recom_frame = tk.Frame(body_frame, bg=Colors.BG_SECONDARY, relief='solid', borderwidth=1)
        recom_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        
        tk.Label(
            recom_frame,
            text="💡 RECOMENDACIÓN",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_SECONDARY,
            fg=Colors.PRIMARY
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        recom_text = tk.Text(
            recom_frame,
            height=6,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        recom_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        recom_text.insert('1.0', analisis['recomendacion'])
        recom_text.config(state='disabled')
        
        # RANGO ÓPTIMO (footer pequeño)
        if 'rango' in analisis:
            rango_min, rango_max = analisis['rango']
            rango_text = f"Rango Óptimo: {rango_min:.2f} - {rango_max:.2f}"
            
            rango_label = tk.Label(
                inner_frame,
                text=rango_text,
                font=Fonts.SMALL,
                bg=Colors.BG_SECONDARY,
                fg=Colors.NEUTRAL,
                padx=10,
                pady=5
            )
            rango_label.pack(fill=tk.X, padx=15, pady=(0, 10))