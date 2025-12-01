"""
Archivo: gui/windows/d1_matriz_ratios.py
Pestaña D1 - Matriz de Ratios Comparativos
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions, NumberFormat
from core.analysis.matriz_ratios import MatrizRatios


class D1MatrizRatiosTab(ttk.Frame):
    """Pestaña D1 - Matriz de Ratios Comparativos"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de D1"""
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
            text="D.1 MATRIZ DE RATIOS COMPARATIVOS",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Subtítulo
        subtitulo = tk.Label(
            scrollable_frame,
            text="Análisis Comparativo de Principales Ratios Financieros (Sector Tecnológico)",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY,
            fg=Colors.NEUTRAL
        )
        subtitulo.pack(pady=(0, Dimensions.PADDING_MEDIUM))
        
        # Obtener análisis
        analisis = MatrizRatios(self.app.balance_data, self.app.income_data)
        matriz = analisis.generar_matriz_completa()
        
        # Crear secciones por categoría
        categorias = ['Patrimonial', 'Financiero', 'Económico']
        
        for categoria in categorias:
            self._crear_seccion_categoria(scrollable_frame, matriz, categoria)
        
        # RESUMEN EJECUTIVO
        self._crear_resumen_ejecutivo(scrollable_frame, matriz)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_seccion_categoria(self, parent, matriz, categoria):
        """Crea una sección para una categoría de ratios"""
        # Frame de la categoría
        categoria_frame = ttk.LabelFrame(
            parent,
            text=f" Ratios de Análisis {categoria} ",
            padding=Dimensions.PADDING_LARGE
        )
        categoria_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                            pady=Dimensions.PADDING_MEDIUM)
        
        # Filtrar ratios de esta categoría
        ratios_categoria = {k: v for k, v in matriz.items() if v['categoria'] == categoria}
        
        # Crear tabla
        tabla_frame = tk.Frame(categoria_frame, bg=Colors.BG_PRIMARY)
        tabla_frame.pack(fill=tk.X, pady=5)
        
        # Configurar grid
        tabla_frame.grid_columnconfigure(0, weight=2)  # Ratio
        tabla_frame.grid_columnconfigure(1, weight=1)  # Año 1
        tabla_frame.grid_columnconfigure(2, weight=1)  # Año 2
        tabla_frame.grid_columnconfigure(3, weight=1)  # Cambio
        tabla_frame.grid_columnconfigure(4, weight=3)  # Interpretación
        
        # Encabezados
        headers = ["Ratio", "Año 1", "Año 2", "Cambio", "Interpretación"]
        for col, header in enumerate(headers):
            tk.Label(
                tabla_frame,
                text=header,
                font=Fonts.HEADER,
                bg=Colors.BG_SECONDARY,
                padx=10,
                pady=8
            ).grid(row=0, column=col, sticky="ew", padx=1, pady=1)
        
        # Filas de datos
        row = 1
        for key, data in ratios_categoria.items():
            # Nombre del ratio
            tk.Label(
                tabla_frame,
                text=data['nombre'],
                font=Fonts.NORMAL_BOLD,
                bg=Colors.BG_PRIMARY,
                anchor="w",
                padx=10,
                pady=8
            ).grid(row=row, column=0, sticky="ew", padx=1, pady=1)
            
            # Año 1
            valor1 = self._formatear_valor(data['ano_1'], data['unidad'])
            tk.Label(
                tabla_frame,
                text=valor1,
                font=Fonts.NORMAL,
                bg=Colors.BG_PRIMARY,
                padx=10,
                pady=8
            ).grid(row=row, column=1, sticky="ew", padx=1, pady=1)
            
            # Año 2 (con color según estado)
            valor2 = self._formatear_valor(data['ano_2'], data['unidad'])
            color_estado = self._get_color_estado(data['estado'])
            tk.Label(
                tabla_frame,
                text=valor2,
                font=Fonts.NORMAL_BOLD,
                bg=color_estado,
                fg="white",
                padx=10,
                pady=8
            ).grid(row=row, column=2, sticky="ew", padx=1, pady=1)
            
            # Cambio (con flecha y color)
            cambio_text = f"{data['simbolo']} {abs(data['cambio_porcentual']):.1f}%"
            color_cambio = self._get_color_cambio(data['simbolo'])
            tk.Label(
                tabla_frame,
                text=cambio_text,
                font=Fonts.NORMAL_BOLD,
                bg=Colors.BG_PRIMARY,
                fg=color_cambio,
                padx=10,
                pady=8
            ).grid(row=row, column=3, sticky="ew", padx=1, pady=1)
            
            # Interpretación
            tk.Label(
                tabla_frame,
                text=data['interpretacion'],
                font=Fonts.SMALL,
                bg=Colors.BG_SECONDARY,
                anchor="w",
                wraplength=400,
                justify="left",
                padx=10,
                pady=8
            ).grid(row=row, column=4, sticky="ew", padx=1, pady=1)
            
            row += 1
    
    def _crear_resumen_ejecutivo(self, parent, matriz):
        """Crea un resumen ejecutivo de la matriz"""
        resumen_frame = ttk.LabelFrame(
            parent,
            text=" Resumen Ejecutivo - Sector Tecnológico ",
            padding=Dimensions.PADDING_LARGE
        )
        resumen_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                          pady=Dimensions.PADDING_MEDIUM)
        
        # Contar estados
        optimos = sum(1 for r in matriz.values() if r['estado'] == 'optimo')
        bajos = sum(1 for r in matriz.values() if r['estado'] == 'bajo')
        altos = sum(1 for r in matriz.values() if r['estado'] == 'alto')
        total = len(matriz)
        
        # Contar mejoras/deterioros
        mejoras = sum(1 for r in matriz.values() if r['direccion'] == 'mejora')
        deterioros = sum(1 for r in matriz.values() if r['direccion'] == 'deterioro')
        estables = sum(1 for r in matriz.values() if r['direccion'] == 'estable')
        
        # Estadísticas
        stats_frame = tk.Frame(resumen_frame, bg=Colors.BG_PRIMARY)
        stats_frame.pack(fill=tk.X, pady=10)
        
        # Grid de estadísticas
        tk.Label(stats_frame, text="ESTADO DE RATIOS (AÑO 2)", 
                 font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=0, columnspan=2, pady=5, sticky="w")
        
        tk.Label(stats_frame, text=f"✓ Óptimos:", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        tk.Label(stats_frame, text=f"{optimos}/{total} ({optimos/total*100:.1f}%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.SUCCESS, fg="white", 
                 padx=5, pady=2).grid(row=1, column=1, padx=10, pady=3, sticky="w")
        
        tk.Label(stats_frame, text=f"⚠ Bajos:", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        tk.Label(stats_frame, text=f"{bajos}/{total} ({bajos/total*100:.1f}%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.DANGER, fg="white", 
                 padx=5, pady=2).grid(row=2, column=1, padx=10, pady=3, sticky="w")
        
        tk.Label(stats_frame, text=f"⚠ Altos:", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=3, column=0, padx=10, pady=3, sticky="w")
        tk.Label(stats_frame, text=f"{altos}/{total} ({altos/total*100:.1f}%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.WARNING, fg="white", 
                 padx=5, pady=2).grid(row=3, column=1, padx=10, pady=3, sticky="w")
        
        tk.Label(stats_frame, text="TENDENCIAS (AÑO 1 vs 2)", 
                 font=Fonts.HEADER, bg=Colors.BG_PRIMARY).grid(
            row=0, column=3, columnspan=2, pady=5, padx=(50, 0), sticky="w")
        
        tk.Label(stats_frame, text=f"↑ Mejoras:", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=1, column=3, padx=(50, 10), pady=3, sticky="w")
        tk.Label(stats_frame, text=f"{mejoras}/{total} ({mejoras/total*100:.1f}%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.SUCCESS, fg="white", 
                 padx=5, pady=2).grid(row=1, column=4, padx=10, pady=3, sticky="w")
        
        tk.Label(stats_frame, text=f"↓ Deterioros:", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=2, column=3, padx=(50, 10), pady=3, sticky="w")
        tk.Label(stats_frame, text=f"{deterioros}/{total} ({deterioros/total*100:.1f}%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.DANGER, fg="white", 
                 padx=5, pady=2).grid(row=2, column=4, padx=10, pady=3, sticky="w")
        
        tk.Label(stats_frame, text=f"= Estables:", 
                 font=Fonts.NORMAL, bg=Colors.BG_PRIMARY).grid(
            row=3, column=3, padx=(50, 10), pady=3, sticky="w")
        tk.Label(stats_frame, text=f"{estables}/{total} ({estables/total*100:.1f}%)", 
                 font=Fonts.NORMAL_BOLD, bg=Colors.INFO, fg="white", 
                 padx=5, pady=2).grid(row=3, column=4, padx=10, pady=3, sticky="w")
        
        # Conclusión
        ttk.Separator(resumen_frame, orient="horizontal").pack(fill=tk.X, pady=10)
        
        conclusion = self._generar_conclusion(optimos, total, mejoras, deterioros)
        
        conclusion_text = tk.Text(
            resumen_frame,
            height=5,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        conclusion_text.pack(fill=tk.X)
        conclusion_text.insert('1.0', conclusion)
        conclusion_text.config(state='disabled')
    
    def _generar_conclusion(self, optimos, total, mejoras, deterioros):
        """Genera conclusión del análisis"""
        pct_optimos = (optimos / total) * 100
        pct_mejoras = (mejoras / total) * 100
        
        texto = "CONCLUSIÓN - CONTEXTO SECTOR TECNOLÓGICO:\n\n"
        
        if pct_optimos >= 70 and pct_mejoras >= 50:
            texto += f"✓ SITUACIÓN EXCELENTE: {pct_optimos:.0f}% de ratios en rango óptimo con {pct_mejoras:.0f}% de mejoras. "
            texto += "La empresa presenta indicadores financieros sólidos, típicos de empresas tecnológicas exitosas. "
            texto += "Mantiene equilibrio entre liquidez, solvencia y rentabilidad, posicionándose favorablemente "
            texto += "para inversión en I+D y expansión."
        
        elif pct_optimos >= 50 and pct_mejoras >= 40:
            texto += f"✓ SITUACIÓN FAVORABLE: {pct_optimos:.0f}% de ratios óptimos con tendencia positiva ({pct_mejoras:.0f}% mejoras). "
            texto += "La empresa muestra salud financiera adecuada para el sector tecnológico. "
            texto += "Áreas de mejora identificadas pueden optimizarse manteniendo el impulso de crecimiento."
        
        elif pct_mejoras > deterioros:
            texto += f"⚠ SITUACIÓN MIXTA CON TENDENCIA POSITIVA: {pct_mejoras:.0f}% mejoras vs {deterioros} deterioros. "
            texto += "Aunque algunos ratios requieren atención, la tendencia general es positiva. "
            texto += "En sector tech, es común priorizar crecimiento sobre márgenes a corto plazo."
        
        else:
            texto += f"⚠ REQUIERE ATENCIÓN: Solo {pct_optimos:.0f}% de ratios óptimos. "
            texto += "La empresa enfrenta desafíos financieros que requieren acción estratégica. "
            texto += "En el competitivo sector tecnológico, es crítico fortalecer liquidez y rentabilidad "
            texto += "para mantener capacidad de innovación."
        
        return texto
    
    def _formatear_valor(self, valor, unidad):
        """Formatea un valor según su unidad"""
        if unidad == 'porcentaje':
            return f"{valor:.2f}%"
        elif unidad == 'veces':
            return f"{valor:.2f}x"
        else:  # ratio
            return f"{valor:.2f}"
    
    def _get_color_estado(self, estado):
        """Retorna color según el estado del ratio"""
        if estado == 'optimo':
            return Colors.SUCCESS
        elif estado == 'bajo':
            return Colors.DANGER
        else:  # alto
            return Colors.WARNING
    
    def _get_color_cambio(self, simbolo):
        """Retorna color según la dirección del cambio"""
        if simbolo == "↑":
            return Colors.SUCCESS
        elif simbolo == "↓":
            return Colors.DANGER
        else:
            return Colors.NEUTRAL