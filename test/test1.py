args = {
    'q': 'title:美丽+year:2013+type:纪录片',
    'sort': 'title',
    'order': 'asc',
}


def format_query_args(args):
    query = {}
    if 'q' in args.keys():
        list_q = args['q'].split('+')
        dict_q = {}
        for l in list_q:
            item = l.split(':')
            dict_q[item[0]] = item[1]

        query['search'] = dict_q

    if 'sort' in args.keys():
        query['sort'] = args['sort']

    if 'order' in args.keys():
        query['order'] = args['order'] == 'asc' and 1 or -1

    return query


print(format_query_args(args))
