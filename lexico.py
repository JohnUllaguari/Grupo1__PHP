import ply.lex as lex
import os
from datetime import datetime

# Palabras reservadas
reserved = {
    'if': 'IF', 'else': 'ELSE', 'elseif': 'ELSEIF', 'while': 'WHILE',
    'for': 'FOR', 'foreach': 'FOREACH', 'echo': 'ECHO', 'function': 'FUNCTION',
    'return': 'RETURN', 'class': 'CLASS', 'extends': 'EXTENDS', 'implements': 'IMPLEMENTS',
    'interface': 'INTERFACE', 'public': 'PUBLIC', 'protected': 'PROTECTED',
    'private': 'PRIVATE', 'static': 'STATIC', 'try': 'TRY', 'catch': 'CATCH',
    'finally': 'FINALLY', 'throw': 'THROW', 'new': 'NEW', 'null': 'NULL',
    'true': 'TRUE', 'false': 'FALSE', 'and': 'AND', 'or': 'OR',
    'define': 'DEFINE', 'as': 'AS'
}

# Tokens
tokens = [
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'ASSIGN', 'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'MODEQ',
    'EQ', 'EEQ', 'NEQ', 'NNEQ', 'LT', 'GT', 'LE', 'GE',
    'ANDAND', 'OROR', 'NOT',
    'INCR', 'DECR',
    'SEMICOLON', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET', 'COMMA', 'COLON',
    'ID', 'NUMBER', 'FLOAT', 'STRING',
    'PHP_OPEN', 'PHP_CLOSE', 'CONCAT', 'DOUBLEARROW', 'VARIABLE'
] + list(reserved.values())

# Expresiones regulares simples
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MOD     = r'%'


t_ASSIGN  = r'='
t_PLUSEQ  = r'\+='
t_MINUSEQ = r'-='
t_TIMESEQ = r'\*='
t_DIVEQ   = r'/='
t_MODEQ   = r'%='

t_EQ    = r'=='
t_EEQ   = r'==='
t_NEQ   = r'!='
t_NNEQ  = r'!=='
t_LT    = r'<'
t_GT    = r'>'
t_LE    = r'<='
t_GE    = r'>='
t_DOUBLEARROW = r'=>'

t_ANDAND = r'&&'
t_OROR   = r'\|\|'
t_NOT    = r'!'

t_INCR = r'\+\+'
t_DECR = r'--'


t_SEMICOLON  = r';'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACKET   = r'\['
t_RBRACKET   = r'\]'
t_COMMA      = r','
t_COLON      = r':'
t_CONCAT     = r'\.'

# Tokens con funciones
def t_STRING(t):
    r'(\"([^\\\n]|(\\.))*?\")|(\'([^\\\n]|(\\.))*?\')'
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'(0x[0-9A-Fa-f]+)|(0[0-7]*)|([1-9]\d*)'
    if t.value.startswith("0x") or t.value.startswith("0X"):
        t.value = int(t.value, 16)
    elif t.value.startswith("0") and len(t.value) > 1:
        t.value = int(t.value, 8)
    else:
        t.value = int(t.value)
    return t

# ✅ Variables (deben iniciar con $)
def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# ✅ Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_PHP_OPEN(t):
    r'<\?php'
    return t

def t_PHP_CLOSE(t):
    r'\?>'
    return t

def t_COMMENT(t):
    r'(//.*|\#.*|/\*[\s\S]*?\*/)'
    pass


# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores léxicos
def t_error(t):
    print(f"[ERROR LÉXICO] Caracter no válido '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# ----------------------
# Crear el analizador léxico
# ----------------------
lexer = lex.lex()

# --- CONFIGURACIÓN PARA PRUEBA
nombre_archivo = "algoritmo_sema.php"
usuario = "JohnUllaguari"

ruta_archivo = os.path.join("algoritmos", nombre_archivo)
carpeta_logs = "logs"
os.makedirs(carpeta_logs, exist_ok=True)

fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
nombre_log = f"lexico-{usuario}-{fecha_hora}.txt"
ruta_log = os.path.join(carpeta_logs, nombre_log)

# Análisis léxico y guardado en log
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

print(f"✅ Análisis léxico completado. Log guardado en: {ruta_log}")
