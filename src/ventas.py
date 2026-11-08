from tabulate import tabulate
from validaciones import ReglaNegocioError
import persistencia


def calcular_descuento(subtotal: float) -> tuple[float, float]:
    if subtotal >= 100000.0:
        return 0.10, subtotal * 0.10
    elif subtotal >= 50000.0:
        return 0.05, subtotal * 0.05
    return 0.0, 0.0


def procesar_venta_interactiva(inventario: dict) -> None:
    carrito = {}

    while True:
        print("\n--- AGREGAR PRODUCTO AL CARRITO ---")
        codigo = input("Ingrese codigo del producto (o presione ENTER para finalizar seleccion): ").strip().upper()
        if not codigo:
            if not carrito:
                print(" Operacion cancelada. El carrito esta vacio.")
                return
            break

        if codigo not in inventario:
            print(f" Error: El producto '{codigo}' no existe.")
            continue

        prod = inventario[codigo]
        stock_disp = prod["stock"] - carrito.get(codigo, 0)
        print(f"Producto: {prod['nombre']} | Precio: ${prod['precio']:,.2f} | Disponible: {stock_disp}")

        if stock_disp <= 0:
            print(" No hay stock disponible para agregar mas unidades de este producto.")
            continue

        try:
            cant_str = input("Cantidad a comprar: ").strip()
            cantidad = int(cant_str)
            if cantidad <= 0:
                print(" La cantidad debe ser mayor a cero.")
                continue
            if cantidad > stock_disp:
                raise ReglaNegocioError(
                    f"Stock insuficiente. Solo quedan {stock_disp} unidades disponibles de {prod['nombre']}."
                )

            carrito[codigo] = carrito.get(codigo, 0) + cantidad
            print(f" {prod['nombre']} x{cantidad} agregado correctamente al carrito.")

        except ValueError:
            print(" Error: Debe ingresar una cantidad entera.")
        except ReglaNegocioError as e:
            print(f" {e}")

        otro = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
        if otro != "s":
            break

    items_detalle = []
    subtotal = 0.0
    for cod, cant in carrito.items():
        p = inventario[cod]
        parcial = p["precio"] * cant
        subtotal += parcial
        items_detalle.append({
            "codigo": cod,
            "nombre": p["nombre"],
            "precio": p["precio"],
            "cantidad": cant,
            "subtotal": parcial
        })

    pct_desc, val_desc = calcular_descuento(subtotal)
    total = subtotal - val_desc

    print("\n" + "=" * 50)
    print("RESUMEN DE VENTA")
    print("=" * 50)
    tabla_resumen = [
        [i["codigo"], i["nombre"], i["cantidad"], f"${i['precio']:,.2f}", f"${i['subtotal']:,.2f}"]
        for i in items_detalle
    ]
    print(tabulate(tabla_resumen, headers=["Codigo", "Producto", "Cant.", "Precio Unit.", "Subtotal"], tablefmt="simple"))
    print("-" * 50)
    print(f"Subtotal:       ${subtotal:,.2f}")
    print(f"Descuento ({int(pct_desc * 100)}%): -${val_desc:,.2f}")
    print(f"TOTAL A PAGAR:  ${total:,.2f}")
    print("=" * 50)

    confirmar = input("¿Confirmar compra? (s/n): ").strip().lower()
    if confirmar != "s":
        print(" Venta cancelada. No se modifico el inventario.")
        return

    while True:
        try:
            monto_pago = float(input("\nIngrese dinero recibido: $").strip().replace(",", "."))
            if monto_pago < total:
                print(f" Pago insuficiente. Faltan ${total - monto_pago:,.2f}. Intente nuevamente.")
                continue
            cambio = monto_pago - total
            print(f" Pago aceptado. Su cambio es: ${cambio:,.2f}")
            break
        except ValueError:
            print(" Error: Ingrese un valor numerico valido.")

    for item in items_detalle:
        inventario[item["codigo"]]["stock"] -= item["cantidad"]

    persistencia.guardar_inventario(inventario)
    persistencia.registrar_venta_archivo(total, items_detalle)
    print(" Venta registrada exitosamente e inventario actualizado.")