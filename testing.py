from lexer import lexer
from parser import parser, variables, get_output, functions



def print_parser(code):
    print("\nCódigo:")
    print(code)

    for line in code.split('\n'):
        line = line.strip()
        if line:
            result = parser.parse(line)

            if result is not None:  # Solo imprime si hay resultado
                print(result)

    output = get_output()
    print(output)

    if len(variables) > 0:
        print("\nVariables definidas:")
        for var, val in variables.items():
            print(f"{var} = {val}")

    if len(functions) > 0:
        print("\nFunciones definidas:")
        print(functions)


codes = {
    "Ejercicio 1: Variable no declarada antes de su uso": """
y = x + 2 ::
x = 5 ::""",
    "Ejercicio 2: Incompatibilidad de tipos en asignaciones": """
x = 5 ::
x = "texto" ::""",
    "Ejercicio 3: Número incorrecto de argumentos en una función": """
def sumar(a, b) {a = a + b ::} ::
resultado = sumar(5) ::
""",
"Ejercicio 4: Operadores incompatibles": """x = "hola" - 5 ::""",
"Ejercicio 5: Condición no booleana en un if": """if (5 + 3) then a = 3 :: endif ::"""
}

for code in codes:
    print()
    print()
    print("-"*10, code, "-"*10)
    print_parser(codes[code])