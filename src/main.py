import sys
import persistencia
import inventario as inv
import ventas as vts
import reportes as rpt
import validaciones as val


def submenu_inventario(inventario: dict) -> None:
    while True:
        print("\n--- GESTION DE INVENTARIO ---")
        print("1. Registrar nuevo producto")
        print("2. Consultar producto por codigo")
        print("3. Consultar productos por categoria")
        print("4. Modificar precio y stock")
        print("5. Eliminar producto")
        print("6. Listar todo el inventario")
        print("7. Regresar al menu principal")

        op = val.leer_opcion_menu("Seleccione una opcion (1-7): ", ["1", "2", "3", "4", "5", "6", "7"])

        if op == "1":
            print("\n[Nuevo Producto]")
            codigo = val.leer_texto_no_vacio("Codigo unico (ej. LAC001): ").upper()
            if codigo in inventario:
                print(f" Error: El codigo {codigo} ya existe. Operacion rechazada.")
                continue

            nombre = val.leer_texto_no_vacio("Nombre comercial: ")
            print(f"Categorias sugeridas: {', '.join(inv.CATEGORIAS_VALIDAS)}")
            categoria = val.leer_texto_no_vacio("Categoria: ")
            precio = val.leer_flotante_positivo("Precio unitario (COP): ")
            stock = val.leer_entero_positivo("Stock inicial: ", permitir_cero=True)
            stock_min = val.leer_entero_positivo("Stock minimo para alerta: ", permitir_cero=False)
            proveedor = val.leer_texto_no_vacio("Proveedor: ")

            try:
                inv.registrar_producto(inventario, codigo, nombre, categoria, precio, stock, stock_min, proveedor)
                persistencia.guardar_inventario(inventario)
                print(" Producto agregado y guardado exitosamente.")
            except val.ReglaNegocioError as e:
                print(f" Error de negocio: {e}")

        elif op == "2":
            codigo = val.leer_texto_no_vacio("Codigo a consultar: ")
            p = inv.consultar_por_codigo(inventario, codigo)
            if p:
                print(inv.formatear_tabla_productos([p]))
            else:
                print(f" No se encontro ningun producto con el codigo '{codigo}'.")

        elif op == "3":
            cat = val.leer_texto_no_vacio("Categoria a buscar: ")
            encontrados = inv.consultar_por_categoria(inventario, cat)
            if encontrados:
                print(inv.formatear_tabla_productos(encontrados))
            else:
                print(f" No hay productos registrados bajo la categoria '{cat}'.")

        elif op == "4":
            codigo = val.leer_texto_no_vacio("Codigo del producto a modificar: ")
            p = inv.consultar_por_codigo(inventario, codigo)
            if not p:
                print(f" Producto '{codigo}' no encontrado.")
                continue

            print(f"Modificando: {p['nombre']} (Precio: ${p['precio']}, Stock: {p['stock']})")
            mod_p = input("¿Desea cambiar el precio? (s/n): ").strip().lower()
            nuevo_precio = val.leer_flotante_positivo("Nuevo precio: ") if mod_p == "s" else None

            mod_s = input("¿Desea cambiar el stock? (s/n): ").strip().lower()
            nuevo_stock = val.leer_entero_positivo("Nuevo stock: ", permitir_cero=True) if mod_s == "s" else None

            try:
                inv.modificar_producto(inventario, codigo, nuevo_precio, nuevo_stock)
                persistencia.guardar_inventario(inventario)
                print(" Producto modificado y guardado con exito.")
            except val.ReglaNegocioError as e:
                print(f" Error: {e}")

        elif op == "5":
            codigo = val.leer_texto_no_vacio("Codigo del producto a eliminar: ")
            try:
                confirmar = input(f"¿Confirma eliminar definitivamente '{codigo}'? (s/n): ").strip().lower()
                if confirmar == "s":
                    eliminado = inv.eliminar_producto(inventario, codigo)
                    persistencia.guardar_inventario(inventario)
                    print(f" Producto '{eliminado['nombre']}' eliminado del sistema.")
            except val.ReglaNegocioError as e:
                print(f" Error: {e}")

        elif op == "6":
            print(inv.formatear_tabla_productos(list(inventario.values())))

        elif op == "7":
            break


def main():
    print("=" * 60)
    print("      BIENVENIDO A TIENDAPY - SISTEMA DE GESTION")
    print("                 Tienda Don Aurelio")
    print("=" * 60)

    inventario = persistencia.cargar_inventario()
    print(f" Sistema iniciado con {len(inventario)} referencias cargadas.")

    while True:
        print("\n" + "=" * 40)
        print("          MENU PRINCIPAL")
        print("=" * 40)
        print("1. Gestion de inventario")
        print("2. Registrar una venta")
        print("3. Ver alertas de stock minimo")
        print("4. Generar reporte de cierre del dia")
        print("5. Guardar datos manualmente")
        print("6. Salir")

        opcion = val.leer_opcion_menu("Seleccione una opcion (1-6): ", ["1", "2", "3", "4", "5", "6"])

        try:
            if opcion == "1":
                submenu_inventario(inventario)
            elif opcion == "2":
                vts.procesar_venta_interactiva(inventario)
            elif opcion == "3":
                rpt.generar_alertas_stock(inventario)
            elif opcion == "4":
                rpt.generar_cierre_del_dia(inventario)
            elif opcion == "5":
                persistencia.guardar_inventario(inventario)
                print(" Datos del inventario guardados correctamente en disco.")
            elif opcion == "6":
                persistencia.guardar_inventario(inventario)
                print("\nInventario sincronizado. ¡Hasta pronto Don Aurelio!")
                sys.exit(0)
        except Exception as error_inesperado:
            print(f" Ha ocurrido un problema imprevisto: {error_inesperado}")
            print("El programa continuara funcionando con seguridad.")


if __name__ == "__main__":
    main()