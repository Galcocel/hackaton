import subprocess
import os
import sys

# --- CONFIGURACIÓN DE ARCHIVOS ---
GENERATOR_SCRIPT = 'generate_tiktok_data.py'
ANALYSIS_SCRIPT = 'analisis_tendencias.py'
ML_SCRIPT = 'generar_ponderacion_ml.py' 

# Archivos de SALIDA a eliminar:
OUTPUT_FILES = [
    'tiktok_simulated_data_final_necesidades.csv', 
    'analisis_tendencias_mensual.json',            
    'diccionario_ponderacion_ml.json'              
]

# --- FUNCIONES DE PIPELINE ---

def cleanup(files_to_delete):
    """Elimina los archivos de salida generados previamente."""
    print("\n🧹 Iniciando la limpieza de archivos de salida...")
    cleaned_count = 0
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"   🗑️ Eliminado: {filename}")
                cleaned_count += 1
            except OSError as e:
                print(f"   ❌ Error al intentar eliminar {filename}: {e}")
    
    if cleaned_count == 0:
        print("   ✅ No se encontraron archivos de salida previos que eliminar.")
    else:
        print("   ✅ Limpieza completada.")
    return True

def run_script(script_name):
    """Ejecuta un script de Python y maneja la salida."""
    print(f"\n{'='*50}")
    print(f"▶️ Iniciando la ejecución de: {script_name}")
    print(f"{'='*50}")
    
    # Verificación de existencia, fundamental en esta versión corta
    if not os.path.exists(script_name):
        print(f"❌ ERROR CRÍTICO: No se encontró el script '{script_name}'.")
        print("Asegúrate de que el archivo existe en esta carpeta.")
        return False
        
    try:
        subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            check=True,         
            text=True
        )
        print(f"\n✅ Éxito al ejecutar {script_name}.")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: La ejecución de {script_name} falló.")
        print(f"Detalles del error: {e}")
        return False
    except FileNotFoundError:
        print(f"\n❌ ERROR: El ejecutable de Python no fue encontrado.")
        return False

def run_pipeline():
    """Ejecuta toda la tubería de datos secuencialmente."""
    print("🤖 INICIANDO PIPELINE DE HACKATHON COMPLETO (Versión Compacta) 📊")
    print("-" * 60)
    
    # 1. LIMPIEZA
    cleanup(OUTPUT_FILES)

    # 2. EJECUCIÓN DE SCRIPTS
    if not run_script(GENERATOR_SCRIPT):
        print("\n🛑 PIPELINE DETENIDO: Fallo en la generación de datos.")
        return

    if not run_script(ANALYSIS_SCRIPT):
        print("\n🛑 PIPELINE DETENIDO: Fallo en el análisis de tendencias.")
        return

    if not run_script(ML_SCRIPT):
        print("\n🛑 PIPELINE DETENIDO: Fallo en la generación del diccionario ML.")
        return

    print("\n\n🎉 **PIPELINE COMPLETADO EXITOSAMENTE** 🎉")
    print("Se han generado los 3 archivos de salida listos para usarse.")


if __name__ == "__main__":
    run_pipeline()