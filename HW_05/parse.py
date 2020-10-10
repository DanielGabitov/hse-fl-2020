import ply.yacc as yacc

from lex import tokens

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

def p_expression_full(p):
    'expression : sitem EQ dis DOT'
    p[0] = ('expression', p[1], ':-', p[3], '.')

def p_expression_small(p):
    'expression : sitem DOT'
    p[0] = ('expression', p[1], '.')

def p_sitem_item(p):
    'sitem : ID item'
    p[0] = ('sitem', p[1], p[2])

def p_sitem_id(p):
    'sitem : ID'
    p[0] = ('sitem', p[1])

def p_item_brplusitem(p):
    'item : LBR item RBR item'
    p[0] = ('item', '(', p[2], p[3], ')', p[5])

def p_item_br(p):
    'item : LBR item RBR'
    p[0] = ('item', '(', p[2], p[3], ')')

def p_item_dis(p):
    'item : LBR dis RBR'
    p[0] = ('item', '(', p[2], ')')

def p_item_sitem(p):
    'item : sitem'
    p[0] = ('item', p[1])


def p_dis_plus(p):
    'dis : con PLUS dis'
    p[0] = ('dis', p[1], ';', p[3])

def p_dis_con(p):
    'dis : con'
    p[0] = ('dis', p[1])

def p_con_mult(p):
    'con : item MULT con'
    p[0] = ('con', p[1], ',', p[3])

def p_con_item(p):
    'con : item'
    p[0] = ('con', p[1])



# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = input()
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)