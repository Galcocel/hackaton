
import pandas as pd
import os
import json

INPUT_FILE = 'tiktok_simulated_data_final_necesidades.csv'
OUTPUT_FILE = 'analisis_tendencias_mensual.json'

def cargar_y_limpiar_datos(file_path):
    if not os.path.exists(file_path):
        print(f"Error: No se encuentra el archivo: {file_path}")
        return None
    
    df = pd.read_csv(file_path)
    df = df[df['vistas'] > 0].copy()
    
    df['fecha_publicacion'] = pd.to_datetime(df['fecha_publicacion'])
    df['mes_anyo'] = df['fecha_publicacion'].dt.to_period('M').astype(str)
    
    df['ratio_likes_por_vista'] = df['likes'] / df['vistas']
    
    return df

def analisis_principal_mensual(df):
    
    resultados_mensuales = {}
    meses_ordenados = sorted(df['mes_anyo'].unique())
    
    for mes in meses_ordenados:
        df_mes = df[df['mes_anyo'] == mes].copy()
        resultados_mes = {}
        
        # 1. ANÁLISIS DE RENDIMIENTO POR NICHO EN ESTE MES
        nicho_stats = df_mes.groupby('nicho_tribu').agg(
            vistas_totales=('vistas', 'sum'),
            total_videos=('video_id', 'count'),
            ratio_engagement_promedio=('ratio_likes_por_vista', 'mean') 
        ).reset_index()
        
        vistas_sorted = nicho_stats.sort_values(by='vistas_totales', ascending=False)
        engagement_sorted = nicho_stats.sort_values(by='ratio_engagement_promedio', ascending=False)
        
        resultados_mes["vistas_totales_nicho"] = vistas_sorted[['nicho_tribu', 'vistas_totales', 'total_videos']].to_dict(orient='records')
        resultados_mes["engagement_promedio_nicho"] = engagement_sorted[['nicho_tribu', 'ratio_engagement_promedio']].to_dict(orient='records')

        # 2. ANÁLISIS DE PRODUCTOS POR NICHO EN ESTE MES (TOP 3)
        productos_por_nicho = {}
        
        for nicho in df_mes['nicho_tribu'].unique():
            df_nicho = df_mes[df_mes['nicho_tribu'] == nicho]
            
            producto_stats = df_nicho.groupby('producto_mercadona').agg(
                frecuencia_videos=('video_id', 'count'),
                vistas_totales=('vistas', 'sum')
            ).reset_index()
            
            top_productos = producto_stats.sort_values(by='vistas_totales', ascending=False).head(3)
            productos_por_nicho[nicho] = top_productos.to_dict(orient='records')
            
        resultados_mes["productos_en_tendencia"] = productos_por_nicho
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
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(resultados_json, f, ensure_ascii=False, indent=4)
    
    print(f"
✅ Análisis MENSAL completado. Archivo generado: {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        pass
