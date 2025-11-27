class Colors:
    """Paleta de colores de la aplicación"""
    
    # Colores principales
    PRIMARY = "#2c3e50"          # Azul oscuro
    SECONDARY = "#34495e"        # Gris oscuro
    ACCENT = "#3498db"           # Azul brillante
    SUCCESS = "#27ae60"          # Verde
    WARNING = "#f39c12"          # Naranja
    DANGER = "#e74c3c"           # Rojo
    INFO = "#16a085"             # Turquesa
    
    # Colores de fondo
    BG_PRIMARY = "#ffffff"       # Blanco
    BG_SECONDARY = "#f0f0f0"     # Gris claro
    BG_DARK = "#2c3e50"          # Azul oscuro
    
    # Colores de texto
    TEXT_PRIMARY = "#2c3e50"     # Texto principal
    TEXT_SECONDARY = "#7f8c8d"   # Texto secundario
    TEXT_LIGHT = "#ecf0f1"       # Texto claro
    TEXT_WHITE = "#ffffff"       # Texto blanco
    
    # Colores para datos financieros
    POSITIVE = "#27ae60"         # Verde (ganancias)
    NEGATIVE = "#e74c3c"         # Rojo (pérdidas)
    NEUTRAL = "#95a5a6"          # Gris (neutral)
    CALCULATED = "#16a085"       # Turquesa (calculado)
    
    # Colores para categorías
    ACTIVO = "#3498db"           # Azul
    PASIVO = "#e67e22"           # Naranja
    PATRIMONIO = "#9b59b6"       # Púrpura
    INGRESOS = "#27ae60"         # Verde
    GASTOS = "#e74c3c"           # Rojo


# ============================================================
# FUENTES
# ============================================================
class Fonts:
    """Configuración de fuentes"""
    
    # Familia de fuentes
    FAMILY = "Arial"
    FAMILY_MONO = "Courier New"
    
    # Tamaños
    SIZE_TITLE = 18              # Títulos principales
    SIZE_SUBTITLE = 14           # Subtítulos
    SIZE_HEADER = 12             # Encabezados
    SIZE_NORMAL = 10             # Texto normal
    SIZE_SMALL = 9               # Texto pequeño
    SIZE_LARGE = 16              # Texto grande
    
    # Fuentes completas (familia, tamaño, peso)
    TITLE = (FAMILY, SIZE_TITLE, "bold")
    SUBTITLE = (FAMILY, SIZE_SUBTITLE, "bold")
    HEADER = (FAMILY, SIZE_HEADER, "bold")
    NORMAL = (FAMILY, SIZE_NORMAL)
    NORMAL_BOLD = (FAMILY, SIZE_NORMAL, "bold")
    SMALL = (FAMILY, SIZE_SMALL)
    LARGE = (FAMILY, SIZE_LARGE, "bold")
    MONO = (FAMILY_MONO, SIZE_NORMAL)


# ============================================================
# DIMENSIONES
# ============================================================
class Dimensions:
    """Dimensiones estándar"""
    
    # Ventanas
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    
    # Padding y márgenes
    PADDING_SMALL = 5
    PADDING_MEDIUM = 10
    PADDING_LARGE = 20
    PADDING_XLARGE = 30
    
    # Tamaños de widgets
    ENTRY_WIDTH = 18
    BUTTON_HEIGHT = 2
    LABEL_WIDTH = 18
    
    # Header
    HEADER_HEIGHT = 80


# ============================================================
# ESTILOS DE BOTONES
# ============================================================
class ButtonStyles:
    """Estilos predefinidos para botones"""
    
    PRIMARY = {
        "bg": Colors.ACCENT,
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#2980b9",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL_BOLD,
        "cursor": "hand2",
        "relief": "flat",
        "borderwidth": 0
    }
    
    SUCCESS = {
        "bg": Colors.SUCCESS,
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#229954",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL_BOLD,
        "cursor": "hand2",
        "relief": "flat"
    }
    
    WARNING = {
        "bg": Colors.WARNING,
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#d68910",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL_BOLD,
        "cursor": "hand2",
        "relief": "flat"
    }
    
    DANGER = {
        "bg": Colors.DANGER,
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#c0392b",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL_BOLD,
        "cursor": "hand2",
        "relief": "flat"
    }
    
    DISABLED = {
        "bg": Colors.NEUTRAL,
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#7f8c8d",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL_BOLD,
        "cursor": "hand2",
        "relief": "flat"
    }
    
    ANALYSIS = {
        "bg": "#9b59b6",
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#8e44ad",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL,
        "cursor": "hand2",
        "relief": "flat"
    }
    
    GRAPHICS = {
        "bg": "#e67e22",
        "fg": Colors.TEXT_WHITE,
        "activebackground": "#d35400",
        "activeforeground": Colors.TEXT_WHITE,
        "font": Fonts.NORMAL,
        "cursor": "hand2",
        "relief": "flat"
    }


# ============================================================
# TEXTOS Y ETIQUETAS
# ============================================================
class Labels:
    """Etiquetas y textos estándar"""
    
    # Títulos principales
    APP_TITLE = "Sistema de Análisis Financiero"
    APP_SUBTITLE = "Análisis Patrimonial, Financiero y Económico"
    
    # Títulos de pestañas
    TAB_BALANCE = "📋 Balance General"
    TAB_ESTADO = "💰 Estado de Resultados"
    TAB_PATRIMONIAL = "🏛️ Análisis Patrimonial"
    TAB_FINANCIERO = "💵 Análisis Financiero"
    TAB_ECONOMICO = "📊 Análisis Económico"
    TAB_DUAL = "🎯 Análisis Dual"
    TAB_GRAFICOS = "📉 Gráficos"
    
    # Encabezados de columnas
    COL_CUENTA = "Cuenta"
    COL_YEAR_1 = "Año 1"
    COL_YEAR_2 = "Año 2"
    COL_CONCEPTO = "Concepto"
    
    # Mensajes
    MSG_CALCULATING = "Calculando..."
    MSG_SAVED = "Datos guardados correctamente"
    MSG_ERROR = "Error al procesar datos"
    MSG_NO_DATA = "No hay datos disponibles"


# ============================================================
# FORMATO DE NÚMEROS
# ============================================================
class NumberFormat:
    """Configuración para formato de números"""
    
    DECIMAL_PLACES = 2
    THOUSANDS_SEP = ","
    DECIMAL_SEP = "."
    
    @staticmethod
    def format(value):
        """Formatea un número con separador de miles y decimales"""
        return f"{value:,.2f}"
    
    @staticmethod
    def format_percent(value):
        """Formatea un porcentaje"""
        return f"{value:.2f}%"
    
    @staticmethod
    def format_currency(value, symbol="Bs."):
        """Formatea como moneda"""
        return f"{symbol} {value:,.2f}"
    
    @staticmethod
    def parse(text):
        """Convierte texto a número"""
        try:
            return float(text.replace(",", ""))
        except:
            return 0.0


# ============================================================
# CONFIGURACIÓN DE VENTANAS
# ============================================================
class WindowConfig:
    """Configuración general de ventanas"""
    
    # Configuración de scrollbars
    SCROLL_SPEED = 120
    
    # Configuración de canvas
    CANVAS_BG = Colors.BG_PRIMARY
    
    # Configuración de frames
    FRAME_BG = Colors.BG_SECONDARY
    
    @staticmethod
    def center_window(window):
        """Centra una ventana en la pantalla"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')


# ============================================================
# CONFIGURACIÓN DE ANÁLISIS
# ============================================================
class AnalysisConfig:
    """Configuración para análisis financieros"""
    
    # Tasas y porcentajes
    TAX_RATE = 0.25              # 25% impuesto a la renta
    INTEREST_RATE = 0.05         # 5% tasa de interés préstamos
    
    # Umbrales de ratios
    LIQUIDEZ_MIN = 1.0
    LIQUIDEZ_IDEAL = 2.0
    ENDEUDAMIENTO_MAX = 0.6
    ROE_MIN = 0.10               # 10%
    ROA_MIN = 0.05               # 5%


# ============================================================
# ICONOS Y EMOJIS
# ============================================================
class Icons:
    """Iconos para la interfaz"""
    
    # Iconos de pestañas
    BALANCE = "📋"
    ESTADO = "💰"
    PATRIMONIAL = "🏛️"
    FINANCIERO = "💵"
    ECONOMICO = "📊"
    DUAL = "🎯"
    GRAFICOS = "📉"
    
    # Iconos de acciones
    SAVE = "💾"
    CALCULATE = "🧮"
    EXPORT = "📤"
    IMPORT = "📥"
    PRINT = "🖨️"
    REFRESH = "🔄"
    INFO = "ℹ️"
    WARNING = "⚠️"
    ERROR = "❌"
    SUCCESS = "✅"
    
    # Iconos de gráficos
    BAR_CHART = "📊"
    LINE_CHART = "📈"
    PIE_CHART = "🥧"
    AREA_CHART = "📉"


# ============================================================
# HELPERS
# ============================================================
def apply_button_style(button, style_dict):
    """Aplica un estilo a un botón"""
    button.config(**style_dict)


def create_styled_label(parent, text, font=Fonts.NORMAL, color=Colors.TEXT_PRIMARY, **kwargs):
    """Crea un label con estilo"""
    import tkinter as tk
    label = tk.Label(
        parent,
        text=text,
        font=font,
        fg=color,
        bg=kwargs.get('bg', Colors.BG_PRIMARY),
        **{k: v for k, v in kwargs.items() if k != 'bg'}
    )
    return label


def create_styled_entry(parent, width=Dimensions.ENTRY_WIDTH, **kwargs):
    """Crea un entry con estilo"""
    from tkinter import ttk
    entry = ttk.Entry(
        parent,
        width=width,
        justify="right",
        font=Fonts.NORMAL,
        **kwargs
    )
    return entry