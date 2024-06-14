import ply.lex as lex

# Palabras reservadas
reserved = {
    'var': 'VAR',
    'for': 'FOR',
    'console': 'CONSOLE',
    'log': 'LOG',
    'global': 'GLOBAL',
    'int': 'INT',
    'out': 'OUT',
    'println': 'PRINTLN',
    'System': 'SYSTEM'  # Agregar System como palabra reservada
}

# Lista de tokens incluyendo las palabras reservadas
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA', 'LT', 'LE',
    'GT', 'GE', 'EQ', 'NE', 'STRING', 'DOT', 'SINGLE_QUOTE'
] + list(reserved.values())

# Reglas simples para los tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_LT = r'<'
t_LE = r'<='  # Nueva regla para el operador menor o igual
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_DOT = r'\.'
t_SINGLE_QUOTE = r"'"

# Expresión regular para identificar IDs y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') if t.value not in reserved else reserved[t.value]  # Verificar palabras reservadas
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contar las líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Manejo de errores
def t_error(t):
    print(f"Línea {t.lineno}.- Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
