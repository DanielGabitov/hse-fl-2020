import ply.lex as lex

tokens = [
    'ID',
    'PLUS',
    'MULT',
    'LBR',
    'RBR',
    'DOT',
    'EQ'
]

t_ID      = r'[A-Za-z_0-9]+'
t_PLUS    = r'\;'
t_MULT    = r'\,'
t_DOT     = r'\.'
t_LBR     = r'\('
t_RBR     = r'\)'
t_EQ      = r':-'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    raise IOError("Illegal character!")

lexer = lex.lex()