# MyLanguage

Linguagem C com palavras reservadas em português e um compilador próprio.

## EBNF

A EBNF da linguagem está descrita no arquivo [EBNF.md](EBNF.md).

## Viabilidade LLVM

O projeto de infraestrutura de compilador LLVM é uma série de tecnologias de compilador e toolchains que pode ser usado para desenvolver o front end de qualquer linguagem de programação e o back end de qualquer conjunto de instruções (ISA). O LLVM é desenhado em volta de uma representação intermediária (IR) independente de linguagem.  

O núcleo do projeto contém todas as ferramentas, bibliotecas e headers necessários para processar uma IR e convertê-la em arquivos de objeto. Ele contém um assembler, disassembler, analisador de bitcode e um otimizador de bitcode.
Outra parte do projeto é o front end em Clang. Esse componente consegue compilar C, C++, Objective C, e Objective C++ em bitcode LLVM - e a partir deles, em arquivos de objeto, usando o LLVM.

Visto isso, no site do LLVM, temos um [guia de exemplo](https://llvm.org/docs/tutorial/OCamlLangImpl1.html) para conseguir compilar uma linguagem qualquer (no caso, a Kaleidoscope). Até o momento, com o Flex e Bison, temos a análise Léxica e Sintática, mas não produzimos uma Abstract Syntax Tree, necessária para a conversão em IR. 

Com isso, é possível concluir que pode-se utilizar o LLVM para gerar o código de nossa linguagem, porém, é necessário implementar a construção da AST.
Por outro lado, a sintaxe do LLVM não é tão simples e o compilador que está sendo feito em aula também poderia realizar o mesmo tipo de trabalho.