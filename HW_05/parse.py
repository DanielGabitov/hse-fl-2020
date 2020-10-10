import ply.yacc as yacc
import sys

from lex import tokens

flag = False

# Error rule for syntax errors
def p_error(p):
    global flag
    flag = False

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
    'item : LBR ID item RBR item'
    p[0] = ('item', '(', p[2], p[3],')', p[5])

def p_item_br(p):
    'item : LBR ID item RBR'
    p[0] = ('item', '(', p[2], p[3], ')')

def p_sitem_dis(p):
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



parser = yacc.yacc()

def main():
    global flag
    f = open("test.txt")
    output_name = ("test.txt").split('.')
    f_out = open(output_name[0] + ".out", 'w')
    s = str(f.read())
    i = 0
    while (i < len(s)):
        line = ""
        while i < len(s) and s[i] != '.':
            line += s[i]
            i += 1 
        if i < len(s):
            line += '.'
        flag = True
        result = parser.parse(line)
        if not flag:
            f_out.write("Syntax Error!" + '\n')
        else:
            f_out.write(str(result) + '\n')
        flag = True
        i += 1

if __name__ == "__main__":
    main()