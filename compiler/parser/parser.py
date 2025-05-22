class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = {
            "type": "Program",
            "imports": [],
            "body": [],
        }
    def parse_function():
        pass


"""
{
'/home/mkx/ForgeLang/tests/main.frg': 
[ Token(KEYWORD, import, 1, 0),Token(STRING, "test.frg", 1, 7),Token(KEYWORD, as, 1, 18),Token(IDENTIFIER, t, 1, 21),Token(SEMICOLON, ;, 1, 22), 
Token(KEYWORD, fun, 3, 0),Token(IDENTIFIER, main, 3, 4),Token(LPAREN, (, 3, 8),Token(RPAREN, ), 3, 9),Token(KEYWORD, void, 3, 11),Token(LBRACE, {, 3, 16), 
Token(IDENTIFIER, t, 4, 4),Token(DOT, ., 4, 5), Token(IDENTIFIER, test_function, 4, 6),Token(LPAREN, (, 4, 19),Token(RPAREN, ), 4, 20), Token(SEMICOLON, ;, 4, 21),
Token(RBRACE, }, 5, 0)], 

'/home/mkx/ForgeLang/tests/test.frg': 
[Token(KEYWORD, fun, 1, 0),Token(IDENTIFIER, test_function, 1, 4),Token(LPAREN, (, 1, 17),Token(RPAREN, ), 1, 18),Token(KEYWORD, void, 1, 20),Token(LBRACE, {, 1, 25),
Token(KEYWORD, outln, 2, 4),Token(LPAREN, (, 2, 9),Token(STRING, "Hello, this test!", 2, 10),Token(RPAREN, ), 2, 29),Token(SEMICOLON, ;, 2, 30),
Token(RBRACE, }, 3, 0)]
}
"""

"""
"fun", "struct", "met", "case", "void", "import", "as",
"i8", "i16", "i32", "i64", "i128",
"u8", "u16", "u32", "u64", "u128",
"f32", "f64", "strc",
"string", "bool",
"out", "outln",
"if", "elf", "els",
"while", "for",
"true", "false",
"try", "catch", "always",
"mut"
"""

def parser(all_tokens):
    for path, tokens in all_tokens.items():
        print(path)
        for t in tokens:
            if t.type == "KEYWORD":
                if t.value == "fun":
                    print("function now")
                

            #print(f"type: {t.type} value: {t.value}\n")