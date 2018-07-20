import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        # 时间和log内容分开, 并且加上分隔符号
        print('***************\n[ {} ]'.format(formatted))
        print(*args, **kwargs)
        print('***************')
        # print(formatted, file=f)
        # print(*args, file=f, **kwargs)
        # print('***************', file=f, )
