"""
Archivo: core/analysis/financial_interpreter.py
Clase para interpretar ratios financieros con base de conocimiento completa
"""

class FinancialInterpreter:
    """
    Clase que interpreta ratios financieros y proporciona análisis detallado
    incluyendo interpretación, causas y recomendaciones según rangos óptimos.
    """
    
    def __init__(self):
        """Inicializa la base de conocimiento de ratios financieros"""
        self.database = self._build_knowledge_base()
    
    def _build_knowledge_base(self):
        """Construye la base de conocimiento completa de ratios"""
        return {
            # ============================================================
            # ANÁLISIS PATRIMONIAL
            # ============================================================
            "fondo_maniobra": {
                "nombre": "Fondo de Maniobra",
                "rango": (0.10, 0.30),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "La empresa depende de financiación de corto plazo para operar.",
                    "causa": "Deuda de corto plazo demasiado alta. Gastos operativos creciendo más rápido que la facturación.",
                    "recomendacion": "Reestructurar deuda a largo plazo, mejorar flujo de caja operativo o renegociar condiciones de pago."
                },
                "optimo": {
                    "interpretacion": "La empresa puede pagar sus deudas de corto plazo sin problemas.",
                    "causa": "Equilibrio adecuado entre activos corrientes y pasivos corrientes.",
                    "recomendacion": "Mantener estrategia actual; seguir monitoreando la gestión del capital de trabajo."
                },
                "alto": {
                    "interpretacion": "Exceso de efectivo ocioso. Falta de reinversión en I+D, marketing o crecimiento.",
                    "causa": "Deuda de corto plazo demasiado baja. Mala planificación del flujo de caja. Inventarios innecesarios.",
                    "recomendacion": "Invertir excedentes en instrumentos de corto plazo. Reinvertir en marketing, crecimiento, I+D."
                }
            },
            
            "razon_liquidez": {
                "nombre": "Razón de Liquidez",
                "rango": (1.5, 2.5),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Riesgo de liquidez y posible dificultad para pagar deudas inmediatas.",
                    "causa": "Insuficientes activos líquidos o pasivos corrientes elevados respecto a la capacidad de pago.",
                    "recomendacion": "Reestructurar deuda a largo plazo, mejorar flujo de caja o reducir dividendos/recompras."
                },
                "optimo": {
                    "interpretacion": "Equilibrio entre seguridad financiera y eficiencia del capital.",
                    "causa": "Gestión adecuada del capital de trabajo.",
                    "recomendacion": "Mantener políticas actuales de gestión de liquidez."
                },
                "alto": {
                    "interpretacion": "Capital excesivo inmovilizado en activos de baja rentabilidad.",
                    "causa": "Exceso de efectivo ocioso o gestión conservadora del capital de trabajo.",
                    "recomendacion": "Invertir excedentes en crecimiento, I+D o devolver capital a accionistas vía dividendos/recompras."
                }
            },
            
            "razon_tesoreria": {
                "nombre": "Razón de Tesorería",
                "rango": (1.0, 1.5),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Riesgo de liquidez inmediata para cubrir obligaciones corrientes.",
                    "causa": "Activos líquidos insuficientes o pasivos corrientes desproporcionados.",
                    "recomendacion": "Solución: Mejorar flujo de caja, renegociar deuda a corto plazo o aumentar líneas de crédito."
                },
                "optimo": {
                    "interpretacion": "Liquidez adecuada sin exceso de recursos inmovilizados.",
                    "causa": "Balance adecuado de tesorería y obligaciones corrientes.",
                    "recomendacion": "Mantener gestión actual de tesorería."
                },
                "alto": {
                    "interpretacion": "Capital circulante excesivo que reduce rentabilidad.",
                    "causa": "Cuentas por cobrar muy elevadas respecto a deudas corto plazo.",
                    "recomendacion": "Solución: Optimizar gestión de efectivo y mejorar política de cobranza para liberar recursos."
                }
            },
            
            "razon_disponibilidad": {
                "nombre": "Razón de Disponibilidad",
                "rango": (0.20, 0.50),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Riesgo de liquidez inmediata para cubrir gastos críticos.",
                    "causa": "Fondo de maniobra insuficiente o gestión agresiva del efectivo. Alto nivel de endeudamiento o activos corrientes mal gestionados.",
                    "recomendacion": "Solución: Aumentar líneas de crédito, mejorar cobranza o ajustar política de dividendos."
                },
                "optimo": {
                    "interpretacion": "Liquidez equilibrada. Caja suficiente, sin caer en excesos. Empresa eficiente.",
                    "causa": "Gestión eficiente del disponible.",
                    "recomendacion": "Mantener políticas actuales de gestión de efectivo."
                },
                "alto": {
                    "interpretacion": "Demasiado efectivo inmovilizado → gestión conservadora, subutilización de recursos.",
                    "causa": "Acumulación excesiva de efectivo sin oportunidades de inversión o uso estratégico. Exceso de fondos o financiación sobredimensionada con recursos propios.",
                    "recomendacion": "Invertir en crecimiento, I+D o recomprar acciones para optimizar rendimiento del capital."
                }
            },
            
            # ============================================================
            # ANÁLISIS FINANCIERO - SOLVENCIA
            # ============================================================
            "ratio_garantia": {
                "nombre": "Ratio de Garantía",
                "rango": (1.5, 2.5),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Riesgo de solvencia elevado con margen insuficiente para absorber pérdidas.",
                    "causa": "Alto nivel de endeudamiento o activos corrientes mal gestionados u obligaciones sobredimensionadas.",
                    "recomendacion": "Fortalecer el balance con ampliaciones de capital o reestructurar deuda para mejorar el ROE."
                },
                "optimo": {
                    "interpretacion": "Solvencia sólida que inspira confianza en acreedores.",
                    "causa": "Balance equilibrado entre activos y pasivos totales.",
                    "recomendacion": "Mantener estructura financiera actual."
                },
                "alto": {
                    "interpretacion": "Estructura excesivamente conservadora con posible ineficiencia del capital.",
                    "causa": "Exceso de activos o financiación sobredimensionada con recursos propios.",
                    "recomendacion": "Optimizar estructura mediante recompras, dividendos o inversiones estratégicas que mejoren el ROE."
                }
            },
            
            "ratio_autonomia": {
                "nombre": "Ratio de Autonomía",
                "rango": (0.8, 1.5),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Dependencia excesiva de financiación externa. La estructura financiera es frágil y vulnerable a cambios en las condiciones crediticias.",
                    "causa": "Alto apalancamiento o patrimonio erosionado por pérdidas acumuladas.",
                    "recomendacion": "Realizar ampliación de capital, retener beneficios o convertir deuda en equity para fortalecer autonomía."
                },
                "optimo": {
                    "interpretacion": "Equilibrio financiero ideal. La empresa mantiene autonomía estratégica mientras aprovecha el apalancamiento para acelerar el ROE.",
                    "causa": "Balance adecuado entre recursos propios y ajenos.",
                    "recomendacion": "Mantener equilibrio actual en estructura de capital."
                },
                "alto": {
                    "interpretacion": "Estructura excesivamente conservadora. Puede indicar incapacidad para acceder a financiación externa o suboptimización del coste de financiación.",
                    "causa": "Exceso de capital propio o dificultad para acceder a financiación externa.",
                    "recomendacion": "Introducir deuda moderada, recomprar acciones o aumentar dividendos para optimizar estructura de capital."
                }
            },
            
            "ratio_calidad_deuda": {
                "nombre": "Ratio de Calidad de Deuda",
                "rango": (0.30, 0.50),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Estructura excesivamente conservadora. Puede tener dificultades para acceder a financiación de largo plazo o suboptimización del coste de financiación.",
                    "causa": "Exceso de financiación a largo plazo o política ultraconservadora.",
                    "recomendacion": "Incorporar instrumentos a corto plazo para necesidades operativas y de financiación para reducir riesgos."
                },
                "optimo": {
                    "interpretacion": "Equilibrio maduro. La empresa administra adecuadamente los vencimientos, combinado estabilidad a largo plazo con flexibilidad y coste.",
                    "causa": "Distribución equilibrada entre deuda de corto y largo plazo.",
                    "recomendacion": "Mantener equilibrio actual de estructura de deuda."
                },
                "alto": {
                    "interpretacion": "Estructura de deuda agresiva. El vencimiento a corto plazo genera presión constante y eleva la vulnerabilidad ante crisis de liquidez.",
                    "causa": "Dependencia excesiva de líneas de crédito a corto plazo o dificultad para acceder a financiación a largo plazo.",
                    "recomendacion": "Refinanciar deuda de corto a largo plazo y diversificar fuentes de financiación."
                }
            },
            
            # ============================================================
            # ANÁLISIS ECONÓMICO - RENTABILIDAD
            # ============================================================
            "rat": {
                "nombre": "Rentabilidad sobre Activos Totales (RAT)",
                "rango": (0.10, 0.20),
                "unidad": "porcentaje",
                "bajo": {
                    "interpretacion": "Ineficiencia en el uso de los activos. La empresa no está generando suficiente beneficio operativo respecto a los que utiliza.",
                    "causa": "Activos improductivos, margen neto insuficiente o posible subvaloración de activos intangibles en balance.",
                    "recomendacion": "Optimizar base de activos, mejorar rentabilidad operativa y racionalizar inversiones no estratégicas."
                },
                "optimo": {
                    "interpretacion": "Eficiencia operativa sólida. La empresa usa sus activos de forma efectiva para generar beneficios, indicando buen management y modelo de negocio escalable.",
                    "causa": "Gestión eficiente de activos y operaciones.",
                    "recomendacion": "Mantener estrategia operativa actual."
                },
                "alto": {
                    "interpretacion": "Excelente desempeño. Característico de empresas con ventajas competitivas sostenibles, modelos de negocio muy eficientes o activos muy optimizados.",
                    "causa": "Activos muy productivos, modelo ultra-eficiente o posible subvaloración de activos intangibles no utilizados.",
                    "recomendacion": "Reinvertir en capacidad para sostener crecimiento y asegurar que los activos reflejen adecuadamente el valor real."
                }
            },
            
            "rpp": {
                "nombre": "Rentabilidad sobre Patrimonio (RPP/ROE)",
                "rango": (0.15, 0.30),
                "unidad": "porcentaje",
                "bajo": {
                    "interpretacion": "No cubre el coste del capital equity. Los accionistas podrían obtener mejor rendimiento en alternativas con similar riesgo.",
                    "causa": "Baja utilidad neta, patrimonio sobredimensionado o estructura de capital ineficiente.",
                    "recomendacion": "Mejorar rentabilidad operativa, optimizar apalancamiento y enfocar inversiones en proyectos de alto ROE."
                },
                "optimo": {
                    "interpretacion": "Creación de valor consistente. La empresa genera retornos atractivos para sus propietarios, ofreciendo rendimientos competitivos y gestión eficiente.",
                    "causa": "Balance adecuado entre utilidad neta y patrimonio.",
                    "recomendacion": "Mantener estrategia actual y monitorear sostenibilidad."
                },
                "alto": {
                    "interpretacion": "Excelente rentabilidad. Sugiere ventaja competitiva extraordinaria y/o apalancamiento financiero muy elevado. Patrimonio neto reducido.",
                    "causa": "Apalancamiento financiero elevado, patrimonio neto reducido o ventaja competitiva extraordinaria.",
                    "recomendacion": "Evaluar sostenibilidad, fortalecer patrimonio si es alto el riesgo y reinvertir para mantener ventajas."
                }
            },
            
            "margen_neto": {
                "nombre": "Margen Neto",
                "rango": (0.15, 0.25),
                "unidad": "porcentaje",
                "bajo": {
                    "interpretacion": "Rentabilidad débil. La empresa retiene muy poco de cada venta después de todos los gastos.",
                    "causa": "Costos operativos elevados, carga fiscal alta o financiamiento con altos intereses.",
                    "recomendacion": "Optimizar gastos generales, revisar estrategia fiscal y refinanciar deuda para reducir carga financiera."
                },
                "optimo": {
                    "interpretacion": "Rentabilidad saludable. Indica eficiencia operativa, poder de fijación de precios y control de costos.",
                    "causa": "Control eficiente de costos y estructura financiera adecuada.",
                    "recomendacion": "Mantener estrategia operativa actual."
                },
                "alto": {
                    "interpretacion": "Excelente rentabilidad. Sugiere ventaja competitiva fuerte, pero requiere verificar sostenibilidad y crecimiento futuro.",
                    "causa": "Control exhaustivo de costos, ventaja competitiva sólida o posible subinversión en crecimiento futuro.",
                    "recomendacion": "Reinvertir en I+D, expansión de mercado o considerar recompra de acciones para optimizar estructura de capital."
                }
            },
            
            "rotacion_activos": {
                "nombre": "Rotación de Activos",
                "rango": (0.8, 1.2),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Ineficiencia en el uso de activos. La empresa no está generando suficientes ventas para el tamaño de su base de activos.",
                    "causa": "Activos ociosos, ventas insuficientes o sobreinversión en capacidad no utilizada.",
                    "recomendacion": "Optimizar base de activos, impulsar mejoras comerciales y racionalizar inversiones no productivas."
                },
                "optimo": {
                    "interpretacion": "Eficiencia equilibrada. La empresa usa activos de forma efectiva para generar ingresos.",
                    "causa": "Balance adecuado entre ventas y activos.",
                    "recomendacion": "Mantener estrategia actual de gestión de activos."
                },
                "alto": {
                    "interpretacion": "Alta productividad de activos. Sin embargo, puede indicar capacidad insuficiente para atender crecimiento futuro.",
                    "causa": "Modelo asset-light extremo, posible subinversión en infraestructura o ventas muy elevadas con base asset muy reducida.",
                    "recomendacion": "Evaluar capacidad de escalabilidad, invertir en activos estratégicos y asegurar que la alta rotación no comprometa calidad o crecimiento futuro."
                }
            },
            
            "apalancamiento": {
                "nombre": "Apalancamiento Financiero",
                "rango": (1.5, 2.5),
                "unidad": "ratio",
                "bajo": {
                    "interpretacion": "Estructura ultraconservadora que limita el potencial de crecimiento.",
                    "causa": "Financiación casi exclusiva con capital propio o acumulación de activo ocioso.",
                    "recomendacion": "Introducir deuda moderada, recomprar acciones o invertir en crecimiento para optimizar ROE."
                },
                "optimo": {
                    "interpretacion": "Equilibrio riesgo–rendimiento. Uso inteligente de deuda para mejorar ROE sin asumir riesgos excesivos, en o sin crisis o desaceleraciones.",
                    "causa": "Balance equilibrado entre recursos propios y deuda.",
                    "recomendacion": "Mantener estructura de capital actual."
                },
                "alto": {
                    "interpretacion": "Estructura agresiva. Alto riesgo financiero que puede amenazar la solvencia, en crisis o desaceleraciones.",
                    "causa": "Exceso de deuda o patrimonio erosionado por pérdidas acumuladas.",
                    "recomendacion": "Reestructurar deuda, ampliar capital social y priorizar retención de beneficios para fortalecer el patrimonio."
                }
            },
            
            "margen_bruto": {
                "nombre": "Margen Bruto",
                "rango": (0.70, 0.80),
                "unidad": "porcentaje",
                "bajo": {
                    "interpretacion": "Problemas estructurales con altos costos directos relativos al precio.",
                    "causa": "Costos de hosting/soporte de arquitectura, arquitectura ineficiente a precios suboptimizados.",
                    "recomendacion": "Optimizar infraestructura cloud, automatizar soporte y revisar estrategias de precios y planes."
                },
                "optimo": {
                    "interpretacion": "Modelo de negocio saludable y escalable típico del sector.",
                    "causa": "Balance adecuado entre costos directos y precios.",
                    "recomendacion": "Mantener eficiencia operativa actual."
                },
                "alto": {
                    "interpretacion": "Eficiencia excepcional pero requiere verificar sostenibilidad.",
                    "causa": "Arquitectura ultra-eficiente, precios premium o posible subinversión en infraestructura crítica.",
                    "recomendacion": "Asegurar capacidad de escalabilidad futura garantizando inversión en escalabilidad y calidad del servicio."
                }
            },
            
            "margen_operativo": {
                "nombre": "Margen Operativo",
                "rango": (0.20, 0.30),
                "unidad": "porcentaje",
                "bajo": {
                    "interpretacion": "Ineficiencia operativa o gastos estructurales elevados.",
                    "causa": "Gastos de operación (ventas/marketing, administración e I+D) ineficientes.",
                    "recomendacion": "Optimizar estructura de costos fijos, automatizar procesos y revisar estrategia comercial para mejorar escalabilidad."
                },
                "optimo": {
                    "interpretacion": "Equilibrio entre rentabilidad y crecimiento.",
                    "causa": "Control eficiente de gastos operativos manteniendo inversión en crecimiento.",
                    "recomendacion": "Mantener balance actual entre rentabilidad y crecimiento."
                },
                "alto": {
                    "interpretacion": "Excelente eficiencia, pero posible riesgo de subinversión en el futuro.",
                    "causa": "Control estricto de gastos operativos o baja inversión en I+D y marketing. Control exhaustivo de costos, ventaja competitiva sólida o posible subinversión en crecimiento futuro.",
                    "recomendacion": "Reinvertir en innovación y expansión comercial para mantener ventaja competitiva a largo plazo."
                }
            }
        }
    
    def evaluate_ratio(self, ratio_name, value):
        """
        Evalúa un ratio financiero y devuelve interpretación completa.
        
        Args:
            ratio_name: Nombre del ratio (ej: 'fondo_maniobra', 'razon_liquidez')
            value: Valor numérico del ratio
            
        Returns:
            dict: Diccionario con interpretación, causa y recomendación
        """
        if ratio_name not in self.database:
            return {
                "error": f"Ratio '{ratio_name}' no encontrado en la base de datos"
            }
        
        data = self.database[ratio_name]
        low, high = data["rango"]
        
        # Determinar el estado
        if value < low:
            status = "bajo"
            details = data["bajo"]
        elif value > high:
            status = "alto"
            details = data["alto"]
        else:
            status = "optimo"
            details = data["optimo"]
        
        return {
            "nombre": data["nombre"],
            "valor": value,
            "rango_optimo": data["rango"],
            "estado": status,
            "unidad": data["unidad"],
            "interpretacion": details["interpretacion"],
            "causa": details["causa"],
            "recomendacion": details["recomendacion"]
        }
    
    def evaluate_multiple_ratios(self, ratios_dict):
        """
        Evalúa múltiples ratios de una vez.
        
        Args:
            ratios_dict: Diccionario con pares {nombre_ratio: valor}
            
        Returns:
            dict: Diccionario con análisis de cada ratio
        """
        results = {}
        for ratio_name, value in ratios_dict.items():
            results[ratio_name] = self.evaluate_ratio(ratio_name, value)
        return results
    
    def get_ratio_info(self, ratio_name):
        """
        Obtiene información básica de un ratio sin evaluarlo.
        
        Args:
            ratio_name: Nombre del ratio
            
        Returns:
            dict: Información del ratio (nombre, rango, unidad)
        """
        if ratio_name not in self.database:
            return None
        
        data = self.database[ratio_name]
        return {
            "nombre": data["nombre"],
            "rango_optimo": data["rango"],
            "unidad": data["unidad"]
        }
    
    def get_all_ratios_names(self):
        """Retorna lista de todos los ratios disponibles"""
        return list(self.database.keys())
    
    def generate_summary(self, ratios_dict):
        """
        Genera un resumen ejecutivo del análisis.
        
        Args:
            ratios_dict: Diccionario con pares {nombre_ratio: valor}
            
        Returns:
            dict: Resumen con contadores y ratios problemáticos
        """
        evaluations = self.evaluate_multiple_ratios(ratios_dict)
        
        bajo_count = 0
        alto_count = 0
        optimo_count = 0
        problematicos = []
        
        for ratio_name, analysis in evaluations.items():
            if "error" in analysis:
                continue
                
            if analysis["estado"] == "bajo":
                bajo_count += 1
                problematicos.append({
                    "ratio": analysis["nombre"],
                    "estado": "bajo",
                    "valor": analysis["valor"]
                })
            elif analysis["estado"] == "alto":
                alto_count += 1
                problematicos.append({
                    "ratio": analysis["nombre"],
                    "estado": "alto",
                    "valor": analysis["valor"]
                })
            else:
                optimo_count += 1
        
        total = bajo_count + alto_count + optimo_count
        
        return {
            "total_ratios": total,
            "optimos": optimo_count,
            "bajos": bajo_count,
            "altos": alto_count,
            "porcentaje_optimo": (optimo_count / total * 100) if total > 0 else 0,
            "ratios_problematicos": problematicos
        }
    
    # ============================================================
    # MÉTODOS PARA OBTENER VALORES ESPECÍFICOS
    # ============================================================
    
    def get_interpretacion(self, ratio_name, value):
        """
        Obtiene SOLO la interpretación de un ratio.
        
        Args:
            ratio_name: Nombre del ratio
            value: Valor del ratio
            
        Returns:
            str: Texto de interpretación
        """
        analysis = self.evaluate_ratio(ratio_name, value)
        if "error" in analysis:
            return analysis["error"]
        return analysis["interpretacion"]
    
    def get_causa(self, ratio_name, value):
        """
        Obtiene SOLO la causa de un ratio.
        
        Args:
            ratio_name: Nombre del ratio
            value: Valor del ratio
            
        Returns:
            str: Texto de causa
        """
        analysis = self.evaluate_ratio(ratio_name, value)
        if "error" in analysis:
            return analysis["error"]
        return analysis["causa"]
    
    def get_recomendacion(self, ratio_name, value):
        """
        Obtiene SOLO la recomendación de un ratio.
        
        Args:
            ratio_name: Nombre del ratio
            value: Valor del ratio
            
        Returns:
            str: Texto de recomendación
        """
        analysis = self.evaluate_ratio(ratio_name, value)
        if "error" in analysis:
            return analysis["error"]
        return analysis["recomendacion"]
    
    def get_estado(self, ratio_name, value):
        """
        Obtiene SOLO el estado (bajo/optimo/alto) de un ratio.
        
        Args:
            ratio_name: Nombre del ratio
            value: Valor del ratio
            
        Returns:
            str: Estado ('bajo', 'optimo', 'alto')
        """
        analysis = self.evaluate_ratio(ratio_name, value)
        if "error" in analysis:
            return "error"
        return analysis["estado"]
    
    def get_rango_optimo(self, ratio_name):
        """
        Obtiene el rango óptimo de un ratio sin evaluarlo.
        
        Args:
            ratio_name: Nombre del ratio
            
        Returns:
            tuple: (valor_minimo, valor_maximo)
        """
        if ratio_name not in self.database:
            return None
        return self.database[ratio_name]["rango"]
    
    def get_nombre_completo(self, ratio_name):
        """
        Obtiene el nombre completo/descriptivo de un ratio.
        
        Args:
            ratio_name: Nombre del ratio (clave)
            
        Returns:
            str: Nombre descriptivo
        """
        if ratio_name not in self.database:
            return None
        return self.database[ratio_name]["nombre"]
    
    def get_unidad(self, ratio_name):
        """
        Obtiene la unidad de medida de un ratio.
        
        Args:
            ratio_name: Nombre del ratio
            
        Returns:
            str: Unidad ('ratio', 'porcentaje', etc.)
        """
        if ratio_name not in self.database:
            return None
        return self.database[ratio_name]["unidad"]
    
    def get_all_details(self, ratio_name, value):
        """
        Obtiene todos los detalles por separado (útil para interfaces).
        
        Args:
            ratio_name: Nombre del ratio
            value: Valor del ratio
            
        Returns:
            dict: Diccionario con cada campo separado
        """
        return {
            "nombre": self.get_nombre_completo(ratio_name),
            "valor": value,
            "estado": self.get_estado(ratio_name, value),
            "rango_optimo": self.get_rango_optimo(ratio_name),
            "unidad": self.get_unidad(ratio_name),
            "interpretacion": self.get_interpretacion(ratio_name, value),
            "causa": self.get_causa(ratio_name, value),
            "recomendacion": self.get_recomendacion(ratio_name, value)
        }