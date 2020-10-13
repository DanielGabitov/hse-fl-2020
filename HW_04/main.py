import sys
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

t_ID      = r'[A-Za-z_]+'
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
    t.lexer.skip(1)
    raise IOError('Error at postion: (' + str(t.lexpos) + ') line: (' + str(t.lineno) + ') - Illegal character.')

## Lexer ##

def check_if_illegal_character(data, cur):
    return isinstance(data[cur][0], str)

def check_length(data, cur):
    if (cur < len(data)):
        return True
    return False

def parse_type(data, cur, type_):
    if check_if_illegal_character(data, cur) or not check_length(data, cur):
        return [cur, False] 

    if data[cur][0].type == type_:
        data[cur][1] = True
        return [cur + 1, data[cur][0].type == type_] 

    return [cur, data[cur][0].type == type_]  


def parse_PLUS(data, cur):
    return parse_type(data, cur, 'PLUS')

def parse_MULT(data, cur):
    return parse_type(data, cur, 'MULT')

def parse_P(data, cur):

    if parse_type(data, cur, 'ID')[1]:
        return parse_type(data, cur, 'ID')

    while True:

        if not parse_type(data, cur, 'LBR')[1]:
            break
        cur_tmp = parse_type(data, cur, 'LBR')[0]

        if not parse_EXP(data, cur_tmp)[1]:
            break
        cur_tmp = parse_EXP(data, cur_tmp)[0]

        if not parse_type(data, cur_tmp, 'RBR')[1]:
            break
        cur_tmp = parse_type(data, cur_tmp, 'RBR')[0]

        return [cur_tmp, True]

    return [cur, False]

def parse_M(data, cur):
    return parse_bracets(parse_P, parse_MULT, data, cur)

def parse_bracets(parse_item, parse_sep, data, cur):

    while True:

        if not parse_item(data, cur)[1]:
            break
        cur_tmp = parse_item(data, cur)[0]

        if not parse_sep(data, cur_tmp)[1]:
            break
        cur_tmp = parse_sep(data, cur_tmp)[0]

        if not parse_bracets(parse_item, parse_sep, data, cur_tmp)[1]:
            break
        cur_tmp = parse_bracets(parse_item, parse_sep, data, cur_tmp)[0]

        return [cur_tmp, True]

    while True:

        if not parse_item(data, cur)[1]:
            break
        cur_tmp = parse_item(data, cur)[0]

        return [cur_tmp, True]

    return [cur, False]




def parse_EXP(data, cur):
    return parse_bracets(parse_M, parse_PLUS, data, cur)

def parse_expression(data, cur):

    while True:

        if not parse_type(data, cur, 'ID')[1]:
            break
        cur_tmp = parse_type(data, cur, 'ID')[0]

        if not parse_type(data, cur_tmp, 'EQ')[1]:
            break
        cur_tmp = parse_type(data, cur_tmp, 'EQ')[0]

        if not parse_EXP(data, cur_tmp)[1]:
            break
        cur_tmp = parse_EXP(data, cur_tmp)[0]

        if not parse_type(data, cur_tmp, 'DOT')[1]:
            break
        cur_tmp = parse_type(data, cur_tmp, 'DOT')[0]

        return [cur_tmp, True]

    while True:

        if not parse_type(data, cur, 'ID')[1]:
            break
        cur_tmp = parse_type(data, cur, 'ID')[0]

        if not parse_type(data, cur_tmp, 'DOT')[1]:
            break
        cur_tmp = parse_type(data, cur_tmp, 'DOT')[0]

        return [cur_tmp, True]

    return [cur, False]

def parse_word(data):
    if parse_expression(data, 0)[1]:
        return "Correct Syntax!"
    else:
        iterator = 0
        if not data[iterator][1]:
            return get_error_line(data[iterator][0])
        while data[iterator][1]:
            iterator += 1
        return get_error_line(data[iterator][0])

def get_error_line(data):
    if isinstance(data, str):
        return data
    return "Error at postion: (" + str(data.lexpos) + ") line: (" + str(data.lineno) + ") - Syntax Error." 

def parse(data):
    word = []
    for elem in data:
        word.append([elem, False])
    return parse_word(word)

def main():
    # name = sys.argv[1]
    # !!!!!!!!!!!!!!!! DONT FORGET!!!!!!!!!!!!!!!!!!! 
    name = 'test.txt'
    f = open(name)
    output_name = (name).split('.')
    f_out = open(output_name[0] + '.out', 'w')
    data = str(f.read())

    lexer.input(data)
    toks = []
    while True:
        try:
            token = lexer.token()
            if not token:
                break
            toks.append(token)
        except IOError as exception:
            toks.append(str(exception))
            continue

    word = []
    for elem in toks:
        word.append(elem)
        if isinstance(elem, str):
            continue
        elif elem.type == 'DOT':
            f_out.write(str(parse(word) + '\n'))
            word.clear()

    if word:
        f_out.write(str(parse(word)) + '\n')

if __name__ == "__main__":
    lexer = lex.lex()
    main()