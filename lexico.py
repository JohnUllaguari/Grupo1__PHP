import ply.lex as lex
import ply.yacc
import os
import subprocess
from datetime import datetime
print("PLY instalado correctamente")

# ----------------------
#  (Joseph Miranda) Palabras reservadas y Operadores
# ----------------------
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'elseif': 'ELSEIF',
    'while': 'WHILE',
    'for': 'FOR',
    'foreach': 'FOREACH',
    'echo': 'ECHO',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'class': 'CLASS',
    'extends': 'EXTENDS',
    'implements': 'IMPLEMENTS',
    'interface': 'INTERFACE',
    'public': 'PUBLIC',
    'protected': 'PROTECTED',
    'private': 'PRIVATE',
    'static': 'STATIC',
    'try': 'TRY',
    'catch': 'CATCH',
    'finally': 'FINALLY',
    'throw': 'THROW',
    'new': 'NEW',
    'null': 'NULL',
    'true': 'TRUE',
    'false': 'FALSE',
    'and': 'AND',
    'or': 'OR',
}

# OPERADORES
# Operadores aritméticos
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'

# Operadores de asignación
t_ASSIGN = r'='
t_PLUSEQ = r'\+='
t_MINUSEQ = r'-='
t_TIMESEQ = r'\*='
t_DIVEQ = r'/='
t_MODEQ = r'%='

# Operadores de comparación
t_EQ = r'=='
t_EEQ = r'==='
t_NEQ = r'!='
t_NNEQ = r'!=='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='

# Operadores lógicos
t_ANDAND = r'&&'
t_OROR = r'\|\|'
t_NOT = r'!'

# Incremento y decremento
t_INCR = r'\+\+'
t_DECR = r'--'


# ----------------------
#  (Steveen Gomez) Delimitadores
# ----------------------
t_PUNTOYCOMA = r';'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PARENIZQ = r'\('
t_PARENDER = r'\)'
t_CORCHETEIZQ = r'\['
t_CORCHETEDER = r'\]'
t_COMA = r','
t_DOSPUNTOS = r':'

# Lista de tokens incluyendo los delimitadores y palabras reservadas
tokens = [
    # Operadores aritméticos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',

    # Operadores de asignación
    'ASSIGN', 'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'MODEQ',

    # Operadores de comparación
    'EQ', 'EEQ', 'NEQ', 'NNEQ', 'LT', 'GT', 'LE', 'GE',

    # Operadores lógicos
    'ANDAND', 'OROR', 'NOT',

    # Incremento/decremento
    'INCR', 'DECR',

    # Delimitadores
    'PUNTOYCOMA', 'LLAVEIZQ', 'LLAVEDER', 'PARENIZQ', 'PARENDER',
    'CORCHETEIZQ', 'CORCHETEDER', 'COMA', 'DOSPUNTOS',

    # Literales y otros
    'ID', 'NUMBER', 'FLOAT', 'STRING',
    'PHP_OPEN', 'PHP_CLOSE'
] + list(reserved.values())


# ----------------------
# Expresiones Regulares en funciones(JOHN ULLAGUARI)
# ----------------------

# Cadenas (comillas simples o dobles)
def t_STRING(t):
    r'(\"([^\\\n]|(\\.))*?\")|(\'([^\\\n]|(\\.))*?\')'
    return t

# Flotantes (número con punto decimal)
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Enteros
def t_NUMBER(t):
    r'(0x[0-9A-Fa-f]+)|(0[0-7]*)|([1-9]\d*)'
    if t.value.startswith("0x") or t.value.startswith("0X"):
        t.value = int(t.value, 16)
    elif t.value.startswith("0") and len(t.value) > 1:
        t.value = int(t.value, 8)
    else:
        t.value = int(t.value)
    return t

# Variables: comienzan con $
def t_ID(t):
    r'(\$?[a-zA-Z_][a-zA-Z0-9_]*)'
    nombre = t.value.lstrip('$')
    if nombre in reserved:
        t.type = reserved[nombre]
    return t

def t_PHP_OPEN(t):
    r'<\?php'
    pass

def t_PHP_CLOSE(t):
    r'\?>'
    pass

# Comentarios (opcional)
def t_COMMENT(t):
    r'(//.*|\#.*)'
    pass

# Punto (concatenación en PHP)
t_CONCAT = r'\.'
tokens.append('CONCAT')


# ----------------------
# Ignorar espacios y tabs
# ----------------------
t_ignore = ' \t'

# ----------------------
# Contador de líneas
# ----------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ----------------------
# Manejo de errores
# ----------------------
def t_error(t):
    print(f"[ERROR LÉXICO] Caracter no válido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# ----------------------
# Crear el analizador léxico
# ----------------------
lexer = lex.lex()

# Prueba de los diferentes ejemplos por intengrante
# Se cambiara el usuario acorde al algoritmo
nombre_archivo = "algoritmo3.php"
usuario = "SteevenGD"

ruta_archivo = os.path.join("algoritmos", nombre_archivo)
carpeta_logs = "logs"
os.makedirs(carpeta_logs, exist_ok=True)

fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
nombre_log = f"lexico-{usuario}-{fecha_hora}.txt"
ruta_log = os.path.join(carpeta_logs, nombre_log)
# ========== Análisis léxico ==========
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    data = archivo.read()
    lexer.input(data)

    with open(ruta_log, 'w', encoding='utf-8') as log:
        log.write(f"Tokens de {nombre_archivo} (usuario: {usuario}):\n\n")
        try:
            for tok in lexer:
                log.write(f"{tok.type} ({tok.value}) - línea {tok.lineno}\n")
        except Exception as e:
            log.write(f"[LEX ERROR]: {e}\n")

print(f"Análisis léxico completado. Log guardado en: {ruta_log}")

