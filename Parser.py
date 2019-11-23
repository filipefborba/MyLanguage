from SymbolTable import SymbolTable
from Tokenizer import Tokenizer
from Node import *


class Parser:
    tokens = None

    @staticmethod
    def parseFactor():
        if (Parser.tokens.actual.type == "INT"):
            node = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return node
        elif (Parser.tokens.actual.type == "BOOL"):
            node = BoolVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return node
        elif (Parser.tokens.actual.type == "MAIS"):
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = UnOp("MAIS", [factor])
            return node
        elif (Parser.tokens.actual.type == "MENOS"):
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = UnOp("MENOS", [factor])
            return node
        elif (Parser.tokens.actual.type == "NOT"):
            Parser.tokens.selectNext()
            factor = Parser.parseFactor()
            node = UnOp("NOT", [factor])
            return node
        elif (Parser.tokens.actual.type == "ABRE_PAR"):
            Parser.tokens.selectNext()
            node = Parser.parseRelExpression()
            if (Parser.tokens.actual.type == "FECHA_PAR"):
                Parser.tokens.selectNext()
                return node
            else:
                raise ValueError(
                    f"Esperava FECHA_PAR, mas recebi {Parser.tokens.actual.type}.")
        elif (Parser.tokens.actual.type == "VAR"):
            iden = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            # Function arguments...
            if (Parser.tokens.actual.type == "ABRE_PAR"):
                func_call = FuncCall(iden, [])
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "FECHA_PAR"):
                    Parser.tokens.selectNext()
                    return func_call
                else:
                    func_call.children.append(Parser.parseRelExpression())
                    while (Parser.tokens.actual.type == "VIRGULA"):
                        Parser.tokens.selectNext()
                        func_call.children.append(Parser.parseRelExpression())
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        return func_call
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR ou VIRGULA, mas recebi {Parser.tokens.actual.type}.")
            else:
                return Identifier(iden, [])
        elif (Parser.tokens.actual.type == "RESERVADO"):
            if (Parser.tokens.actual.value == "scan"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "ABRE_PAR"):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        node = Scan(None, [])
                        return node
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR, mas recebi {Parser.tokens.actual.type}.")
                else:
                    raise ValueError(
                        f"Esperava ABRE_PAR, mas recebi {Parser.tokens.actual.type}.")
            else:
                raise ValueError(
                    f"Esperava scan, mas recebi {Parser.tokens.actual.type}.")
        else:
            print(Parser.tokens.actual.type, Parser.tokens.actual.value)
            raise ValueError(
                f"Esperava INT/BOOL/MAIS/MENOS/NOT/ABRE_PAR/VAR/SCAN, mas recebi {Parser.tokens.actual.type}.")
        return node

    @staticmethod
    def parseTerm():
        node = Parser.parseFactor()
        while(Parser.tokens.actual.type == "MULT" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "E"):
            if (Parser.tokens.actual.type == "MULT"):
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = BinOp("MULT", [node, factor])
            elif (Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = BinOp("DIV", [node, factor])
            elif (Parser.tokens.actual.type == "E"):
                Parser.tokens.selectNext()
                factor = Parser.parseFactor()
                node = BinOp("E", [node, factor])
        return node

    @staticmethod
    def parseExpression():
        node = Parser.parseTerm()
        while(Parser.tokens.actual.type == "MAIS" or Parser.tokens.actual.type == "MENOS" or Parser.tokens.actual.type == "OU"):
            if (Parser.tokens.actual.type == "MAIS"):
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = BinOp("MAIS", [node, term])
            elif (Parser.tokens.actual.type == "MENOS"):
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = BinOp("MENOS", [node, term])
            elif (Parser.tokens.actual.type == "OU"):
                Parser.tokens.selectNext()
                term = Parser.parseTerm()
                node = BinOp("OU", [node, term])
        return node

    @staticmethod
    def parseRelExpression():
        node = Parser.parseExpression()
        if (Parser.tokens.actual.type == "MAIOR_QUE"):
            Parser.tokens.selectNext()
            exp = Parser.parseExpression()
            node = BinOp("MAIOR_QUE", [node, exp])
        elif (Parser.tokens.actual.type == "MENOR_QUE"):
            Parser.tokens.selectNext()
            exp = Parser.parseExpression()
            node = BinOp("MENOR_QUE", [node, exp])
        elif (Parser.tokens.actual.type == "IGUAL"):
            Parser.tokens.selectNext()
            exp = Parser.parseExpression()
            node = BinOp("IGUAL", [node, exp])
        return node

    @staticmethod
    def parseStatement():
        if (Parser.tokens.actual.type == "VAR"):
            iden = Identifier(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "ATRIB"):
                Parser.tokens.selectNext()
                value = Parser.parseRelExpression()
                node = AssigmentOp("ATRIB", [iden, value])
                if (Parser.tokens.actual.type == "PONTO_VIRGULA"):
                    Parser.tokens.selectNext()
                    return node
                else:
                    raise ValueError(
                        f"Esperava PONTO_VIRGULA, mas recebi {Parser.tokens.actual.type}.")
            else:
                raise ValueError(
                    f"Esperava ATRIB, mas recebi {Parser.tokens.actual.type}.")
        elif (Parser.tokens.actual.type == "RESERVADO"):
            if (Parser.tokens.actual.value in ["int", "bool"]):
                var_type = Type(Parser.tokens.actual.value)
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "VAR"):
                    iden = Identifier(Parser.tokens.actual.value, [])
                    node = VarDec('VARDEC', [var_type, iden])
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "PONTO_VIRGULA"):
                        Parser.tokens.selectNext()
                        return node
                    else:
                        raise ValueError(
                            f"Esperava PONTO_VIRGULA, mas recebi {Parser.tokens.actual.type}.")
                else:
                    raise ValueError(
                        f"Esperava VAR, mas recebi {Parser.tokens.actual.type}.")
            elif (Parser.tokens.actual.value == "imprima"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "ABRE_PAR"):
                    Parser.tokens.selectNext()
                    rel_exp = Parser.parseRelExpression()
                    node = Print("IMPRIMA", [rel_exp])
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == "PONTO_VIRGULA"):
                            Parser.tokens.selectNext()
                            return node
                        else:
                            raise ValueError(
                                f"Esperava PONTO_VIRGULA, mas recebi {Parser.tokens.actual.type}.")
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR, mas recebi {Parser.tokens.actual.type}.")
                else:
                    raise ValueError(
                        f"Esperava ABRE_PAR, mas recebi {Parser.tokens.actual.type}.")

            elif (Parser.tokens.actual.value == "se"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "ABRE_PAR"):
                    Parser.tokens.selectNext()
                    rel_exp = Parser.parseRelExpression()
                    node = If("SE", [rel_exp])
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        true_stat = Parser.parseStatement()
                        node.children.append(true_stat)
                        if (Parser.tokens.actual.value == "senao"):
                            Parser.tokens.selectNext()
                            false_stat = Parser.parseStatement()
                            node.children.append(false_stat)
                            return node
                        else:
                            return node
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR, mas recebi {Parser.tokens.actual.type}.")
                else:
                    raise ValueError(
                        f"Esperava ABRE_PAR, mas recebi {Parser.tokens.actual.type}.")

            elif (Parser.tokens.actual.value == "enquanto"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "ABRE_PAR"):
                    Parser.tokens.selectNext()
                    rel_exp = Parser.parseRelExpression()
                    node = While("ENQUANTO", [rel_exp])
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        stat = Parser.parseStatement()
                        node.children.append(stat)
                        return node
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR, mas recebi {Parser.tokens.actual.type}.")
                else:
                    raise ValueError(
                        f"Esperava ABRE_PAR, mas recebi {Parser.tokens.actual.type}.")

            elif (Parser.tokens.actual.value == "retorne"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "ABRE_PAR"):
                    Parser.tokens.selectNext()
                    rel_exp = Parser.parseRelExpression()
                    return_node = Return("RETORNE", [rel_exp])
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == "PONTO_VIRGULA"):
                            Parser.tokens.selectNext()
                            return return_node
                        else:
                            raise ValueError(
                                f"Esperava PONTO_VIRGULA, mas recebi {Parser.tokens.actual.type}.")
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR, mas recebi {Parser.tokens.actual.type}.")
                else:
                    raise ValueError(
                        f"Esperava ABRE_PAR, mas recebi {Parser.tokens.actual.type}.")

        elif (Parser.tokens.actual.type == "PONTO_VIRGULA"):
            Parser.tokens.selectNext()
            return NoOp(None, [])
        else:
            return Parser.parseBlock()

    @staticmethod
    def parseBlock():
        if (Parser.tokens.actual.type == "ABRE_CHAVE"):
            Parser.tokens.selectNext()
            statements = Statements()
            while (Parser.tokens.actual.type != "FECHA_CHAVE"):
                stat = Parser.parseStatement()
                statements.children.append(stat)
            Parser.tokens.selectNext()
            return statements
        else:
            raise ValueError(
                f"Esperava ABRE_CHAVE, mas recebi {Parser.tokens.actual.type}.")

    @staticmethod
    def parseFunction():
        func_type = Parser.parseType()
        if (Parser.tokens.actual.type == "VAR" or Parser.tokens.actual.type == "PRINCIPAL"):
            func_iden = Identifier(
                Parser.tokens.actual.value, [])
            func_dec = FuncDec(Parser.tokens.actual.value, [
                VarDec(Parser.tokens.actual.value, [func_type, func_iden])])
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "ABRE_PAR"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "FECHA_PAR"):
                    Parser.tokens.selectNext()
                    func_dec.children.append(Parser.parseBlock())
                    return func_dec
                else:
                    arg_type = Parser.parseType()
                    if (Parser.tokens.actual.type == "VAR"):
                        arg_iden = Identifier(Parser.tokens.actual.value, [])
                        func_dec.children.append(
                            VarDec(arg_iden.value, [arg_type, arg_iden]))
                        Parser.tokens.selectNext()
                    else:
                        raise ValueError(
                            f"Esperava VAR, mas recebi {Parser.tokens.actual.type}.")
                    while (Parser.tokens.actual.type == "VIRGULA"):
                        Parser.tokens.selectNext()
                        arg_type = Parser.parseType()
                        if (Parser.tokens.actual.type == "VAR"):
                            arg_iden = Identifier(
                                Parser.tokens.actual.value, [])
                            func_dec.children.append(
                                VarDec(arg_iden.value, [arg_type, arg_iden]))
                            Parser.tokens.selectNext()
                        else:
                            raise ValueError(
                                f"Esperava VAR, mas recebi {Parser.tokens.actual.type}.")
                    if (Parser.tokens.actual.type == "FECHA_PAR"):
                        Parser.tokens.selectNext()
                        func_dec.children.append(Parser.parseBlock())
                        return func_dec
                    else:
                        raise ValueError(
                            f"Esperava FECHA_PAR or VIRGULA, mas recebi {Parser.tokens.actual.type}.")
            else:
                raise ValueError(
                    f"Esperava ABRE_PAR, mas recebi {Parser.tokens.actual.type}.")
        else:
            raise ValueError(
                f"Esperava VAR, mas recebi {Parser.tokens.actual.type}.")

    @staticmethod
    def parseType():
        if (Parser.tokens.actual.value == "int"):
            node = Type(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            return node
        else:
            raise ValueError(
                f"Esperava int, mas recebi {Parser.tokens.actual.value}.")

    @staticmethod
    def parseProgram():
        statements = Statements()
        while (Parser.tokens.actual.type != "EOF"):
            statements.children.append(Parser.parseFunction())

        statements.children.append(FuncCall("principal", []))
        return statements

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        result = Parser.parseProgram()
        # print(result)  # Prints the AST
        return result
