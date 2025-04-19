TOKEN_TYPES = {
    'KEYWORD': 'KEYWORD',  # ключевые слова
    'IDENTIFIER': 'IDENTIFIER',  # идентификаторы
    'NUMBER': 'NUMBER',  # числа
    'STRING': 'STRING',  # строки
    'SYMBOL': 'SYMBOL',  # символы
    'TYPE': 'TYPE',  # типы данных
    'OPERATOR': 'OPERATOR',  # операторы
    'EOF': 'EOF'  # конец файла
}

KEYWORDS = {'func', 'out', 'inp', 'for', 'while', 'try', 'catch', 'always'}  # ключевые слова для регулярных выражений
TYPES = {'i8', 'i16', 'i32', 'i64', 'i128', 'u8', 'u16', 'u32', 'u64', 'u128', 'f16', 'f32', 'f64', 'str', 'bool', 'arr'} # типы данных для ключевых выражений
OPERATORS = {'+', '-', '*', '/', '%', '=', '==', '!=', '>', '<', '>=', '<=', '&&', '||'} # операторы