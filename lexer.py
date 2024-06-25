import ply.lex as lex

# Palabras reservadas en C
reserved = {
    'int': 'INT',
    'return': 'RETURN',
    'for': 'FOR'
}

# Lista de tokens incluyendo las palabras reservadas
tokens = [
    'ID', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA', 'LT', 'LE',
    'GT', 'GE', 'EQ', 'NE', 'INCLUDE'
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
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Regla para los números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para los identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Regla para las directivas de preprocesador
def t_INCLUDE(t):
    r'\#include\s*<.*?>'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contar las líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Manejo de errores
def t_error(t):
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()
