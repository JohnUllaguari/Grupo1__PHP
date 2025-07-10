# Analizador Léxico, Sintáctico y Semántico de PHP con Interfaz Gráfica

Este proyecto implementa un **analizador léxico, sintáctico y semántico para archivos PHP**, desarrollado con **Python y PLY**, que funciona mediante una **interfaz gráfica** construida con **Tkinter**.

El usuario puede:
- Seleccionar archivos PHP desde su computadora.
- Escribir o editar código PHP directamente en la interfaz.
- Ejecutar cada análisis de forma independiente.
- Ver los resultados y errores detectados en cada etapa.

### **Librerías/bibliotecas Python**

| Biblioteca | Versión recomendada | Descripción |
|------------|---------------------|--------------|
| Python     | ≥ 3.10              | Intérprete principal |
| PLY        | 3.11 o superior     | Analizador léxico y sintáctico (Python Lex-Yacc) |
| Tkinter    | Viene incluido      | Interfaz gráfica de usuario (GUI) |
| subprocess | Nativo de Python    | Ejecuta scripts desde la interfaz |
| pprint / json | Nativo de Python | Formatea el árbol sintáctico (AST) en los logs |
