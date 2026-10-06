"""Análisis y evaluación de expresiones matemáticas con solo la biblioteca estándar.

El usuario escribe f(x) como texto (ej. ``x^2 - 3x + 2``, ``ln(x)``, ``exp(-x)``,
``log(x) + sqrt(x)``) y esta módulo la convierte en una función de Python
``f(x) -> float`` sin usar ``eval`` ni dependencias externas.
"""

import math
from typing import Callable, List, NamedTuple

Funcion = Callable[[float], float]


class ErrorFuncion(ValueError):
    """Error detectado al interpretar la expresión de la función."""


_CONSTANTES = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


def _log(x: float, base: float = 10.0) -> float:
    """log(x) en base 10 y log(x, b) en base b."""
    if base <= 0 or base == 1:
        raise ErrorFuncion("La base del logaritmo debe ser positiva y distinta de 1.")
    if x <= 0:
        raise ErrorFuncion("El logaritmo solo está definido para valores positivos.")
    if base == 10.0:
        return math.log10(x)
    return math.log(x, base)


def _cbrt(x: float) -> float:
    return math.copysign(abs(x) ** (1.0 / 3.0), x)


# nombre -> (mínimo de argumentos, máximo de argumentos, función)
_FUNCIONES = {
    "sin": (1, 1, math.sin),
    "cos": (1, 1, math.cos),
    "tan": (1, 1, math.tan),
    "asin": (1, 1, math.asin),
    "acos": (1, 1, math.acos),
    "atan": (1, 1, math.atan),
    "sinh": (1, 1, math.sinh),
    "cosh": (1, 1, math.cosh),
    "tanh": (1, 1, math.tanh),
    "sqrt": (1, 1, math.sqrt),
    "cbrt": (1, 1, _cbrt),
    "exp": (1, 1, math.exp),
    "ln": (1, 1, math.log),
    "log": (1, 2, _log),
    "log10": (1, 1, math.log10),
    "log2": (1, 1, math.log2),
    "abs": (1, 1, abs),
    "floor": (1, 1, math.floor),
    "ceil": (1, 1, math.ceil),
    "round": (1, 1, round),
    "pow": (2, 2, pow),
}


class _Token(NamedTuple):
    tipo: str
    texto: str
    pos: int


def _tokenizar(expresion: str) -> List[_Token]:
    """Divide la expresión en números, nombres, operadores y paréntesis."""
    tokens: List[_Token] = []
    i, n = 0, len(expresion)
    while i < n:
        char = expresion[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit() or (char == "." and i + 1 < n and expresion[i + 1].isdigit()):
            j = i
            while j < n and (expresion[j].isdigit() or expresion[j] == "."):
                j += 1
            if j < n and expresion[j] in "eE":
                k = j + 1
                if k < n and expresion[k] in "+-":
                    k += 1
                if k < n and expresion[k].isdigit():
                    j = k
                    while j < n and expresion[j].isdigit():
                        j += 1
            texto = expresion[i:j]
            try:
                float(texto)
            except ValueError:
                raise ErrorFuncion(
                    f'Número inválido "{texto}" en la posición {i + 1}.'
                )
            tokens.append(_Token("num", texto, i))
            i = j
            continue
        if char.isalpha() or char == "_":
            j = i
            while j < n and (expresion[j].isalnum() or expresion[j] == "_"):
                j += 1
            tokens.append(_Token("name", expresion[i:j], i))
            i = j
            continue
        if expresion[i:i + 2] == "**":
            tokens.append(_Token("op", "^", i))
            i += 2
            continue
        if char in "+-*/%^":
            tokens.append(_Token("op", char, i))
            i += 1
            continue
        if char in "(,":
            tokens.append(_Token(char, char, i))
            i += 1
            continue
        if char == ")":
            tokens.append(_Token(")", char, i))
            i += 1
            continue
        raise ErrorFuncion(f'Carácter inválido "{char}" en la posición {i + 1}.')
    tokens.append(_Token("fin", "", n))
    return tokens


def _combinar(op: str, izq: Funcion, der: Funcion) -> Funcion:
    if op == "+":
        return lambda x: izq(x) + der(x)
    if op == "-":
        return lambda x: izq(x) - der(x)
    if op == "*":
        return lambda x: izq(x) * der(x)
    if op == "/":
        return lambda x: izq(x) / der(x)
    if op == "%":
        return lambda x: izq(x) % der(x)
    raise ErrorFuncion(f'Operador desconocido "{op}".')


class _Parser:
    """Analizador descendente recursivo que construye una función evaluable."""

    def __init__(self, tokens: List[_Token]):
        self.tokens = tokens
        self.pos = 0

    def _actual(self) -> _Token:
        return self.tokens[self.pos]

    def _avanzar(self) -> _Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self) -> Funcion:
        if self._actual().tipo == "fin":
            raise ErrorFuncion("La expresión está vacía.")
        funcion = self._expr()
        token = self._actual()
        if token.tipo != "fin":
            raise ErrorFuncion(
                f'Sobra "{token.texto}" en la posición {token.pos + 1}.'
            )
        return funcion

    def _expr(self) -> Funcion:
        izq = self._termino()
        while self._actual().tipo == "op" and self._actual().texto in "+-":
            op = self._avanzar().texto
            izq = _combinar(op, izq, self._termino())
        return izq

    def _termino(self) -> Funcion:
        izq = self._unario()
        while True:
            token = self._actual()
            if token.tipo == "op" and token.texto in "*/%":
                op = self._avanzar().texto
                izq = _combinar(op, izq, self._unario())
            elif token.tipo in ("num", "name", "("):
                # Multiplicación implícita: 3x, 2(x + 1), x·exp(x)
                der = self._unario()
                izq = lambda x, a=izq, b=der: a(x) * b(x)
            else:
                break
        return izq

    def _unario(self) -> Funcion:
        token = self._actual()
        if token.tipo == "op" and token.texto in "+-":
            self._avanzar()
            funcion = self._unario()
            if token.texto == "-":
                return lambda x: -funcion(x)
            return funcion
        return self._potencia()

    def _potencia(self) -> Funcion:
        base = self._primario()
        if self._actual().tipo == "op" and self._actual().texto == "^":
            self._avanzar()
            exponente = self._unario()
            return lambda x: base(x) ** exponente(x)
        return base

    def _primario(self) -> Funcion:
        token = self._actual()
        if token.tipo == "num":
            self._avanzar()
            valor = float(token.texto)
            return lambda x, v=valor: v
        if token.tipo == "(":
            self._avanzar()
            funcion = self._expr()
            if self._actual().tipo != ")":
                raise ErrorFuncion(
                    f"Falta cerrar el paréntesis abierto en la posición {token.pos + 1}."
                )
            self._avanzar()
            return funcion
        if token.tipo == "name":
            self._avanzar()
            return self._nombre(token)
        if token.tipo == "fin":
            raise ErrorFuncion("La expresión termina antes de lo esperado.")
        raise ErrorFuncion(
            f'No se esperaba "{token.texto}" en la posición {token.pos + 1}.'
        )

    def _nombre(self, token: _Token) -> Funcion:
        nombre = token.texto
        if nombre in _FUNCIONES:
            if self._actual().tipo != "(":
                raise ErrorFuncion(
                    f'La función "{nombre}" se escribe con paréntesis, '
                    f'por ejemplo {nombre}(x).'
                )
            return self._llamada(nombre)
        if nombre in _CONSTANTES:
            valor = _CONSTANTES[nombre]
            return lambda x, v=valor: v
        if nombre.lower() == "x":
            return lambda x: x
        raise ErrorFuncion(
            f'Nombre desconocido "{nombre}" en la posición {token.pos + 1}. '
            f"Usa la variable x, las constantes ({', '.join(_CONSTANTES)}) "
            f"o funciones como {', '.join(list(_FUNCIONES)[:6])}."
        )

    def _llamada(self, nombre: str) -> Funcion:
        min_arg, max_arg, funcion = _FUNCIONES[nombre]
        self._avanzar()  # consume "("
        argumentos: List[Funcion] = []
        if self._actual().tipo == ")":
            self._avanzar()
        else:
            while True:
                argumentos.append(self._expr())
                token = self._actual()
                if token.tipo == ",":
                    self._avanzar()
                    continue
                if token.tipo == ")":
                    self._avanzar()
                    break
                raise ErrorFuncion(
                    f'Falta una coma o el cierre de ")" en la posición '
                    f"{token.pos + 1}."
                )
        if not min_arg <= len(argumentos) <= max_arg:
            esperado = str(min_arg) if min_arg == max_arg else f"{min_arg} a {max_arg}"
            raise ErrorFuncion(
                f'La función "{nombre}" recibe {esperado} argumento(s), '
                f"pero se escribieron {len(argumentos)}."
            )
        # Evita la captura tardía de variables del bucle.
        args = tuple(argumentos)
        return lambda x: funcion(*[argumento(x) for argumento in args])


def parsear_funcion(expresion: str) -> Funcion:
    """Convierte una expresión escrita por el usuario en una función ``f(x)``.

    Args:
        expresion: Texto con la fórmula, ej. ``x^2 - 3x + 2`` o ``ln(x) / x``.

    Returns:
        Funcion: Función evaluable en cualquier ``x``.

    Raises:
        ErrorFuncion: Si la expresión es inválida (subclase de ValueError).
    """
    if not expresion or not expresion.strip():
        raise ErrorFuncion("La expresión está vacía.")
    return _Parser(_tokenizar(expresion.strip())).parse()
