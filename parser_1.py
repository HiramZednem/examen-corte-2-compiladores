import ply.yacc as yacc
from lexer import tokens, lexer

# Variables para el análisis semántico
defined_variables = set()  # Conjunto para almacenar variables definidas

# Definición de la gramática
def p_program(p):
    '''program : includes function'''
    # Validar que las variables definidas estén utilizadas correctamente
    validate_variables()
    p[0] = "La estructura del código está bien."

def p_includes(p):
    '''includes : INCLUDE includes
                | INCLUDE
                | empty'''
    pass

def p_function(p):
    '''function : type ID LPAREN RPAREN LBRACE declarations statements RETURN NUMBER SEMICOLON RBRACE'''
    p[0] = f"Función {p[2]} declarada correctamente."

def p_type(p):
    '''type : INT'''
    p[0] = p[1]

def p_declarations(p):
    '''declarations : declaration declarations
                    | declaration
                    | empty'''
    pass

def p_declaration(p):
    '''declaration : type ID ASSIGN NUMBER SEMICOLON'''
    defined_variables.add(p[2])  # Agregar variable a conjunto de variables definidas
    p[0] = f"Declaración: int {p[2]} = {p[4]};"  # Mensaje informativo

def p_statements(p):
    '''statements : statement statements
                  | statement
                  | empty'''
    pass

def p_statement(p):
    '''statement : assignment
                 | for_loop'''
    pass

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    validate_variable_definition(p[1])
    p[0] = p[1]

def p_expression(p):
    '''expression : ID
                  | NUMBER
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if isinstance(p[1], str):
        validate_variable_definition(p[1])

def p_for_loop(p):
    '''for_loop : FOR LPAREN assignment SEMICOLON condition SEMICOLON increment RPAREN LBRACE statements RBRACE'''
    validate_for_loop_variables(p[3], p[5], p[7])  # Validar variables dentro del for loop
    p[0] = f"For loop desde {p[3]} hasta {p[5]} con incremento {p[7]} y bloque: {p[10]}"

def p_condition(p):
    '''condition : expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression
                 | expression EQ expression
                 | expression NE expression'''
    pass

def p_increment(p):
    '''increment : ID PLUS PLUS
                 | ID MINUS MINUS'''
    validate_variable_definition(p[1])
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

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
        raise SyntaxError(f"Error de sintaxis al final del archivo en la línea {lexer.lineno}. Falta una llave de cierre o punto y coma.")

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
