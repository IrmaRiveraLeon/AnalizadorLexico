import os
import re

# ------------------------------
# 1. CATEGORÍAS DE TOKENS
# ------------------------------
PALABRAS_RESERVADAS = {
    "int", "float", "void", "if", "else", "while", "return", "main"
}

OPERADORES_ARIT = {"+": "MAS", "-": "MENOS", "*": "MULT", "/": "DIV"}
OPERADORES_REL = {"==": "IGUAL", "<": "MENOR", ">": "MAYOR"}
AGRUPACION = {"(": "PA", ")": "PC", "{": "LLA", "}": "LLC", ";": "PYC"}

# ------------------------------
# 2. QUITAR COMENTARIOS
# ------------------------------
def limpiar_comentarios(texto):
    texto = re.sub(r"/\*.*?\*/", "", texto, flags=re.DOTALL)  # bloque
    texto = re.sub(r"//.*", "", texto)  # linea
    return texto

# ------------------------------
# 3. ANALIZADOR LÉXICO
# ------------------------------
def analizar_linea(linea, numero):
    tokens = []
    palabras = re.findall(r"[A-Za-z_]\w*|==|[-+*/(){};<>]|[0-9]+", linea)

    for p in palabras:

        # Palabra reservada
        if p in PALABRAS_RESERVADAS:
            tokens.append((numero, p, p.upper(), "PALABRA_RESERVADA"))

        # Operadores aritméticos
        elif p in OPERADORES_ARIT:
            tokens.append((numero, p, OPERADORES_ARIT[p], "OPERADOR_ARITMÉTICO"))

        # Operadores relacionales
        elif p in OPERADORES_REL:
            tokens.append((numero, p, OPERADORES_REL[p], "OPERADOR_RELACIONAL"))

        # Agrupación
        elif p in AGRUPACION:
            tokens.append((numero, p, AGRUPACION[p], "AGRUPACIÓN"))

        # Números
        elif p.isdigit():
            tokens.append((numero, p, "NUM", "NÚMERO"))

        # Identificadores
        else:
            tokens.append((numero, p, "ID", "IDENTIFICADOR"))

    return tokens

# ------------------------------
# 4. PROCESAR UN ARCHIVO
# ------------------------------
def procesar_archivo(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8-sig") as f:
        contenido = f.read()

    contenido = limpiar_comentarios(contenido)

    tokens = []
    for num, linea in enumerate(contenido.split("\n"), start=1):
        linea = linea.strip()  # Limpia BOM, espacios y tabs invisibles

        if linea:  # Solo analiza si NO está vacía
            tokens.extend(analizar_linea(linea, num))

    return tokens

# ------------------------------
# 5. ESCRIBIR ARCHIVO DE TOKENS
# ------------------------------
def escribir_tokens(nombre, tokens):
    salida = f"tokens_{nombre}.txt"

    with open(salida, "w", encoding="utf-8") as f:
        f.write("Renglón\tToken\tLexema\tCategoría\n")
        for renglon, lexema, token, categoria in tokens:
            f.write(f"{renglon}\t{lexema}\t{token}\t{categoria}\n")

    print(f"✔ Archivo generado: {salida}")

# ------------------------------
# 6. LEER TODOS LOS CASOS
# ------------------------------
def procesar_carpeta():
    carpeta = "casos"

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".txt"):
            ruta = os.path.join(carpeta, archivo)
            nombre = archivo.replace(".txt", "")
            print(f"Procesando {archivo}...")

            tokens = procesar_archivo(ruta)
            escribir_tokens(nombre, tokens)

# Ejecutar
procesar_carpeta()

