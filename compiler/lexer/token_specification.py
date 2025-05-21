TOKEN_SPECIFICATION = [
    ("NUMBER",   r'\b\d+(\.\d+)?\b'),       # Лікі
    ("STRING",   r'"([^"\\]|\\.)*"'),       # Строкі
    ("ID",       r'\b[A-Za-z_][A-Za-z0-9_]*\b'),  # Ідэнтыфікатары
    ("LBRACK",   r'\['),
    ("RBRACK",   r'\]'),
    ("ASSIGN",   r'='),
    ("COLON",    r':'),
    ("DOT",      r'\.'),                   # <== ДАДАЙ ВОСЬ ГЭТА
    ("SEMICOLON",r';'),
    ("COMMA",    r','),
    ("LPAREN",   r'\('),
    ("RPAREN",   r'\)'),
    ("LBRACE",   r'\{'),
    ("RBRACE",   r'\}'),
    ("OP",       r'[+\-*/]'),
    ("SKIP",     r'[ \t]+'),
    ("NEWLINE",  r'\n'),
    ("MISMATCH", r'.'),
]