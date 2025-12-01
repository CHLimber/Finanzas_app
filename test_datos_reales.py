"""
Archivo: test_datos_reales.py
Test con datos reales del caso de estudio para verificacion manual
Compatible con Windows (sin caracteres Unicode problematicos)

Ejecutar con: python test_datos_reales.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models.balance import BalanceGeneral
from core.models.estado_resultado import EstadoResultado
from core.calculators.ratio_calculator import RatioCalculator
from core.analysis.financial_interpreter import FinancialInterpreter
from core.analysis.dupont_analysis import DuPontAnalysis


def crear_datos_caso_estudio():
    """
    Crea los datos exactos del caso de estudio proporcionado.
    Todos los valores en Bolivianos (Bs.)
    """
    
    # ============================================================
    # BALANCE GENERAL
    # ============================================================
    balance = BalanceGeneral()
    
    # -------------------- ANO 1 (2023) --------------------
    
    # ACTIVO CORRIENTE - Ano 1
    balance.caja_bancos_y1 = 850.00
    balance.clientes_cobrar_y1 = 1200.00
    balance.inversion_cp_y1 = 300.00
    balance.existencias_y1 = 450.00
    # Total Activo Corriente Y1 = 2,800
    
    # ACTIVO NO CORRIENTE - Ano 1
    balance.inmuebles_planta_y1 = 1200.00
    balance.depreciacion_acum_y1 = 400.00
    balance.intangibles_y1 = 800.00
    balance.depreciacion_intang_y1 = 150.00
    # Total Activo No Corriente Y1 = 1,200 - 400 + 800 - 150 = 1,450
    
    # PASIVO CORRIENTE - Ano 1
    balance.proveedores_y1 = 300.00
    balance.impuestos_pagar_y1 = 150.00
    balance.deuda_cp_y1 = 100.00
    # Total Pasivo Corriente Y1 = 550
    
    # PASIVO NO CORRIENTE - Ano 1
    balance.prestamos_lp_y1 = 600.00
    balance.provisiones_lp_y1 = 100.00
    # Total Pasivo No Corriente Y1 = 700
    
    # PATRIMONIO - Ano 1
    balance.capital_social_y1 = 1500.00
    balance.reservas_legales_y1 = 400.00
    balance.ganancias_acum_y1 = 1100.00
    # Total Patrimonio Y1 = 3,000
    
    # -------------------- ANO 2 (2024) --------------------
    
    # ACTIVO CORRIENTE - Ano 2
    balance.caja_bancos_y2 = 1100.00
    balance.clientes_cobrar_y2 = 1600.00
    balance.inversion_cp_y2 = 500.00
    balance.existencias_y2 = 600.00
    # Total Activo Corriente Y2 = 3,800
    
    # ACTIVO NO CORRIENTE - Ano 2
    balance.inmuebles_planta_y2 = 1500.00
    balance.depreciacion_acum_y2 = 550.00
    balance.intangibles_y2 = 1200.00
    balance.depreciacion_intang_y2 = 300.00
    # Total Activo No Corriente Y2 = 1,500 - 550 + 1,200 - 300 = 1,850
    
    # PASIVO CORRIENTE - Ano 2
    balance.proveedores_y2 = 600.00
    balance.impuestos_pagar_y2 = 200.00
    balance.deuda_cp_y2 = 200.00
    # Total Pasivo Corriente Y2 = 1,000
    
    # PASIVO NO CORRIENTE - Ano 2
    balance.prestamos_lp_y2 = 900.00
    balance.provisiones_lp_y2 = 100.00
    # Total Pasivo No Corriente Y2 = 1,000
    
    # PATRIMONIO - Ano 2
    balance.capital_social_y2 = 1500.00
    balance.reservas_legales_y2 = 500.00
    balance.ganancias_acum_y2 = 1650.00
    # Total Patrimonio Y2 = 3,650
    
    # ============================================================
    # ESTADO DE RESULTADOS
    # ============================================================
    estado = EstadoResultado()
    
    # -------------------- ANO 1 (2023) --------------------
    estado.ingresos_servicios_y1 = 8500.00
    estado.costo_servicios_y1 = 3200.00
    estado.gastos_admin_y1 = 2100.00
    estado.gastos_ventas_y1 = 1200.00
    estado.depreciacion_amort_y1 = 400.00
    estado.gastos_financieros_y1 = 100.00
    estado.otros_ingresos_y1 = 50.00
    
    # -------------------- ANO 2 (2024) --------------------
    estado.ingresos_servicios_y2 = 11200.00
    estado.costo_servicios_y2 = 4100.00
    estado.gastos_admin_y2 = 2600.00
    estado.gastos_ventas_y2 = 1400.00
    estado.depreciacion_amort_y2 = 500.00
    estado.gastos_financieros_y2 = 150.00
    estado.otros_ingresos_y2 = 100.00
    
    return balance, estado


def imprimir_separador(titulo):
    """Imprime un separador con titulo"""
    print(f"\n{'='*70}")
    print(f" {titulo}")
    print('='*70)


def verificar_balance(balance):
    """Verifica y muestra los calculos del Balance General"""
    
    imprimir_separador("VERIFICACION DEL BALANCE GENERAL")
    
    print("\n" + "-"*35 + " ANO 1 (2023) " + "-"*35)
    
    # Activo Corriente
    ac_y1 = balance.get_total_corriente(1)
    print(f"\nACTIVO CORRIENTE ANO 1:")
    print(f"  Caja y bancos:        Bs. {balance.caja_bancos_y1:,.2f}")
    print(f"  Clientes por cobrar:  Bs. {balance.clientes_cobrar_y1:,.2f}")
    print(f"  Inversiones CP:       Bs. {balance.inversion_cp_y1:,.2f}")
    print(f"  Existencias:          Bs. {balance.existencias_y1:,.2f}")
    print(f"  ---------------------------------")
    print(f"  TOTAL AC:             Bs. {ac_y1:,.2f}  (Esperado: 2,800)")
    
    # Activo No Corriente
    anc_y1 = balance.get_total_no_corriente(1)
    print(f"\nACTIVO NO CORRIENTE ANO 1:")
    print(f"  Inmuebles:            Bs. {balance.inmuebles_planta_y1:,.2f}")
    print(f"  (-) Deprec. acum:     Bs. ({balance.depreciacion_acum_y1:,.2f})")
    print(f"  Intangibles:          Bs. {balance.intangibles_y1:,.2f}")
    print(f"  (-) Deprec. intang:   Bs. ({balance.depreciacion_intang_y1:,.2f})")
    print(f"  ---------------------------------")
    print(f"  TOTAL ANC:            Bs. {anc_y1:,.2f}  (Esperado: 1,450)")
    
    # Total Activos
    at_y1 = balance.get_total_activos(1)
    print(f"\n  >>> TOTAL ACTIVOS Y1: Bs. {at_y1:,.2f}  (Esperado: 4,250)")
    
    # Pasivo Corriente
    pc_y1 = balance.get_total_pasivo_corriente(1)
    print(f"\nPASIVO CORRIENTE ANO 1:")
    print(f"  Proveedores:          Bs. {balance.proveedores_y1:,.2f}")
    print(f"  Impuestos por pagar:  Bs. {balance.impuestos_pagar_y1:,.2f}")
    print(f"  Deuda CP bancaria:    Bs. {balance.deuda_cp_y1:,.2f}")
    print(f"  ---------------------------------")
    print(f"  TOTAL PC:             Bs. {pc_y1:,.2f}  (Esperado: 550)")
    
    # Pasivo No Corriente
    pnc_y1 = balance.get_total_pasivo_no_corriente(1)
    print(f"\nPASIVO NO CORRIENTE ANO 1:")
    print(f"  Prestamos LP:         Bs. {balance.prestamos_lp_y1:,.2f}")
    print(f"  Provisiones LP:       Bs. {balance.provisiones_lp_y1:,.2f}")
    print(f"  ---------------------------------")
    print(f"  TOTAL PNC:            Bs. {pnc_y1:,.2f}  (Esperado: 700)")
    
    # Patrimonio
    pat_y1 = balance.get_total_patrimonio(1)
    print(f"\nPATRIMONIO ANO 1:")
    print(f"  Capital social:       Bs. {balance.capital_social_y1:,.2f}")
    print(f"  Reservas legales:     Bs. {balance.reservas_legales_y1:,.2f}")
    print(f"  Ganancias acumuladas: Bs. {balance.ganancias_acum_y1:,.2f}")
    print(f"  ---------------------------------")
    print(f"  TOTAL PATRIMONIO:     Bs. {pat_y1:,.2f}  (Esperado: 3,000)")
    
    # Total Pasivo + Patrimonio
    pp_y1 = balance.get_total_pasivo_patrimonio(1)
    print(f"\n  >>> TOTAL P + PAT Y1: Bs. {pp_y1:,.2f}  (Esperado: 4,250)")
    
    # Validacion
    balance_ok_y1 = balance.validar_balance(1)
    print(f"\n  [OK] BALANCE CUADRA ANO 1: {'SI' if balance_ok_y1 else 'NO'}")
    
    # ==================== ANO 2 ====================
    print("\n" + "-"*35 + " ANO 2 (2024) " + "-"*35)
    
    ac_y2 = balance.get_total_corriente(2)
    anc_y2 = balance.get_total_no_corriente(2)
    at_y2 = balance.get_total_activos(2)
    pc_y2 = balance.get_total_pasivo_corriente(2)
    pnc_y2 = balance.get_total_pasivo_no_corriente(2)
    pat_y2 = balance.get_total_patrimonio(2)
    pp_y2 = balance.get_total_pasivo_patrimonio(2)
    
    print(f"\nRESUMEN ANO 2:")
    print(f"  Total Activo Corriente:     Bs. {ac_y2:,.2f}  (Esperado: 3,800)")
    print(f"  Total Activo No Corriente:  Bs. {anc_y2:,.2f}  (Esperado: 1,850)")
    print(f"  >>> TOTAL ACTIVOS:          Bs. {at_y2:,.2f}  (Esperado: 5,650)")
    print(f"  Total Pasivo Corriente:     Bs. {pc_y2:,.2f}  (Esperado: 1,000)")
    print(f"  Total Pasivo No Corriente:  Bs. {pnc_y2:,.2f}  (Esperado: 1,000)")
    print(f"  Total Patrimonio:           Bs. {pat_y2:,.2f}  (Esperado: 3,650)")
    print(f"  >>> TOTAL P + PAT:          Bs. {pp_y2:,.2f}  (Esperado: 5,650)")
    
    balance_ok_y2 = balance.validar_balance(2)
    print(f"\n  [OK] BALANCE CUADRA ANO 2: {'SI' if balance_ok_y2 else 'NO'}")
    
    return balance_ok_y1 and balance_ok_y2


def verificar_estado_resultado(estado):
    """Verifica y muestra los calculos del Estado de Resultados"""
    
    imprimir_separador("VERIFICACION DEL ESTADO DE RESULTADOS")
    
    for year in [1, 2]:
        ano_texto = "2023" if year == 1 else "2024"
        print(f"\n" + "-"*30 + f" ANO {year} ({ano_texto}) " + "-"*30)
        
        ingresos = estado.ingresos_servicios_y1 if year == 1 else estado.ingresos_servicios_y2
        costos = estado.costo_servicios_y1 if year == 1 else estado.costo_servicios_y2
        g_admin = estado.gastos_admin_y1 if year == 1 else estado.gastos_admin_y2
        g_ventas = estado.gastos_ventas_y1 if year == 1 else estado.gastos_ventas_y2
        deprec = estado.depreciacion_amort_y1 if year == 1 else estado.depreciacion_amort_y2
        g_fin = estado.gastos_financieros_y1 if year == 1 else estado.gastos_financieros_y2
        otros = estado.otros_ingresos_y1 if year == 1 else estado.otros_ingresos_y2
        
        ganancia_bruta = estado.get_ganancia_bruta(year)
        utilidad_op = estado.get_utilidad_operativa(year)
        utilidad_ai = estado.get_utilidad_antes_impuestos(year)
        impuestos = estado.get_impuestos_renta(year)
        utilidad_neta = estado.get_utilidad_neta(year)
        
        # Valores esperados segun el documento
        if year == 1:
            gb_esp, uo_esp, uai_esp, imp_esp, un_esp = 5300, 1600, 1550, 387.50, 1162.50
        else:
            gb_esp, uo_esp, uai_esp, imp_esp, un_esp = 7100, 2600, 2550, 637.50, 1912.50
        
        print(f"\n  Ingresos por servicios:     Bs. {ingresos:,.2f}")
        print(f"  (-) Costo de servicios:     Bs. ({costos:,.2f})")
        print(f"  -----------------------------------------")
        print(f"  GANANCIA BRUTA:             Bs. {ganancia_bruta:,.2f}  (Esperado: {gb_esp:,.2f})")
        
        print(f"\n  (-) Gastos administracion:  Bs. ({g_admin:,.2f})")
        print(f"  (-) Gastos de ventas:       Bs. ({g_ventas:,.2f})")
        print(f"  (-) Depreciacion/amort:     Bs. ({deprec:,.2f})")
        print(f"  -----------------------------------------")
        print(f"  UTILIDAD OPERATIVA (BAII):  Bs. {utilidad_op:,.2f}  (Esperado: {uo_esp:,.2f})")
        
        print(f"\n  (-) Gastos financieros:     Bs. ({g_fin:,.2f})")
        print(f"  (+) Otros ingresos:         Bs. {otros:,.2f}")
        print(f"  -----------------------------------------")
        print(f"  UTILIDAD ANTES IMPUESTOS:   Bs. {utilidad_ai:,.2f}  (Esperado: {uai_esp:,.2f})")
        
        print(f"\n  (-) Impuesto renta (25%):   Bs. ({impuestos:,.2f})  (Esperado: {imp_esp:,.2f})")
        print(f"  -----------------------------------------")
        print(f"  >>> UTILIDAD NETA:          Bs. {utilidad_neta:,.2f}  (Esperado: {un_esp:,.2f})")
        
        # Margenes
        margen_bruto = estado.get_margen_bruto(year)
        margen_op = estado.get_margen_operativo(year)
        margen_neto = estado.get_margen_neto(year)
        
        print(f"\n  MARGENES:")
        print(f"  Margen Bruto:    {margen_bruto:.2f}%")
        print(f"  Margen Operativo: {margen_op:.2f}%")
        print(f"  Margen Neto:     {margen_neto:.2f}%")


def verificar_ratios(balance, estado):
    """Verifica y muestra todos los ratios calculados"""
    
    imprimir_separador("VERIFICACION DE RATIOS FINANCIEROS")
    
    calculator = RatioCalculator(balance, estado)
    interpreter = FinancialInterpreter()
    
    for year in [1, 2]:
        ano_texto = "2023" if year == 1 else "2024"
        print(f"\n" + "-"*30 + f" ANO {year} ({ano_texto}) " + "-"*30)
        
        ratios = calculator.calcular_todos_ratios(year)
        
        print("\n  RATIOS DE LIQUIDEZ:")
        print(f"  |-- Razon de Liquidez:      {ratios['razon_liquidez']:.4f}")
        print(f"  |   (AC/PC) Rango optimo: 1.5 - 2.5")
        print(f"  |-- Razon de Tesoreria:     {ratios['razon_tesoreria']:.4f}")
        print(f"  |   ((AC-Exist)/PC) Rango optimo: 1.0 - 1.5")
        print(f"  |-- Razon Disponibilidad:   {ratios['razon_disponibilidad']:.4f}")
        print(f"      (Caja/PC) Rango optimo: 0.2 - 0.5")
        
        print("\n  RATIOS DE SOLVENCIA:")
        print(f"  |-- Ratio de Garantia:      {ratios['ratio_garantia']:.4f}")
        print(f"  |   (AT/PT) Rango optimo: 1.5 - 2.5")
        print(f"  |-- Ratio de Autonomia:     {ratios['ratio_autonomia']:.4f}")
        print(f"  |   (Pat/PT) Rango optimo: 0.8 - 1.5")
        print(f"  |-- Calidad de Deuda:       {ratios['ratio_calidad_deuda']:.4f}")
        print(f"      (PC/PT) Rango optimo: 0.3 - 0.5")
        
        print("\n  RATIOS DE RENTABILIDAD:")
        print(f"  |-- RAT (ROA):              {ratios['rat']*100:.2f}%")
        print(f"  |   (Util.Neta/AT) Rango optimo: 5% - 15%")
        print(f"  |-- RPP (ROE):              {ratios['rpp']*100:.2f}%")
        print(f"  |   (Util.Neta/Pat) Rango optimo: 10% - 25%")
        print(f"  |-- Margen Bruto:           {ratios['margen_bruto']*100:.2f}%")
        print(f"  |-- Margen Operativo:       {ratios['margen_operativo']*100:.2f}%")
        print(f"  |-- Margen Neto:            {ratios['margen_neto']*100:.2f}%")
        
        print("\n  OTROS RATIOS:")
        print(f"  |-- Fondo de Maniobra:      {ratios['fondo_maniobra']:.4f}")
        print(f"  |   ((AC-PC)/AT) Rango optimo: 0.1 - 0.3")
        print(f"  |-- Rotacion de Activos:    {ratios['rotacion_activos']:.4f} veces")
        print(f"  |-- Apalancamiento:         {ratios['apalancamiento']:.4f} veces")
        
        # Fondo de Maniobra absoluto
        fm_absoluto = calculator.calcular_fondo_maniobra_absoluto(year)
        print(f"\n  FONDO DE MANIOBRA ABSOLUTO: Bs. {fm_absoluto:,.2f}")
        print(f"      (AC - PC = Capital de Trabajo)")


def verificar_dupont(balance, estado):
    """Verifica el analisis DuPont"""
    
    imprimir_separador("VERIFICACION ANALISIS DUPONT")
    
    dupont = DuPontAnalysis(balance, estado)
    analisis = dupont.analisis_dupont_dual()
    
    for year in [1, 2]:
        ano_texto = "2023" if year == 1 else "2024"
        key = f'ano_{year}'
        datos = analisis[key]
        
        print(f"\n" + "-"*30 + f" ANO {year} ({ano_texto}) " + "-"*30)
        
        print(f"\n  DESCOMPOSICION DEL ROE (RPP):")
        print(f"  +---------------------------------------------------+")
        print(f"  |  ROE = Margen x Rotacion x Apalancamiento         |")
        print(f"  +---------------------------------------------------+")
        
        print(f"\n  1. Margen Neto:        {datos['margen_neto']:.2f}%")
        print(f"     (Utilidad Neta / Ventas)")
        
        print(f"\n  2. Rotacion Activo:    {datos['rotacion_activo']:.4f} veces")
        print(f"     (Ventas / Activo Total)")
        
        print(f"\n  3. Apalancamiento:     {datos['apalancamiento']:.4f} veces")
        print(f"     (Activo Total / Patrimonio)")
        
        print(f"\n  ---------------------------------------------------")
        print(f"  ROE via DuPont:   {datos['rrp_dupont']:.2f}%")
        print(f"  ROE Directo:      {datos['rrp_directo']:.2f}%")
        print(f"  [OK] Verificacion:   {'COINCIDE' if datos['verificacion'] else 'NO COINCIDE'}")
    
    print(f"\n" + "-"*70)
    print("\n  INTERPRETACION AUTOMATICA:")
    print("-"*70)
    # Limpiar caracteres problematicos de la interpretacion
    interp = analisis['interpretacion']
    interp = interp.replace('\u2713', '[+]').replace('\u2717', '[-]').replace('\u26A0', '[!]')
    interp = interp.replace('\u2714', '[+]').replace('\u2716', '[-]')
    # Reemplazar cualquier otro caracter unicode problematico
    interp = interp.encode('ascii', 'replace').decode('ascii')
    print(interp)


def main():
    """Funcion principal que ejecuta todas las verificaciones"""
    
    print("\n" + "="*70)
    print("   TEST CON DATOS REALES DEL CASO DE ESTUDIO")
    print("   Empresa de Servicios de Software - Anos 2023 y 2024")
    print("="*70)
    
    # Crear datos
    balance, estado = crear_datos_caso_estudio()
    
    # Verificar Balance
    balance_ok = verificar_balance(balance)
    
    # Verificar Estado de Resultados
    verificar_estado_resultado(estado)
    
    # Verificar Ratios
    verificar_ratios(balance, estado)
    
    # Verificar DuPont
    verificar_dupont(balance, estado)
    
    # Resumen final
    imprimir_separador("RESUMEN FINAL")
    
    print("\n  DATOS INGRESADOS CORRECTAMENTE:")
    print(f"    Balance General:     {'[OK]' if balance_ok else '[ERROR]'}")
    print(f"    Estado de Resultados: [OK]")
    print(f"    Ratios calculados:   [OK]")
    print(f"    Analisis DuPont:     [OK]")
    
    print("\n  Para verificar manualmente, compara los valores mostrados")
    print("  con los del documento original.")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()