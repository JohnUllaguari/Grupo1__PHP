from sintactico_php_ply import parser
import os
from datetime import datetime

# Tabla de símbolos para tipos conocidos
symbol_table = {}
semantic_errors = []

# Joseph Miranda
# OPERACIONES VALIDAS
#ASIGNACIONES COMPATIBLES

def infer_type(node):
    """Inferir tipos para asignaciones y comparaciones"""
    if isinstance(node, tuple):
        nodetype = node[0]

        if nodetype == 'assign':
            _, var, expr = node
            expr_type = infer_type(expr)

            if var in symbol_table:
                var_type = symbol_table[var]
                if var_type != expr_type:
                    semantic_errors.append(
                        f"Asignación incompatible: {var} ({var_type}) = {expr_type}"
                    )
            else:
                symbol_table[var] = expr_type  # primer uso define tipo
            return expr_type

        elif nodetype == 'expression':
            if len(node) == 4:
                _, left, op, right = node
                left_type = infer_type(left)
                right_type = infer_type(right)

                if op in ('+', '-', '*', '/', '%'):
                    if left_type != 'number' or right_type != 'number':
                        semantic_errors.append(
                            f"Operación inválida: {op} entre {left_type} y {right_type}"
                        )
                    return 'number'
                if op == '.':
                    if left_type != 'string' or right_type != 'string':
                        semantic_errors.append(
                            f"Concatenación inválida entre {left_type} y {right_type}"
                        )
                    return 'string'
            elif len(node) == 2:
                _, val = node
                return infer_type(val)

        elif nodetype == 'condition':
            _, left, _, right = node
            left_type = infer_type(left)
            right_type = infer_type(right)

            if left_type != right_type:
                semantic_errors.append(
                    f"Comparación incompatible: {left_type} vs {right_type}"
                )
            return 'boolean'

    elif isinstance(node, int) or isinstance(node, float):
        return 'number'
    elif isinstance(node, str):
        if node.startswith('"') or node.startswith("'"):
            return 'string'
        elif node.startswith('$'):
            return symbol_table.get(node, 'unknown')
        else:
            return 'id'

    return 'unknown'


# STEEVEN GÓMEZ
# VERIFICAR RETURN
# VALIDAR BREAK Y CONTINUE
def check_return_usage(node):
    if isinstance(node, tuple) and node[0] == 'return':
        if 'function' not in [n[0] for n in node[1:-1]]:  # Buscar contexto de función
            semantic_errors.append("Return usado fuera de contexto de función")

def check_loop_control(node):
    if isinstance(node, tuple) and node[0] in ('break', 'continue'):
        if 'while' not in [n[0] for n in node[1:-1]] and 'for' not in [n[0] for n in node[1:-1]]:
            semantic_errors.append(f"{node[0]} usado fuera de bucle")

# ----------------------------------------------
# Reglas semánticas de John Ullaguari
# ----------------------------------------------

# 1. Validar que readline() solo se use dentro de una asignación
def check_readline_assignment(node):
    if isinstance(node, tuple) and node[0] == 'stmt_expr':
        expr = node[1]
        if isinstance(expr, tuple) and expr[0] == 'input_readline':
            semantic_errors.append("Uso inválido de readline(): debe asignarse a una variable.")

# 2. Validar que las clases no estén vacías (deben tener métodos o atributos)
def check_class_non_empty(node):
    if isinstance(node, tuple) and node[0] == 'class_def':
        _, class_name, body = node
        if not body:
            semantic_errors.append(f"La clase '{class_name}' está vacía. Debe tener al menos un método o atributo.")

def analizar(ast):
    if not ast or ast[0] != 'program':
        semantic_errors.append("AST inválido o vacío")
        return  # No interrumpir, solo registrar el error y salir

    for stmt in ast[1]:
        try:
            if stmt[0] == 'assign':
                infer_type(stmt)
            elif stmt[0] == 'condition':
                infer_type(stmt)
            elif stmt[0] in ['if', 'if_else']:
                _, cond, *blocks = stmt
                infer_type(cond)
            
            # Aplicar reglas semánticas
            check_return_usage(stmt)
            check_loop_control(stmt)
            check_readline_assignment(stmt)
            check_class_non_empty(stmt)
        except Exception as e:
            semantic_errors.append(f"Error en análisis semántico: {str(e)}")

# Variables con tipos explícitos
symbol_table['$texto'] = 'string'
symbol_table['$numero'] = 'number'
symbol_table['$otro'] = 'number'

nombre_archivo = "algoritmo_sema.php"
usuario = "JohnUllaguari"
carpeta_logs = "logsSemantico"
os.makedirs(carpeta_logs, exist_ok=True)
fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
ruta_log = os.path.join(carpeta_logs, f"semantico-{usuario}-{fecha_hora}.txt")
ruta_archivo = os.path.join("algoritmos", nombre_archivo)

with open(ruta_archivo, 'r', encoding='utf-8') as f:
    data = f.read()

try:
    ast = parser.parse(data)
    if ast is None:
        print("❌ Error sintáctico: No se generó árbol sintáctico.")
    else:
        analizar(ast)
except Exception as e:
    print(f"❌ Error en el parser: {e}")

with open(ruta_log, 'w', encoding='utf-8') as log:
    log.write(f"Errores semánticos en {nombre_archivo}:\n\n")
    if semantic_errors:
        for err in semantic_errors:
            log.write(err + "\n")
    else:
        log.write("Sin errores semánticos.\n")

print(f"✅ Análisis semántico completado. Log guardado en: {ruta_log}")
