import matplotlib.pyplot as plt
import numpy as np

def grafico_analisis_financiero(datos_año1, datos_año2, año1="Año 1", año2="Año 2"):
    """
    Gráfico de Análisis Financiero - Liquidez y Solvencia
    
    Parámetros:
    datos_año1 y datos_año2 son diccionarios con las claves:
    {
        'liquidez_general': float,
        'tesoreria': float,
        'disponibilidad': float,
        'garantia': float,
        'autonomia': float,
        'calidad_deuda': float
    }
    """
    fig = plt.figure(figsize=(16, 10))
    
    # Título principal
    fig.suptitle('ANÁLISIS FINANCIERO - LIQUIDEZ Y SOLVENCIA', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # ============ RATIOS DE LIQUIDEZ ============
    ax1 = plt.subplot(2, 1, 1)
    
    # Datos de liquidez
    categorias_liquidez = ['Liquidez\nGeneral', 'Razón de\nTesorería', 'Razón de\nDisponibilidad']
    valores_año1_liq = [
        datos_año1['liquidez_general'],
        datos_año1['tesoreria'],
        datos_año1['disponibilidad']
    ]
    valores_año2_liq = [
        datos_año2['liquidez_general'],
        datos_año2['tesoreria'],
        datos_año2['disponibilidad']
    ]
    
    x = np.arange(len(categorias_liquidez))
    ancho = 0.35
    
    barras1 = ax1.bar(x - ancho/2, valores_año1_liq, ancho, label=año1, 
                      color='#4169E1', edgecolor='black', linewidth=1.5)
    barras2 = ax1.bar(x + ancho/2, valores_año2_liq, ancho, label=año2,
                      color='#48D1CC', edgecolor='black', linewidth=1.5)
    
    # Añadir valores sobre las barras
    for barras in [barras1, barras2]:
        for barra in barras:
            height = barra.get_height()
            ax1.text(barra.get_x() + barra.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Línea de referencia en 1.0 para liquidez
    ax1.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Referencia mínima')
    
    ax1.set_ylabel('Ratio', fontsize=12, fontweight='bold')
    ax1.set_title('RATIOS DE LIQUIDEZ', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categorias_liquidez, fontsize=11)
    ax1.legend(fontsize=10, loc='upper right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    # ============ RATIOS DE SOLVENCIA ============
    ax2 = plt.subplot(2, 1, 2)
    
    # Datos de solvencia
    categorias_solvencia = ['Ratio de\nGarantía', 'Ratio de\nAutonomía', 'Calidad de\nDeuda']
    valores_año1_solv = [
        datos_año1['garantia'],
        datos_año1['autonomia'],
        datos_año1['calidad_deuda']
    ]
    valores_año2_solv = [
        datos_año2['garantia'],
        datos_año2['autonomia'],
        datos_año2['calidad_deuda']
    ]
    
    x2 = np.arange(len(categorias_solvencia))
    
    barras3 = ax2.bar(x2 - ancho/2, valores_año1_solv, ancho, label=año1,
                      color='#FFA500', edgecolor='black', linewidth=1.5)
    barras4 = ax2.bar(x2 + ancho/2, valores_año2_solv, ancho, label=año2,
                      color='#FFD700', edgecolor='black', linewidth=1.5)
    
    # Añadir valores sobre las barras
    for barras in [barras3, barras4]:
        for barra in barras:
            height = barra.get_height()
            ax2.text(barra.get_x() + barra.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.set_ylabel('Ratio', fontsize=12, fontweight='bold')
    ax2.set_title('RATIOS DE SOLVENCIA', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(categorias_solvencia, fontsize=11)
    ax2.legend(fontsize=10, loc='upper right')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    plt.tight_layout()
    return fig


def grafico_analisis_economico(datos_año1, datos_año2, año1="Año 1", año2="Año 2", benchmark_roa=None, benchmark_roe=None):
    """
    Gráfico de Análisis Económico - Rentabilidad
    
    Parámetros:
    datos_año1 y datos_año2 son diccionarios con las claves:
    {
        'roa': float,  # Return on Assets (%)
        'roe': float,  # Return on Equity (%)
        'margen_neto': float,  # (%)
        'rotacion_activo': float,
        'apalancamiento': float,
        'margen_bruto': float,  # (%)
        'margen_operativo': float  # (%)
    }
    benchmark_roa, benchmark_roe: valores de referencia del sector (opcional)
    """
    fig = plt.figure(figsize=(16, 12))
    
    # Título principal
    fig.suptitle('ANÁLISIS ECONÓMICO - RENTABILIDAD\nRENTABILIDAD ECONÓMICA Y FINANCIERA', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # ============ RENTABILIDAD ECONÓMICA Y FINANCIERA (ROA/ROE) ============
    ax1 = plt.subplot(3, 1, 1)
    
    categorias_rent = ['ROA\n(Return on Assets)', 'ROE\n(Return on Equity)']
    valores_año1_rent = [datos_año1['roa'], datos_año1['roe']]
    valores_año2_rent = [datos_año2['roa'], datos_año2['roe']]
    
    x = np.arange(len(categorias_rent))
    ancho = 0.35
    
    barras1 = ax1.bar(x - ancho/2, valores_año1_rent, ancho, label=año1,
                      color="#2133D2", edgecolor='black', linewidth=1.5)
    barras2 = ax1.bar(x + ancho/2, valores_año2_rent, ancho, label=año2,
                      color="#961EB4", edgecolor='black', linewidth=1.5)
    
    # Añadir valores sobre las barras
    for barras in [barras1, barras2]:
        for barra in barras:
            height = barra.get_height()
            ax1.text(barra.get_x() + barra.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    
    ax1.set_ylabel('Rentabilidad (%)', fontsize=12, fontweight='bold')
    ax1.set_title('', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categorias_rent, fontsize=11)
    ax1.legend(fontsize=9, loc='upper right')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_axisbelow(True)
    
    # ============ ANÁLISIS DUPONT ============
    ax2 = plt.subplot(3, 1, 2)
    
    categorias_dupont = ['Rotación del\nActivo', 'Apalancamiento\nFinanciero']
    valores_año1_dupont = [datos_año1['rotacion_activo'], datos_año1['apalancamiento']]
    valores_año2_dupont = [datos_año2['rotacion_activo'], datos_año2['apalancamiento']]
    
    x2 = np.arange(len(categorias_dupont))
    
    # Crear líneas con puntos
    for i in range(len(categorias_dupont)):
        # Línea de conexión
        ax2.plot([x2[i]-0.15, x2[i]+0.15], 
                [valores_año1_dupont[i], valores_año2_dupont[i]],
                'o-', linewidth=3, markersize=12, color='#9B59B6', alpha=0.6)
        
        # Puntos destacados
        ax2.plot(x2[i]-0.15, valores_año1_dupont[i], 'o', 
                markersize=15, color='#8E44AD', label=año1 if i==0 else "", 
                markeredgecolor='black', markeredgewidth=2)
        ax2.plot(x2[i]+0.15, valores_año2_dupont[i], 'o',
                markersize=15, color="#DD2323", label=año2 if i==0 else "",
                markeredgecolor='black', markeredgewidth=2)
        
        # Valores
        ax2.text(x2[i]-0.15, valores_año1_dupont[i], f'{valores_año1_dupont[i]:.2f}',
                ha='right', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
        ax2.text(x2[i]+0.15, valores_año2_dupont[i], f'{valores_año2_dupont[i]:.2f}',
                ha='left', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
    
    ax2.set_ylabel('Ratio', fontsize=12, fontweight='bold')
    ax2.set_title('ANÁLISIS DUPONT', fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(categorias_dupont, fontsize=11)
    ax2.legend(fontsize=10, loc='upper right')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_axisbelow(True)
    
    # ============ MÁRGENES DE GANANCIA ============
    ax3 = plt.subplot(3, 1, 3)
    
    categorias_margenes = ['Margen\nBruto', 'Margen\nOperativo', 'Margen\nNeto']
    valores_año1_marg = [datos_año1['margen_bruto'], datos_año1['margen_operativo'], datos_año1['margen_neto']]
    valores_año2_marg = [datos_año2['margen_bruto'], datos_año2['margen_operativo'], datos_año2['margen_neto']]
    
    x3 = np.arange(len(categorias_margenes))
    
    # Crear líneas con puntos para cada margen
    colores = ['#E74C3C', '#3498DB', '#F39C12']
    
    for i in range(len(categorias_margenes)):
        # Línea de conexión
        ax3.plot([x3[i]-0.2, x3[i]+0.2], 
                [valores_año1_marg[i], valores_año2_marg[i]],
                'o-', linewidth=3, markersize=12, color=colores[i], alpha=0.6)
        
        # Puntos destacados
        ax3.plot(x3[i]-0.2, valores_año1_marg[i], 'o',
                markersize=15, color=colores[i], label=f'{categorias_margenes[i]} {año1}',
                markeredgecolor='black', markeredgewidth=2, alpha=0.8)
        ax3.plot(x3[i]+0.2, valores_año2_marg[i], 'o',
                markersize=15, color=colores[i], 
                markeredgecolor='black', markeredgewidth=2)
        
        # Valores
        ax3.text(x3[i]-0.2, valores_año1_marg[i], f'{valores_año1_marg[i]:.1f}%',
                ha='right', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
        ax3.text(x3[i]+0.2, valores_año2_marg[i], f'{valores_año2_marg[i]:.1f}%',
                ha='left', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='black'))
    
    # Etiquetas de año en la parte inferior
    ax3.text(-0.3, min(min(valores_año1_marg), min(valores_año2_marg)) * 0.95,
            año1, ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue'))
    ax3.text(len(categorias_margenes)-0.7, min(min(valores_año1_marg), min(valores_año2_marg)) * 0.95,
            año2, ha='center', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen'))
    
    ax3.set_ylabel('Margen (%)', fontsize=12, fontweight='bold')
    ax3.set_title('MÁRGENES DE GANANCIA', fontsize=14, fontweight='bold', pad=15)
    ax3.set_xticks(x3)
    ax3.set_xticklabels(categorias_margenes, fontsize=11)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.set_axisbelow(True)
    
    plt.tight_layout()
    return fig


# ============ EJEMPLO DE USO ============
if __name__ == "__main__":
    
    # Datos de ejemplo para Análisis Financiero
    datos_financiero_2023 = {
        'liquidez_general': 1.8,
        'tesoreria': 1.2,
        'disponibilidad': 0.5,
        'garantia': 2.5,
        'autonomia': 0.45,
        'calidad_deuda': 0.60
    }
    
    datos_financiero_2024 = {
        'liquidez_general': 2.1,
        'tesoreria': 1.5,
        'disponibilidad': 0.7,
        'garantia': 2.8,
        'autonomia': 0.52,
        'calidad_deuda': 0.55
    }
    
    # Datos de ejemplo para Análisis Económico
    datos_economico_2023 = {
        'roa': 8.5,
        'roe': 15.2,
        'margen_neto': 12.5,
        'rotacion_activo': 1.5,
        'apalancamiento': 2.1,
        'margen_bruto': 35.0,
        'margen_operativo': 18.5
    }
    
    datos_economico_2024 = {
        'roa': 10.2,
        'roe': 18.5,
        'margen_neto': 15.0,
        'rotacion_activo': 1.7,
        'apalancamiento': 2.3,
        'margen_bruto': 38.5,
        'margen_operativo': 21.0
    }
    
    # Generar gráficos
    fig1 = grafico_analisis_financiero(datos_financiero_2023, datos_financiero_2024, "2023", "2024")
    plt.show()
    
    fig2 = grafico_analisis_economico(datos_economico_2023, datos_economico_2024, "2023", "2024",
                                      benchmark_roa=9.0, benchmark_roe=16.0)
    plt.show()
    
    # Para guardar los gráficos
    # fig1.savefig('analisis_financiero.png', dpi=300, bbox_inches='tight')
    # fig2.savefig('analisis_economico.png', dpi=300, bbox_inches='tight')