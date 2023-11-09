"""
Tokens and Lexer for sea-lang
=============================


"""
import yace.slang.ply.lex as lex

tokens = []

tokens += [
    "CONST",
    "LONG",
    "SHORT",
    "SIGNED",
    "UNSIGNED",
]

tokens += [
    "CHAR",
    "DOUBLE",
    "FLOAT",
    "INT",
    "VOID",
]

tokens += [
    "TYPE_INT_FIXED_WIDTH",
    "TYPE_FLT_FIXED_WIDTH",
]

tokens += [
    "LIT_STR",
    "LIT_CHR",
    "LIT_FLT",
    "LIT_HEX",
    "LIT_INT",
    "LIT_NUM",
]

tokens += [
    "ASSIGN",
    "ASTERISK",
    "COMMENT_MULTI",
    "DOUBLE_QUOTE",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "LPAREN",
    "RPAREN",
    "COMMA",
    "LT",
    "GT",
    "COLON",
    "SEMI",
]

tokens += [
    "ENUM",
    "STRUCT",
    "UNION",
]

tokens += [
    "EXTERN",
    "STATIC",
    "TYPEDEF",
    "INCLUDE",
    "INCLUDE_SYSTEM",
    "INCLUDE_USER",
    "DEFINE",
]

tokens += [
    "ID",
]


def t_CONST(tok):
    r"const"

    return tok


def t_EXTERN(tok):
    r"extern"
    return tok


def t_STATIC(tok):
    r"static"
    return tok


def t_TYPEDEF(tok):
    r"typedef"
    return tok


def t_INCLUDE(tok):
    r"\#include"
    return tok


def t_DEFINE(tok):
    r"\#define"
    return tok


def t_ENUM(tok):
    r"enum"
    return tok


def t_STRUCT(tok):
    r"struct"

    return tok


def t_UNION(tok):
    r"union"

    return tok


# Scalar types
def t_CHAR(tok):
    r"char"

    return tok


def t_DOUBLE(tok):
    r"double"

    return tok


def t_FLOAT(tok):
    r"float"

    return tok


def t_INT(tok):
    r"int"

    return tok


def t_VOID(tok):
    r"void"

    return tok


def t_LONG(tok):
    r"long"

    return tok


def t_SHORT(tok):
    r"short"

    return tok


def t_SIGNED(tok):
    r"signed"

    return tok


def t_UNSIGNED(tok):
    r"unsigned"

    return tok


def t_TYPE_FLT_FIXED_WIDTH(tok):
    r"f32|f64"

    return tok


def t_TYPE_INT_FIXED_WIDTH(tok):
    (
        r"i8|i16|i32|i64|"
        r"u8|u16|u32|u64|"
        r"uint8_t|int16_t|int32_t|int64_t|"
        r"uint8_t|uint16_t|uint32_t|uint64_t"
    )

    return tok


# Delimeters
def t_ASSIGN(tok):
    r"="
    return tok


def t_ASTERISK(tok):
    r"\*"
    return tok


t_DOUBLE_QUOTE = r"\""
t_LT = r"<"
t_GT = r">"
t_COLON = r":"
t_COMMA = r","
t_LBRACE = r"\{"
t_LBRACKET = r"\["
t_LPAREN = r"\("
t_RBRACE = r"\}"
t_RBRACKET = r"\]"
t_RPAREN = r"\)"
t_SEMI = r";"


# Literals / Constants
def t_LIT_HEX(tok):
    r"(0x[A-Za-f0-9]+)|([0-9]+)"

    tok.value = int(tok.value, 16)

    return tok


def t_LIT_FLT(tok):
    r"((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?"

    tok.value = float(tok.value)

    return tok


def t_LIT_INT(tok):
    r"\d+([uU]|[lL]|[uU][lL]|[lL][uU])?"

    tok.value = int(tok.value)

    return tok


# Literal for array sizes
def t_LIT_NUM(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_LIT_STR(tok):
    r"\"([^\\\n]|(\\.))*?\" "

    return tok


def t_LIT_CHR(tok):
    r"(L)?'([^\\\n]|(\\.))*?'"

    return tok


def t_COMMENT_MULTI(tok):
    r"/\*(.|\n)*?\*/"

    tok.lexer.lineno += tok.value.count("\n")
    lines = tok.value.split("\n")

    comment = []
    for count, ln in enumerate(lines):
        if count in [0, len(lines) - 1]:  # Drop the first and last line
            continue

        ln = ln.lstrip()
        if not count:
            ln = ln.lstrip("/")
        ln = ln.lstrip("*")
        if (count + 1) == len(lines):
            ln = ln.strip("/")

        comment.append(ln)

    tok.value = "\n".join(comment)

    return tok


# Identifiers
def t_ID(tok):
    r"[A-Za-z_][A-Za-z0-9_]*"

    return tok


def t_INCLUDE_SYSTEM(tok):
    r"<[A-Za-z0-9_\./]+>"

    return tok


def t_INCLUDE_USER(tok):
    r"\"[A-Za-z0-9_\./]+\" "

    return tok


t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(tok):
    print(f"Illegal character '{tok.value[0]}'")
    tok.lexer.skip(1)


lexer = lex.lex()
