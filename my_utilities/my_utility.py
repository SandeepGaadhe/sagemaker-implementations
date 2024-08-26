def print_all_variables2():
    # not working
    print('insdie print_all_variables')
    variables_dict = {key: value for key, value in globals().items() if not key.startswith('__') \
                                                                      and not callable(value) \
                                                                      and not key.startswith('_')
                     }
    return variables_dict
    # for key, value in sorted(variables_dict.items()):
    #     if key.startswith('_'):
    #         continue
    #     if isinstance(value, str):
    #         print(f'{key} : {value}')
    #     else:
    #         print(f'{key} : {type(value)}')