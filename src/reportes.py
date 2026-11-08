from datetime import datetime
from collections import defaultdict
from tabulate import tabulate
import persistencia


def generar_alertas_stock(inventario: dict) -> None:
    alertas_por_proveedor = defaultdict(list)

    for p in inventario.values():
        if p["stock"] <= p["stock_minimo"]:
            estado = "AGOTADO" if p["stock"] == 0 else "BAJO STOCK"
            alertas_por_proveedor[p["proveedor"]].append([
                p["codigo"],
                p["nombre"],
                p["categoria"],
                p["stock"],
                p["stock_minimo"],
                estado
            ])

    if not alertas_por_proveedor:
        print("\n No hay productos en alerta. Todo el inventario supera el stock minimo.")
        return

    print("\n" + "=" * 65)
    print(" REPORTE DE ALERTAS DE REABASTECIMIENTO")
    print("=" * 65)

    for prov, items in alertas_por_proveedor.items():
        print(f"\nProveedor: {prov}")
        print(tabulate(
            items,
            headers=["Codigo", "Producto", "Categoria", "Stock Actual", "Minimo", "Estado"],
            tablefmt="grid"
        ))


def generar_cierre_del_dia(inventario: dict, fecha_consulta: str = None) -> None:
    if not fecha_consulta:
        fecha_consulta = datetime.now().strftime("%Y-%m-%d")

    historial = persistencia.cargar_historial_ventas()
    ventas_hoy = [v for v in historial if v["fecha"] == fecha_consulta]

    print("\n" + "=" * 60)
    print(f" CIERRE DE CAJA DEL DIA: {fecha_consulta}")
    print("=" * 60)

    num_transacciones = len(ventas_hoy)
    if num_transacciones == 0:
        print(f"No se registraron ventas en la fecha {fecha_consulta}.")
        return

    total_vendido = sum(v["total"] for v in ventas_hoy)
    ticket_promedio = total_vendido / num_transacciones

    conteo_productos = defaultdict(int)
    categorias_activas = set()

    for v in ventas_hoy:
        for item in v["items"]:
            c = item["codigo"]
            cant = item["cantidad"]
            conteo_productos[c] += cant
            if c in inventario:
                categorias_activas.add(inventario[c]["categoria"])

    mas_vendido_cod, mas_vendido_cant = max(conteo_productos.items(), key=lambda x: x[1])
    nombre_mas_vendido = inventario.get(mas_vendido_cod, {}).get("nombre", mas_vendido_cod)

    productos_sin_ventas = [
        f"{p['codigo']} - {p['nombre']}"
        for p in inventario.values()
        if p["codigo"] not in conteo_productos
    ]

    print(f"• Total vendido:               ${total_vendido:,.2f} COP")
    print(f"• Numero de transacciones:     {num_transacciones}")
    print(f"• Ticket promedio:             ${ticket_promedio:,.2f} COP")
    print(f"• Producto mas vendido:        {nombre_mas_vendido} ({mas_vendido_cant} unidades)")
    print(f"• Categorias con movimiento:   {', '.join(sorted(categorias_activas)) if categorias_activas else 'Ninguna'}")
    print(f"• Total productos sin ventas:  {len(productos_sin_ventas)}")

    if productos_sin_ventas:
        print("\nListado de referencias sin venta hoy:")
        for sin_v in productos_sin_ventas[:10]:
            print(f"  - {sin_v}")
        if len(productos_sin_ventas) > 10:
            print(f"  ... y {len(productos_sin_ventas) - 10} referencias mas.")
    print("=" * 60)