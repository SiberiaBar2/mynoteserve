from datetime import datetime


def model_list(result):
    list_result = []

    for row in result:
        print(row)
        my_dict = {}
        for k, v in row.__dict__.items():
            print(k, v)
            if not k.startswith('_sa'):
                my_dict[k] = v
        print('my_dict', my_dict)
        list_result.append(my_dict)

    return list_result

def model_object(row, is_print = False):
    my_dict = {}
    for k, v in row.__dict__.items():
        print(k, v)
        if not k.startswith('_sa'):
            my_dict[k] = v
    if is_print == True:
        print('my_dict', my_dict)
    return my_dict


def model_to_json(result):
    dict = {}
    for k, v in result.__dict__.items():
        if not k.startswith('_sa'):
            if isinstance(v, datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            dict[k] = v
    return dict