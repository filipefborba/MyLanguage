import argparse
from Parser import Parser
from Tokenizer import Tokenizer
from PrePro import PrePro
from SymbolTable import SymbolTable


def readFile(path):
    with open(path, 'rb') as file:
        data = file.read().decode('utf-8')
    data = PrePro.filter(data)
    file.close()
    return data


def main():
    # try:
    # Read arguments from command line
    parser = argparse.ArgumentParser(
        description='Compilador da linguagem C em português. Por favor, utilize .c como arquivo.')
    parser.add_argument('path', type=str, help='caminho para arquivo .c')
    args = parser.parse_args()

    # Parser execution
    symbol_table = SymbolTable()
    code = readFile(args.path)
    result = Parser.run(code)
    if (Parser.tokens.actual.type == "EOF"):
        result.evaluate(symbol_table)
    else:
        raise ValueError(
            f"Esperava EOF, mas recebi {Parser.tokens.actual.type}.")
    # except Exception as err:
    #     print(err)


if __name__ == "__main__":
    main()
