from lexer import lexer
from parser import parser, variables, run
from clear_code import preprocess_code


code = '''
i = 1 ::
write(i, " es par") ::
'''
final_code = preprocess_code(code)

ast = parser.parse(final_code)

run(ast)



print("\nVariables definidas:")
for var, val in variables.items():
    print(f"{var} = {val}")