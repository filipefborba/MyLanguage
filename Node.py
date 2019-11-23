from SymbolTable import SymbolTable, StaticTable


class Node():
    def __init__(self):
        self.value = None
        self.children = []

    def __repr__(self):
        return f"//{self.value} | {self.children}\\"

    def evaluate(self, symbol_table):
        print("Função Evaluate da classe abstrata Node.")


class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        child0 = self.children[0].evaluate(symbol_table)
        child1 = self.children[1].evaluate(symbol_table)
        if (child0[1] == child1[1]):  # (value, type) || childx[1] -> type
            if self.value == "MAIS":
                return (child0[0] + child1[0], "int")
            elif self.value == "MENOS":
                return (child0[0] - child1[0], "int")
            elif self.value == "MULT":
                return (child0[0] * child1[0], "int")
            elif self.value == "DIV":
                return (child0[0] // child1[0], "int")
            elif self.value == "MAIOR_QUE":
                return (child0[0] > child1[0], "bool")
            elif self.value == "MENOR_QUE":
                return (child0[0] < child1[0], "bool")
            elif self.value == "IGUAL":
                return (child0[0] == child1[0], "bool")
            elif self.value == "E":
                return (child0[0] and child1[0], "bool")
            elif self.value == "OU":
                return (child0[0] or child1[0], "bool")
        else:
            raise ValueError(f"Operação inválida {child0[1]} com {child1[1]}")


class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        child0 = self.children[0].evaluate(symbol_table)
        if (child0[1] == "int"):
            if self.value == "MAIS":
                return (child0[0], "int")
            elif self.value == "MENOS":
                return (-child0[0], "int")
            else:
                raise ValueError(
                    f"Operação inválida {self.value} com {child0[1]}")
        elif (child0[1] == "bool"):
            if self.value == "NOT":
                return (not child0[0], "bool")
            else:
                raise ValueError(
                    f"Operação inválida {self.value} com {child0[1]}")
        else:
            raise ValueError(
                f"Unop operação inválida {self.value} com {child0[1]}")


class NoOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        pass


class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        symbol_table.declare_variable(
            self.children[0].evaluate(symbol_table), self.children[1].value)


class FuncDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        StaticTable.declare_variable(StaticTable, "FUNCAO", self.value)
        StaticTable.set_variable(StaticTable, self.value, (self, "FUNCAO"))


class FuncCall(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        func_reference, func_type = StaticTable.get_variable(
            StaticTable, self.value)
        new_ST = SymbolTable()
        if (func_type == "FUNCAO"):
            # VarDec da Funcao (especial!)
            func_reference.children[0].evaluate(new_ST)

            # Argumentos
            for i in range(1, len(func_reference.children) - 1):
                func_reference.children[i].evaluate(new_ST)
                arg_val, arg_type = self.children[i-1].evaluate(symbol_table)
                new_ST.set_variable(
                    func_reference.children[i].value, (arg_val, arg_type))

            # Statements
            func_reference.children[-1].evaluate(new_ST)

            # Retorna o valor guardado no nome da funcao
            return new_ST.get_variable(self.value)

        else:
            raise ValueError(
                f"Esperava FUNCAO, mas recebi {func_type}.")
        return


class AssigmentOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        symbol_table.set_variable(
            self.children[0].value, self.children[1].evaluate(symbol_table))


class Type(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def evaluate(self, symbol_table):
        return self.value


class IntVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def evaluate(self, symbol_table):
        return (self.value, "int")


class BoolVal(Node):
    def __init__(self, value):
        self.value = value
        self.children = []

    def evaluate(self, symbol_table):
        return (self.value, "bool")


class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        return symbol_table.get_variable(self.value)


class Return(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        return_name = list(symbol_table.table.keys())[0]
        symbol_table.set_variable(
            return_name, self.children[0].evaluate(symbol_table))


class Statements(Node):
    def __init__(self):
        self.value = None
        self.children = []

    def evaluate(self, symbol_table):
        for child in self.children:
            if (child.value == "RETORNE"):
                child.evaluate(symbol_table)
                break
            child.evaluate(symbol_table)


class While(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        if (self.children[0].evaluate(symbol_table)[1] == "bool"):
            while (self.children[0].evaluate(symbol_table)[0] == True):
                self.children[1].evaluate(symbol_table)
            return
        else:
            raise ValueError(
                f"Esperava BOOL dentro do 'enquanto', mas recebi {self.children[0].evaluate(symbol_table)[1]}.")


class If(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        if (self.children[0].evaluate(symbol_table)[1] == "bool"):
            if (self.children[0].evaluate(symbol_table)[0] == True):
                return self.children[1].evaluate(symbol_table)
            elif (len(self.children) == 3):
                return self.children[2].evaluate(symbol_table)
        else:
            raise ValueError(
                f"Esperava BOOL dentro do 'se', mas recebi {self.children[0].evaluate(symbol_table)[1]}.")


class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        print(self.children[0].evaluate(symbol_table)[0])


class Scan(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        scan = int(input())
        self.value = scan
        return (self.value, "int")
