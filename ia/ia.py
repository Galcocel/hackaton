import json

# Ruta del archivo JSON
RUTA_JSON = "datos.json"

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
    print(obtener_pesos_cliente("cliente1"))
    print(obtener_pesos_ciudad("Valencia"))

    modificar_pesos_cliente("cliente1", [0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 0.1])
    modificar_pesos_ciudad("Valencia", [0.1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1])