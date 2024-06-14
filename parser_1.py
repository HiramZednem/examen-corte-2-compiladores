import ply.yacc as yacc
from lexer import tokens, lexer

# Variables para el análisis semántico
defined_variables = set()  # Conjunto para almacenar variables definidas

# Definición de la gramática
def p_program(p):
    '''program : declaration for_loop'''
    # Validar que las variables definidas estén utilizadas correctamente
    validate_variables()
    p[0] = "La estructura del código está bien."

def p_declaration(p):
    '''declaration : INT ID SEMICOLON'''
    defined_variables.add(p[2])  # Agregar variable a conjunto de variables definidas
    p[0] = f"Declaración: int {p[2]};"  # Mensaje informativo

def p_for_loop(p):
    '''for_loop : FOR LPAREN assignment SEMICOLON condition SEMICOLON increment RPAREN LBRACE block RBRACE'''
    validate_for_loop_variables(p[3], p[5], p[7])  # Validar variables dentro del for loop
    p[0] = f"For loop desde {p[3]} hasta {p[5]} con incremento {p[7]} y bloque: {p[10]}"

def p_assignment(p):
    '''assignment : ID ASSIGN NUMBER'''
    p[0] = p[1]  # Devolver el nombre de la variable asignada
    validate_variable_definition(p[1])

def p_condition(p):
    '''condition : ID LE NUMBER'''
    p[0] = p[1]  # Devolver el nombre de la variable de la condición
    validate_variable_definition(p[1])

def p_increment(p):
    '''increment : ID PLUS PLUS'''
    p[0] = p[1]  # Devolver el nombre de la variable del incremento
    validate_variable_definition(p[1])

def p_block(p):
    '''block : system_println_statement'''
    p[0] = p[1]

def p_system_println_statement(p):
    '''system_println_statement : SYSTEM DOT OUT DOT PRINTLN LPAREN ID RPAREN SEMICOLON'''
    validate_variable_definition(p[7])
    p[0] = f"Impresión: System.out.println({p[7]})"

def validate_variable_definition(variable):
    if variable not in defined_variables:
        raise ValueError(f"Error semántico: Variable '{variable}' no definida correctamente en la línea {lexer.lineno}.")

def validate_for_loop_variables(assignment_var, condition_var, increment_var):
    validate_variable_definition(assignment_var)
    validate_variable_definition(condition_var)
    validate_variable_definition(increment_var)

def validate_variables():
    for var in defined_variables:
        if not ('a' <= var <= 'z'):
            raise ValueError(f"Error semántico: Variable '{var}' no permitida en la estructura en la línea {lexer.lineno}.")

# Manejo de errores
def p_error(p):
    if p:
        error_message = f"Línea {p.lineno}.- Error de sintaxis en '{p.value}'"
        raise SyntaxError(error_message)
    else:
        raise SyntaxError(f"Error de sintaxis al final del archivo en la línea {lexer.lexer.lineno}. Falta una llave de cierre o punto y coma.")

# Construir el parser
parser = yacc.yacc()

def parse_semantic(code):
    global defined_variables
    defined_variables = set()
    lexer.lineno = 1  # Reiniciar el número de línea
    try:
        result = parser.parse(code)
        return result if result else 'La estructura del código está bien'
    except (SyntaxError, ValueError) as e:
        raise e

# Función para analizar el código
def parse_code(code):
    global defined_variables
    defined_variables = set()  # Reiniciar variables definidas para cada análisis
    lexer.lineno = 1  # Reiniciar el número de línea
    try:
        result = parser.parse(code)
        return result if result else "La estructura del código está bien."
    except (SyntaxError, ValueError) as e:
        raise e
