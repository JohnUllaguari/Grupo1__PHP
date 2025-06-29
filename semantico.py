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

def analizar(ast):
    if not ast or ast[0] != 'program':
        raise Exception("AST inválido o vacío")

    for stmt in ast[1]:
        if stmt[0] == 'assign':
            infer_type(stmt)
        elif stmt[0] == 'condition':
            infer_type(stmt)
        elif stmt[0] in ['if', 'if_else']:
            _, cond, *blocks = stmt
            infer_type(cond)

# Variables con tipos explícitos
symbol_table['$texto'] = 'string'
symbol_table['$numero'] = 'number'
symbol_table['$otro'] = 'number'

nombre_archivo = "algoritmo1_3.php"
usuario = "JosephMiranda87"
carpeta_logs = "logsSemantico"
os.makedirs(carpeta_logs, exist_ok=True)
fecha_hora = datetime.now().strftime("%d%m%Y-%Hh%M")
ruta_log = os.path.join(carpeta_logs, f"semantico-{usuario}-{fecha_hora}.txt")

with open(f"algoritmos/{nombre_archivo}", 'r', encoding='utf-8') as f:
    data = f.read()
    ast = parser.parse(data)
    analizar(ast)

with open(ruta_log, 'w', encoding='utf-8') as log:
    log.write(f"Errores semánticos en {nombre_archivo}:\n\n")
    if semantic_errors:
        for err in semantic_errors:
            log.write(err + "\n")
    else:
        log.write("Sin errores semánticos.\n")

print(f"Log generado: {ruta_log}")
