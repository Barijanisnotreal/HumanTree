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
    {texto_biografico}
    """

    try:
        respuesta = ollama.generate(model=modelo, prompt=instrucciones, options={'temperature': 0.0})
        
        return respuesta['response'].strip()
        
    except Exception as e:
        return f"[!] Error en la ejecución: {e}"


if __name__ == "__main__":
    entrada = ""
    while entrada != "salir":
        entrada = input("\n>>>>>")
        if entrada.lower() == "salir":
            break
        sujeto = "none"
        print("\nProcesando...\n")
        resultado = extraer_relaciones_sujeto(sujeto, entrada)
        print(resultado)