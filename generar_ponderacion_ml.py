
import json
from collections import defaultdict
import os

INPUT_JSON_FILE = 'analisis_tendencias_mensual.json'
OUTPUT_JSON_FILE = 'diccionario_ponderacion_ml.json'


def generar_diccionario_ponderacion_porcentual(input_file: str) -> dict:
    
    if not os.path.exists(input_file):
        print(f"❌ Error: No se encuentra el archivo de entrada: {input_file}")
        return {}
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error al cargar o parsear el JSON: {e}")
        return {}
        
    ponderacion_acumulada_nicho = defaultdict(int)
    
    if 'analisis_mensual' not in data:
        print("❌ Error: Estructura JSON inválida. Falta la clave 'analisis_mensual'.")
        return {}
        
    for mes, datos_mes in data['analisis_mensual'].items():
        for registro in datos_mes.get('vistas_totales_nicho', []):
            try:
                nicho = registro['nicho_tribu']
                ponderacion_bruta = registro['vistas_totales']
                
                ponderacion_acumulada_nicho[nicho] += ponderacion_bruta
                
            except KeyError:
                print(f"Advertencia: Registro incompleto en el mes {mes}. Se omite.")
                continue

    suma_total_ponderacion = sum(ponderacion_acumulada_nicho.values())
    
    diccionario_final_porcentual = {}
    if suma_total_ponderacion > 0:
        for nicho, ponderacion_bruta in ponderacion_acumulada_nicho.items(): 
            porcentaje = (ponderacion_bruta / suma_total_ponderacion) * 100
            diccionario_final_porcentual[nicho] = round(porcentaje, 2)
    
    return diccionario_final_porcentual

def main():
    print("🤖 Iniciando generación de diccionario de ponderación para ML...")
    
    diccionario_ml = generar_diccionario_ponderacion_porcentual(INPUT_JSON_FILE)
    
    if not diccionario_ml:
        return

    try:
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(diccionario_ml, f, ensure_ascii=False, indent=4)
            
        print(f"
✅ Diccionario de Ponderación ML generado exitosamente.")
        print(f"   💾 Archivo guardado como: {OUTPUT_JSON_FILE}")

    except Exception as e:
        print(f"❌ Error al guardar el archivo JSON: {e}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        pass
