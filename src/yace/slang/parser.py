"""
LALR(1) parser for sea-lang
===========================

Stuff that is missing:

* Type specifications
* Function declarations
* Function pointers

Produce an AST. This should make use of the current structures of Yace.
"""
import yace.slang.ply.yacc as yacc

# We need noqa, since 'tokens' is never referred to, however, it is used by PLY
# introspectively. Thus, to avoid the removal of the import by 'ruff', then
# ignore with noqa
from yace.slang.lexer import tokens  # noqa


# Parser rules
def p_api(p):
    """api : api declaration
    | declaration"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_declaration(p):
    """declaration  : COMMENT_MULTI
    | include_directive
    | define_directive
    | TYPEDEF type_specifier ID
    | enum_declaration
    | struct_declaration"""
    p[0] = p[1]


def p_include_directive(p):
    """include_directive    : INCLUDE INCLUDE_SYSTEM
    | INCLUDE INCLUDE_USER"""

    is_system = f"{p[2][0]}{p[2][-1]}" == "<>"
    path = p[2].replace('"', "").replace("<", "").replace(">", "")

    p[0] = ("include", path, is_system)


def p_define_directive(p):
    """define_directive   : DEFINE ID literal"""
    p[0] = ("define", p[2], p[3])


def p_literal(p):
    """literal  : LIT_STR
    | LIT_CHR
    | LIT_FLT
    | LIT_HEX
    | LIT_INT"""
    p[0] = p[1]


def p_type_specifier(p):
    """type_specifier   : type_chr
    | type_int
    | type_flt"""

    p[0] = p[1]


def p_type_chr(p):
    """type_chr : CHAR
    | SIGNED CHAR
    | UNSIGNED CHAR"""
    p[0] = ("chr", p[1:])


def p_type_int(p):
    """type_int : INT
    | SIGNED INT
    | UNSIGNED INT
    | SHORT
    | SHORT INT
    | SIGNED SHORT
    | SIGNED SHORT INT
    | UNSIGNED SHORT
    | UNSIGNED SHORT INT
    | LONG
    | LONG INT
    | SIGNED LONG
    | SIGNED LONG INT
    | UNSIGNED LONG
    | UNSIGNED LONG INT
    | LONG LONG
    | LONG LONG INT
    | SIGNED LONG LONG
    | SIGNED LONG LONG INT
    | UNSIGNED LONG LONG
    | UNSIGNED LONG LONG INT
    | TYPE_INT_FIXED_WIDTH
    """
    p[0] = ("int", p[1:])


def p_type_flt(p):
    """type_flt : FLOAT
    | DOUBLE
    | LONG DOUBLE
    | TYPE_FLT_FIXED_WIDTH"""
    p[0] = ("flt", p[1:])


# enum foo { BAR, BAZ = 1, JAZZ = 0x2 }
def p_enum_declaration(p):
    r"""enum_declaration : ENUM ID LBRACE enum_list RBRACE SEMI"""

    p[0] = ("enum", p[2], p[4])


def p_enum_list(p):
    """enum_list : enum_list COMMA enum_item
    | enum_item"""
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_enum_item(p):
    """enum_item : ID
    | ID ASSIGN LIT_INT
    | ID ASSIGN LIT_HEX"""
    if len(p) == 2:
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[3])


#
# struct foo { int bar; double baz; }
#


def p_struct_declaration(p):
    "struct_declaration : STRUCT ID LBRACE struct_members RBRACE SEMI"
    p[0] = ("struct", p[2], p[4])


def p_struct_members(p):
    """struct_members   : struct_members struct_member
    | struct_member"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


def p_struct_member(p):
    """struct_member : type_specifier ID array_dimension SEMI
    | type_specifier ID SEMI"""
    if len(p) == 5:
        # Member with an array dimension
        p[0] = ("member", p[1], p[2], p[3])
    else:
        # Member without an array dimension
        p[0] = ("member", p[1], p[2])


def p_array_dimension(p):
    """array_dimension  : LBRACKET RBRACKET
    | LBRACKET LIT_NUM RBRACKET
    | LBRACKET LIT_NUM RBRACKET array_dimension"""
    if len(p) == 3:  # Flexible array-member
        p[0] = [p[2]]
    elif len(p) == 4:  # Array
        p[0] = [p[2]]
    else:  # Multi-dimension array
        p[0] = [p[2]] + p[4]


def p_error(p):
    if p:
        print(f"Syntax error at line ({p.lineno}); unexpected: '{p.value}'")
        return

    print("Syntax error at EOF")


def get_parser():
    """Grab and return the parser"""

    return yacc.yacc()
