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
    "INT8",
    "INT16",
    "INT32",
    "INT64",
    "UINT8",
    "UINT16",
    "UINT32",
    "UINT64",
]

tokens += [
    "F32",
    "F64",
    "I8",
    "I16",
    "I32",
    "I64",
    "U8",
    "U16",
    "U32",
    "U64",
]

tokens += [
    "LIT_STR",
    "LIT_CHR",
    "LIT_FLT",
    "LIT_HEX",
    "LIT_INT",
]

tokens += [
    "ASSIGN",
    "ASTERISK",
    "COMMENT_MULTI",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "LPAREN",
    "RPAREN",
    "COMMA",
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
    r"float"

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
    r"signd"

    return tok


def t_UNSIGNED(tok):
    r"unsigned"

    return tok


def t_F32(tok):
    r"f32"

    return tok


def t_F64(tok):
    r"f64"

    return tok


def t_I8(tok):
    r"i8"

    return tok


def t_I16(tok):
    r"i16"

    return tok


def t_I32(tok):
    r"i32"

    return tok


def t_I64(tok):
    r"i64"

    return tok


def t_U8(tok):
    r"u8"
    return tok


def t_U16(tok):
    r"u16"

    return tok


def t_U32(tok):
    r"u32"

    return tok


def t_U64(tok):
    r"u64"

    return tok


def t_INT8(tok):
    r"int8_t"

    return tok


t_INT16 = r"int16_t"
t_INT32 = r"int32_t"
t_INT64 = r"int64_t"

t_UINT8 = r"uint8_t"
t_UINT16 = r"uint16_t"
t_UINT32 = r"uint32_t"
t_UINT64 = r"uint64_t"


# Delimeters
def t_ASSIGN(tok):
    r"="
    return tok


def t_ASTERISK(tok):
    r"\*"
    return tok


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
    r"(0x[a-f0-9]+)|([0-9]+)"

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


def t_error(tok):
    print(f"Illegal character '{tok.value[0]}'")
    tok.lexer.skip(1)


def get_lexer():
    """Build the lexer"""

    return lex.lex()
