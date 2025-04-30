import ply.yacc as yacc
from lexer import tokens  # Asume que tu código anterior está en lexer.py

variables = {}
functions = {}
output = []


def p_program(p):
    "program : statement_list"


def p_statement_list(p):
    """statement_list : statement
                      | statement DPOINTS statement_list"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_statement(p):
    """statement : assignment DPOINTS
                 | write DPOINTS
                 | capture DPOINTS
                 | expression DPOINTS
                 | if_statement DPOINTS
                 | function_statement DPOINTS"""


def p_write(p):
    """write : WRITE '(' STRING ')'
             | WRITE '(' expression ')'
             | WRITE '(' STRING ',' expression ')' """

    if len(p) == 5:  # write("message")
        output.append(str(p[3]))
    elif len(p) == 6:  # write(expression)
        output.append(str(p[3]))
    elif len(p) == 7:  # write("message", expression)
        output.append(str(p[3]) + str(p[5]))


def p_capture(p):
    "capture : CAPTURE '(' ID ')'"
    var = p[3]
    output.append(f"Ingreso solicitado para variable '{p[3]}'")
    variables[var] = "valor_simulado"  # Puedes poner aquí un valor fijo


def p_function_def(p):
    "function_statement : DEF ID '(' params ')' '{' statement_list '}'"
    functions[p[2]] = p[4]  # t[4] es la lista de parámetros
    # Opcional: guardar statements para análisis futuro


def p_params_multiple(p):
    "params : ID ',' params"
    p[0] = [p[1]] + p[3]


def p_params_single(p):
    "params : ID"
    p[0] = [p[1]]


def p_params_empty(p):
    "params : "
    p[0] = []


def p_function_call(p):
    "term : ID '(' arguments ')'"
    func_name = p[1]
    if func_name not in functions:
        output.append(f"Error: Function '{func_name}' not declared.")
    elif len(functions[func_name]) != len(p[3]):
        output.append(
            f"Error: Function '{func_name}' expects {len(functions[func_name])} arguments, received {len(p[3])}.")
    p[0] = 0  # puede devolver un valor de retorno en el futuro


def p_arguments_multiple(p):
    "arguments : expression ',' arguments"
    p[0] = [p[1]] + p[3]


def p_arguments_single(p):
    "arguments : expression"
    p[0] = [p[1]]


def p_arguments_empty(p):
    "arguments : "
    p[0] = []


def p_if_statement(p):
    """if_statement : IF '(' condition ')' THEN statement_list ENDIF
                    | if_statement"""
    p[0] = ('if', p[3], p[6], p[7])


def p_opt_else(p):
    """opt_else : ELSE statement_list
                | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_empty(p):
    "empty :"
    p[0] = None


def p_condition(p):
    "condition : boolean_expr"
    p[0] = p[1]


def p_boolean_expr_or(p):
    "boolean_expr : boolean_expr OR boolean_expr"
    p[0] = ('or', p[1], p[3])


def p_boolean_expr_and(p):
    "boolean_expr : boolean_expr AND boolean_expr"
    p[0] = ('and', p[1], p[3])


def p_boolean_expr_not(p):
    "boolean_expr : NOT boolean_expr"
    p[0] = ('not', p[2])


def p_boolean_expr_paren(p):
    "boolean_expr : '(' boolean_expr ')'"
    p[0] = p[2]


def p_boolean_expr_rel(p):
    "boolean_expr : expression relational_operator expression"
    p[0] = (p[2], p[1], p[3])


def p_condition(p):
    """condition : expression"""  # Acepta cualquier expresión
    if isinstance(p[1], bool):
        p[0] = p[1]
    else:
        error_msg = f"Error: Condition must be boolean, got {p[1]} (type: {type(p[1]).__name__})"
        output.append(error_msg)
        p[0] = False


def p_relational_operator(p):
    """relational_operator : '<'
                           | '>'
                           | LESSEQ
                           | GREATEREQ
                           | EQUALS
                           | NOTEQ"""
    p[0] = p[1]


def p_assignment(p):
    "assignment : ID ASSIGN expression"
    if p[3] is None:
        error_message = f"Error: Incomplete assignment for '{p[1]}'"
        output.append(error_message)
        p[0] = None
    else:
        try:
            if type(variables[p[1]]) == type(p[3]):
                variables[p[1]] = p[3]
                p[0] = p[3]
            else:
                error_message = f"Error: Incompatibility in data type. '{p[1]}' is {type(variables[p[1]]).__name__} not {type(p[3]).__name__}."
                output.append(error_message)
        except KeyError:
            variables[p[1]] = p[3]
            p[0] = p[3]


def p_expression_plus(p):
    "expression : expression '+' term"
    if type(p[1]) != type(p[3]):
        error_message = f"Error: You cannot add {type(p[1]).__name__} with {type(p[3]).__name__}"
        output.append(error_message)
    else:
        p[0] = p[1] + p[3]


def p_expression_minus(p):
    "expression : expression '-' term"
    if type(p[1]) != type(p[3]):
        error_message = f"Error: You cannot subtract {type(p[3]).__name__} to {type(p[1]).__name__}"
        output.append(error_message)
    else:
        p[0] = p[1] - p[3]


def p_expression_term(p):
    "expression : term"
    p[0] = p[1]


def p_term_times(p):
    "term : term '*' factor"
    if type(p[1]) != type(p[3]):
        error_message = f"Error: You cannot multiply {type(p[1]).__name__} with {type(p[3]).__name__}"
        output.append(error_message)
    else:
        p[0] = p[1] * p[3]


def p_term_div(p):
    "term : term '/' factor"
    if type(p[1]) != type(p[3]):
        error_message = f"Error: You cannot divide {type(p[1]).__name__} with {type(p[3]).__name__}"
        output.append(error_message)
    else:
        p[0] = p[1] / p[3]


def p_term_factor(p):
    "term : factor"
    p[0] = p[1]


def p_factor_num(p):
    "factor : NUMBER"
    p[0] = p[1]


def p_factor_string(p):
    "factor : STRING"
    p[0] = p[1]


def p_factor_expr(p):
    "factor : '(' expression ')'"
    p[0] = p[2]


def p_factor_id(p):
    "factor : ID"
    try:
        p[0] = variables[p[1]]
    except KeyError:
        error_message = f"Error: Variable '{p[1]}' not defined."
        output.append(error_message)

        p[0] = 0


errorFound = False


def p_error(p):
    global errorFound
    errorFound = True
    if p:
        error_message = f"Syntax error at '{p.value}'."
        output.append(error_message)
    else:
        error_message = "Syntax error at end of input"
        output.append(error_message)


def get_output():
    global output
    result = "\n".join(output)
    output = []  # Clear after getting output
    return result


# Build the parser
parser = yacc.yacc(start="program")
