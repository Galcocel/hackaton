import json
import os

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import numpy as np

# Cargar modelo de embeddings (solo una vez)
model = SentenceTransformer("all-MiniLM-L6-v2")
import numpy as np
import json

# Cargar modelo de embeddings (solo una vez)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ruta del JSON
RUTA_JSON = "clientes_ciudades.json"

def actualizar_pesos_cliente_con_lista(nombre_cliente, lista_compra, clf, alpha=0.5):
    """
    Actualiza los pesos de un cliente combinando los actuales con los generados
    a partir de una lista de compra. Usa alpha como factor de mezcla.
    """
    # Cargar datos
    with open(RUTA_JSON, "r") as archivo:
        datos = json.load(archivo)

    # Verificar cliente
    if nombre_cliente not in datos["clientes"]:
        print(f"Cliente '{nombre_cliente}' no encontrado.")
        return

    # Obtener pesos actuales
    pesos_actuales = np.array(datos["clientes"][nombre_cliente])

    # Generar embedding y predicción
    frase = " ".join(lista_compra)
    embedding = model.encode(frase).reshape(1, -1)
    nuevos_pesos = np.array(clf.predict_proba(embedding)[0])

    # Mezclar pesos (alpha controla cuánto influye la nueva predicción)
    pesos_actualizados = (1 - alpha) * pesos_actuales + alpha * nuevos_pesos

    # Guardar en JSON
    datos["clientes"][nombre_cliente] = pesos_actualizados.tolist()
    with open(RUTA_JSON, "w") as archivo:
        json.dump(datos, archivo, indent=2)

    print(f"Pesos de '{nombre_cliente}' actualizados con la lista de compra.")
    return pesos_actualizados.tolist()


# Ruta del archivo JSON (ubicada junto a este script)
# Esto asegura que el script encuentre datos.json aunque se ejecute desde otra carpeta
RUTA_JSON = os.path.join(os.path.dirname(__file__), "datos.json")

# Cargar datos desde el JSON
def cargar_datos():
    try:
        with open(RUTA_JSON, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("Archivo JSON no encontrado.")
        return {"clientes": {}, "ciudades": {}}

# Guardar datos en el JSON
def guardar_datos(datos):
    with open(RUTA_JSON, "w") as archivo:
        json.dump(datos, archivo, indent=2)
        print("Cambios guardados correctamente.")

# Consultar pesos de un cliente
def obtener_pesos_cliente(nombre_cliente):
    datos = cargar_datos()
    pesos = datos["clientes"].get(nombre_cliente)
    if pesos:
        return pesos
    else:
        print(f"Cliente '{nombre_cliente}' no encontrado.")
        return None

# Consultar pesos de una ciudad
def obtener_pesos_ciudad(nombre_ciudad):
    datos = cargar_datos()
    pesos = datos["ciudades"].get(nombre_ciudad)
    if pesos:
        return pesos
    else:
        print(f"Ciudad '{nombre_ciudad}' no encontrada.")
        return None

# Modificar pesos de un cliente
def modificar_pesos_cliente(nombre_cliente, nuevos_pesos):
    if len(nuevos_pesos) != 7:
        print("Error: El array debe tener exactamente 7 valores.")
        return
    datos = cargar_datos()
    if nombre_cliente in datos["clientes"]:
        datos["clientes"][nombre_cliente] = nuevos_pesos
        guardar_datos(datos)
        print(f"Pesos de '{nombre_cliente}' actualizados.")
    else:
        print(f"Cliente '{nombre_cliente}' no encontrado.")

# Modificar pesos de una ciudad
def modificar_pesos_ciudad(nombre_ciudad, nuevos_pesos):
    if len(nuevos_pesos) != 7:
        print("Error: El array debe tener exactamente 7 valores.")
        return
    datos = cargar_datos()
    if nombre_ciudad in datos["ciudades"]:
        datos["ciudades"][nombre_ciudad] = nuevos_pesos
        guardar_datos(datos)
        print(f"Pesos de ciudad '{nombre_ciudad}' actualizados.")
    else:
        print(f"Ciudad '{nombre_ciudad}' no encontrada.")

# Ejemplo de uso
if __name__ == "__main__":
    
    lista = ["manzanas", "plátanos", "leche", "pan"]

    cliente = "cliente1"

    nuevos_pesos = actualizar_pesos_cliente_con_lista(cliente, lista, alpha=0.5)

    modificar_pesos_cliente(cliente, nuevos_pesos)

    print(nuevos_pesos)