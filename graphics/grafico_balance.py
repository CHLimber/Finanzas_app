import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.rcParams.update({
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})


def grafico_balance(activo_nc, activo_c, patrimonio, pasivo_nc, pasivo_c,anio):

    # Calcular totales
    total_activo = activo_nc + activo_c
    total_pasivo_patrimonio = patrimonio + pasivo_nc + pasivo_c
    
    # Calcular proporciones
    prop_activo_nc = activo_nc / total_activo if total_activo > 0 else 0
    prop_activo_c = activo_c / total_activo if total_activo > 0 else 0
    
    prop_patrimonio = patrimonio / total_pasivo_patrimonio if total_pasivo_patrimonio > 0 else 0
    prop_pasivo_nc = pasivo_nc / total_pasivo_patrimonio if total_pasivo_patrimonio > 0 else 0
    prop_pasivo_c = pasivo_c / total_pasivo_patrimonio if total_pasivo_patrimonio > 0 else 0
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Tamaño de los cuadrados
    ancho = 3.5
    altura = 8
    
    # PRIMER CUADRADO - ACTIVOS
    x1 = 1
    y1_base = 1
    
    # Activo No Corriente (arriba, celeste)
    altura_anc = altura * prop_activo_nc
    rect_anc = patches.Rectangle((x1, y1_base + altura * prop_activo_c), ancho, altura_anc,
                                  linewidth=3, edgecolor='black', facecolor='#48D1CC')
    ax.add_patch(rect_anc)
    
    # Texto Activo No Corriente
    if prop_activo_nc > 0.05:
        ax.text(x1 + ancho/2, y1_base + altura * prop_activo_c + altura_anc/2,
                f'ACTIVO NO\nCORRIENTE\n{prop_activo_nc*100:.1f}%',
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Activo Corriente (abajo, azul)
    altura_ac = altura * prop_activo_c
    rect_ac = patches.Rectangle((x1, y1_base), ancho, altura_ac,
                                linewidth=3, edgecolor='black', facecolor='#4169E1')
    ax.add_patch(rect_ac)
    
    # Texto Activo Corriente
    if prop_activo_c > 0.05:
        ax.text(x1 + ancho/2, y1_base + altura_ac/2,
                f'ACTIVO\nCORRIENTE\n{prop_activo_c*100:.1f}%',
                ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    # SEGUNDO CUADRADO - PASIVO Y PATRIMONIO
    x2 = 5.5
    y2_base = 1
    
    # Patrimonio Neto (arriba, amarillo)
    altura_pat = altura * prop_patrimonio
    y_pat = y2_base + altura * prop_pasivo_c + altura * prop_pasivo_nc
    rect_pat = patches.Rectangle((x2, y_pat), ancho, altura_pat,
                                 linewidth=3, edgecolor='black', facecolor='#F0E68C')
    ax.add_patch(rect_pat)
    
    # Texto Patrimonio
    if prop_patrimonio > 0.05:
        ax.text(x2 + ancho/2, y_pat + altura_pat/2,
                f'PATRIMONIO\nNETO\n{prop_patrimonio*100:.1f}%',
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Pasivo No Corriente (medio, naranja)
    altura_pnc = altura * prop_pasivo_nc
    y_pnc = y2_base + altura * prop_pasivo_c
    rect_pnc = patches.Rectangle((x2, y_pnc), ancho, altura_pnc,
                                 linewidth=3, edgecolor='black', facecolor='#FFA500')
    ax.add_patch(rect_pnc)
    
    # Texto Pasivo No Corriente
    if prop_pasivo_nc > 0.05:
        ax.text(x2 + ancho/2, y_pnc + altura_pnc/2,
                f'PASIVO NO\nCORRIENTE\n{prop_pasivo_nc*100:.1f}%',
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Pasivo Corriente (abajo, naranja oscuro)
    altura_pc = altura * prop_pasivo_c
    rect_pc = patches.Rectangle((x2, y2_base), ancho, altura_pc,
                                linewidth=3, edgecolor='black', facecolor='#FF8C00')
    ax.add_patch(rect_pc)
    
    # Texto Pasivo Corriente
    if prop_pasivo_c > 0.05:
        ax.text(x2 + ancho/2, y2_base + altura_pc/2,
                f'PASIVO\nCORRIENTE\n{prop_pasivo_c*100:.1f}%',
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Títulos de los cuadrados
    ax.text(x1 + ancho/2, y1_base + altura + 0.5,
            'ACTIVO', ha='center', va='center', fontsize=14, fontweight='bold')
    ax.text(x2 + ancho/2, y2_base + altura + 0.5,
            'PASIVO + PATRIMONIO', ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Línea punteada entre cuadrados
    ax.plot([x1 + ancho + 0.2, x2 - 0.2], [y1_base + altura/2, y2_base + altura/2],
            'k--', linewidth=1.5, alpha=0.5)
    
    
    plt.title(f'Balance General año {anio}', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig