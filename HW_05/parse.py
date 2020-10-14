import ply.yacc as yacc
import sys

from lex import tokens

flag = False

# Error rule for syntax errors
def p_error(p):
    global flag
    flag = False

def p_expression_full(p):
    'expression : atom1 EQ exp DOT'
    p[0] = ('expression', p[1], ':-', p[3], '.')

def p_expression_small(p):
    'expression : atom1 DOT'
    p[0] = ('expression', p[1], '.')

def p_exp_plus(p):
    'exp : m PLUS exp'
    p[0] = ('exp', p[1], ';', p[3])

def p_exp_m(p):
    'exp : m'
    p[0] = ('exp', p[1])

def p_m_mult(p):
    'm : pa MULT m'
    p[0] = ('m', p[1], ',', p[3])

def p_m_pa(p):
    'm : pa'
    p[0] = ('m', p[1])

def p_pa_atom1(p):
    'pa : atom1'
    p[0] = ('pa', p[1])

def p_pa_expbr(p):
    'pa : LBR exp RBR'
    p[0] = ('pa', '(', p[2], ')')

def p_atom1_id(p):
    'atom1 : ID'
    p[0] = ('atom1', p[1])

def p_atom1_atom2(p):
    'atom1 : ID atom2'
    p[0] = ('atom1', p[1], p[2])

def p_atom2_big(p):
    'atom2 : LBR atom3 RBR atom2'
    p[0] = ('atom2', '(', p[2], ')', p[4])

def p_atom2_small(p):
    'atom2 : LBR atom3 RBR'
    p[0] = ('atom2', '(', p[2], ')')

def p_atom2_atom1(p):
    'atom2 : atom1'
    p[0] = ('atom2', p[1]) 

def p_atom3_idbr(p):
    'atom3 : LBR atom3 RBR'
    p[0] = ('atom3', '(', p[2], ')')

def p_atom3_id(p):
    'atom3 : atom1'
    p[0] = ('atom3', p[1])


parser = yacc.yacc()

def main():
    global flag
    name = sys.argv[1] 
    f = open(name)
    output_name = (name).split('.')
    f_out = open(output_name[0] + '.out', 'w')
    s = str(f.read())
    i = 0
    while (i < len(s)):
        line = ''
        while i < len(s) and s[i] != '.':
            line += s[i]
            i += 1 
        if i < len(s) and s[i] == '.':
            line += '.'
            i += 1
        if not line.strip(' \n\t'):
            break
        flag = True
        try:
            result = parser.parse(line)
            if not flag:
                f_out.write("Syntax Error!" + '\n')
            else:
                f_out.write(str(result) + '\n')
            flag = True
            i += 1
        except IOError as exception:
            f_out.write("Syntax Error!" + '\n')


if __name__ == "__main__":
    main()