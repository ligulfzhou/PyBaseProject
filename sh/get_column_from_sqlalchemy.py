def get_columns(s):
    s = s.split('\n')
    s = list(filter(bool, s))
    s = [i.strip() for i in s]
    s = [i.split('=') for i in s]
    s = [i[0] for i in s]
    s = [i.strip() for i in s]
    return s
