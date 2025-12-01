"""
Archivo: gui/windows/a5_diagnostico.py
Pestaña A5 - Diagnóstico Patrimonial
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions
from core.analysis.diagnostico_patrimonial import DiagnosticoPatrimonialDual


class A5DiagnosticoTab(ttk.Frame):
    """Pestaña A5 - Diagnóstico Patrimonial"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
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
            text="A.5 DIAGNÓSTICO PATRIMONIAL",
            font=Fonts.TITLE
        ).pack(pady=Dimensions.PADDING_LARGE)
        
        # Descripción
        desc_frame = ttk.Frame(scrollable_frame)
        desc_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, pady=Dimensions.PADDING_MEDIUM)
        
        desc_text = (
            "El Diagnóstico Patrimonial evalúa la salud financiera estructural de la empresa "
            "clasificándola en cuatro estados posibles:\n\n"
            "• EQUILIBRIO TOTAL: Estructura muy sólida (PN > PT, FM > 0)\n"
            "• EQUILIBRIO NORMAL: Estructura estable con mayor deuda (PN < PT, FM > 0)\n"
            "• CRISIS: Problemas de liquidez (FM < 0, pero AT > PT)\n"
            "• INSOLVENCIA: Quiebra técnica (AT < PT o PN < 0)"
        )
        
        tk.Label(
            desc_frame,
            text=desc_text,
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            wraplength=800,
            justify="left",
            padx=15,
            pady=15,
            relief="solid",
            borderwidth=1
        ).pack(fill=tk.X)
        
        # Realizar análisis
        from core.analysis.diagnostico_patrimonial import DiagnosticoPatrimonialDual
        diagnostico = DiagnosticoPatrimonialDual(self.app.balance_data)
        resultado = diagnostico.analisis_dual()
        
        # ============================================================
        # DIAGNÓSTICO AÑO 1
        # ============================================================
        diag_y1_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Diagnóstico Patrimonial - Año 1 ",
            padding=Dimensions.PADDING_LARGE
        )
        diag_y1_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        y1 = resultado["year_1"]
        
        # Estado y nivel de riesgo
        estado_y1_label = tk.Label(
            diag_y1_frame,
            text=f"Estado: {y1['estado']}  |  Nivel de Riesgo: {y1['nivel_riesgo']}",
            font=Fonts.HEADER,
            bg=self._get_color_estado(y1['estado']),
            fg="white",
            padx=15,
            pady=10,
            relief="raised",
            borderwidth=2
        )
        estado_y1_label.pack(fill=tk.X, pady=(0, 10))
        
        # Interpretación
        text_y1 = tk.Text(
            diag_y1_frame,
            height=10,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_y1.pack(fill=tk.X)
        text_y1.insert('1.0', y1['interpretacion'])
        text_y1.config(state='disabled')
        
        # ============================================================
        # DIAGNÓSTICO AÑO 2
        # ============================================================
        diag_y2_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Diagnóstico Patrimonial - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        diag_y2_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                        pady=Dimensions.PADDING_MEDIUM)
        
        y2 = resultado["year_2"]
        
        # Estado y nivel de riesgo
        estado_y2_label = tk.Label(
            diag_y2_frame,
            text=f"Estado: {y2['estado']}  |  Nivel de Riesgo: {y2['nivel_riesgo']}",
            font=Fonts.HEADER,
            bg=self._get_color_estado(y2['estado']),
            fg="white",
            padx=15,
            pady=10,
            relief="raised",
            borderwidth=2
        )
        estado_y2_label.pack(fill=tk.X, pady=(0, 10))
        
        # Interpretación
        text_y2 = tk.Text(
            diag_y2_frame,
            height=10,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_y2.pack(fill=tk.X)
        text_y2.insert('1.0', y2['interpretacion'])
        text_y2.config(state='disabled')
        
        # ============================================================
        # EVOLUCIÓN
        # ============================================================
        evol_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Evolución del Estado Patrimonial ",
            padding=Dimensions.PADDING_LARGE
        )
        evol_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                    pady=Dimensions.PADDING_MEDIUM)
        
        evol_label = tk.Label(
            evol_frame,
            text=resultado['evolucion'],
            font=Fonts.NORMAL_BOLD,
            bg=Colors.INFO,
            fg="white",
            wraplength=700,
            justify="left",
            padx=15,
            pady=15,
            relief="raised",
            borderwidth=2
        )
        evol_label.pack(fill=tk.X)
        
        # ============================================================
        # RECOMENDACIONES AÑO 2
        # ============================================================
        rec_frame = ttk.LabelFrame(
            scrollable_frame,
            text=" Recomendaciones - Año 2 ",
            padding=Dimensions.PADDING_LARGE
        )
        rec_frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE,
                    pady=Dimensions.PADDING_MEDIUM)
        
        recomendaciones = y2['recomendaciones']
        
        for i, rec in enumerate(recomendaciones, 1):
            rec_label = tk.Label(
                rec_frame,
                text=rec,
                font=Fonts.NORMAL,
                bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY,
                wraplength=700,
                justify="left",
                padx=10,
                pady=8,
                anchor="w"
            )
            rec_label.pack(fill=tk.X, pady=3)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _get_color_estado(self, estado):
        """Retorna color según el estado patrimonial"""
        colores = {
            "EQUILIBRIO TOTAL": Colors.SUCCESS,
            "EQUILIBRIO NORMAL": Colors.INFO,
            "CRISIS": Colors.WARNING,
            "INSOLVENCIA": Colors.DANGER,
            "NO CLASIFICADO": Colors.NEUTRAL
        }
        return colores.get(estado, Colors.PRIMARY)