#compiler
from lexer.lexer import lexer
import sys

path = "main.frg"

version = "0.1"


def main():
    #with open(path, 'r') as main_code:
        #code = main_code.read()
    #tokens = lexer(code)
    #print(tokens)
    print(sys.argv)

main()