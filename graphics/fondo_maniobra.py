import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})


def grafico_barras_simple(fm_año1, fm_año2, año1="Año 1", año2="Año 2"):
    """
    Gráfico de barras simple para comparar fondo de maniobra
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    años = [año1, año2]
    valores = [fm_año1, fm_año2]
    colores = ['#4169E1', '#48D1CC']
    
    barras = ax.bar(años, valores, color=colores, width=0.6, edgecolor='black', linewidth=2)
    
    # Añadir valores sobre las barras
    for i, (barra, valor) in enumerate(zip(barras, valores)):
        height = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., height,
                f'${valor:,.0f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Monto ($)', fontsize=12, fontweight='bold')
    ax.set_title('Comparación Fondo de Maniobra', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Formato de eje Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    return fig


def grafico_barras_con_variacion(fm_año1, fm_año2, año1="Año 1", año2="Año 2"):
    """
    Gráfico de barras con indicador de variación porcentual
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    años = [año1, año2]
    valores = [fm_año1, fm_año2]
    
    # Calcular variación
    if fm_año1 != 0:
        variacion = ((fm_año2 - fm_año1) / abs(fm_año1)) * 100
    else:
        variacion = 0
    
    # Color según aumente o disminuya
    colores = ['#4169E1', '#2ECC71' if fm_año2 > fm_año1 else '#E74C3C']
    
    barras = ax.bar(años, valores, color=colores, width=0.6, edgecolor='black', linewidth=2)
    
    # Añadir valores sobre las barras
    for i, (barra, valor) in enumerate(zip(barras, valores)):
        height = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2., height,
                f'${valor:,.0f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Añadir flecha y porcentaje de variación
    ax.annotate('', xy=(1, fm_año2), xytext=(0, fm_año1),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray', linestyle='--'))
    
    mid_x = 0.5
    mid_y = (fm_año1 + fm_año2) / 2
    signo = '+' if variacion > 0 else ''
    ax.text(mid_x, mid_y, f'{signo}{variacion:.1f}%',
            ha='center', va='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    ax.set_ylabel('Monto ($)', fontsize=12, fontweight='bold')
    ax.set_title('Fondo de Maniobra - Variación Anual', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Formato de eje Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    return fig


def grafico_linea_tendencia(fm_año1, fm_año2, año1="Año 1", año2="Año 2"):
    """
    Gráfico de línea para mostrar tendencia
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    años = [año1, año2]
    valores = [fm_año1, fm_año2]
    
    # Línea principal
    ax.plot(años, valores, marker='o', linewidth=3, markersize=12, 
            color='#4169E1', label='Fondo de Maniobra')
    
    # Rellenar área bajo la línea
    ax.fill_between(range(len(años)), valores, alpha=0.3, color='#4169E1')
    
    # Añadir valores en los puntos
    for i, (año, valor) in enumerate(zip(años, valores)):
        ax.text(i, valor, f'${valor:,.0f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'))
    
    # Calcular variación
    if fm_año1 != 0:
        variacion = ((fm_año2 - fm_año1) / abs(fm_año1)) * 100
        color_var = 'green' if variacion > 0 else 'red'
        signo = '+' if variacion > 0 else ''
        ax.text(0.5, max(valores) * 0.95, f'Variación: {signo}{variacion:.1f}%',
                ha='center', fontsize=12, fontweight='bold', color=color_var,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow'))
    
    ax.set_ylabel('Monto ($)', fontsize=12, fontweight='bold')
    ax.set_title('Evolución del Fondo de Maniobra', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Formato de eje Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    return fig


def grafico_comparativo_completo(fm_año1, fm_año2, año1="Año 1", año2="Año 2"):
    """
    Gráfico completo con múltiples visualizaciones
    """
    fig = plt.figure(figsize=(14, 5))
    
    # Calcular variación
    if fm_año1 != 0:
        variacion = ((fm_año2 - fm_año1) / abs(fm_año1)) * 100
        diferencia = fm_año2 - fm_año1
    else:
        variacion = 0
        diferencia = fm_año2
    
    # Subplot 1: Barras comparativas
    ax1 = plt.subplot(1, 3, 1)
    años = [año1, año2]
    valores = [fm_año1, fm_año2]
    colores = ['#4169E1', '#2ECC71' if fm_año2 > fm_año1 else '#E74C3C']
    
    barras = ax1.bar(años, valores, color=colores, width=0.6, edgecolor='black', linewidth=2)
    for barra, valor in zip(barras, valores):
        height = barra.get_height()
        ax1.text(barra.get_x() + barra.get_width()/2., height,
                f'${valor:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax1.set_ylabel('Monto ($)', fontsize=10, fontweight='bold')
    ax1.set_title('Comparación', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Subplot 2: Variación porcentual
    ax2 = plt.subplot(1, 3, 2)
    color_var = '#2ECC71' if variacion > 0 else '#E74C3C'
    ax2.bar(['Variación'], [variacion], color=color_var, width=0.5, 
            edgecolor='black', linewidth=2)
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax2.text(0, variacion, f'{variacion:+.1f}%',
            ha='center', va='bottom' if variacion > 0 else 'top', 
            fontsize=14, fontweight='bold')
    ax2.set_ylabel('Variación (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Variación Porcentual', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Subplot 3: Diferencia absoluta
    ax3 = plt.subplot(1, 3, 3)
    color_dif = '#2ECC71' if diferencia > 0 else '#E74C3C'
    ax3.bar(['Diferencia'], [diferencia], color=color_dif, width=0.5,
            edgecolor='black', linewidth=2)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.text(0, diferencia, f'${diferencia:+,.0f}',
            ha='center', va='bottom' if diferencia > 0 else 'top',
            fontsize=12, fontweight='bold')
    ax3.set_ylabel('Monto ($)', fontsize=10, fontweight='bold')
    ax3.set_title('Diferencia Absoluta', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.suptitle('Análisis Completo del Fondo de Maniobra', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig


# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo
    fondo_maniobra_2023 = 150000
    fondo_maniobra_2024 = 15000
    
    # Opción 1: Barras simples
    fig1 = grafico_barras_simple(fondo_maniobra_2023, fondo_maniobra_2024, "2023", "2024")
    plt.show()
    
    # Opción 2: Barras con variación
    fig2 = grafico_barras_con_variacion(fondo_maniobra_2023, fondo_maniobra_2024, "2023", "2024")
    plt.show()
    
    # Opción 3: Línea de tendencia
    fig3 = grafico_linea_tendencia(fondo_maniobra_2023, fondo_maniobra_2024, "2023", "2024")
    plt.show()
    
    # Opción 4: Análisis completo
    fig4 = grafico_comparativo_completo(fondo_maniobra_2023, fondo_maniobra_2024, "2023", "2024")
    plt.show()
    
    # Para guardar cualquier gráfico
    # fig1.savefig('fondo_maniobra.png', dpi=300, bbox_inches='tight')