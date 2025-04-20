from tokenizer import lexer

# Test it out
data = '''
write("hello") ::
if blabla == delokos then
    blabla <= lokos then
        $ 3 + 4 * 10
        a = c + b
endif ::
a = capture() ::
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
for tok in lexer:     # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)