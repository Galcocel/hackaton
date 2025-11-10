import pandas as pd
import json
from collections import defaultdict
import os

# Nombre del archivo JSON de entrada (el que generaste en el análisis mensual)
INPUT_JSON_FILE = 'analisis_tendencias_mensual.json'
# Nombre del archivo de salida para el diccionario de ML
OUTPUT_JSON_FILE = 'diccionario_ponderacion_ml.json'


def generar_diccionario_ponderacion_porcentual(input_file: str) -> dict:
    """
    Procesa el JSON mensual para generar un diccionario de Nicho: Ponderación (%)
    para Machine Learning. La ponderación es (Vistas Totales) normalizado.
    """
    
    if not os.path.exists(input_file):
        print(f"❌ Error: No se encuentra el archivo de entrada: {input_file}")
        return {}
    
    # 1. Cargar el JSON
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error al cargar o parsear el JSON: {e}")
        return {}
        
    # Inicializar el acumulador principal
    ponderacion_acumulada_nicho = defaultdict(int)
    
    if 'analisis_mensual' not in data:
        print("❌ Error: Estructura JSON inválida. Falta la clave 'analisis_mensual'.")
        return {}
        
    for mes, datos_mes in data['analisis_mensual'].items():
        # Acumular la métrica de tendencia (Vistas Totales) de cada nicho a través de todos los meses.
        for registro in datos_mes.get('vistas_totales_nicho', []):
            try:
                nicho = registro['nicho_tribu']
                # Usamos vistas totales como la Ponderación Bruta de Tendencia
                ponderacion_bruta = registro['vistas_totales']
                
                ponderacion_acumulada_nicho[nicho] += ponderacion_bruta
                
            except KeyError:
                print(f"Advertencia: Registro incompleto en el mes {mes}. Se omite.")
                continue

    # 2. Calcular la Ponderación Total (suma de la ponderación de todos los nichos)
    suma_total_ponderacion = sum(ponderacion_acumulada_nicho.values())
    
    # 3. Normalizar a Porcentaje
    diccionario_final_porcentual = {}
    if suma_total_ponderacion > 0:
        # CORRECCIÓN: Usamos ponderacion_acumulada_nicho, la variable correcta.
        for nicho, ponderacion_bruta in ponderacion_acumulada_nicho.items(): 
            # (Ponderación Bruta / Suma Total) * 100
            porcentaje = (ponderacion_bruta / suma_total_ponderacion) * 100
            # Redondeamos a dos decimales
            diccionario_final_porcentual[nicho] = round(porcentaje, 2)
    
    return diccionario_final_porcentual

def main():
    print("🤖 Iniciando generación de diccionario de ponderación para ML...")
    
    # 1. Generar el diccionario
    diccionario_ml = generar_diccionario_ponderacion_porcentual(INPUT_JSON_FILE)
    
    if not diccionario_ml:
        print("❌ Proceso de ponderación fallido o diccionario vacío.")
        return

    # 2. Guardar el diccionario final en formato JSON
    try:
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(diccionario_ml, f, ensure_ascii=False, indent=4)
            
        print(f"\n✅ Diccionario de Ponderación ML generado exitosamente.")
        print(f"   💾 Archivo guardado como: {OUTPUT_JSON_FILE}")
        
        print("\n--- Vista Previa del Diccionario (Nicho: Porcentaje) ---")
        top_nichos = sorted(diccionario_ml.items(), key=lambda item: item[1], reverse=True)[:3]
        for nicho, porcentaje in top_nichos:
            print(f"   • {nicho}: {porcentaje:.2f}%")
        print("-------------------------------------------------------")

    except Exception as e:
        print(f"❌ Error al guardar el archivo JSON: {e}")

if __name__ == "__main__":
    main()