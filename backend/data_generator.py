import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# === PRODUCTOS POR TRIBU ===
productos_gym = [
    {"id": "P001", "name": "Claras de huevo (6 uds)", "cat": "Proteína", "price": 4.5, "tags": "Gym Enthusiast"},
    {"id": "P002", "name": "Avena integral (1kg)", "cat": "Carbohidratos", "price": 2.3, "tags": "Gym Enthusiast"},
    {"id": "P003", "name": "Pechuga de pollo (500g)", "cat": "Proteína", "price": 4.15, "tags": "Gym Enthusiast"},
    {"id": "P004", "name": "Arroz integral (1kg)", "cat": "Carbohidratos", "price": 1.8, "tags": "Gym Enthusiast"},
    {"id": "P005", "name": "Brócoli (500g)", "cat": "Verdura", "price": 1.2, "tags": "Gym Enthusiast"},
    {"id": "P006", "name": "Proteína whey (1kg)", "cat": "Suplemento", "price": 24.5, "tags": "Gym Enthusiast"},
]

productos_vegano = [
    {"id": "P010", "name": "Tofu ecológico (400g)", "cat": "Proteína", "price": 3.2, "tags": "Vegano"},
    {"id": "P011", "name": "Bebida de soja (1L)", "cat": "Lácteos Alt", "price": 1.5, "tags": "Vegano"},
    {"id": "P012", "name": "Garbanzos ecológicos", "cat": "Legumbre", "price": 2.1, "tags": "Vegano"},
    {"id": "P013", "name": "Tahini (300g)", "cat": "Condimento", "price": 4.5, "tags": "Vegano"},
    {"id": "P014", "name": "Quinoa (500g)", "cat": "Cereal", "price": 3.8, "tags": "Vegano"},
    {"id": "P015", "name": "Aguacate (4 uds)", "cat": "Fruta", "price": 4.2, "tags": "Vegano"},
]

productos_familia = [
    {"id": "P020", "name": "Leche entera (6 pack)", "cat": "Lácteos", "price": 5.4, "tags": "Familia Numerosa"},
    {"id": "P021", "name": "Pan de molde", "cat": "Panadería", "price": 1.2, "tags": "Familia Numerosa"},
    {"id": "P022", "name": "Yogures naturales (12 uds)", "cat": "Lácteos", "price": 3.6, "tags": "Familia Numerosa"},
    {"id": "P023", "name": "Pasta (3 packs)", "cat": "Carbohidratos", "price": 2.7, "tags": "Familia Numerosa"},
    {"id": "P024", "name": "Tomate frito (3 botes)", "cat": "Conserva", "price": 2.1, "tags": "Familia Numerosa"},
    {"id": "P025", "name": "Galletas (2 packs)", "cat": "Dulce", "price": 3.0, "tags": "Familia Numerosa"},
]

productos_estudiante = [
    {"id": "P030", "name": "Pasta instantánea (5 uds)", "cat": "Preparado", "price": 3.5, "tags": "Conveniente/Express"},
    {"id": "P031", "name": "Pizza congelada", "cat": "Congelado", "price": 2.8, "tags": "Conveniente/Express"},
    {"id": "P032", "name": "Bebida energética (4 uds)", "cat": "Bebida", "price": 4.0, "tags": "Conveniente/Express"},
    {"id": "P033", "name": "Patatas fritas", "cat": "Snack", "price": 1.5, "tags": "Conveniente/Express"},
    {"id": "P034", "name": "Sandwich mixto", "cat": "Preparado", "price": 2.2, "tags": "Conveniente/Express"},
]

productos_gourmet = [
    {"id": "P040", "name": "Queso manchego curado", "cat": "Queso", "price": 8.5, "tags": "Gourmet/Premium"},
    {"id": "P041", "name": "Aceite de oliva virgen extra", "cat": "Aceite", "price": 12.0, "tags": "Gourmet/Premium"},
    {"id": "P042", "name": "Jamón ibérico (100g)", "cat": "Embutido", "price": 15.5, "tags": "Gourmet/Premium"},
    {"id": "P043", "name": "Vino tinto reserva", "cat": "Bebida", "price": 9.5, "tags": "Gourmet/Premium"},
    {"id": "P044", "name": "Chocolate 85% cacao", "cat": "Dulce", "price": 3.8, "tags": "Gourmet/Premium"},
]

# === MAPEO TRIBU → PRODUCTOS ===
tribu_productos = {
    "Gym Enthusiast": productos_gym,
    "Vegano": productos_vegano,
    "Familia": productos_familia,
    "Estudiante": productos_estudiante,
    "Gourmet": productos_gourmet,
}

def generar_usuarios(n_users=500):
    """Genera usuarios con diferentes perfiles/tribus"""
    users = []
    tribus = list(tribu_productos.keys())
    
    for i in range(n_users):
        tribu = random.choice(tribus)
        users.append({
            "user_id": f"U{i:04d}",
            "age": random.randint(18, 65),
            "location": random.choice(["Valencia", "Madrid", "Barcelona", "Sevilla", "Bilbao"]),
            "tribu": tribu,
            "first_purchase": datetime.now() - timedelta(days=random.randint(30, 730))
        })
    
    return pd.DataFrame(users)

def generar_tickets(users_df, n_tickets_per_user_range=(8, 20)):
    """Genera tickets de compra según el perfil de cada usuario"""
    tickets = []
    ticket_items = []
    ticket_counter = 0
    
    for _, user in users_df.iterrows():
        productos_pool = tribu_productos[user['tribu']]
        n_tickets = random.randint(*n_tickets_per_user_range)
        
        for t in range(n_tickets):
            ticket_id = f"T{ticket_counter:06d}"
            days_offset = int((datetime.now() - user['first_purchase']).days * (t / n_tickets))
            ticket_date = user['first_purchase'] + timedelta(days=days_offset)
            
            # Seleccionar 3-7 productos
            n_productos = random.randint(3, 7)
            productos_comprados = random.sample(productos_pool, min(n_productos, len(productos_pool)))
            
            total_amount = 0
            for producto in productos_comprados:
                quantity = random.randint(1, 4)
                subtotal = producto['price'] * quantity
                total_amount += subtotal
                
                ticket_items.append({
                    "ticket_id": ticket_id,
                    "product_id": producto['id'],
                    "product_name": producto['name'],
                    "category": producto['cat'],
                    "quantity": quantity,
                    "unit_price": producto['price'],
                    "subtotal": round(subtotal, 2),
                    "tags": producto['tags']
                })
            
            tickets.append({
                "ticket_id": ticket_id,
                "user_id": user['user_id'],
                "date": ticket_date.strftime("%Y-%m-%d"),
                "total_amount": round(total_amount, 2),
                "store_location": f"Mercadona {user['location']}"
            })
            
            ticket_counter += 1
    
    return pd.DataFrame(tickets), pd.DataFrame(ticket_items)

def generar_catalogo_productos():
    """Genera el catálogo completo de productos"""
    todos_productos = []
    for productos in tribu_productos.values():
        todos_productos.extend(productos)
    
    # Eliminar duplicados por ID
    productos_unicos = {p['id']: p for p in todos_productos}
    return pd.DataFrame(list(productos_unicos.values()))

def main():
    print("🚀 Generando base de datos simulada...")
    
    # Crear carpeta data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Generar datos
    print("📊 Generando usuarios...")
    users_df = generar_usuarios(n_users=500)
    
    print("🛒 Generando tickets de compra...")
    tickets_df, items_df = generar_tickets(users_df, n_tickets_per_user_range=(10, 20))
    
    print("📦 Generando catálogo de productos...")
    products_df = generar_catalogo_productos()
    
    # Guardar CSVs
    users_df.to_csv('data/users.csv', index=False)
    tickets_df.to_csv('data/tickets.csv', index=False)
    items_df.to_csv('data/ticket_items.csv', index=False)
    products_df.to_csv('data/products.csv', index=False)
    
    # Estadísticas
    print("\n✅ Base de datos generada exitosamente!")
    print(f"   👥 Usuarios: {len(users_df)}")
    print(f"   🎫 Tickets: {len(tickets_df)}")
    print(f"   📝 Items de compra: {len(items_df)}")
    print(f"   📦 Productos en catálogo: {len(products_df)}")
    print(f"\n   Distribución por tribu:")
    for tribu, count in users_df['tribu'].value_counts().items():
        print(f"      • {tribu}: {count} usuarios ({count/len(users_df)*100:.1f}%)")
    
    print(f"\n💾 Archivos guardados en: backend/data/")

if __name__ == "__main__":
    main()