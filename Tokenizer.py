from Token import Token


class Tokenizer:
    def __init__(self, origin="", position=0, actual=None):
        self.origin = origin
        self.position = position
        self.actual = actual
        self.reserved_words = ["imprima", "scan", "se", "senao", "retorne",
                               "enquanto", "int", "bool", "principal", "Verdadeiro", "Falso"]

    def checkNext(self, char):
        if (self.position+1 < len(self.origin)):
            if (self.origin[self.position+1] == char):
                return True
            else:
                return False
        else:
            raise ValueError(
                f"Final de string inesperado na posição {self.position+1}")

    def selectNext(self):
        while (self.origin[self.position] == " " or self.origin[self.position] == "\n"):
            self.position += 1
            if (self.position >= len(self.origin)):
                self.actual = Token("EOF", "EOF")
                return
        if (self.position >= len(self.origin)):
            self.actual = Token("EOF", "EOF")
            return

        token_value = ""  # variable to store integer value or variable name

        if (self.origin[self.position].isdigit()):
            while (self.origin[self.position].isdigit()):
                token_value += self.origin[self.position]
                self.position += 1
                if (self.position == len(self.origin)):
                    break
            self.actual = Token("INT", int(token_value))

        elif ((self.origin[self.position].isalnum() or self.origin[self.position] == "_") and not self.origin[self.position].isdigit()):
            while (self.origin[self.position].isalnum() or self.origin[self.position] == "_"):
                token_value += self.origin[self.position]
                self.position += 1
                if (self.position == len(self.origin)):
                    break
            if (token_value in self.reserved_words):
                if (token_value == "principal"):
                    self.actual = Token("PRINCIPAL", token_value)
                elif (token_value == "Verdadeiro" or token_value == "Falso"):
                    self.actual = Token("BOOL", token_value)
                else:
                    self.actual = Token("RESERVADO", token_value)
            else:
                self.actual = Token("VAR", token_value)

        elif (self.origin[self.position] == "+"):
            self.actual = Token("MAIS", "+")
            self.position += 1

        elif (self.origin[self.position] == "-"):
            self.actual = Token("MENOS", "-")
            self.position += 1

        elif (self.origin[self.position] == "*"):
            self.actual = Token("MULT", "*")
            self.position += 1

        elif (self.origin[self.position] == "/"):
            self.actual = Token("DIV", "/")
            self.position += 1

        elif (self.origin[self.position] == "("):
            self.actual = Token("ABRE_PAR", "(")
            self.position += 1

        elif (self.origin[self.position] == ")"):
            self.actual = Token("FECHA_PAR", ")")
            self.position += 1

        elif (self.origin[self.position] == "="):
            if (self.checkNext("=")):
                self.actual = Token("IGUAL", "==")
                self.position += 2
            else:
                self.actual = Token("ATRIB", "=")
                self.position += 1

        elif (self.origin[self.position] == "|"):
            if (self.checkNext("|")):
                self.actual = Token("OU", "||")
                self.position += 2
            else:
                raise ValueError(
                    f"Esperava | mas recebi {self.origin[self.position+1]}.")

        elif (self.origin[self.position] == "&"):
            if (self.checkNext("&")):
                self.actual = Token("E", "&&")
                self.position += 2
            else:
                raise ValueError(
                    f"Esperava & mas recebi {self.origin[self.position+1]}.")

        elif (self.origin[self.position] == ">"):
            self.actual = Token("MAIOR_QUE", ">")
            self.position += 1

        elif (self.origin[self.position] == "<"):
            self.actual = Token("MENOR_QUE", "<")
            self.position += 1

        elif (self.origin[self.position] == "~"):
            self.actual = Token("NOT", "~")
            self.position += 1

        elif (self.origin[self.position] == ","):
            self.actual = Token("VIRGULA", ",")
            self.position += 1

        elif (self.origin[self.position] == ";"):
            self.actual = Token("PONTO_VIRGULA", ";")
            self.position += 1

        elif (self.origin[self.position] == "{"):
            self.actual = Token("ABRE_CHAVE", "{")
            self.position += 1

        elif (self.origin[self.position] == "}"):
            self.actual = Token("FECHA_CHAVE", "}")
            self.position += 1

        else:
            raise ValueError("Token não identificado pelo Tokenizer")
