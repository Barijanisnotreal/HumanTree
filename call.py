import ollama

def extraer_relaciones_sujeto(sujeto_principal: str, texto_biografico: str, modelo: str = "phi3") -> str:
    """
    Extrae las relaciones familiares directas de un sujeto específico en un texto.

    Esta función envía un texto y unas instrucciones estructuradas a un modelo de
    lenguaje local a través de la API de Ollama. Obliga al modelo a extraer
    únicamente las relaciones familiares del sujeto principal proporcionado y a
    devolverlas en un formato predefinido estricto.

    Args:
        sujeto_principal (str): El nombre de la persona cuyas relaciones se
            desean extraer (ej. "Christopher Nolan").
        texto_biografico (str): El párrafo o texto completo que contiene la
            información biográfica a analizar.
        modelo (str, optional): El nombre del modelo local instalado en Ollama
            que procesará la solicitud. Por defecto es "phi3".

    Returns:
        str: Una cadena de texto con las relaciones familiares extraídas en el 
            formato "Sujeto -> [Relación] -> Persona B". Si ocurre un error 
            durante la conexión con Ollama, devuelve el mensaje del error.

    Raises:
        Exception: Captura y devuelve como texto cualquier excepción originada 
            por un fallo de conexión o ejecución de la librería `ollama`.
    """
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

    print(f"Conectando con el servidor local de Ollama (Modelo: {modelo})...")
    print("Enviando el texto a evaluación...\n")

    try:
        respuesta = ollama.generate(model=modelo, prompt=instrucciones)
        
        print("=========================================")
        print("   RELACIONES FAMILIARES EXTRAÍDAS")
        print("=========================================")
        return respuesta['response'].strip()
        
    except Exception as e:
        return f"[!] Error en la ejecución: {e}"

# 


# --- Ejecutar el Test ---
if __name__ == "__main__":
    print(extraer_relaciones_sujeto("Ungofa", "Ungofa es una persona importante en la vida de Christopher Nolan. Ungofa es capaz de hacer muchas cosas, pero no es su hermano ni su cónyuge. Ungofa conoció a Emma Thomas, la productora de Christopher Nolan, y también ha trabajado con Jonathan Nolan, el hermano del director. Ungofa es el rey del mambo. Ungofa es hijo de Jeffrey Epstein. Ungofa es el padre de Juan De Dios"))