class ReglaNegocioError(Exception):
    pass


def leer_texto_no_vacio(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print(" Error: El campo no puede estar vacio. Intente de nuevo.")


def leer_entero_positivo(mensaje: str, permitir_cero: bool = False) -> int:
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if permitir_cero and valor == 0:
                return valor
            if valor <= 0:
                limite = "mayor o igual a cero" if permitir_cero else "estrictamente mayor a cero"
                print(f" Error: El valor debe ser {limite}.")
                continue
            return valor
        except ValueError:
            print(" Error: Debe ingresar un numero entero valido.")


def leer_flotante_positivo(mensaje: str) -> float:
    while True:
        entrada = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if valor <= 0:
                print(" Error: El valor debe ser un numero estrictamente positivo.")
                continue
            return valor
        except ValueError:
            print(" Error: Debe ingresar un numero decimal valido.")


def leer_opcion_menu(mensaje: str, opciones_validas: list[str]) -> str:
    while True:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f" Opcion invalida. Opciones disponibles: {', '.join(opciones_validas)}")