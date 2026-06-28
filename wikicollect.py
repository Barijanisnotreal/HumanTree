import requests
import csv
import time
from tqdm import tqdm

# 1. CONFIGURACIÓN
URL_WIKIDATA = "https://query.wikidata.org/sparql"
ARCHIVO_SALIDA = "wikipedia_human_tags.csv"
HEADERS = {
    'User-Agent': 'WikiHumanTagCollector/2.0 (barijanrosita@gmail.com)'
}

def ejecutar_consulta(query):
    intentos = 3
    for i in range(intentos):
        try:
            response = requests.get(URL_WIKIDATA, params={'format': 'json', 'query': query}, headers=HEADERS, timeout=60)
            if response.status_code == 429:
                time.sleep(30)
                continue
            response.raise_for_status()
            return response.json()
        except Exception:
            time.sleep(5 * (i + 1))
    return None

def guardar_en_csv(resultados):
    with open(ARCHIVO_SALIDA, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        for fila in resultados:
            escritor.writerow([fila])

def generar_intervalos():
    intervalos = []
    intervalos.append(("0001-01-01", "1400-01-01", "Antigüedad"))
    for año in range(1400, 1700, 50):
        intervalos.append((f"{año}-01-01", f"{año+50}-01-01", f"{año}-{año+50}"))
    for año in range(1700, 1900, 10):
        intervalos.append((f"{año}-01-01", f"{año+10}-01-01", f"{año}-{año+10}"))
    for año in range(1900, 2026, 2):
        intervalos.append((f"{año}-01-01", f"{año+2}-01-01", f"{año}-{año+2}"))
    return intervalos

def main():
    print(f"Iniciando descarga. Los datos se guardarán en '{ARCHIVO_SALIDA}'\n")
    
    try:
        with open(ARCHIVO_SALIDA, mode='x', newline='', encoding='utf-8') as archivo:
            csv.writer(archivo).writerow(["wikipedia_title"])
    except FileExistsError:
        pass 

    intervalos = generar_intervalos()
    letras_abecedario = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    total_tareas = len(intervalos) + len(letras_abecedario)
    total_recuperado = 0

    # Inicializamos la barra de progreso general
    with tqdm(total=total_tareas, desc="Progreso Total", unit="lote") as barra_progreso:
        
        # FASE 1: Fechas de nacimiento
        for desde, hasta, descripcion in intervalos:
            # Actualizamos el texto de la barra para saber por qué año vamos
            barra_progreso.set_description(f"Buscando: {descripcion}")
            
            query = f"""
            SELECT ?wpTitle WHERE {{
              ?item wdt:P31 wd:Q5 .
              ?item wdt:P569 ?birth .
              FILTER(?birth >= "{desde}"^^xsd:dateTime && ?birth < "{hasta}"^^xsd:dateTime)
              ?wpUrl schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> .
              BIND(SUBSTR(STR(?wpUrl), 31) AS ?wpTitle)
            }}
            """
            
            datos = ejecutar_consulta(query)
            if datos:
                tags_bloque = [fila['wpTitle']['value'] for fila in datos['results']['bindings']]
                guardar_en_csv(tags_bloque)
                total_recuperado += len(tags_bloque)
                
                # Mostramos el número de tags acumulados a la derecha de la barra
                barra_progreso.set_postfix(tags_guardados=total_recuperado)
            
            barra_progreso.update(1) # Avanzamos un paso en la barra
            time.sleep(2.0)

        # FASE 2: Sin fecha registrada
        for letra in letras_abecedario:
            barra_progreso.set_description(f"Buscando sin fecha: Letra {letra}")
            
            query_sin_fecha = f"""
            SELECT ?wpTitle WHERE {{
              ?item wdt:P31 wd:Q5 .
              MINUS {{ ?item wdt:P569 ?birth . }}
              ?wpUrl schema:about ?item ; schema:isPartOf <https://en.wikipedia.org/> .
              BIND(SUBSTR(STR(?wpUrl), 31) AS ?wpTitle)
              FILTER(STRSTARTS(STR(?wpTitle), "{letra}"))
            }}
            """
            
            datos = ejecutar_consulta(query_sin_fecha)
            if datos:
                tags_bloque = [fila['wpTitle']['value'] for fila in datos['results']['bindings']]
                guardar_en_csv(tags_bloque)
                total_recuperado += len(tags_bloque)
                barra_progreso.set_postfix(tags_guardados=total_recuperado)
                
            barra_progreso.update(1)
            time.sleep(2.0)

    print(f"\n¡Proceso finalizado! Se han guardado {total_recuperado} tags exitosamente.")

if __name__ == "__main__":
    main()