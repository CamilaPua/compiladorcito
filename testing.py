from lexer import lexer
from parser import parser, variables


code = '''
a = 5+2 ::
'''


for line in code.split('\n'):
    line = line.strip()
    if line:
        result = parser.parse(line)

        if result is not None:  # Solo imprime si hay resultado
            print(result)


print("\nVariables definidas:")
for var, val in variables.items():
    print(f"{var} = {val}")
