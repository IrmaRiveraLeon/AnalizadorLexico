import re

class Token:
    def __init__(self, tipo, valor, linea):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea

    def __str__(self):
        return f"<{self.tipo}: '{self.valor}' (línea {self.linea})>"
    def __repr__(self):
        return self.__str__()

class AnalizadorLexico:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.linea = 1

        self.patrones = [
            ('WHITESPACE', r'[ \t]+'),
            ('NEWLINE', r'\n'),

            # Comentarios siempre antes de cualquier otra cosa
            ('COMMENT_MULTI',  r'/\*[\s\S]*?\*/'),
            ('COMMENT_SINGLE', r'//.*'),

            ('KEYWORD', r'\b(if|else|switch|case|breake|while|for|return|int|float)\b'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('NUMBER', r'\d+\.?\d*'),
            ('OPERATOR', r'[+\-*/=<>]'),
            ('DELIMITER', r'[;()\[\]{}]'),
            ('ERROR', r'.'),
        ]

    def tokenizar(self):
        tokens = []
        while self.pos < len(self.codigo):
            encontrado = False

            for tipo, patron in self.patrones:
                regex = re.compile(patron)
                match = regex.match(self.codigo, self.pos)

                if match:
                    valor = match.group(0)

                    # Manejo de nueva línea
                    if tipo == 'NEWLINE':
                        self.linea += 1

                    # Ignorar comentarios y espacios
                    elif tipo not in ['WHITESPACE', 'NEWLINE', 'COMMENT_MULTI', 'COMMENT_SINGLE']:
                        tokens.append(Token(tipo, valor, self.linea))

                    # Avanzamos la posición del lexer
                    self.pos = match.end()
                    encontrado = True
                    break

            if not encontrado:
                self.pos += 1

        return tokens




# Ejemplo 1: Código simple
print("=" * 50)
print("EJEMPLO 1: Código simple")
print("=" * 50)

codigo1 = "int x = 10;"
lexer1 = AnalizadorLexico(codigo1)
tokens1 = lexer1.tokenizar()

print(f"Código fuente: {codigo1}")
print("\nTokens generados:")
for token in tokens1:
    print(token)


# Ejemplo 2: Declaración con operaciones
print("\n" + "=" * 50)
print("EJEMPLO 2: Declaración con operaciones")
print("=" * 50)

codigo2 = "float precio = 99.99 + 10;"
lexer2 = AnalizadorLexico(codigo2)
tokens2 = lexer2.tokenizar()

print(f"Código fuente: {codigo2}")
print("\nTokens generados:")
for token in tokens2:
    print(token)


# Ejemplo 3: Estructura de control
print("\n" + "=" * 50)
print("EJEMPLO 3: Estructura de control")
print("=" * 50)

codigo3 = """if (x > 5) {
    return x;
}"""
lexer3 = AnalizadorLexico(codigo3)
tokens3 = lexer3.tokenizar()

print(f"Código fuente:\n{codigo3}")
print("\nTokens generados:")
for token in tokens3:
    print(token)

# Ejemplo 4: Múltiples líneas
print("\n" + "=" * 50)
print("EJEMPLO 4: Programa completo")
print("=" * 50)

codigo4 = """int suma = 0;
for (i = 1; i < 10; i = i + 1) {
    suma = suma + i;
}
return suma;"""

lexer4 = AnalizadorLexico(codigo4)
tokens4 = lexer4.tokenizar()

print(f"Código fuente:\n{codigo4}")
print(f"\nTotal de tokens generados: {len(tokens4)}")
print("\nTokens generados:")
for token in tokens4:
    print(token)

# Ejemplo 5: Comentarios mezclados con código
print("\n" + "=" * 50)
print("EJEMPLO 5: Comentarios mezclados con código")
print("=" * 50)

codigo5 = """// Este es un comentario inicial
int resultado = 0;   // Inicializamos la variable

/* Bloque
   de comentario
   que debe ser ignorado */
resultado = resultado + 5;  /* comentario al final */

// Última línea sin código
"""

lexer5 = AnalizadorLexico(codigo5)
tokens5 = lexer5.tokenizar()

print(f"Código fuente:\n{codigo5}")
print("\nTokens generados:")
for token in tokens5:
    print(token)


# Ejemplo 6: Operadores múltiples, comparaciones y delimitadores
print("\n" + "=" * 50)
print("EJEMPLO 6: Operadores y comparaciones")
print("=" * 50)

codigo6 = """
if (a < 10) {
    b = a * 2;
    while (b > 0) {
        b = b - 1; // decremento
    }
}
"""

lexer6 = AnalizadorLexico(codigo6)
tokens6 = lexer6.tokenizar()

print(f"Código fuente:\n{codigo6}")
print("\nTokens generados:")
for token in tokens6:
    print(token)


#Ejemplo 7: Identificadores, números flotantes y casos límite
print("\n" + "=" * 50)
print("EJEMPLO 7: Identificadores y números flotantes")
print("=" * 50)

codigo7 = """
float promedio_final = 123.456;
/* ignorar esta parte
promedio_final = 0;
*/
int contador123 = 50;
contador123 = contador123 + 1.5;

// Identificadores parecidos a keywords
floatify = 20;
returningValue = 99;
"""

lexer7 = AnalizadorLexico(codigo7)
tokens7 = lexer7.tokenizar()

print(f"Código fuente:\n{codigo7}")
print("\nTokens generados:")
for token in tokens7:
    print(token)
