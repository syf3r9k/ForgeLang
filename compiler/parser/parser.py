class Token:
    def __init__(self, type_, value, line=None, column=None):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = {
            "type": "Program",
            "imports": [],
            "body": [],
        }

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, *types):
        tok = self.peek()
        if tok and tok.type in types:
            self.pos += 1
            return tok
        return None

    def expect(self, type_, value=None):
        tok = self.peek()
        if not tok:
            raise SyntaxError(f"Unexpected end of input, expected {type_} {value}")
        if tok.type != type_:
            raise SyntaxError(f"Expected token type {type_}, got {tok.type} ('{tok.value}') at pos {self.pos}")
        if value is not None and tok.value != value:
            raise SyntaxError(f"Expected token value '{value}', got '{tok.value}' at pos {self.pos}")
        self.pos += 1
        return tok

    def parse(self):
        while self.peek() is not None:
            tok = self.peek()
            if tok.type == "KEYWORD" and tok.value == "import":
                self.ast["imports"].append(self.parse_import())
            elif tok.type == "KEYWORD" and tok.value == "fun":
                self.ast["body"].append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected token: {tok.type} '{tok.value}' at pos {self.pos}")
        return self.ast

    def parse_import(self):
        self.expect("KEYWORD", "import")
        path_token = self.expect("STRING")
        self.expect("KEYWORD", "as")
        alias_token = self.expect("IDENTIFIER")
        self.expect("SEMICOLON")
        return {
            "type": "Import",
            "path": path_token.value,
            "alias": alias_token.value
        }

    def parse_function(self):
        self.expect("KEYWORD", "fun")
        name_token = self.expect("IDENTIFIER")
        self.expect("LPAREN")
        self.expect("RPAREN")
        self.expect("KEYWORD", "void")
        body_stmts = self.parse_block()
        return {
            "type": "Function",
            "name": name_token.value,
            "return": "void",
            "body": body_stmts
        }

    def parse_block(self):
        self.expect("LBRACE")
        statements = []
        while True:
            tok = self.peek()
            if tok is None:
                raise SyntaxError("Unexpected end of input inside block")
            if tok.type == "RBRACE":
                break
            statements.append(self.parse_statement())
        self.expect("RBRACE")
        return statements

    def parse_statement(self):
        tok = self.peek()

        if tok.type == "KEYWORD" and tok.value == "case":
            self.expect("KEYWORD", "case")

            mutable = False
            if self.peek().type == "KEYWORD" and self.peek().value == "mut":
                self.expect("KEYWORD", "mut")
                mutable = True

            var_name = self.expect("IDENTIFIER").value

            allowed_types = ("i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64",
                            "f32", "f64", "bool", "string")
            tok_type = self.peek()
            if tok_type.type in ("IDENTIFIER", "KEYWORD") and tok_type.value in allowed_types:
                var_type = self.expect(tok_type.type).value
            else:
                raise SyntaxError(f"Expected type token, got {tok_type.type} ('{tok_type.value}') at pos {self.pos}")

            self.expect("ASSIGN")

            expr = self.parse_expression()

            self.expect("SEMICOLON")

            return {
                "type": "VariableDeclaration",
                "mutable": mutable,
                "name": var_name,
                "var_type": var_type,
                "value": expr,
            }

        elif tok.type == "IDENTIFIER":
            # Самае цікавае — разбор імя з доступам праз DOT
            name = self.expect("IDENTIFIER").value

            # Падтрымка доступу праз DOT: obj.prop.method()
            while self.peek() and self.peek().type == "DOT":
                self.expect("DOT")
                attr = self.expect("IDENTIFIER").value
                # Ствараем вузел MemberAccess, дзе object — папярэдні, property — новы атрыбут
                name = {
                    "type": "MemberAccess",
                    "object": name,
                    "property": attr
                }

            next_tok = self.peek()

            if next_tok.type == "ASSIGN":
                self.expect("ASSIGN")
                expr = self.parse_expression()
                self.expect("SEMICOLON")
                return {
                    "type": "Assignment",
                    "name": name,
                    "value": expr,
                }
            elif next_tok.type == "LPAREN":
                self.expect("LPAREN")
                args = []
                if self.peek().type != "RPAREN":
                    args.append(self.parse_expression())
                    while self.peek().type == "COMMA":
                        self.expect("COMMA")
                        args.append(self.parse_expression())
                self.expect("RPAREN")
                self.expect("SEMICOLON")
                return {
                    "type": "FunctionCall",
                    "name": name,
                    "args": args,
                }
            else:
                raise SyntaxError(f"Unexpected token after identifier: {next_tok.type} ('{next_tok.value}') at pos {self.pos}")

        elif tok.type == "KEYWORD" and tok.value == "outln":
            self.expect("KEYWORD", "outln")
            self.expect("LPAREN")
            args = []
            if self.peek().type != "RPAREN":
                args.append(self.parse_expression())
                while self.peek().type == "COMMA":
                    self.expect("COMMA")
                    args.append(self.parse_expression())
            self.expect("RPAREN")
            self.expect("SEMICOLON")
            return {
                "type": "FunctionCall",
                "name": "outln",
                "args": args,
            }

        else:
            raise SyntaxError(f"Unexpected token {tok.type} ('{tok.value}') at pos {self.pos}")


    def parse_expression(self):
        return self.parse_binary_expression()

    def parse_binary_expression(self, min_precedence=0):
        left = self.parse_primary()

        # Табліца прыярытэтаў для аператараў
        precedences = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
        }

        while True:
            tok = self.peek()
            if tok is None or tok.type != "OP" or tok.value not in precedences:
                break
            op_prec = precedences[tok.value]
            if op_prec < min_precedence:
                break
            op = self.expect("OP").value
            right = self.parse_binary_expression(op_prec + 1)
            left = {
                "type": "BinaryExpression",
                "operator": op,
                "left": left,
                "right": right,
            }

        return left

    def parse_primary(self):
        tok = self.peek()
        if tok.type in ("NUMBER", "STRING", "IDENTIFIER"):
            return self.expect(tok.type).value
        elif tok.type == "LPAREN":
            self.expect("LPAREN")
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token in expression: {tok.type} '{tok.value}' at pos {self.pos}")


def parser(all_tokens):
    for path, tokens in all_tokens.items():
        print(f"=== Парсим файл: {path} ===")
        p = Parser(tokens)
        ast = p.parse()
        print(ast)
