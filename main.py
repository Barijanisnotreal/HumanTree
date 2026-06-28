import ollama

sujeto_principal = "Christopher Nolan"
texto_biografico = "Christopher Nolan está casado con la productora Emma Thomas. Además, suele trabajar con su hermano, el guionista Jonathan Nolan." # El texto de la wikipedia

instrucciones = f"""
Actúa como un sistema automatizado de extracción de datos.
El sujeto principal de este texto es: {sujeto_principal}.

REGLAS ESTRICTAS:
1. Extrae TODAS las relaciones familiares que involucren a {sujeto_principal}.
2. Usa ESTRICTAMENTE el formato "{sujeto_principal} -> [Relación] -> Persona B".
3. Las relaciones permitidas son solo: [Cónyuge], [Hermano], [Padre], [Hijo], [Primo].
4. No extraigas relaciones entre personas secundarias.

TEXTO A ANALIZAR:
{texto_biografico}
"""

print("Conectando con el servidor local de Ollama...")
print("Enviando el texto a Phi-3...\n")

print("=========================================")
print("   RELACIONES FAMILIARES EXTRAÍDAS")
print("=========================================")