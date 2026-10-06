# Proyecto 3 - Metodo de Interpolacion Lineal

Implementacion del metodo de interpolacion lineal para estimar el valor de una funcion `f(x)` a partir de dos puntos conocidos, desarrollado como proyecto del curso de Analisis Numerico (5to semestre).

## Descripcion

La interpolacion lineal aproxima el valor de una funcion reemplazando su grafica por la recta que pasa por dos puntos conocidos `(x0, f(x0))` y `(x1, f(x1))`, uno a la izquierda y otro a la derecha del valor `x` que se desea estimar:

```
                 f(x1) - f(x0)
f(x) = f(x0) +  ------------- · (x - x0)
                 x1 - x0
```

El termino `(f(x1) - f(x0)) / (x1 - x0)` es la pendiente de la recta. El programa evalua `f(x0)` y `f(x1)` a partir de una funcion escrita por el usuario, aplica la formula y muestra ademas el valor exacto de `f(x)` (si es posible calcularlo) junto con el error absoluto y relativo de la aproximacion.

## Requisitos

- Python 3.8 o superior (desarrollado en Python 3.14)
- No requiere dependencias externas (solo biblioteca estandar: `math`)

## Ejecucion

```bash
# Opcion 1: usar el script de ejecucion
bash exec.sh

# Opcion 2: ejecutar directamente
python3 src/main.py
```

## Estructura del proyecto

```
.
├── exec.sh                         # Script de ejecucion
├── README.md
├── src/
│   ├── main.py                     # Punto de entrada
│   └── modules/
│       ├── __init__.py             # Paquete
│       ├── funciones.py            # Lector/evaluador de expresiones f(x)
│       ├── interpolacion.py        # Algoritmo de interpolacion lineal
│       ├── menu.py                 # Menu interactivo
│       └── utils.py                # Funciones de utilidad (reutilizadas)
```

## Uso

Al ejecutar el programa se muestra un menu interactivo con las siguientes opciones:

1. **Interpolar un valor de f(x)** - Solicita:
   - La funcion `f(x)` escrita como texto (ej: `x^2 - 3x + 2`, `ln(x) + 1`, `log(x)`, `exp(-x)`)
   - El extremo izquierdo `x0`
   - El extremo derecho `x1` (debe ser mayor que `x0`)
   - El valor de `x` a interpolar

2. **Sintaxis de las funciones** - Muestra las operaciones, funciones y constantes admitidas.

3. **Salir** - Termina el programa.

Ejemplo de salida:

```
=== Resultados ===
  f(x) = x^2 - 3x + 2
  x0 = 1.0   f(x0) = 0.0
  x1 = 3.0   f(x1) = 2.0
  Pendiente m = (f(x1) - f(x0)) / (x1 - x0) = (2.0 - 0.0) / (3.0 - 1.0) = 1.0

  f(2.0) ≈ 1.0
  f(2.0) ≈ 1  (6 decimales)

  Valor exacto f(2.0) = 0.0
  Error absoluto = |exacto - aproximado| = 1.0
```

Si `x` queda fuera del intervalo `[x0, x1]` el programa avisa que se hizo extrapolacion.

## Sintaxis de las funciones

El lector de expresiones (`modules/funciones.py`) convierte el texto del usuario en una funcion evaluable sin usar `eval` ni librerias externas:

| Tipo | Admitidos |
| ---- | --------- |
| Variable | `x` |
| Operadores | `+  -  *  /  %  ^` (o `**`), parentesis y multiplicacion implicita (`3x`, `2(x+1)`) |
| Logaritmos | `log(x)` (base 10), `log(x, b)` (base b), `log10(x)`, `log2(x)`, `ln(x)` |
| Exponencial | `exp(x)` |
| Raices | `sqrt(x)`, `cbrt(x)` |
| Trigonometricas | `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sinh`, `cosh`, `tanh` |
| Otras | `abs(x)`, `floor(x)`, `ceil(x)`, `round(x)`, `pow(a, b)` |
| Constantes | `pi`, `e`, `tau` |

Notacion cientifica admitida: `2e-3`. Ejemplos de expresiones validas: `x^2 - 3x + 2`, `ln(x) + log(x)`, `exp(-x^2)`, `sin(x) / x`.

Toda entrada invalida (parentesis sin cerrar, nombre desconocido, division entre cero, argumentos fuera de dominio) se reporta con un mensaje y se regresa al menú.

## Funcionamiento del algoritmo

1. Se lee y valida la funcion `f(x)` (tokenizador + analizador descendente recursivo).
2. Se piden `x0 < x1` y el valor de `x` a estimar.
3. Se evaluan `f(x0)` y `f(x1)` con la funcion parseada.
4. Se aplica la formula `f(x) = f(x0) + ((f(x1) - f(x0)) / (x1 - x0)) * (x - x0)`.
5. Se muestra el resultado, y si es posible, el valor exacto de `f(x)` con su error absoluto y relativo.

## Reutilizacion

- `modules/utils.py` reutiliza funciones de los proyectos anteriores: `leer_opcion`, `leer_real` y `borrar_consola`/`pausar` (Proyecto 2) y `formatear_a_decimal` (Proyecto 1).
- `src/main.py` y `modules/__init__.py` replican la misma estructura de entrada usada en los Proyectos 1 y 2.

## Autores

Desarrollado como proyecto del curso de Analisis Numerico.
