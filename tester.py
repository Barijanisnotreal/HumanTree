import ollama
import pandas as pd

def extraer_relaciones_gold_standard(texto: str, modelo: str = "phi3") -> str:
    """
    Analiza un texto con el Prompt Maestro reforzado (Few-Shot) en inglés.
    """
    prompt_maestro = f"""You are a strict, robotic data extraction system. Your ONLY task is to extract family relationships and birthdates exactly as instructed.

UNBREAKABLE RULES:
1. FORMAT: Use ONLY "Entity_A ---> [LABEL] ---> Entity_B".
2. LABELS: Only use [SPOUSE], [CHILD], [PARENT], [SIBLING], and [BIRTHDATE].
3. BIDIRECTIONAL: [SPOUSE] and [SIBLING] relationships MUST be written both ways (A to B, and B to A) on separate lines.
4. BOTH PARENTS RULE: If two people adopt or have a child together, you MUST extract the [CHILD] relationship for BOTH parents, and the [PARENT] relationship mapping the child to BOTH parents.
5. NO ASSUMPTIONS: Do NOT add a [SPOUSE] relationship just because two people share a child or adopt. Only use [SPOUSE] if the text explicitly says they are married or "hitched".
6. EXACT DATES ONLY: Extract [BIRTHDATE] ONLY if a specific numerical date (e.g., DD/MM/YYYY) is provided. Ignore relative words like "yesterday".
7. If there are no relationships, output absolutely nothing.

REFERENCE EXAMPLES:

Text: Emily and Thomas adopted James years ago. Many mistakenly believe they are their nephew. The internet connection failed several times.
Output:
Emily ---> [CHILD] ---> James
Thomas ---> [CHILD] ---> James
James ---> [PARENT] ---> Emily
James ---> [PARENT] ---> Thomas

Text: Thomas is hitched to James. Their kid Sarah had a bday yesterday. They also bought a new printer for the office.
Output:
Thomas ---> [SPOUSE] ---> James
James ---> [SPOUSE] ---> Thomas
Thomas ---> [CHILD] ---> Sarah
James ---> [CHILD] ---> Sarah
Sarah ---> [PARENT] ---> Thomas
Sarah ---> [PARENT] ---> James

Text: Laura was born on 05/12/1980. They are married to Sophia. Their child Olivia was born on 02/08/2010. Jonathan is the sibling of Laura.
Output:
Laura ---> [SPOUSE] ---> Sophia
Sophia ---> [SPOUSE] ---> Laura
Laura ---> [CHILD] ---> Olivia
Sophia ---> [CHILD] ---> Olivia
Olivia ---> [PARENT] ---> Laura
Olivia ---> [PARENT] ---> Sophia
Laura ---> [SIBLING] ---> Jonathan
Jonathan ---> [SIBLING] ---> Laura
Laura ---> [BIRTHDATE] ---> 05/12/1980
Olivia ---> [BIRTHDATE] ---> 02/08/2010

TEXT TO ANALYZE:
{texto}
Output:"""

    try:
        # Temperature a 0.0 es crucial para mantenerlo predecible
        respuesta = ollama.generate(model=modelo, prompt=prompt_maestro, options={'temperature': 0.0})
        return respuesta['response'].strip()
    except Exception as e:
        return ""

def evaluar_dataset(ruta_csv: str, modelo: str = "phi3"):
    """
    Ejecuta una evaluación automatizada del dataset completo y muestra 
    el progreso caso por caso en tiempo real.

    Args:
        ruta_csv (str): Ruta del archivo CSV generado previamente.
        modelo (str, optional): Modelo de Ollama a evaluar. Por defecto "phi3".
    """
    print(f"Cargando dataset desde {ruta_csv}...")
    try:
        df = pd.read_csv(ruta_csv)
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo '{ruta_csv}'.")
        return

    # Manejamos los valores nulos (cuando se espera silencio absoluto)
    df['expected_output'] = df['expected_output'].fillna("")
    
    total_casos = len(df)
    aciertos = 0
    errores = []

    print("="*60)
    print(f" INICIANDO EVALUACIÓN EN TIEMPO REAL (Modelo: {modelo})")
    print("="*60)
    
    for index, row in df.iterrows():
        id_caso = row['id']
        texto_input = row['input']
        salida_esperada = str(row['expected_output']).strip()
        
        # Llamada a la IA
        salida_ia = extraer_relaciones_gold_standard(texto_input, modelo).strip()
        
        # Lógica de comparación matemática basada en conjuntos (sets)
        set_esperado = set([linea.strip() for linea in salida_esperada.split('\n') if linea.strip()])
        set_ia = set([linea.strip() for linea in salida_ia.split('\n') if linea.strip()])
        
        if set_ia == set_esperado:
            aciertos += 1
            print(f"[{index + 1}/{total_casos}] Caso {id_caso}: ✅ ACIERTO")
        else:
            errores.append(id_caso)
            print(f"[{index + 1}/{total_casos}] Caso {id_caso}: ❌ ERROR")
            print(f"   - Se esperaba: {set_esperado}")
            print(f"   - IA devolvió: {set_ia}")
            print("-" * 40) # Separador visual para los errores

    # --- REPORTE FINAL ---
    accuracy = (aciertos / total_casos) * 100
    
    print("\n" + "="*50)
    print("      REPORTE FINAL DE EVALUACIÓN")
    print("="*50)
    print(f"Total casos analizados: {total_casos}")
    print(f"Aciertos: {aciertos}")
    print(f"Fallos: {len(errores)}")
    print(f"PORCENTAJE DE ACIERTO (ACCURACY): {accuracy:.2f}%")
    print("="*50)

# --- Ejecutar el Test ---
if __name__ == "__main__":
    # Asegúrate de poner el nombre exacto de tu archivo
    evaluar_dataset("family_relations_noisy_1000_EN.csv", modelo="phi3")