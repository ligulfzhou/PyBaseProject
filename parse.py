from tornado.options import options, define
define('debug', default=True, help='enable debug mode')
options.parse_command_line()

from control import ctrl


def parse_url(i):
    if '](' not in i:
        return '', ''

    if ')' in i:
        i = i.split(')')[0]
    if '[' in i:
        i = i.split('[')[1]
    try:
        name, url = list(filter(bool, i.split('](')))
        return name, url
    except:
        print(i)
        return '', ''

def parse(item):
    print("=====item======")
    print(item)
    items = list(filter(bool, item.split('|')))
    if len(items) != 5:
        print(item)
        return

    cname, curl = parse_url(items[1])
    company = {
        'city': items[0],
        'name': cname,
        'url': curl,
        'dt': items[2],
        'tt': items[3],
        'tp': 0
    }
    c = ctrl.api.add_model('Company', company)
    print(c)

    refs = []
    for i in list(filter(bool, items[4].split('['))):
        t, url = parse_url(i)
        if not t or not url:
            print("===============error item===========")
            print(i)
            continue
        refs.append({
            'title': t,
            'company_id': c['id'],
            'url': url
        })
    if refs:
        refs = ctrl.api.add_models('Ref', refs)
    print(refs)

def load_items():
    with open('./data/996.txt') as f:
        items = f.read()

    items = list(filter(bool, items.split('\n')))
    [parse(item) for item in items]

if __name__ == '__main__':
    # testitem = '|上海|[上海联影医疗科技有限公司](https://www.united-imaging.com/cn/home/)|2019年4月4日|996、无加班费|[看准网](https://www.kanzhun.com/pl6045694.html)、 [CSDN](https://bbs.csdn.net/topics/380214818)、[看准网](https://www.kanzhun.com/pl6212987.html)|'
    # parse(testitem)
    load_items()

