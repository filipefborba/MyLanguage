class SymbolTable:
    def __init__(self):
        self.table = {}

    def get_variable(self, var_name):
        if (var_name not in self.table):
            raise ValueError(f"Variavel {var_name} não declarada.")
        return self.table[var_name]

    def declare_variable(self, var_type, var_name):
        if (var_name in self.table):
            raise ValueError(
                f"Nome de variável inválido {var_name}, já declarado.")
        self.table[var_name] = (None, var_type)

    def set_variable(self, var_name, var_value):
        if (var_name not in self.table):
            raise ValueError(f"Variável {var_name} não declarada.")

        variable = self.get_variable(var_name)
        if (type(var_value) is tuple):
            if (variable[1] == var_value[1]):
                self.table[var_name] = (var_value[0], var_value[1])
            else:
                raise ValueError(
                    f"Atribuição de variável inválida: antigo {variable[1]} com o novo {var_value[1]}")
        else:
            self.table[var_name] = (var_value, variable[1])


class StaticTable:
    table = {}

    def get_variable(self, var_name):
        if (var_name not in self.table):
            raise ValueError(f"Variavel {var_name} não declarada.")
        return self.table[var_name]

    def declare_variable(self, var_type, var_name):
        if (var_name in self.table):
            raise ValueError(
                f"Nome de variável inválido {var_name}, já declarado.")
        self.table[var_name] = (None, var_type)

    def set_variable(self, var_name, var_value):
        if (var_name not in self.table):
            raise ValueError(f"Variável {var_name} não declarada.")

        variable = StaticTable.get_variable(StaticTable, var_name)
        if (type(var_value) is tuple):
            if (variable[1] == var_value[1]):
                self.table[var_name] = (var_value[0], var_value[1])
            else:
                raise ValueError(
                    f"Atribuição de variável inválida: antigo {variable[1]} com o novo {var_value[1]}")
        else:
            self.table[var_name] = (var_value, variable[1])
