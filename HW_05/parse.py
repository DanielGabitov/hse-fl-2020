import ply.yacc as yacc
import sys

from lex import tokens

flag = False

# Error rule for syntax errors
def p_error(p):
    global flag
    flag = False

def p_expression_full(p):
    'expression : sitem EQ exp DOT'
    p[0] = ('expression', p[1], ':-', p[3], '.')

def p_expression_small(p):
    'expression : sitem DOT'
    p[0] = ('expression', p[1], '.')

def p_exp_plus(p):
    'exp : m PLUS exp'
    p[0] = ('exp', p[1], ';', p[3])

def p_exp_m(p):
    'exp : m'
    p[0] = ('exp', p[1])

def p_m_pa(p):
    'm : pa'
    p[0] = ('m', p[1])

def p_m_mult(p):
    'm : pa MULT m'
    p[0] = ('m', p[1], ',', p[3])

def p_pa_sitem(p):
    'pa : sitem'
    p[0] = ('pa', p[1])

def p_pa_expbr(p):
    'pa : LBR exp RBR'
    p[0] = ('pa', '(', p[2], ')')

def p_sitem_id(p):
    'sitem : ID'
    p[0] = ('sitem', p[1])

def p_sitem_item(p):
    'sitem : ID item'
    p[0] = ('sitem', p[1], p[2])

def p_item_big(p):
    'item : LBR ID sitem RBR item'
    p[0] = ('item', '(', p[2], p[3], ')', p[5])

def p_item_small(p):
    'item : LBR ID sitem RBR'
    p[0] = ('item', '(', p[2], p[3], ')')

def p_item_sitem(p):
    'item : sitem'
    p[0] = ('item', p[1])


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