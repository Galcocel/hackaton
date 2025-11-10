import pandas as pd
import os
import json

# --- CONFIGURACIÓN ---
INPUT_FILE = 'tiktok_simulated_data_final_necesidades.csv'
OUTPUT_FILE = 'analisis_tendencias_mensual.json'

def cargar_y_limpiar_datos(file_path):
    """Carga el CSV, limpia los datos y prepara la columna de Mes/Año."""
    if not os.path.exists(file_path):
        print(f"Error: No se encuentra el archivo en la ruta especificada: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df = df[df['vistas'] > 0].copy()
    
    # Conversión y preparación de la columna de tiempo CRUCIAL
    df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
    # Creamos una columna Mes/Año para agrupar (ej. '2025-02')
    df['mes_anyo'] = df['fecha_publicacion'].dt.to_period('M').astype(str)
    
    # Cálculo de métrica clave: Ratio de Engagement (Likes por Vista)
    df['ratio_likes_por_vista'] = df['likes'] / df['vistas']
    
    return df

def analisis_principal_mensual(df):
    """
    Realiza el análisis de Vistas Totales, Engagement y Productos Top por Nicho,
    agrupado por cada mes.
    """
    
    resultados_mensuales = {}
    
    # Ordenamos los meses para que aparezcan cronológicamente en el JSON
    meses_ordenados = sorted(df['mes_anyo'].unique())
    
    for mes in meses_ordenados:
        df_mes = df[df['mes_anyo'] == mes].copy()
        
        # Diccionario para almacenar los resultados del mes actual
        resultados_mes = {}
        
        # =======================================================
        # 1. ANÁLISIS DE RENDIMIENTO POR NICHO EN ESTE MES
        # =======================================================
        nicho_stats = df_mes.groupby('nicho_tribu').agg(
            vistas_totales=('vistas', 'sum'),
            total_videos=('video_id', 'count'),
            ratio_engagement_promedio=('ratio_likes_por_vista', 'mean') 
        ).reset_index()
        
        # Vistas y Engagement
        vistas_sorted = nicho_stats.sort_values(by='vistas_totales', ascending=False)
        engagement_sorted = nicho_stats.sort_values(by='ratio_engagement_promedio', ascending=False)
        
        resultados_mes["vistas_totales_nicho"] = vistas_sorted[['nicho_tribu', 'vistas_totales', 'total_videos']].to_dict(orient='records')
        resultados_mes["engagement_promedio_nicho"] = engagement_sorted[['nicho_tribu', 'ratio_engagement_promedio']].to_dict(orient='records')

        # =======================================================
        # 2. ANÁLISIS DE PRODUCTOS POR NICHO EN ESTE MES (TOP 3)
        # =======================================================
        productos_por_nicho = {}
        
        for nicho in df_mes['nicho_tribu'].unique():
            df_nicho = df_mes[df_mes['nicho_tribu'] == nicho]
            
            # Agrupamos por producto y sumamos las vistas
            producto_stats = df_nicho.groupby('producto_mercadona').agg(
                frecuencia_videos=('video_id', 'count'),
                vistas_totales=('vistas', 'sum')
            ).reset_index()
            
            # Ordenamos por Vistas Totales (indicador de tendencia)
            top_productos = producto_stats.sort_values(by='vistas_totales', ascending=False).head(3)
            
            productos_por_nicho[nicho] = top_productos.to_dict(orient='records')
            
        resultados_mes["productos_en_tendencia"] = productos_por_nicho
        
        # Almacenar resultados del mes en el diccionario principal
        resultados_mensuales[mes] = resultados_mes

    return {
        "fecha_analisis": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        "analisis_mensual": resultados_mensuales
    }

def main():
    print(f"🚀 Iniciando análisis de datos de {INPUT_FILE} con desglose mensual...")
    
    df_analisis = cargar_y_limpiar_datos(INPUT_FILE)
    
    if df_analisis is None:
        return
        
    resultados_json = analisis_principal_mensual(df_analisis)
    
    # Exportar el resultado consolidado a JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(resultados_json, f, ensure_ascii=False, indent=4)
    
    print("\n" + "=" * 60)
    print(f"✅ ¡Análisis MENSAL completado! Archivo JSON generado para Angular.")
    print(f"   💾 Archivo guardado como: {OUTPUT_FILE}")
    print("   La estructura ahora permite crear gráficos de evolución temporal.")
    print("=" * 60)

if __name__ == "__main__":
    # Nota importante: Asegúrate de que tu script de generación de datos simule
    # fechas distribuidas en varios meses para que este análisis funcione bien.
    main()