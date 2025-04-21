from tokenizer import lexer
from parser import parser



# while True:
#     try:
#         s = input('>> ')
#     except EOFError:
#         break
#     if not s.strip(): continue
#     result = parser.parse(s)
#     if result is not None:  # Solo imprime si hay resultado
#         print(result)

# Test it out
# write("hello") ::
# if blabla == delokos then
#     blabla <= lokos then
data = '''
c = 3 + 4 * 10
'''
# endif ::
# a = capture() ::

# Give the lexer some input
# lexer.input(data)

# # Tokenize
# for tok in lexer:     # No more input
#     print(tok.type, tok.value, tok.lineno, tok.lexpos)


result = parser.parse(data)

if result is not None:  # Solo imprime si hay resultado
    print(result)