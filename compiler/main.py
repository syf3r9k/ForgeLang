# compiler.py

from lexer.lexer import lexer
from parser.parser import parser
import sys
import re
import os

path = "tests/main.frg"
version = "0.1"
debug_info = int(sys.argv[2])
processed_files = set()

def get_imports_from_code(code):
    return re.findall(r'import\s+"([^"]+)"\s+as\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*;', code)

def process_file(filepath):
    tokens_by_file = {}
    fullpath = os.path.abspath(filepath)
    if fullpath in processed_files:
        return tokens_by_file
    processed_files.add(fullpath)
    with open(fullpath, 'r') as f:
        code = f.read()
        if debug_info == 1:
            print(f"\n==> Lexing the file: {filepath}")
            print(code)
        file_tokens = lexer(code)
        tokens_by_file[fullpath] = file_tokens
        imports = get_imports_from_code(code)
        for imp_path, alias in imports:
            import_path = os.path.join(os.path.dirname(filepath), imp_path)
            tokens_by_file.update(process_file(import_path))
    return tokens_by_file

def main():
    all_tokens_by_file = process_file(sys.argv[1])
    if debug_info == 1:
        print("\n=== Tokens by file ===")
        for path, tokens in all_tokens_by_file.items():
            print(f"\n-- {path} --")
            for t in tokens:
                print(t)
    parser(all_tokens_by_file)

if __name__ == "__main__":
    main()
