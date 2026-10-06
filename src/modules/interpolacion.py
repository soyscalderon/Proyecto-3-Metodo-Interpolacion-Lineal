"""Método de interpolación lineal: f(x) ≈ f(x0) + ((f(x1) - f(x0)) / (x1 - x0)) * (x - x0)."""

from modules.funciones import ErrorFuncion, Funcion, parsear_funcion
from modules.utils import formatear_a_decimal, leer_real


def interpolar_lineal(
    x: float, x0: float, x1: float, f_x0: float, f_x1: float
) -> float:
    """Aplica la interpolación lineal entre dos puntos conocidos.

    Args:
        x: Valor de x donde se desea estimar f(x).
        x0: Extremo izquierdo del intervalo.
        x1: Extremo derecho del intervalo.
        f_x0: Valor de la función en x0.
        f_x1: Valor de la función en x1.

    Returns:
        float: Valor aproximado de f(x).

    Raises:
        ValueError: Si x0 y x1 son iguales (división entre cero).
    """
    if x0 == x1:
        raise ValueError("Los puntos x0 y x1 deben ser distintos.")
    return f_x0 + ((f_x1 - f_x0) / (x1 - x0)) * (x - x0)


def _evaluar(funcion: Funcion, x: float) -> float:
    """Evalúa f(x) traduciendo los errores comunes a mensajes claros."""
    try:
        return float(funcion(x))
    except ErrorFuncion:
        raise
    except ZeroDivisionError:
        raise ValueError(f"La función tiene una división entre cero en x = {x}.")
    except OverflowError:
        raise ValueError(f"La función desborda el rango de valores en x = {x}.")
    except ValueError as error:
        raise ValueError(f"La función no está definida en x = {x}: {error}")


def ejecutar_interpolacion() -> None:
    """Interactiva: lee f(x), x0, x1 y x, y muestra el valor interpolado."""
    print("\n--- Interpolación Lineal ---\n")
    print("Escribe f(x) usando la variable x.")
    print("Ejemplos:  x^2 - 3x + 2   |   ln(x) + 1   |   log(x)   |   exp(-x)")
    print("(Escribe la opción 2 del menú para ver toda la sintaxis)\n")

    expresion = input("Función f(x): ").strip()
    try:
        funcion = parsear_funcion(expresion)
    except ErrorFuncion as error:
        print(f"Error en la función: {error}")
        return

    x0 = leer_real("Extremo izquierdo x0: ")
    x1 = leer_real("Extremo derecho x1: ")

    if x0 >= x1:
        print("Error: x0 debe ser menor que x1 (izquierda antes que derecha).")
        return

    x = leer_real(f"Valor de x a interpolar (entre {x0} y {x1}): ")

    try:
        f_x0 = _evaluar(funcion, x0)
        f_x1 = _evaluar(funcion, x1)
        aproximado = interpolar_lineal(x, x0, x1, f_x0, f_x1)
    except ValueError as error:
        print(f"Error: {error}")
        return

    pendiente = (f_x1 - f_x0) / (x1 - x0)

    print("\n=== Resultados ===")
    print(f"  f(x) = {expresion}")
    print(f"  x0 = {x0}   f(x0) = {f_x0}")
    print(f"  x1 = {x1}   f(x1) = {f_x1}")
    print(
        f"  Pendiente m = (f(x1) - f(x0)) / (x1 - x0) "
        f"= ({f_x1} - {f_x0}) / ({x1} - {x0}) = {pendiente}"
    )
    print(f"\n  f({x}) ≈ {aproximado}")
    print(f"  f({x}) ≈ {formatear_a_decimal(aproximado)}  (6 decimales)")

    try:
        exacto = _evaluar(funcion, x)
    except ValueError:
        print("\n  No fue posible evaluar f(x) en ese punto para comparar.")
        return

    error_absoluto = abs(exacto - aproximado)
    print(f"\n  Valor exacto f({x}) = {exacto}")
    print(f"  Error absoluto = |exacto - aproximado| = {error_absoluto}")
    if exacto != 0:
        print(f"  Error relativo = {error_absoluto / abs(exacto)}")
    if x < x0 or x > x1:
        print(
            f"  Nota: x = {x} queda fuera del intervalo [{x0}, {x1}], "
            "por lo que se realizó extrapolación."
        )
