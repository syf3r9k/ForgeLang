#compiler
from lexer.lexer import lexer
import sys
import re

path = "tests/main.frg"

version = "0.1"

def get_imports_from_file(code):
    imports = re.findall(r'import\s+"([^"]+)"\s*;', code)
    return imports

def main():
    with open(path, 'r') as main_code:
        code = main_code.read()
    print(f"{code}\n")
    get_imports_from_file()
    maincode_tokens = lexer(code)

    print(maincode_tokens)

main()