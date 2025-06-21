import ply.yacc as yacc
from lexico import tokens
import os
from datetime import datetime

start = 'program'

# Integrante 1 - Joseph Miranda
# Estructura de datos: []
def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_array_literal(p):
    'expression : LBRACKET expression_list RBRACKET'
    p[0] = ('array', p[2])

# Estructura de control: if-else

def p_condition(p):
    '''condition : expression ANDAND expression
                 | expression OROR expression
                 | expression EQ expression
                 | expression NEQ expression
                 | expression LT expression
                 | expression GT expression
                 | expression LE expression
                 | expression GE expression'''
    p[0] = ('condition',) + tuple(p[1:])

def p_if_else(p):
    'statement : IF LPAREN condition RPAREN block ELSE block'
    p[0] = ('if_else', p[3], p[5], p[7])

# Tipo de funcion

def p_function_def(p):
    'statement : FUNCTION ID LPAREN parameter_list RPAREN block'
    p[0] = ('function_def', p[2], p[4], p[6])

def p_parameter_list(p):
    '''parameter_list : VARIABLE
                      | parameter_list COMMA VARIABLE
                      | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]










# EXTRAS PARA FUNCIONALIDADES DE LAS DEFINICIONES - Joseph Miranda
def p_expression_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MOD expression
                  | expression CONCAT expression
                  | VARIABLE
                  | NUMBER
                  | FLOAT
                  | STRING
                  | function_call
                  | array_access'''
    p[0] = ('expression',) + tuple(p[1:])

def p_assignment(p):
    'assignment : VARIABLE ASSIGN expression'
    p[0] = ('assign', p[1], p[3])

def p_array_push(p):
    'assignment : VARIABLE LBRACKET RBRACKET ASSIGN expression'
    p[0] = ('array_push', p[1], p[5])

def p_statement_assignment(p):
    'statement : assignment SEMICOLON'
    p[0] = p[1]

def p_return_statement(p):
    'statement : RETURN expression SEMICOLON'
    p[0] = ('return', p[2])

def p_array_function(p):
    'expression : ID LPAREN RPAREN'
    p[0] = ('array_call', p[1])


def p_expression_incr(p):
    'expression : expression INCR'
    p[0] = ('incr', p[1])

def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = ('block', p[2])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_empty(p):
    'empty :'
    p[0] = None

def p_program(p):
    '''program : PHP_OPEN statement_list PHP_CLOSE
               | statement_list'''
    p[0] = ('program', p[2]) if len(p) == 4 else ('program', p[1])

def p_error(p):
    if p:
        print(f"[SYNTACTIC ERROR] Unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("[SYNTACTIC ERROR] Unexpected end of input")




#Crear parser
parser = yacc.yacc()


# Pruebas
nombre_archivo = "algoritmo2.php"  # archivo PHP a analizar
usuario = "JosephMiranda87"          # cambia por tu usuario Git
ruta_archivo = os.path.join("algoritmos", nombre_archivo)

# Crear carpeta logs si no existe
carpeta_logs = "logsSintactico"
os.makedirs(carpeta_logs, exist_ok=True)

fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
nombre_log = f"sintactico-{usuario}-{fecha_hora}.txt"
ruta_log = os.path.join(carpeta_logs, nombre_log)

# Leer y analizar archivo
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    data = archivo.read()
    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write(f"Análisis sintáctico de {nombre_archivo} (usuario: {usuario}):\n\n")
        try:
            result = parser.parse(data)
            if result:
                log.write("Resultado del árbol sintáctico:\n")
                log.write(str(result))
            else:
                log.write("No se generó árbol sintáctico.\n")
        except Exception as e:
            log.write(f"[SYNTACTIC ERROR]: {e}\n")

print(f"Análisis sintáctico completado. Log guardado en: {ruta_log}")



