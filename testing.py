from lexer import lexer
from parser import parser, variables, get_output


code = '''
a ="hola"-5 ::
'''


for line in code.split('\n'):
    line = line.strip()
    if line:
        result = parser.parse(line)

        if result is not None:  # Solo imprime si hay resultado
            print(result)

output = get_output()
print(output)

print("\nVariables definidas:")
for var, val in variables.items():
    print(f"{var} = {val}")
