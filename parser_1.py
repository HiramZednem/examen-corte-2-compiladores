import ply.yacc as yacc
from lexer import tokens

# Definición de la gramática
def p_program(p):
    '''program : for_loop console_statement'''
    p[0] = "La estructura del código está bien."

def p_for_loop(p):
    '''for_loop : FOR LPAREN VAR ID ASSIGN NUMBER SEMICOLON ID LT NUMBER SEMICOLON ID PLUS PLUS RPAREN LBRACE block RBRACE'''
    p[0] = "For loop from {p[6]} to {p[10]} with step 1 and block: {p[16]}"

def p_console_statement(p):
    '''console_statement : CONSOLE DOT LOG LPAREN expression RPAREN SEMICOLON'''
    p[0] = "Console log: {p[5]}"

def p_expression(p):
    '''expression : SINGLE_QUOTE ID ID SINGLE_QUOTE PLUS ID
                  | GLOBAL'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]} + {p[3]}"

def p_block(p):
    '''block : console_statement'''
    p[0] = p[1]

def p_error(p):
    if p:
        error_message = f"Error de sintaxis en '{p.value}' en la línea {p.lineno}."
        raise SyntaxError(error_message)
    else:
        raise SyntaxError("Error de sintaxis al final del archivo. Falta una llave de cierre o punto y coma.")

# Construir el parser
parser = yacc.yacc()

# Función para analizar el código
def parse_code(code):
    try:
        result = parser.parse(code)
        return result if result else "La estructura del código está bien."
    except SyntaxError as e:
        return str(e)
