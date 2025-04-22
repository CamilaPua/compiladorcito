import ply.yacc as yacc
from lexer import tokens

variables = {}
outputs = []


def p_statement(p):
    """statement : assignment DPOINTS
                 | expression DPOINTS
                 | write DPOINTS
                 | capture DPOINTS"""
    p[0] = p[1]


def p_assignment(p):
    "assignment : ID ASSIGN expression"
    variables[p[1]] = p[3]
    p[0] = p[3]


def p_expression_plus(p):
    "expression : expression '+' term"
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    "expression : expression '-' term"
    p[0] = p[1] - p[3]


def p_expression_term(p):
    "expression : term"
    p[0] = p[1]


def p_term_times(p):
    "term : term '*' factor"
    p[0] = p[1] * p[3]


def p_term_div(p):
    "term : term '/' factor"
    p[0] = p[1] / p[3]


def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


def p_factor_num(p):
    "factor : NUMBER"
    p[0] = p[1]


def p_factor_var(p):
    "factor : ID"
    try:
        p[0] = variables[p[1]]
    except KeyError:
        print(f"Error: Variable '{p[1]}' not defined.")
        p[0] = 0  # Default value


def p_factor_expr(p):
    "factor : '(' expression ')'"
    p[0] = p[2]


def p_write(p):
    '''write : WRITE '(' STRING ')'
             | WRITE '(' expression ')'
             | WRITE '(' STRING ',' expression ')' '''
    
    if len(p) == 5:  # write("mensaje")
        outputs.append(str(p[3]))
    elif len(p) == 6:  # write(expresion)
        outputs.append(str(p[3]))
    elif len(p) == 7:  # write("mensaje", expresion)
        outputs.append(str(p[3]) + str(p[5]))


def p_capture(p):
    "capture : CAPTURE '(' ID ')'"
    outputs.append(f"Input requested for variable '{p[3]}'")
    variables[p[3]] = "simulated_value" 


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'. Line: {p.lineno}")
    else:
        print("Syntax error at end of input")


def get_outputs():
    global outputs
    results = "\n".join(outputs)
    outputs = []
    return results


parser = yacc.yacc()
