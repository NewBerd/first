# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
from bosonnlp import BosonNLP


input_txt = open('杨小牛_搜狗百科.txt', 'r', encoding='utf-8')
# 有的文件编码使用GBK形式，在读文件时需要再添加一个参数：encoding='utf-8'
# 有的记事本文件编码使用ANSI,读文件添加encoding='utf-8'反而会报错


lines = input_txt.readlines()
for line in lines:
    nlp = BosonNLP('QhCMB7FS.33943.0OYvhfw0JCx8')
    result = nlp.tag(line)[0]['word']
    output_txt = open('杨小牛_搜狗百科_split_unattributed.txt', mode='a', encoding='utf-8')
    output_txt.write('{}\n'.format(result))
    # output_txt.write('{}\n'.format(' '.join(result)))
    output_txt.close()





# # 注意：在测试时请更换为您的API token。
# nlp = BosonNLP('QhCMB7FS.33943.0OYvhfw0JCx8')
# s = '游戏很喜欢，希望赶紧过了无法打开家园这一块，要不买之前给哥提醒也可以，买完之后告诉玩家进不去要等审核有一点小生气。'
# result = nlp.tag(s)[0]['word']
# print(' '.join(result))
# print(result)

# 注意：在测试时请更换为您的API token。
# nlp = BosonNLP('QhCMB7FS.33943.0OYvhfw0JCx8')
#
# s = ['亚投行意向创始成员国确定为57个', '“流量贵”频被吐槽']
#
# result = nlp.tag(s)
#
# for d in result:
    # d 是一个字典，字典中的键是字符串，字典里的值是字符串组成的列表
    # print(d)
    # print(d['word'])
    # print(d['tag'])
    # c = zip(d['word'], d['tag'])
    # e = list(c)
    # print(e)
    # print(' '.join(['%s/%s' % it for it in zip(d['word'], d['tag'])]))
    # zip()函数将两个列表






