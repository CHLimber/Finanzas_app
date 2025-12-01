"""
Archivo: gui/windows/analisis_patrimonial.py
Pestaña principal de Análisis Patrimonial con 5 sub-pestañas separadas
"""

import tkinter as tk
from tkinter import ttk
from config import Colors, Fonts

from gui.windows.a1_fondo_maniobra import A1FondoManiobraTab
from gui.windows.a2_vertical import A2VerticalTab
from gui.windows.a3_horizontal import A3HorizontalTab
from gui.windows.a4_cce import A4CCETab
from gui.windows.a5_diagnostico import A5DiagnosticoTab


class AnalisisPatrimonialTab(ttk.Frame):
    """Pestaña principal de Análisis Patrimonial"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.sub_notebook = None
        self.datos_desactualizados = False
        self.label_estado = None
        self.btn_actualizar = None
        
        self.crear_interfaz()
        
        if hasattr(self.app, 'on_data_change_callbacks'):
            self.app.on_data_change_callbacks.append(self.marcar_desactualizado)
    
    def crear_interfaz(self):
        for widget in self.winfo_children():
            widget.destroy()
    
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(
            titulo_frame,
            text="ANÁLISIS PATRIMONIAL",
            font=Fonts.TITLE
        ).pack(side=tk.LEFT, padx=10)
        
        self.label_estado = tk.Label(
            titulo_frame,
            text="⚠️ Datos modificados - Clic en Actualizar",
            font=Fonts.NORMAL,
            bg=Colors.WARNING,
            fg="white",
            padx=10,
            pady=5,
            relief="raised"
        )
        if self.datos_desactualizados:
            self.label_estado.pack(side=tk.LEFT, padx=10)
        
        self.btn_actualizar = tk.Button(
            titulo_frame,
            text="🔄 Actualizar",
            font=Fonts.NORMAL_BOLD,
            bg=Colors.INFO,
            fg="white",
            cursor="hand2",
            command=self.actualizar_contenido
        )
        self.btn_actualizar.pack(side=tk.RIGHT, padx=10)
        
        self.sub_notebook = ttk.Notebook(self)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # ✅ AÑADE ESTAS LÍNEAS AQUÍ:
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=Fonts.NORMAL)
        
        self.crear_pestanas()
        
        self.datos_desactualizados = False
        if self.label_estado:
            self.label_estado.pack_forget()
    
    def crear_pestanas(self):
        """Crea las 5 pestañas del análisis patrimonial"""
        
        a1_tab = A1FondoManiobraTab(self.sub_notebook, self.app)
        self.sub_notebook.add(a1_tab, text="A1 - Fondo Maniobra")
        
        a2_tab = A2VerticalTab(self.sub_notebook, self.app)
        self.sub_notebook.add(a2_tab, text="A2 - Vertical")
        
        a3_tab = A3HorizontalTab(self.sub_notebook, self.app)
        self.sub_notebook.add(a3_tab, text="A3 - Horizontal")
        
        a4_tab = A4CCETab(self.sub_notebook, self.app)
        self.sub_notebook.add(a4_tab, text="A4 - CCE")
        
        a5_tab = A5DiagnosticoTab(self.sub_notebook, self.app)
        self.sub_notebook.add(a5_tab, text="A5 - Diagnóstico")
    
    def marcar_desactualizado(self):
        """
        Se llama automáticamente cuando se modifican datos en Balance/Estado.
        Muestra el indicador visual sin actualizar aún.
        """
        self.datos_desactualizados = True
        if self.label_estado and self.label_estado.winfo_exists():
            self.label_estado.pack(side=tk.LEFT, padx=10)
            # Hacer parpadear el botón actualizar
            if self.btn_actualizar and self.btn_actualizar.winfo_exists():
                self.btn_actualizar.config(bg=Colors.SUCCESS)
                self.after(300, lambda: self.btn_actualizar.config(bg=Colors.INFO))
    
    def actualizar_contenido(self):
        """
        Actualiza manualmente el contenido cuando el usuario hace clic.
        Cierra figuras de matplotlib antes de recrear.
        """
        try:
            # Cerrar todas las figuras de matplotlib para liberar memoria
            import matplotlib.pyplot as plt
            plt.close('all')
            
            # Recrear toda la interfaz con datos actualizados
            self.crear_interfaz()
            
            print("✅ Análisis patrimonial actualizado correctamente")
            
        except Exception as e:
            print(f"❌ Error al actualizar análisis patrimonial: {e}")
            # Mostrar error al usuario
            if hasattr(self, 'label_estado') and self.label_estado:
                self.label_estado.config(
                    text=f"❌ Error al actualizar: {str(e)[:50]}...",
                    bg=Colors.DANGER
                )