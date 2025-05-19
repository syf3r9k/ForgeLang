# compiler.py

from lexer.lexer import lexer
import sys
import re
import os

#path to main file
path = "tests/main.frg"

#info about compiler
version = "0.1"

#flags
debug_info = 1

processed_files = set()

def get_imports_from_code(code):
    return re.findall(r'import\s+"([^"]+)"\s*;', code)

def process_file(filepath):
    tokens = []
    fullpath = os.path.abspath(filepath)
    if fullpath in processed_files:
        return tokens
    processed_files.add(fullpath)
    with open(fullpath, 'r') as f:
        code = f.read()
        if debug_info == 1:
            print(f"\n==> Lexing the file: {filepath}")
            print(code)
        file_tokens = lexer(code)
        tokens.extend(file_tokens)
        imports = get_imports_from_code(code)
        for imp in imports:
            import_path = os.path.join(os.path.dirname(filepath), imp)
            tokens.extend(process_file(import_path))
    return tokens

def main():
    all_tokens = process_file(path)
    if debug_info == 1:
        print("\n=== All tokens ===")
        for t in all_tokens:
            print(t)

if __name__ == "__main__":
    main()
