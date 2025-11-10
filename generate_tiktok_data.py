
import pandas as pd
import random
from datetime import datetime, timedelta

# --- 1. DEFINICIÓN DE NICHOS (Basados en Necesidad/Dieta) ---
NICHOS = [
    "Gym Enthusiast", "Vegano", "Eco-Friendly", "Celíaco/Intolerancias", 
    "Gourmet/Premium", "Conveniente/Express", "Familia Numerosa"
]

# --- 2. PRODUCTOS ASOCIADOS Y TEMAS ---
PRODUCTOS_POR_NICHO = {
    "Gym Enthusiast": ["Queso Fresco Batido 0%", "Claras de Huevo", "Barrita de Proteínas (Sabor Varios)", "Crema de Cacahuete Natural"],
    "Vegano": ["Tofu Ecológico Hacendado", "Bebida de Avena BIO", "Hamburguesas Vegetales (Sabor X)", "Hummus Clásico"],
    "Eco-Friendly": ["Huevos Ecológicos (L)", "Bolsas Reutilizables Fruta", "Champú Sólido", "Arroz Integral BIO"],
    "Celíaco/Intolerancias": ["Pan de Molde Sin Gluten", "Leche Sin Lactosa", "Pasta de Maíz/Arroz (Sin Gluten)", "Galletas de Arroz"],
    "Gourmet/Premium": ["Aceite de Oliva Virgen Extra (AOVE) Selección", "Jamón Ibérico Loncheado", "Queso Curado Añejo", "Vino Tinto Reserva"],
    "Conveniente/Express": ["Ensalada Completa Lista para Comer", "Lasaña de Carne Refrigerada", "Pizza Congelada Variada", "Bandeja de Sushi"],
    "Familia Numerosa": ["Pack Ahorro de Leche Entera (6L)", "Detergente Lavadora Formato XL", "Pasta Espagueti (1kg)", "Arroz Redondo (Saco 5kg)"]
}

TEMAS_POR_NICHO = {
    "Gym Enthusiast": {"titulos": ["Receta Post-Entreno Proteica", "La Mejor Proteína Barata", "Cena FIT en 10 minutos"], "hashtags_base": ["gymtok", "fitness", "proteina", "mercadona"]},
    "Vegano": {"titulos": ["Tofu Revuelto Épico", "Alternativas Vegetales TOP", "Postres Veganos Rápidos"], "hashtags_base": ["vegano", "plantbased", "tofu", "mercadona"]},
    "Eco-Friendly": {"titulos": ["Productos Zero Waste", "Mi Compra a Granel", "Alternativas Sostenibles"], "hashtags_base": ["ecofriendly", "sostenible", "zerowaste", "bio"]},
    "Celíaco/Intolerancias": {"titulos": ["Pan Sin Gluten que Sabe a Pan Real", "Mi Compra CERO LACTOSA", "Postres aptos para Celíacos"], "hashtags_base": ["singluten", "celiaco", "glutenfree", "sinlactosa"]},
    "Gourmet/Premium": {"titulos": ["Catando el Queso Curado", "Aceite de Oliva AOVE: El Test", "Cena Romántica Premium"], "hashtags_base": ["gourmet", "cata", "recetapremium", "jamon"]},
    "Conveniente/Express": {"titulos": ["Cena por Menos de 5€ y en 5 Minutos", "Platos Preparados que Valen la Pena", "Tuppers de la Semana para Solteros"], "hashtags_base": ["rapido", "express", "cenafacil", "soltero"]},
    "Familia Numerosa": {"titulos": ["Compra Mensual (MAXI CESTA)", "Tuppers para Toda la Semana Familiar", "Recetas de Pasta que Encantan a Todos"], "hashtags_base": ["familia", "comprasemanal", "organizacion", "packahorro"]}
}


def generate_tiktok_data(n_entries=8000):
    data = []
    video_counter = 1
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180) 

    print(f"Generando {n_entries} entradas de TikTok con producto asociado (Necesidad/Dieta)...")

    for i in range(n_entries):
        pesos = [4, 4, 3, 2, 1, 3, 3]
        nicho = random.choices(NICHOS, weights=pesos, k=1)[0]
        temas = TEMAS_POR_NICHO[nicho]
        
        producto = random.choice(PRODUCTOS_POR_NICHO[nicho])

        titulo = random.choice(temas["titulos"])
        
        num_random_tags = random.randint(2, 4)
        random_tags = random.sample(temas["hashtags_base"], num_random_tags)
        
        if random.random() < 0.6: random_tags.append("mercadona")
        if random.random() < 0.4: random_tags.append("hacendado")
        if random.random() < 0.2: random_tags.append(producto.lower().split('(')[0].strip().replace(' ', ''))

        hashtags = ", ".join(f"#{tag}" for tag in random_tags)
        
        url_id = random.randint(700000000000000000, 800000000000000000)
        url = f"https://www.tiktok.com/@simulated_user/video/{url_id}"
        
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
            "producto_mercadona": producto,
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

def main():
    tiktok_df = generate_tiktok_data(n_entries=8000)
    filename = 'tiktok_simulated_data_final_necesidades.csv'
    tiktok_df.to_csv(filename, index=False, encoding='utf-8')
    print(f"
✅ Base de Datos Simulada generada: {filename}")

if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("ERROR: La librería 'pandas' no está instalada. Ejecuta: pip install pandas")
