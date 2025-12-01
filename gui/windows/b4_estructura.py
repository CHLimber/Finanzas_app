"""
Archivo: gui/windows/b4_estructura.py
Pestaña B4 - Estructura Financiera
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions
from core.analysis.estructura_financiera import EstructuraFinanciera


class B4EstructuraTab(ttk.Frame):
    """Pestaña B4 - Análisis de Estructura Financiera"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de B4"""
        
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
            text="B.4 ESTRUCTURA FINANCIERA",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Obtener datos
        balance = self.app.balance_data
        
        # ✅ USAR MÉTODOS CORRECTOS
        # Año 1
        estructura_y1 = EstructuraFinanciera(
            pasivo_corriente=balance.get_total_pasivo_corriente(year=1),
            pasivo_no_corriente=balance.get_total_pasivo_no_corriente(year=1),
            patrimonio=balance.get_total_patrimonio(year=1),
            sector='tecnologia'
        )
        
        # Año 2
        estructura_y2 = EstructuraFinanciera(
            pasivo_corriente=balance.get_total_pasivo_corriente(year=2),
            pasivo_no_corriente=balance.get_total_pasivo_no_corriente(year=2),
            patrimonio=balance.get_total_patrimonio(year=2),
            sector='tecnologia'
        )


        # Sección: Composición del Financiamiento
        self._crear_composicion(scrollable_frame, estructura_y1, estructura_y2)
        
        # Sección: Análisis por Componente
        self._crear_analisis_componentes(scrollable_frame, estructura_y1, estructura_y2)
        
        # Sección: Rangos Óptimos Sector Tecnológico
        self._crear_rangos_sector(scrollable_frame, estructura_y1)
        
        # Sección: Diagnóstico General
        self._crear_diagnostico(scrollable_frame, estructura_y1, estructura_y2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_composicion(self, parent, est_y1, est_y2):
        """Crea la tabla de composición lado a lado"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" 📊 Composición del Financiamiento ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Crear dos columnas lado a lado
        container = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        container.pack(fill=tk.X, expand=True)
        
        # Columna Año 1
        col_y1 = tk.Frame(container, bg=Colors.BG_PRIMARY)
        col_y1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(
            col_y1,
            text="AÑO 1",
            font=Fonts.HEADER,
            bg=Colors.INFO,
            fg="white",
            pady=10
        ).pack(fill=tk.X)
        
        self._crear_tabla_componentes(col_y1, est_y1, 1)
        
        # Separador
        ttk.Separator(container, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Columna Año 2
        col_y2 = tk.Frame(container, bg=Colors.BG_PRIMARY)
        col_y2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        tk.Label(
            col_y2,
            text="AÑO 2",
            font=Fonts.HEADER,
            bg=Colors.INFO,
            fg="white",
            pady=10
        ).pack(fill=tk.X)
        
        self._crear_tabla_componentes(col_y2, est_y2, 2)
    
    def _crear_tabla_componentes(self, parent, estructura, year):
        """Crea tabla de componentes para un año"""
        
        pcts = estructura.porcentajes()
        
        # ✅ Frame con grid
        tabla_frame = tk.Frame(parent, bg=Colors.BG_PRIMARY)
        tabla_frame.pack(fill=tk.X, padx=Dimensions.PADDING_LARGE, pady=Dimensions.PADDING_MEDIUM)
        
        # ✅ QUITAR minsize COMPLETAMENTE
        tabla_frame.columnconfigure(0, weight=1)  # ✅ Solo weight, sin minsize
        tabla_frame.columnconfigure(1, weight=2)  # ✅ Solo weight, sin minsize
        
        componentes = [
            ("Pasivo Corriente", pcts['pct_pc'], 'pasivo_corriente'),
            ("Pasivo No Corriente", pcts['pct_pnc'], 'pasivo_no_corriente'),
            ("Patrimonio Neto", pcts['pct_pn'], 'patrimonio'),
            ("", None, None),
            ("DEUDA TOTAL", pcts['pct_deuda_total'], 'deuda_total')
        ]
        
        row = 0
        for nombre, valor, key in componentes:
            if valor is None:
                ttk.Separator(tabla_frame, orient="horizontal").grid(
                    row=row, column=0, columnspan=2, sticky="ew", pady=8
                )
                row += 1
                continue
            
            # Nombre
            tk.Label(
                tabla_frame,
                text=nombre,
                font=Fonts.NORMAL_BOLD if key == 'deuda_total' else Fonts.NORMAL,
                bg=Colors.BG_PRIMARY,
                anchor="w"
            ).grid(row=row, column=0, sticky="w", padx=5, pady=5)
            
            # Valor
            valor_text = f"{valor*100:.1f}%"
            
            # Color
            if key:
                estado = estructura.evaluar_componente(key)
                bg_color = {
                    'optimo': Colors.SUCCESS,
                    'aceptable': Colors.WARNING,
                    'riesgoso': Colors.DANGER
                }.get(estado, Colors.NEUTRAL)
            else:
                bg_color = Colors.NEUTRAL
            
            # ✅ SIN width fijo, solo padding
            tk.Label(
                tabla_frame,
                text=valor_text,
                font=Fonts.LARGE if key == 'deuda_total' else Fonts.NORMAL_BOLD,
                bg=bg_color,
                fg="white",
                padx=8,  # ✅ Padding moderado
                pady=4,
                relief="raised",
                anchor="center"
            ).grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            
            row += 1

    
    def _crear_analisis_componentes(self, parent, est_y1, est_y2):
        """Crea análisis detallado de cada componente"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" 📝 Interpretación por Componente ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        interp_y1 = est_y1.interpretar()
        interp_y2 = est_y2.interpretar()
        
        componentes = [
            ("Patrimonio Neto (Recursos Propios)", 'patrimonio'),
            ("Deuda Total", 'deuda_total'),
            ("Pasivo Corriente (Corto Plazo)", 'pasivo_corriente'),
            ("Pasivo No Corriente (Largo Plazo)", 'pasivo_no_corriente')
        ]
        
        for nombre, key in componentes:
            self._crear_analisis_componente_dual(
                frame, nombre, key,
                interp_y1[key], interp_y2[key],
                est_y1, est_y2
            )
    
    def _crear_analisis_componente_dual(self, parent, nombre, key, interp_y1, interp_y2, est_y1, est_y2):
        """Crea análisis dual de un componente"""
        
        comp_frame = ttk.LabelFrame(
            parent,
            text=f" {nombre} ",
            padding=10
        )
        comp_frame.pack(fill=tk.X, pady=10)
        
        # Container lado a lado
        container = tk.Frame(comp_frame, bg=Colors.BG_PRIMARY)
        container.pack(fill=tk.X, expand=True)
        
        # Año 1
        col_y1 = tk.Frame(container, bg=Colors.BG_PRIMARY)
        col_y1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            col_y1,
            text="Año 1",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY
        ).pack(anchor='w')
        
        text_y1 = tk.Text(
            col_y1,
            height=4,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        text_y1.pack(fill=tk.X)
        text_y1.insert('1.0', interp_y1)
        text_y1.config(state='disabled')
        
        # Separador
        ttk.Separator(container, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Año 2
        col_y2 = tk.Frame(container, bg=Colors.BG_PRIMARY)
        col_y2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        tk.Label(
            col_y2,
            text="Año 2",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY
        ).pack(anchor='w')
        
        text_y2 = tk.Text(
            col_y2,
            height=4,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        text_y2.pack(fill=tk.X)
        text_y2.insert('1.0', interp_y2)
        text_y2.config(state='disabled')
    
    def _crear_rangos_sector(self, parent, estructura):
        """Crea sección de rangos óptimos"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" 🎯 Rangos Óptimos - Sector Tecnológico ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        rangos = estructura.rangos_optimos_sector()
        
        for componente, rango in rangos.items():
            fila = tk.Frame(frame, bg=Colors.BG_PRIMARY)
            fila.pack(fill=tk.X, pady=3)
            
            tk.Label(
                fila,
                text=f"{componente}:",
                font=Fonts.NORMAL_BOLD,
                bg=Colors.BG_PRIMARY,
                anchor="w",
                width=20
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                fila,
                text=rango,
                font=Fonts.NORMAL,
                bg=Colors.BG_SECONDARY,
                fg=Colors.INFO,
                anchor="w",
                padx=10,
                pady=3
            ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def _crear_diagnostico(self, parent, est_y1, est_y2):
        """Crea diagnóstico general"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" ✅ Diagnóstico General ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Container lado a lado
        container = tk.Frame(frame, bg=Colors.BG_PRIMARY)
        container.pack(fill=tk.X, expand=True)
        
        # Año 1
        diag_y1 = est_y1.diagnostico()
        col_y1 = self._crear_diagnostico_columna(container, "AÑO 1", diag_y1)
        col_y1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Separador
        ttk.Separator(container, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Año 2
        diag_y2 = est_y2.diagnostico()
        col_y2 = self._crear_diagnostico_columna(container, "AÑO 2", diag_y2)
        col_y2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
    
    def _crear_diagnostico_columna(self, parent, titulo, diagnostico):
        """Crea columna de diagnóstico"""
        
        col = tk.Frame(parent, bg=Colors.BG_PRIMARY)
        
        # Título
        tk.Label(
            col,
            text=titulo,
            font=Fonts.HEADER,
            bg=Colors.BG_PRIMARY
        ).pack(anchor='w', pady=(0, 5))
        
        # Nivel
        nivel_colors = {
            'ÓPTIMA': Colors.SUCCESS,
            'EQUILIBRADA': Colors.INFO,
            'ACEPTABLE': Colors.WARNING,
            'RIESGOSA': Colors.DANGER
        }
        
        tk.Label(
            col,
            text=diagnostico['nivel'],
            font=Fonts.LARGE,
            bg=nivel_colors.get(diagnostico['nivel'], Colors.NEUTRAL),
            fg="white",
            padx=20,
            pady=10,
            relief="raised"
        ).pack(fill=tk.X, pady=5)
        
        # Descripción
        text = tk.Text(
            col,
            height=3,
            wrap='word',
            font=Fonts.SMALL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=5
        )
        text.pack(fill=tk.X)
        text.insert('1.0', diagnostico['descripcion'])
        text.config(state='disabled')
        
        return col