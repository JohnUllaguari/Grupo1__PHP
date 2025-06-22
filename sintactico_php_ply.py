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

#-----------------------------------------------------------------------------------------------#
# --- Estructura de datos: array() largo asociativo (John Ullaguari)
def p_array_long(p):
    '''expression : ID LPAREN array_pairs RPAREN'''
    p[0] = ('array_assoc', p[1], p[3])

def p_array_pairs(p):
    '''array_pairs : STRING DOUBLEARROW expression
                   | array_pairs COMMA STRING DOUBLEARROW expression'''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = p[1] + [(p[3], p[5])]

# --- Estructura de control: foreach (John Ullaguari)
def p_foreach_loop(p):
    'statement : FOREACH LPAREN VARIABLE AS VARIABLE RPAREN block'
    p[0] = ('foreach', p[3], p[5], p[7])

# --- Tipo de función: método estático dentro de clase (John Ullaguari)
def p_class_static_method(p):
    'class_static_method : STATIC FUNCTION ID LPAREN RPAREN block'
    p[0] = ('static_method', p[3], p[6])

# --- Conector de métodos estáticos o sentencias normales dentro de la clase (John Ullaguari)
def p_class_statement(p):
    '''class_statement : class_static_method
                       | statement'''
    p[0] = p[1]

# --- Lista de sentencias dentro del cuerpo de la clase (John Ullaguari)
def p_class_body(p):
    '''class_body : class_statement
                  | class_body class_statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

# --- Definición de clase como statement principal (John Ullaguari)
def p_class_def(p):
    'statement : CLASS ID LBRACE class_body RBRACE'
    p[0] = ('class_def', p[2], p[4])

# --- Echo como statement (John Ullaguari)
def p_statement_echo(p):
    'statement : ECHO expression SEMICOLON'
    p[0] = ('echo', p[2])

# --- Funciones de expresión como statement (readline, etc.) (John Ullaguari)
def p_statement_expression(p):
    'statement : expression SEMICOLON'
    p[0] = ('stmt_expr', p[1])

# --- Ingreso de datos por teclado con readline() (Young_Lopez XD)
def p_input_read(p):
    'expression : ID LPAREN STRING RPAREN'
    if p[1] == "readline":
        p[0] = ('input_readline', p[3])
    else:
        p[0] = ('func_call', p[1], [p[3]])


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
                  | ID LPAREN expression_list RPAREN
                  | VARIABLE LBRACKET expression RBRACKET'''
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

# ============================== #
# === Aportes de Steeven Gómez === #
# ============================== #

# --- Estructura de datos: array multidimensional (Steeven Gómez)
def p_array_multidimensional(p):
    '''expression : LBRACKET expression_list_of_lists RBRACKET'''
    p[0] = ('array_multidimensional', p[2])

def p_expression_list_of_lists(p):
    '''expression_list_of_lists : LBRACKET expression_list RBRACKET
                                | expression_list_of_lists COMMA LBRACKET expression_list RBRACKET'''
    if len(p) == 4:
        p[0] = [p[2]]
    else:
        p[0] = p[1] + [p[4]]

# --- Estructura de control: while loop (Steeven Gómez)
def p_while_loop(p):
    'statement : WHILE LPAREN condition RPAREN block'
    p[0] = ('while', p[3], p[5])

# --- Tipo de función: función anónima (Steeven Gómez)
def p_anonymous_function(p):
    'expression : FUNCTION LPAREN parameter_list RPAREN block'
    p[0] = ('anonymous_function', p[3], p[5])

# Crear parser
parser = yacc.yacc()


# Pruebas
nombre_archivo = "algoritmos2_2.php"  # archivo PHP a analizar
# nombre_archivo = "Lenguajes de Programacion\Grupo1__PHP\algoritmos\algoritmos2_1.php"
usuario = "SteevenGD"          # cambia por tu usuario Git
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