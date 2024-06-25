from flask import Flask, request, render_template
import lexer
import parser_1

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    syntax_result = ''
    semantic_result = ''
    counts = {
        'reserved': 0, 'id': 0, 'number': 0, 'symbol': 0,
        'lparen': 0, 'rparen': 0, 'lbrace': 0, 'rbrace': 0
    }

    if request.method == 'POST':
        code = request.form['code']
        lexer.lexer.lineno = 1  # Reiniciar el número de línea
        lexer.lexer.input(code)
        while True:
            tok = lexer.lexer.token()
            if not tok:
                break
            tokens.append(tok)
            if tok.type in counts:
                counts[tok.type] += 1

        # Calcular recuentos por columna
        for token in tokens:
            if token.type in ['FOR', 'VAR', 'CONSOLE', 'LOG', 'GLOBAL','INT','SYSTEM','PRINTLN','OUT']:
                counts['reserved'] += 1
            elif token.type == 'ID':
                counts['id'] += 1
            elif token.type == 'NUMBER':
                counts['number'] += 1
            elif token.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'DOT', 'SEMICOLON', 'COMMA', 'SINGLE_QUOTE']:
                counts['symbol'] += 1
            elif token.type == 'LPAREN':
                counts['lparen'] += 1
            elif token.type == 'RPAREN':
                counts['rparen'] += 1
            elif token.type == 'LBRACE':
                counts['lbrace'] += 1
            elif token.type == 'RBRACE':
                counts['rbrace'] += 1

        try:
            syntax_result = parser_1.parse_code(code)
        except SyntaxError as e:
            syntax_result = str(e)
        except ValueError as e:
            semantic_result = str(e)
        
        try:
            semantic_result = parser_1.parse_semantic(code)
        except SyntaxError as e:
            syntax_result = str(e)
        except ValueError as e:
            semantic_result = str(e)

    return render_template('index.html', tokens=tokens, syntax_result=syntax_result, semantic_result=semantic_result, counts=counts)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
