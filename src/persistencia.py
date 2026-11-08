import os
from datetime import datetime

RUTA_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ARCHIVO_INVENTARIO = os.path.join(RUTA_DATA, "inventario.txt")
ARCHIVO_VENTAS = os.path.join(RUTA_DATA, "ventas.txt")


def asegurar_directorio() -> None:
    if not os.path.exists(RUTA_DATA):
        os.makedirs(RUTA_DATA)


def cargar_inventario() -> dict:
    asegurar_directorio()
    inventario = {}

    if not os.path.exists(ARCHIVO_INVENTARIO):
        print(" Advertencia: 'data/inventario.txt' no existe. Se iniciara con inventario vacio.")
        return inventario

    with open(ARCHIVO_INVENTARIO, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split("|")
            if len(partes) != 7:
                print(f" [Advertencia Linea {num_linea}] Formato corrupto omitido: '{linea}'")
                continue

            codigo, nombre, categoria, precio_str, stock_str, stock_min_str, proveedor = partes
            try:
                precio = float(precio_str)
                stock = int(stock_str)
                stock_minimo = int(stock_min_str)

                if precio <= 0 or stock < 0 or stock_minimo < 0:
                    print(f" [Advertencia Linea {num_linea}] Valores numericos no validos en: '{linea}'")
                    continue

                inventario[codigo.upper()] = {
                    "codigo": codigo.upper(),
                    "nombre": nombre,
                    "categoria": categoria,
                    "precio": precio,
                    "stock": stock,
                    "stock_minimo": stock_minimo,
                    "proveedor": proveedor
                }
            except ValueError:
                print(f" [Advertencia Linea {num_linea}] Error numerico al procesar: '{linea}'")

    return inventario


def guardar_inventario(inventario: dict) -> None:
    asegurar_directorio()
    with open(ARCHIVO_INVENTARIO, "w", encoding="utf-8") as f:
        for prod in inventario.values():
            linea = (
                f"{prod['codigo']}|{prod['nombre']}|{prod['categoria']}|"
                f"{prod['precio']:.1f}|{prod['stock']}|{prod['stock_minimo']}|{prod['proveedor']}\n"
            )
            f.write(linea)


def registrar_venta_archivo(total: float, items: list[dict], fecha_str: str = None) -> None:
    asegurar_directorio()
    if not fecha_str:
        fecha_str = datetime.now().strftime("%Y-%m-%d")

    str_items = "; ".join([f"{item['codigo']}:{item['cantidad']}" for item in items])
    linea = f"{fecha_str} {total:.1f} {str_items}\n"

    with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as f:
        f.write(linea)


def cargar_historial_ventas() -> list[dict]:
    asegurar_directorio()
    ventas = []
    if not os.path.exists(ARCHIVO_VENTAS):
        return ventas

    with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea:
                continue
            if "|" in linea:
                partes = linea.split("|")
            else:
                partes = linea.split(" ", 2)

            if len(partes) != 3:
                continue

            fecha, total_str, detalle_str = partes
            try:
                total = float(total_str)
                items = []
                for token in detalle_str.split(";"):
                    token = token.strip()
                    if ":" in token:
                        c, cant = token.split(":")
                        items.append({"codigo": c.strip(), "cantidad": int(cant.strip())})
                ventas.append({"fecha": fecha.strip(), "total": total, "items": items})
            except ValueError:
                print(f" [Advertencia Ventas Linea {num_linea}] Error en formato de venta.")

    return ventas