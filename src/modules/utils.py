import os
import sys


def leer_opcion(prompt: str, lower: int, upper: int) -> int:
    """Lee un entero dentro del rango cerrado [lower, upper]."""
    while True:
        entrada = input(prompt).strip()
        try:
            valor = int(entrada)
            if lower <= valor <= upper:
                return valor
            print(f"Opción fuera de rango (se esperaba entre {lower} y {upper}).")
        except ValueError:
            print(f'"{entrada}" no es un número entero válido.')


def leer_real(prompt: str) -> float:
    """Lee un número real del usuario."""
    while True:
        entrada = input(prompt).strip()
        try:
            return float(entrada)
        except ValueError:
            print(f'"{entrada}" no es un número real válido.')


def formatear_a_decimal(valor) -> str:
    """Fraccion, string u objeto Decimal a decimal(string)."""
    texto = f"{float(valor):.6f}".rstrip("0").rstrip(".")
    return texto if texto not in ("", "-") else "0"


def borrar_consola():
    """
    Detecta el sistema operativo y si esta en TTY.\n
    Luego, borra la consola.
    """
    if not sys.stdin.isatty():
        return
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """
    Detecta el sistema operativo y si esta en TTY.\n
    Luego, simula el comportamiento de pause en cmd.
    """
    if not sys.stdin.isatty():
        return
    if os.name == "nt":
        os.system("pause")
    else:
        input("Presiona Enter para continuar...")
