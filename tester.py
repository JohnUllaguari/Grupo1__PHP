import lexer_php
import datetime
import os

# ----------------------------
# CONFIGURACIÓN
# ----------------------------
usuario_git = "JohnUllaguari"  # Lo vamos a ir cambiando conforme quien haga las pruebas
archivo_php = "ejemplos/algoritmo1.php"  # Lo vamos cambiando segun el algoritmo probado
carpeta_logs = "logs"

# ----------------------------
# GENERAR NOMBRE DE LOG
# ----------------------------
now = datetime.datetime.now()
nombre_log = f"lexico-{usuario_git}-{now.strftime('%d-%m-%Y-%Hh%M')}.txt"


os.makedirs(carpeta_logs, exist_ok=True)

# ----------------------------
# LEER ARCHIVO PHP
# ----------------------------
with open(archivo_php, 'r', encoding='utf-8') as f:
    codigo = f.read()

lexer_php.lexer.input(codigo)

# ----------------------------
# Analizar y guardar tokens
# ----------------------------
with open(os.path.join(carpeta_logs, nombre_log), 'w', encoding='utf-8') as log:
    log.write(f"LOG DE ANALIZADOR LÉXICO PARA: {archivo_php}\n\n")
    while True:
        tok = lexer_php.lexer.token()
        if not tok:
            break
        log.write(f"{tok.type:<15}  valor: {tok.value}  línea: {tok.lineno}\n")
