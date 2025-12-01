"""
Archivo: gui/windows/b3_comparativa.py
Pestana B3 - Comparativa de Ratios (año 1 vs año 2)
CORREGIDO: La tendencia ahora se evalua comparando con el rango optimo,
no simplemente si subio o bajo.
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts, Dimensions
from core.calculators.ratio_calculator import RatioCalculator
from core.analysis.financial_interpreter import FinancialInterpreter


class B3ComparativaTab(ttk.Frame):
    """Pestana B3 - Comparativa de Ratios entre año 1 y año 2"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz de B3"""
        
        canvas = tk.Canvas(self, bg=Colors.BG_PRIMARY)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=Colors.BG_PRIMARY)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Titulo
        titulo = tk.Label(
            scrollable_frame,
            text="B.3 COMPARATIVA DE RATIOS - año 1 VS año 2",
            font=Fonts.TITLE,
            bg=Colors.BG_PRIMARY
        )
        titulo.pack(pady=Dimensions.PADDING_LARGE)
        
        # Calculadoras
        calculator = RatioCalculator(self.app.balance_data, self.app.income_data)
        interpreter = FinancialInterpreter()
        
        # SECCION 1: COMPARATIVA DE LIQUIDEZ
        self._crear_seccion_liquidez(scrollable_frame, calculator, interpreter)
        
        # SECCION 2: COMPARATIVA DE SOLVENCIA
        self._crear_seccion_solvencia(scrollable_frame, calculator, interpreter)
        
        # SECCION 3: CONCLUSION GENERAL
        self._crear_conclusion_general(scrollable_frame, calculator, interpreter)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _crear_seccion_liquidez(self, parent, calculator, interpreter):
        """Crea la seccion de comparativa de liquidez"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" Comparativa de Liquidez ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Tabla comparativa
        headers = ["Ratio", "año 1", "año 2", "Variacion", "Tendencia"]
        
        for col, header in enumerate(headers):
            tk.Label(
                frame,
                text=header,
                font=Fonts.HEADER,
                bg=Colors.BG_SECONDARY,
                relief="raised",
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="ew", padx=2, pady=2)
        
        # Ratios de liquidez
        ratios_liquidez = [
            ("Razon de Liquidez General", "razon_liquidez"),
            ("Razon de Tesoreria", "razon_tesoreria"),
            ("Razon de Disponibilidad", "razon_disponibilidad")
        ]
        
        for idx, (nombre, key) in enumerate(ratios_liquidez, start=1):
            self._crear_fila_comparativa(frame, idx, nombre, key, calculator, interpreter)
        
        # Interpretacion de liquidez
        self._crear_interpretacion_liquidez(parent, calculator, interpreter)
    
    def _crear_seccion_solvencia(self, parent, calculator, interpreter):
        """Crea la seccion de comparativa de solvencia"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" Comparativa de Solvencia ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Tabla comparativa
        headers = ["Ratio", "año 1", "año 2", "Variacion", "Tendencia"]
        
        for col, header in enumerate(headers):
            tk.Label(
                frame,
                text=header,
                font=Fonts.HEADER,
                bg=Colors.BG_SECONDARY,
                relief="raised",
                padx=10,
                pady=5
            ).grid(row=0, column=col, sticky="ew", padx=2, pady=2)
        
        # Ratios de solvencia
        ratios_solvencia = [
            ("Ratio de Garantia", "ratio_garantia"),
            ("Ratio de Autonomia", "ratio_autonomia"),
            ("Ratio de Calidad de Deuda", "ratio_calidad_deuda")
        ]
        
        for idx, (nombre, key) in enumerate(ratios_solvencia, start=1):
            self._crear_fila_comparativa(frame, idx, nombre, key, calculator, interpreter)
        
        # Interpretacion de solvencia
        self._crear_interpretacion_solvencia(parent, calculator, interpreter)
    
    def _evaluar_tendencia_vs_optimo(self, ratio_key, valor_y1, valor_y2, interpreter):
        """
        Evalua la tendencia comparando con el rango optimo.
        
        LOGICA CORREGIDA:
        - Si el valor se ACERCA al rango optimo -> Mejoro
        - Si el valor se ALEJA del rango optimo -> Empeoro
        - Si ambos estan en el rango optimo -> Estable/Optimo
        - Si la distancia al optimo es similar -> Estable
        
        Returns:
            tuple: (texto_tendencia, color_tendencia)
        """
        # Obtener rango optimo
        rango = interpreter.get_rango_optimo(ratio_key)
        
        if rango is None:
            # Si no hay rango definido, usar logica simple
            if valor_y2 > valor_y1 * 1.05:
                return ("Subio", Colors.NEUTRAL)
            elif valor_y2 < valor_y1 * 0.95:
                return ("Bajo", Colors.NEUTRAL)
            else:
                return ("Estable", Colors.NEUTRAL)
        
        rango_min, rango_max = rango
        punto_medio_optimo = (rango_min + rango_max) / 2
        
        # Calcular distancia al rango optimo para cada año
        distancia_y1 = self._calcular_distancia_al_optimo(valor_y1, rango_min, rango_max)
        distancia_y2 = self._calcular_distancia_al_optimo(valor_y2, rango_min, rango_max)
        
        # Determinar estado de cada año
        estado_y1 = interpreter.get_estado(ratio_key, valor_y1)
        estado_y2 = interpreter.get_estado(ratio_key, valor_y2)
        
        # CASO 1: Ambos en rango optimo
        if estado_y1 == "optimo" and estado_y2 == "optimo":
            return ("Optimo", Colors.SUCCESS)
        
        # CASO 2: Paso de fuera del optimo a dentro del optimo
        if estado_y1 != "optimo" and estado_y2 == "optimo":
            return ("Mejoro (ahora optimo)", Colors.POSITIVE)
        
        # CASO 3: Paso de dentro del optimo a fuera
        if estado_y1 == "optimo" and estado_y2 != "optimo":
            return ("Empeoro (salio de optimo)", Colors.NEGATIVE)
        
        # CASO 4: Ambos fuera del optimo - comparar distancias
        # Si la distancia disminuyo, mejoro (se acerco al optimo)
        # Si la distancia aumento, empeoro (se alejo del optimo)
        
        diferencia_distancia = distancia_y1 - distancia_y2  # Positivo si mejoro
        
        # Umbral de 5% del rango para considerar cambio significativo
        umbral = (rango_max - rango_min) * 0.1
        
        if diferencia_distancia > umbral:
            # Se acerco al optimo
            return ("Mejoro (se acerca a optimo)", Colors.POSITIVE)
        elif diferencia_distancia < -umbral:
            # Se alejo del optimo
            return ("Empeoro (se aleja de optimo)", Colors.NEGATIVE)
        else:
            # Cambio no significativo
            if estado_y2 == "bajo":
                return ("Estable (bajo)", Colors.WARNING)
            elif estado_y2 == "alto":
                return ("Estable (alto)", Colors.WARNING)
            else:
                return ("Estable", Colors.NEUTRAL)
    
    def _calcular_distancia_al_optimo(self, valor, rango_min, rango_max):
        """
        Calcula la distancia de un valor al rango optimo.
        
        Returns:
            float: 0 si esta dentro del rango, distancia positiva si esta fuera
        """
        if valor < rango_min:
            return rango_min - valor
        elif valor > rango_max:
            return valor - rango_max
        else:
            return 0  # Esta dentro del rango optimo
    
    def _crear_fila_comparativa(self, parent, row, nombre, key, calculator, interpreter):
        """Crea una fila de la tabla comparativa"""
        
        # Calcular valores
        if hasattr(calculator, f'calcular_{key}'):
            valor_y1 = getattr(calculator, f'calcular_{key}')(year=1)
            valor_y2 = getattr(calculator, f'calcular_{key}')(year=2)
        else:
            valor_y1 = 0.0
            valor_y2 = 0.0
        
        # Calcular variacion porcentual
        if valor_y1 != 0:
            variacion = ((valor_y2 - valor_y1) / abs(valor_y1)) * 100
        else:
            variacion = 0.0
        
        # Determinar tendencia basada en PROXIMIDAD AL RANGO OPTIMO
        tendencia, color_tendencia = self._evaluar_tendencia_vs_optimo(
            key, valor_y1, valor_y2, interpreter
        )
        
        # Nombre del ratio
        tk.Label(
            parent,
            text=nombre,
            font=Fonts.NORMAL_BOLD,
            bg=Colors.BG_PRIMARY,
            anchor="w"
        ).grid(row=row, column=0, sticky="ew", padx=5, pady=3)
        
        # año 1
        tk.Label(
            parent,
            text=f"{valor_y1:.2f}",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY
        ).grid(row=row, column=1, padx=5, pady=3)
        
        # año 2
        tk.Label(
            parent,
            text=f"{valor_y2:.2f}",
            font=Fonts.NORMAL,
            bg=Colors.BG_PRIMARY
        ).grid(row=row, column=2, padx=5, pady=3)
        
        # Variacion
        tk.Label(
            parent,
            text=f"{variacion:+.1f}%",
            font=Fonts.NORMAL_BOLD,
            fg=Colors.POSITIVE if variacion > 0 else Colors.NEGATIVE if variacion < 0 else Colors.NEUTRAL,
            bg=Colors.BG_PRIMARY
        ).grid(row=row, column=3, padx=5, pady=3)
        
        # Tendencia (ahora basada en rango optimo)
        tk.Label(
            parent,
            text=tendencia,
            font=Fonts.NORMAL_BOLD,
            fg=color_tendencia,
            bg=Colors.BG_PRIMARY
        ).grid(row=row, column=4, padx=5, pady=3)
    
    def _crear_interpretacion_liquidez(self, parent, calculator, interpreter):
        """Crea la interpretacion de liquidez"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" Interpretacion - Liquidez ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Generar interpretacion
        interpretacion = self._generar_interpretacion_liquidez(calculator, interpreter)
        
        text_widget = tk.Text(
            frame,
            height=8,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.X)
        text_widget.insert('1.0', interpretacion)
        text_widget.config(state='disabled')
    
    def _crear_interpretacion_solvencia(self, parent, calculator, interpreter):
        """Crea la interpretacion de solvencia"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" Interpretacion - Solvencia ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Generar interpretacion
        interpretacion = self._generar_interpretacion_solvencia(calculator, interpreter)
        
        text_widget = tk.Text(
            frame,
            height=8,
            wrap='word',
            font=Fonts.NORMAL,
            bg=Colors.BG_SECONDARY,
            relief='flat',
            padx=10,
            pady=10
        )
        text_widget.pack(fill=tk.X)
        text_widget.insert('1.0', interpretacion)
        text_widget.config(state='disabled')
    
    def _crear_conclusion_general(self, parent, calculator, interpreter):
        """Crea la conclusion general"""
        
        frame = ttk.LabelFrame(
            parent,
            text=" Conclusion General ",
            padding=Dimensions.PADDING_LARGE
        )
        frame.pack(fill=tk.X, padx=Dimensions.PADDING_XLARGE, 
                  pady=Dimensions.PADDING_MEDIUM)
        
        # Generar conclusion
        conclusion = self._generar_conclusion_general(calculator, interpreter)
        
        text_widget = tk.Text(
            frame,
            height=5,
            wrap='word',
            font=Fonts.NORMAL_BOLD,
            bg="#FFFACD",  # Amarillo claro
            relief='flat',
            padx=15,
            pady=10
        )
        text_widget.pack(fill=tk.X)
        text_widget.insert('1.0', conclusion)
        text_widget.config(state='disabled')
    
    def _generar_interpretacion_liquidez(self, calculator, interpreter):
        """Genera la interpretacion de liquidez basada en rangos optimos"""
        
        # Calcular ratios
        r_liq_y1 = calculator.calcular_razon_liquidez(year=1)
        r_liq_y2 = calculator.calcular_razon_liquidez(year=2)
        
        r_teso_y1 = calculator.calcular_razon_tesoreria(year=1)
        r_teso_y2 = calculator.calcular_razon_tesoreria(year=2)
        
        r_disp_y1 = calculator.calcular_razon_disponibilidad(year=1)
        r_disp_y2 = calculator.calcular_razon_disponibilidad(year=2)
        
        # Obtener rangos optimos
        rango_liq = interpreter.get_rango_optimo("razon_liquidez")
        rango_teso = interpreter.get_rango_optimo("razon_tesoreria")
        rango_disp = interpreter.get_rango_optimo("razon_disponibilidad")
        
        # Obtener estados
        estado_liq_y1 = interpreter.get_estado("razon_liquidez", r_liq_y1)
        estado_liq_y2 = interpreter.get_estado("razon_liquidez", r_liq_y2)
        
        estado_teso_y1 = interpreter.get_estado("razon_tesoreria", r_teso_y1)
        estado_teso_y2 = interpreter.get_estado("razon_tesoreria", r_teso_y2)
        
        estado_disp_y1 = interpreter.get_estado("razon_disponibilidad", r_disp_y1)
        estado_disp_y2 = interpreter.get_estado("razon_disponibilidad", r_disp_y2)
        
        texto = f"""ANALISIS DE LIQUIDEZ (año 1 -> año 2):

RAZON DE LIQUIDEZ: Paso de {r_liq_y1:.2f} a {r_liq_y2:.2f}
  - Rango optimo: {rango_liq[0]:.2f} - {rango_liq[1]:.2f}
  - Estado año 1: {estado_liq_y1.upper()} | Estado año 2: {estado_liq_y2.upper()}
  - {self._describir_evolucion_vs_optimo(estado_liq_y1, estado_liq_y2, r_liq_y1, r_liq_y2, rango_liq)}

RAZON DE TESORERIA: Paso de {r_teso_y1:.2f} a {r_teso_y2:.2f}
  - Rango optimo: {rango_teso[0]:.2f} - {rango_teso[1]:.2f}
  - Estado año 1: {estado_teso_y1.upper()} | Estado año 2: {estado_teso_y2.upper()}
  - {self._describir_evolucion_vs_optimo(estado_teso_y1, estado_teso_y2, r_teso_y1, r_teso_y2, rango_teso)}

RAZON DE DISPONIBILIDAD: Paso de {r_disp_y1:.2f} a {r_disp_y2:.2f}
  - Rango optimo: {rango_disp[0]:.2f} - {rango_disp[1]:.2f}
  - Estado año 1: {estado_disp_y1.upper()} | Estado año 2: {estado_disp_y2.upper()}
  - {self._describir_evolucion_vs_optimo(estado_disp_y1, estado_disp_y2, r_disp_y1, r_disp_y2, rango_disp)}"""
        
        return texto
    
    def _generar_interpretacion_solvencia(self, calculator, interpreter):
        """Genera la interpretacion de solvencia basada en rangos optimos"""
        
        # Calcular ratios
        r_gar_y1 = calculator.calcular_ratio_garantia(year=1)
        r_gar_y2 = calculator.calcular_ratio_garantia(year=2)
        
        r_aut_y1 = calculator.calcular_ratio_autonomia(year=1)
        r_aut_y2 = calculator.calcular_ratio_autonomia(year=2)
        
        r_cal_y1 = calculator.calcular_ratio_calidad_deuda(year=1)
        r_cal_y2 = calculator.calcular_ratio_calidad_deuda(year=2)
        
        # Obtener rangos optimos
        rango_gar = interpreter.get_rango_optimo("ratio_garantia")
        rango_aut = interpreter.get_rango_optimo("ratio_autonomia")
        rango_cal = interpreter.get_rango_optimo("ratio_calidad_deuda")
        
        # Obtener estados
        estado_gar_y1 = interpreter.get_estado("ratio_garantia", r_gar_y1)
        estado_gar_y2 = interpreter.get_estado("ratio_garantia", r_gar_y2)
        
        estado_aut_y1 = interpreter.get_estado("ratio_autonomia", r_aut_y1)
        estado_aut_y2 = interpreter.get_estado("ratio_autonomia", r_aut_y2)
        
        estado_cal_y1 = interpreter.get_estado("ratio_calidad_deuda", r_cal_y1)
        estado_cal_y2 = interpreter.get_estado("ratio_calidad_deuda", r_cal_y2)
        
        texto = f"""ANALISIS DE SOLVENCIA (año 1 -> año 2):

RATIO DE GARANTIA: Paso de {r_gar_y1:.2f} a {r_gar_y2:.2f}
  - Rango optimo: {rango_gar[0]:.2f} - {rango_gar[1]:.2f}
  - Estado año 1: {estado_gar_y1.upper()} | Estado año 2: {estado_gar_y2.upper()}
  - {self._describir_evolucion_vs_optimo(estado_gar_y1, estado_gar_y2, r_gar_y1, r_gar_y2, rango_gar)}

RATIO DE AUTONOMIA: Paso de {r_aut_y1:.2f} a {r_aut_y2:.2f}
  - Rango optimo: {rango_aut[0]:.2f} - {rango_aut[1]:.2f}
  - Estado año 1: {estado_aut_y1.upper()} | Estado año 2: {estado_aut_y2.upper()}
  - {self._describir_evolucion_vs_optimo(estado_aut_y1, estado_aut_y2, r_aut_y1, r_aut_y2, rango_aut)}

RATIO DE CALIDAD DE DEUDA: Paso de {r_cal_y1:.2f} a {r_cal_y2:.2f}
  - Rango optimo: {rango_cal[0]:.2f} - {rango_cal[1]:.2f}
  - Estado año 1: {estado_cal_y1.upper()} | Estado año 2: {estado_cal_y2.upper()}
  - {self._describir_evolucion_vs_optimo(estado_cal_y1, estado_cal_y2, r_cal_y1, r_cal_y2, rango_cal)}"""
        
        return texto
    
    def _describir_evolucion_vs_optimo(self, estado_y1, estado_y2, valor_y1, valor_y2, rango):
        """Genera descripcion de la evolucion respecto al rango optimo"""
        
        rango_min, rango_max = rango
        
        # Ambos optimos
        if estado_y1 == "optimo" and estado_y2 == "optimo":
            return "Se mantiene dentro del rango optimo. Excelente."
        
        # Entro al optimo
        if estado_y1 != "optimo" and estado_y2 == "optimo":
            return f"MEJORA: Entro al rango optimo desde un nivel {estado_y1}."
        
        # Salio del optimo
        if estado_y1 == "optimo" and estado_y2 != "optimo":
            return f"DETERIORO: Salio del rango optimo hacia un nivel {estado_y2}."
        
        # Ambos fuera - calcular si se acerco o alejo
        dist_y1 = self._calcular_distancia_al_optimo(valor_y1, rango_min, rango_max)
        dist_y2 = self._calcular_distancia_al_optimo(valor_y2, rango_min, rango_max)
        
        if dist_y2 < dist_y1:
            return f"MEJORA: Se acerca al rango optimo (aun {estado_y2})."
        elif dist_y2 > dist_y1:
            return f"DETERIORO: Se aleja del rango optimo (sigue {estado_y2})."
        else:
            return f"ESTABLE: Se mantiene fuera del optimo ({estado_y2})."
    
    def _generar_conclusion_general(self, calculator, interpreter):
        """Genera la conclusion general basada en rangos optimos"""
        
        # Evaluar cada ratio vs su rango optimo
        ratios = [
            ('razon_liquidez', calculator.calcular_razon_liquidez),
            ('razon_tesoreria', calculator.calcular_razon_tesoreria),
            ('razon_disponibilidad', calculator.calcular_razon_disponibilidad),
            ('ratio_garantia', calculator.calcular_ratio_garantia),
            ('ratio_autonomia', calculator.calcular_ratio_autonomia),
            ('ratio_calidad_deuda', calculator.calcular_ratio_calidad_deuda)
        ]
        
        mejoras = 0
        empeoramientos = 0
        estables_optimos = 0
        estables_fuera = 0
        
        for key, calc_func in ratios:
            valor_y1 = calc_func(year=1)
            valor_y2 = calc_func(year=2)
            
            estado_y1 = interpreter.get_estado(key, valor_y1)
            estado_y2 = interpreter.get_estado(key, valor_y2)
            rango = interpreter.get_rango_optimo(key)
            
            if rango is None:
                continue
            
            rango_min, rango_max = rango
            dist_y1 = self._calcular_distancia_al_optimo(valor_y1, rango_min, rango_max)
            dist_y2 = self._calcular_distancia_al_optimo(valor_y2, rango_min, rango_max)
            
            # Clasificar cambio
            if estado_y1 == "optimo" and estado_y2 == "optimo":
                estables_optimos += 1
            elif estado_y1 != "optimo" and estado_y2 == "optimo":
                mejoras += 1
            elif estado_y1 == "optimo" and estado_y2 != "optimo":
                empeoramientos += 1
            elif dist_y2 < dist_y1 - 0.05:  # Se acerco significativamente
                mejoras += 1
            elif dist_y2 > dist_y1 + 0.05:  # Se alejo significativamente
                empeoramientos += 1
            else:
                estables_fuera += 1
        
        # Generar conclusion
        total = mejoras + empeoramientos + estables_optimos + estables_fuera
        
        if mejoras > empeoramientos and estables_optimos >= 2:
            conclusion = f"""CONCLUSION: La posicion financiera de la empresa MEJORO entre el año 1 y el año 2.

Indicadores que mejoraron (se acercaron al optimo): {mejoras}
Indicadores que empeoraron (se alejaron del optimo): {empeoramientos}
Indicadores estables en rango optimo: {estables_optimos}
Indicadores estables fuera del optimo: {estables_fuera}

La empresa muestra una tendencia positiva, acercandose a los rangos optimos recomendados."""
        
        elif empeoramientos > mejoras:
            conclusion = f"""CONCLUSION: La posicion financiera de la empresa EMPEORO entre el año 1 y el año 2.

Indicadores que mejoraron (se acercaron al optimo): {mejoras}
Indicadores que empeoraron (se alejaron del optimo): {empeoramientos}
Indicadores estables en rango optimo: {estables_optimos}
Indicadores estables fuera del optimo: {estables_fuera}

La empresa muestra una tendencia negativa, alejandose de los rangos optimos. Se requieren acciones correctivas."""
        
        else:
            conclusion = f"""CONCLUSION: La posicion financiera de la empresa se MANTUVO ESTABLE entre el año 1 y el año 2.

Indicadores que mejoraron (se acercaron al optimo): {mejoras}
Indicadores que empeoraron (se alejaron del optimo): {empeoramientos}
Indicadores estables en rango optimo: {estables_optimos}
Indicadores estables fuera del optimo: {estables_fuera}

Los indicadores no muestran cambios significativos respecto a los rangos optimos."""
        
        return conclusion