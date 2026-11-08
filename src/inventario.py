from tabulate import tabulate
from validaciones import ReglaNegocioError

CATEGORIAS_VALIDAS = ["Lacteos", "Bebidas", "Aseo", "Abarrotes", "Snacks"]


def registrar_producto(inventario: dict, codigo: str, nombre: str, categoria: str,
                       precio: float, stock: int, stock_minimo: int, proveedor: str) -> None:
    codigo_limpio = codigo.strip().upper()
    if codigo_limpio in inventario:
        raise ReglaNegocioError(f"El codigo '{codigo_limpio}' ya pertenece a otro producto.")

    if precio <= 0 or stock < 0 or stock_minimo <= 0:
        raise ReglaNegocioError("Precios, stock o umbrales deben cumplir los limites numericos.")

    inventario[codigo_limpio] = {
        "codigo": codigo_limpio,
        "nombre": nombre.strip(),
        "categoria": categoria.strip(),
        "precio": float(precio),
        "stock": int(stock),
        "stock_minimo": int(stock_minimo),
        "proveedor": proveedor.strip()
    }


def consultar_por_codigo(inventario: dict, codigo: str):
    return inventario.get(codigo.strip().upper())


def consultar_por_categoria(inventario: dict, categoria: str) -> list[dict]:
    cat_busqueda = categoria.strip().lower()
    return [p for p in inventario.values() if p["categoria"].lower() == cat_busqueda]


def modificar_producto(inventario: dict, codigo: str, nuevo_precio: float = None, nuevo_stock: int = None) -> None:
    codigo_limpio = codigo.strip().upper()
    if codigo_limpio not in inventario:
        raise ReglaNegocioError(f"El producto con codigo '{codigo_limpio}' no existe.")

    if nuevo_precio is not None:
        if nuevo_precio <= 0:
            raise ReglaNegocioError("El precio debe ser estrictamente positivo.")
        inventario[codigo_limpio]["precio"] = nuevo_precio

    if nuevo_stock is not None:
        if nuevo_stock < 0:
            raise ReglaNegocioError("El stock no puede ser negativo.")
        inventario[codigo_limpio]["stock"] = nuevo_stock


def eliminar_producto(inventario: dict, codigo: str) -> dict:
    codigo_limpio = codigo.strip().upper()
    if codigo_limpio not in inventario:
        raise ReglaNegocioError(f"El producto '{codigo_limpio}' no existe en el inventario.")
    return inventario.pop(codigo_limpio)


def formatear_tabla_productos(productos: list[dict]) -> str:
    if not productos:
        return "No hay productos para mostrar."
    tabla = []
    for p in productos:
        tabla.append([
            p["codigo"],
            p["nombre"],
            p["categoria"],
            f"${p['precio']:,.2f}",
            p["stock"],
            p["stock_minimo"],
            p["proveedor"]
        ])
    encabezados = ["Codigo", "Nombre", "Categoria", "Precio (COP)", "Stock", "Stock Min.", "Proveedor"]
    return tabulate(tabla, headers=encabezados, tablefmt="grid")