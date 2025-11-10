import pandas as pd
import random
from datetime import datetime, timedelta

# --- 1. DEFINICIÓN DE NICHOS (Basados en Necesidad/Dieta) ---
NICHOS = [
    "Gym Enthusiast",
    "Vegano",
    "Eco-Friendly",
    "Celíaco/Intolerancias",
    "Gourmet/Premium",
    "Conveniente/Express",
    "Familia Numerosa"
]

# --- 2. PRODUCTOS ASOCIADOS POR NICHO ---
# Diccionario que asocia el nicho con productos específicos de Mercadona.
PRODUCTOS_POR_NICHO = {
    "Gym Enthusiast": [
        "Queso Fresco Batido 0%", 
        "Claras de Huevo", 
        "Barrita de Proteínas (Sabor Varios)",
        "Crema de Cacahuete Natural",
        "Pechuga de Pavo Loncheada"
    ],
    "Vegano": [
        "Tofu Ecológico Hacendado", 
        "Bebida de Avena BIO", 
        "Hamburguesas Vegetales (Sabor X)",
        "Hummus Clásico",
        "Garbanzos Cocidos (Bote)"
    ],
    "Eco-Friendly": [
        "Huevos Ecológicos (L)", 
        "Bolsas Reutilizables Fruta", 
        "Champú Sólido",
        "Arroz Integral BIO",
        "Detergente Ecológico"
    ],
    "Celíaco/Intolerancias": [
        "Pan de Molde Sin Gluten", 
        "Leche Sin Lactosa", 
        "Pasta de Maíz/Arroz (Sin Gluten)",
        "Galletas de Arroz",
        "Pan Tostado Sin Gluten"
    ],
    "Gourmet/Premium": [
        "Aceite de Oliva Virgen Extra (AOVE) Selección", 
        "Jamón Ibérico Loncheado", 
        "Queso Curado Añejo",
        "Vino Tinto Reserva",
        "Chocolate 85% Cacao"
    ],
    "Conveniente/Express": [
        "Ensalada Completa Lista para Comer", 
        "Lasaña de Carne Refrigerada", 
        "Pizza Congelada Variada",
        "Bandeja de Sushi",
        "Tortilla de Patatas Envasada"
    ],
    "Familia Numerosa": [
        "Pack Ahorro de Leche Entera (6L)", 
        "Detergente Lavadora Formato XL", 
        "Pasta Espagueti (1kg)",
        "Huevos Talla L (Docena)",
        "Arroz Redondo (Saco 5kg)"
    ]
}

# (El diccionario TEMAS_POR_NICHO se mantiene como lo proporcionaste)
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


# --- 3. FUNCIÓN GENERADORA ---
def generate_tiktok_data(n_entries=8000):
    """Genera una base de datos simulada de videos de TikTok con el producto asociado."""
    data = []
    video_counter = 1
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    print(f"Generando {n_entries} entradas de TikTok con producto asociado (Necesidad/Dieta)...")

    for i in range(n_entries):
        # 1. Seleccionar Nicho (Tribu)
        pesos = [4, 4, 3, 2, 1, 3, 3] # Pesos para los 7 nichos
        nicho = random.choices(NICHOS, weights=pesos, k=1)[0]
        temas = TEMAS_POR_NICHO[nicho]
        
        # 2. Seleccionar Producto Asociado (¡NUEVA LÓGICA!)
        producto = random.choice(PRODUCTOS_POR_NICHO[nicho])

        # 3. Generar Título y Hashtags
        titulo = random.choice(temas["titulos"]) 
        
        num_random_tags = random.randint(2, 4)
        random_tags = random.sample(temas["hashtags_base"], num_random_tags)
        
        # Añadir tags de marca, genéricos y producto específico
        if random.random() < 0.6: random_tags.append("mercadona")
        if random.random() < 0.4: random_tags.append("hacendado")
        if random.random() < 0.2: random_tags.append(producto.lower().split('(')[0].strip().replace(' ', '')) # Hashtag del producto

        hashtags = ", ".join(f"#{tag}" for tag in random_tags)
        
        # 4. Generar URL, Fecha, y Métricas
        url_id = random.randint(700000000000000000, 800000000000000000)
        url = f"{temas['urls_base']}video/{url_id}"
        
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        fecha_pub = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d %H:%M:%S")

        base_views = random.randint(5000, 50000)
        
        if nicho in ["Gym Enthusiast", "Vegano", "Conveniente/Express"]:
            base_views *= random.randint(2, 5) 
            
        views = base_views
        likes = int(views * random.uniform(0.02, 0.08)) 
        comments = int(likes * random.uniform(0.05, 0.15)) 

        data.append({
            "video_id": f"V{video_counter:05d}",
            "nicho_tribu": nicho, 
            "producto_mercadona": producto, # ¡NUEVA COLUMNA DE PRODUCTO!
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

# --- 4. FUNCIÓN PRINCIPAL Y GUARDADO ---
def main():
    print("🚀 Generando Base de Datos Simulada de TikTok (8000 entradas) con PRODUCTO ASOCIADO...")
    
    tiktok_df = generate_tiktok_data(n_entries=8000)
    
    filename = 'tiktok_simulated_data_final_necesidades.csv'
    tiktok_df.to_csv(filename, index=False, encoding='utf-8')
    
    print("\n✅ Base de Datos Simulada (FINAL) generada exitosamente!")
    print(f"   🎥 Total de Videos: {len(tiktok_df)}")
    print(f"   💾 Archivo guardado como: {filename}")
    
    print("\n   Tarea completada. La columna 'producto_mercadona' vincula la tendencia al inventario.")

if __name__ == "__main__":
    main()