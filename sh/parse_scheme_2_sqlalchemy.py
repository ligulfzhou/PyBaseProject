import sys


def convert_to_sqlalchemy_name(t):
    t = str.upper(t)
    if not t.startswith('TINYINT') and not t.startswith('BIGINT'):
        t = t.replace('INT', 'INTEGER')
    return t


def parse(txt, output='schema.txt'):
    txt = txt.split('\n')
    txt = list(filter(bool, list(map(lambda i: i.strip(), txt))))
    txt_list = [i.split(' ') for i in txt]
    txt_list = [i[:2] for i in txt_list]
    res = []
    for idx, i in enumerate(txt_list):
        a = i[0].replace('`', '')
        b = convert_to_sqlalchemy_name(i[1])
        if not idx:
            b = "Column(" + b + ", primary_key=True)"
        else:
            b = "NotNullColumn(" + b + ")"
        res.append('%s = %s' % (a, b))
    joined = '\n'.join(res)
    print(joined)
    with open(output, 'w') as f:
        f.writelines([joined])


if __name__ == '__main__':
    parse(sys.argv[1])
