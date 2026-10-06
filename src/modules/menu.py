from modules.interpolacion import ejecutar_interpolacion
from modules.utils import (
    borrar_consola,
    leer_opcion,
    pausar,
)


def _mostrar_sintaxis():
    """Lista la sintaxis que acepta el lector de funciones."""
    print("\n--- Sintaxis de las funciones ---\n")
    print("Variable:")
    print("  x                     única variable permitida")
    print("\nOperadores:")
    print("  +  -  *  /            suma, resta, multiplicación, división")
    print("  ^  o  **              potencia (2^3 = 8)")
    print("  %                     residuo")
    print("  ( )                   agrupación")
    print("  Multiplicación implícita: 3x = 3*x, 2(x + 1) = 2*(x + 1)")
    print("\nFunciones:")
    print("  log(x)                logaritmo en base 10 (log(x, b) usa base b)")
    print("  log10(x)  log2(x)     logaritmos en base 10 y 2")
    print("  ln(x)                 logaritmo natural (base e)")
    print("  exp(x)                exponencial e^x")
    print("  sqrt(x)  cbrt(x)      raíz cuadrada y raíz cúbica")
    print("  abs(x)                valor absoluto")
    print("  sin(x) cos(x) tan(x)  funciones trigonométricas")
    print("  asin(x) acos(x) atan(x)  funciones trigonométricas inversas")
    print("  sinh(x) cosh(x) tanh(x)  funciones hiperbólicas")
    print("  floor(x) ceil(x)      parte entera hacia abajo / arriba")
    print("  pow(a, b)             potencia a^b")
    print("\nConstantes:")
    print("  pi = 3.141592...      e = 2.718281...      tau = 2*pi")
    print("\nEjemplos de expresiones:")
    print("  x^2 - 3x + 2          polinomio")
    print("  ln(x) + log(x)        logaritmos")
    print("  exp(-x^2)             exponencial")
    print("  sin(x) / x            trigonométrica")
    print()


def run():
    """Método principal para ejecutar el menú."""
    while True:
        borrar_consola()
        print("=== Método de Interpolación Lineal ===\n")
        print("Menú:")
        print("  1) Interpolar un valor de f(x)")
        print("  2) Sintaxis de las funciones")
        print("  3) Salir")

        opcion = leer_opcion("Selecciona una opción (1-3): ", 1, 3)

        try:
            if opcion == 1:
                ejecutar_interpolacion()
            elif opcion == 2:
                _mostrar_sintaxis()
            elif opcion == 3:
                print("¡Hasta luego!")
                break
        except ValueError as error:
            print(f"Error: {error}\n")
        except (KeyboardInterrupt, EOFError):
            print("\n¡Hasta luego!")
            break

        pausar()
