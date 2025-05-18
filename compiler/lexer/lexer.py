import re
from lexer.keywords import *
from lexer.token_specification import *
token_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)
class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value}, {self.line}, {self.column})'
def lexer(code):
    line_num = 1
    line_start = 0
    tokens = []
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == "NUMBER":
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
            tokens.append(Token("NUMBER", value, line_num, column))
        elif kind == "ID":
            if value in KEYWORDS:
                tokens.append(Token("KEYWORD", value, line_num, column))
            else:
                tokens.append(Token("IDENTIFIER", value, line_num, column))
        elif kind == "STRING":
            tokens.append(Token("STRING", value, line_num, column))
        elif kind == "NEWLINE":
            line_num += 1
            line_start = mo.end()
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            raise RuntimeError(f'Unexpected character {value!r} at line {line_num} column {column}')
        else:
            tokens.append(Token(kind, value, line_num, column))

    return tokens