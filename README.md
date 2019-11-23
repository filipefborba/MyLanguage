# MyLanguage

Linguagem C com palavras reservadas em português e um compilador próprio.

## EBNF

* programa = { funcao };
* funcao = tipo, identificador, "(", { tipo, identificador, ","}, ")", bloco;
* bloco = "{", { afirmacao }, "}";
* afirmacao = sem_op | declaracao | atribuicao | imprima | se | enquanto | bloco | "int", identificador | "retorne", "(", expressao_rel, ")", ";";
* tipo = "int";
* sem_op = ";";
* declaracao = ("int" | "bool"), identificador, ";";
* atribuicao = identificador, "=", expressao, ";";
* imprime = "imprime", "(", expressao, ")", ";";
* se = "se", "(", expressao_rel, ")", afirmacao, { senao };
* senao = "senao", afirmacao;
* enquanto = "enquanto", "(", expressao_rel, ")", afirmacao;
* expressao_rel = expressao | { ("==" | ">" | "<"), expressao };
* expressao = termo, { ("+" | "-" | "//"), termo };
* termo = fator, { ("*" | "/" | "&&"), fator };
* fator = (("+" | "-" | "~"), fator) | numero | "(", expressao_rel, ")" | identificador, { "(", { expressao_rel, "," } ")"} | scan, "(", ")";
* identificador = caracter, { caracter | digito | "_" };
* numero = digito, { digito };
* caracter = ( a | ... | z | A | ... | Z);
* digito = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0);

## Viabilidade LLVM

O projeto de infraestrutura de compilador LLVM é uma série de tecnologias de compilador e toolchains que pode ser usado para desenvolver o front end de qualquer linguagem de programação e o back end de qualquer conjunto de instruções (ISA). O LLVM é desenhado em volta de uma representação intermediária (IR) independente de linguagem.  

O núcleo do projeto contém todas as ferramentas, bibliotecas e headers necessários para processar uma IR e convertê-la em arquivos de objeto. Ele contém um assembler, disassembler, analisador de bitcode e um otimizador de bitcode.
Outra parte do projeto é o front end em Clang. Esse componente consegue compilar C, C++, Objective C, e Objective C++ em bitcode LLVM - e a partir deles, em arquivos de objeto, usando o LLVM.

Visto isso, no site do LLVM, temos um [guia de exemplo](https://llvm.org/docs/tutorial/OCamlLangImpl1.html) para conseguir compilar uma linguagem qualquer (no caso, a Kaleidoscope). Até o momento, com o Flex e Bison, temos a análise Léxica e Sintática, mas não produzimos uma Abstract Syntax Tree, necessária para a conversão em IR. 

Com isso, é possível concluir que pode-se utilizar o LLVM para gerar o código de nossa linguagem, porém, é necessário implementar a construção da AST.
Por outro lado, a sintaxe do LLVM não é tão simples e o compilador que está sendo feito em aula também poderia realizar o mesmo tipo de trabalho.

## Como usar

Para utilizar o compilador, basta utilizar o exemplo a seguir:  

```
python3 main.py testes/teste1.txt  
```
O programa exemplo em questão (teste1.txt) imprime 1 para as expressões que realmente dão Verdadeiro.

Caso queira fazer um exemplo próprio, basta criar um arquivo de texto seguindo a gramática definida e compilar da mesma forma que acima.  
Use como exemplo as outras entradas de teste!
