#compiler
from lexer.lexer import lexer

path = "tests/main.frg"

def main():
    with open(path, 'r') as main_code:
        code = main_code.read()
    tokens = lexer(code)
    print(tokens)

main()