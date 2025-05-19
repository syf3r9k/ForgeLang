#compiler
from lexer.lexer import lexer

path = "tests/main.frg"

version = "0.1"


def main():
    with open(path, 'r') as main_code:
        code = main_code.read()
    tokens = lexer(code)
    print(tokens)

main()