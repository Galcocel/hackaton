import pandas as pd
import random
from datetime import datetime, timedelta

# --- 1. DEFINICIÓN DE NICHOS Y TEMAS AMPLIADOS ---
NICHOS = [
    "Gym Enthusiast",
    "Vegano",
    "Eco-Friendly",
    "Celíaco/Intolerancias",
    "Gourmet/Premium",
    "Conveniente/Express",
    "Familia Numerosa"
]

# Diccionario de palabras clave (títulos, hashtags) por nicho
TEMAS_POR_NICHO = {
    "Gym Enthusiast": {
        "titulos": ["Receta Post-Entreno Proteica", "La Mejor Proteína Barata de Hacendado", "Cena FIT en 10 minutos"],
        "hashtags_base": ["gymtok", "fitness", "proteina", "mercadona", "recetasfit", "volumen"],
        "urls_base": "https://www.tiktok.com/@gymfoodie/"
    },
    "Vegano": {
        "titulos": ["Tofu Revuelto Épico", "Alternativas Vegetales TOP en el Súper", "Postres Veganos Ricos y Rápidos"],
        "hashtags_base": ["vegano", "plantbased", "tofu", "mercadona", "recetasveganas", "singluten"],
        "urls_base": "https://www.tiktok.com/@veganlife_es/"
    },
    "Eco-Friendly": {
        "titulos": ["Productos Zero Waste de Mercadona", "Mi Compra a Granel", "Alternativas Sostenibles en el Baño"],
        "hashtags_base": ["ecofriendly", "sostenible", "zerowaste", "bio", "plasticfree", "productosverdes"],
        "urls_base": "https://www.tiktok.com/@eco_hacks/"
    },
    "Celíaco/Intolerancias": {
        "titulos": ["Pan Sin Gluten que Sabe a Pan Real", "Mi Compra CERO LACTOSA", "Postres aptos para Celíacos"],
        "hashtags_base": ["singluten", "celiaco", "glutenfree", "sinlactosa", "intolerancia", "apto"],
        "urls_base": "https://www.tiktok.com/@celiaco_reviews/"
    },
    "Gourmet/Premium": {
        "titulos": ["Catando el Queso Manchego Curado", "Aceite de Oliva AOVE: El Test", "Ideas para una Cena Romántica Premium"],
        "hashtags_base": ["gourmet", "cata", "recetapremium", "jamon", "aove", "delicatessen"],
        "urls_base": "https://www.tiktok.com/@gourmet_reviews/"
    },
    "Conveniente/Express": {
        "titulos": ["Cena por Menos de 5€ y en 5 Minutos", "Platos Preparados que Valen la Pena", "Tuppers de la Semana para Solteros"],
        "hashtags_base": ["rapido", "express", "cenafacil", "soltero", "comidapreparada", "ahorratiempo"],
        "urls_base": "https://www.tiktok.com/@quickmeals_es/"
    },
    "Familia Numerosa": {
        "titulos": ["Compra Mensual en Mercadona (MAXI CESTA)", "Tuppers para Toda la Semana Familiar", "Recetas de Pasta que Encantan a Todos"],
        "hashtags_base": ["familia", "comprasemanal", "organizacion", "recetasencasa", "packahorro", "granel"],
        "urls_base": "https://www.tiktok.com/@misfamiliafood/"
    }
}

# --- 2. FUNCIÓN GENERADORA ---
def generate_tiktok_data(n_entries=8000):
    """Genera una base de datos simulada de videos de TikTok con la nueva lista de nichos."""
    data = []
    video_counter = 1
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    print(f"Generando {n_entries} entradas de TikTok con nichos ampliados...")

    for i in range(n_entries):
        # 1. Seleccionar Nicho (Tribu)
        # Hacemos que algunos nichos (Gym/Vegano/Familia) sean ligeramente más comunes
        pesos = [4, 4, 3, 2, 1, 3, 3] # Pesos para los 7 nichos
        nicho = random.choices(NICHOS, weights=pesos, k=1)[0]
        temas = TEMAS_POR_NICHO[nicho]
        
        # 2. Generar Título y Hashtags
        titulo = random.choice(temas["titulos"])
        
        num_random_tags = random.randint(2, 4)
        random_tags = random.sample(temas["hashtags_base"], num_random_tags)
        
        # Añadir tags de marca y genéricos
        if random.random() < 0.6: random_tags.append("mercadona")
        if random.random() < 0.4: random_tags.append("hacendado")
        if random.random() < 0.3: random_tags.append("recetasfaciles")
            
        hashtags = ", ".join(f"#{tag}" for tag in random_tags)
        
        # 3. Generar URL (Simulada)
        url_id = random.randint(700000000000000000, 800000000000000000)
        url = f"{temas['urls_base']}video/{url_id}"
        
        # 4. Generar Fecha de Publicación
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        fecha_pub = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M:%S")

        # 5. Generar Métricas de Engagement (Ligeramente sesgado por nicho)
        base_views = random.randint(5000, 50000)
        
        if nicho in ["Gym Enthusiast", "Vegano", "Conveniente/Express"]:
            base_views *= random.randint(2, 5) # Mayor viralidad
            
        views = base_views
        likes = int(views * random.uniform(0.02, 0.08)) 
        comments = int(likes * random.uniform(0.05, 0.15)) 

        data.append({
            "video_id": f"V{video_counter:05d}",
            "nicho_tribu": nicho, # ¡Esta es la columna target para el ML!
            "titulo": titulo,
            "hashtags": hashtags,
            "url_video": url,
            "fecha_publicacion": fecha_pub,
            "vistas": views,
            "likes": likes,
            "comentarios": comments
        })
        video_counter += 1
        
    return pd.DataFrame(data)

# --- 3. FUNCIÓN PRINCIPAL Y GUARDADO ---
def main():
    print("🚀 Iniciando la generación de la Base de Datos Simulada de TikTok (8000 entradas)...")
    
    tiktok_df = generate_tiktok_data(n_entries=8000)
    
    filename = 'tiktok_simulated_data_ampliada.csv'
    tiktok_df.to_csv(filename, index=False, encoding='utf-8')
    
    print("\n✅ Base de Datos Simulada de TikTok generada exitosamente!")
    print(f"   🎥 Total de Videos: {len(tiktok_df)}")
    print(f"   💾 Archivo guardado como: {filename}")
    
    print("\n   Distribución por Nicho (para el ML):")
    for tribu, count in tiktok_df['nicho_tribu'].value_counts().items():
        print(f"      • {tribu}: {count} videos")

if __name__ == "__main__":
    main()