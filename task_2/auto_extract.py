 #-*- coding:utf-8 -*-
import os,sys 
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.insert(0,parentdir) 

from bosonnlp import BosonNLP
from jieba import cut
import json
import re
import os
import os.path as op
from Extract_job_infos.Extract_job_infos import main_han
#导入任务一的包
from task_1.baidu import baidu_extract
from task_1.sougou import sougou_extract
from task_1.hudong import hudong_extract
from task_1.bk360 import bk360_extract




# def words_cut(filename, isJieba=True):#分词，返回列表
#     text_cut = []
#
#     if isJieba:
#         with open(filename, 'r', encoding='utf-8') as f:
#             for line in f.readlines():
#                 line = line.strip()#去除空白符
#                 seg_line = cut(line)#返回的是生成器，只可遍历一遍
#                 line_str = " ".join(seg_line) + "\n"
#                 text_cut.append(line_str)
#         return text_cut
#
#     nlp = BosonNLP('QhCMB7FS.33943.0OYvhfw0JCx8')
#     with open(filename, 'r', encoding='utf-8') as f:
#         for line in f.readlines():
#             line_list = nlp.tag(line)[0]['word']#分词，返回一个嵌套的列表格式为[{'word':[分好的词], ''}]
#             line_str = " ".join(line_list)+'\n'#将列表连接为字符串
#             text_cut.append(line_str)
#     return text_cut

def words_cut(txt_lines, isJieba=True):#分词，返回列表
    text_cut = []
    if isJieba:
        for line in txt_lines:
            line = line.strip()#去除空白符
            seg_line = cut(line)#返回的是生成器，只可遍历一遍
            line_str = " ".join(seg_line) + "\n"
            text_cut.append(line_str)
        return text_cut

    nlp = BosonNLP('QhCMB7FS.33943.0OYvhfw0JCx8')
    for line in txt_lines:
        line_list = nlp.tag(line)[0]['word']#分词，返回一个嵌套的列表格式为[{'word':[分好的词], ''}]
        line_str = " ".join(line_list)+'\n'#将列表连接为字符串
        text_cut.append(line_str)
    return text_cut

def read_regex(filename):
    '''读取正则文件，返回一个字典'''
    with open(filename,'r',encoding='utf8') as f:
        dict_str = f.read()
        dict_ = eval(dict_str)
        return dict_

def read_academician(filename):
    lines = []
    with open(filename,'r',encoding='utf-8') as f:
        for line in f.readlines():
            lines.append(line)
    return lines

def traversal(dict_, lines):
    '''遍历一个正则字典，抽取信息
    dict_:正则字典
    lines:待抽取的文本，用列表表示
    dic:字典，用于存储抽取出来的信息
    return: 一个字典，里面是抽出来的信息'''
    dict_result = {}
    for key, value in dict_.items():
        if isinstance(value,dict):#如果值是字典，递归遍历
            dict_result[key] = traversal(value, lines)#将返回的字典存入信息字典中，不破坏原来的结构
        else :#否则是正则表达式，进行抽取
            # print(key,":",value)
            k = 0#记录每条正则抽取出来的信息条数
            for line in lines:#对于每一个正则，遍历院士信息所有行，寻求匹配
                line = line.strip()#去除两端的空白符
                # print(line)
                result = re.findall(value,line)
                      
                if result:#如果匹配到结果
                    result = re.sub(r'\s*','',result[0])#去除空白符
                    k += 1
                    if k == 1:
                        dict_result[key] = result
                    elif k == 2:#如果抽取到多条结果就存到列表当中
                        dict_result[key] = [dict_result[key]]
                        dict_result[key].append(result)
                    else:
                        dict_result[key].append(result)
            if k == 0:#如果没有抽取到任何结果，则置空
                dict_result[key] = ""
    return dict_result

def save_dict(dict,filename):
    with open(filename,'w',encoding='utf-8') as f:
        json.dump(dict,f,ensure_ascii=False)

def save_cut(text_cut, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(text_cut)

def cutdir(path, dirname1, dirname2):
    #获取院士文件夹下所有的文件，进行分词
    text_list = []
    for root, dirs, files in os.walk(path):#默认为广度优先，root为当前目录，
        #dirs为当前目录下的目录，files为当前目录下的文件。
        # print(root,files)
        if files:
            for name in files:
                text_list.append(os.path.join(root, name))
    #对每一个文件进行分词
    for txt in text_list:
        print("cutting the file %s" % (txt))
        dirpath = op.dirname(txt)#获取txt的路径
        dirpath = dirpath.replace(dirname1, dirname2)
        if not op.exists(dirpath):#创建分词文件夹
            os.mkdir(dirpath)
        txtname = op.basename(txt)#获取最底层的名字（文件名）
        save_path = op.join(dirpath, txtname) #替换文件夹，将二者结合成新的路径
        text_cut = words_cut(txt)#分词
        save_cut(text_cut, save_path)#保存
        print("save the cutfile %s" % (save_path))
    print("一共对%s个文件进行了分词。" % (len(text_list)))

def extractdir(path, dirname1, dirname2):
    #获取所有已经分词的文件    
    text_list = []
    for root, dirs, files in os.walk(path):#默认为广度优先
        if files:
            for name in files:
                text_list.append(os.path.join(root, name))
    #读取正则表达式
    filename='regexpression.txt'
    dict_ = read_regex(filename)
    #信息抽取
    for txt in text_list:
        # print(txt)
        print("extracting the file %s" % (txt))
        dirpath = op.dirname(txt)#获取路径
        dirpath = dirpath.replace(dirname1, dirname2)
        # print(dirpath)
        if not op.exists(dirpath):#创建简历文件夹
            os.mkdir(dirpath)
        txtname = op.basename(txt)#获取最底层的名字（文件名）
        save_path = op.join(dirpath, txtname) #将二者结合成新的路径
        lines = read_academician(txt)
        dict_jiben = traversal(dict_, lines)
        work, time = main_han('title_list.py', txt)
        dict_jiben["人物履历"]["工作经历"]["人物经历"] = work
        dict_jiben["人物履历"]["工作经历"]["任职经历"] = time
        save_dict(dict_jiben,save_path)
        print("save the resumefile %s" % (save_path))
    print("一共抽取了%s个文件。" % (len(text_list)))


def main():

    # name = input('请输入要提取的院士姓名：')
    name = "方滨兴"
    # print(name)
    #百度百科
    baidu = baidu_extract(name)#爬取信息
    # print("baidu:\n", baidu)
    baidu = words_cut(baidu)#分词处理
    # print("cut:\n", baidu)
    work, time = main_han('title_list.py', baidu)
    # print(work, time)
    baidu = traversal(read_regex("regexpression.txt"), baidu)#抽取信息
    baidu["人物履历"]["工作经历"]["人物经历"] = work
    baidu["人物履历"]["工作经历"]["任职经历"] = time
    baidu["院士名"] = name
    baidu["百科名"] = "百度百科"
    print("baidu:\n", baidu)
    #搜狗百科
    sougou = sougou_extract(name)#爬取信息
    # print("sougou:\n", sougou)
    sougou = words_cut(sougou)  # 分词处理
    # print("cut:\n", baidu)
    work, time = main_han('title_list.py', sougou)
    # print(work, time)
    sougou = traversal(read_regex("regexpression.txt"), sougou)  # 抽取信息
    sougou["人物履历"]["工作经历"]["人物经历"] = work
    sougou["人物履历"]["工作经历"]["任职经历"] = time
    sougou["院士名"] = name
    sougou["百科名"] = "搜狗百科"
    print("sougou:\n", sougou)
    #互动百科
    hudong = hudong_extract(name)
    hudong = words_cut(hudong)  # 分词处理
    # print("cut:\n", baidu)
    work, time = main_han('title_list.py', hudong)
    hudong = traversal(read_regex("regexpression.txt"), hudong)
    hudong["人物履历"]["工作经历"]["人物经历"] = work
    hudong["人物履历"]["工作经历"]["任职经历"] = time
    hudong["院士名"] = name
    hudong["百科名"] = "互动百科"
    print("hudong:\n", hudong)
    #360百科
    bk360 = bk360_extract(name)
    bk360 = words_cut(bk360)  # 分词处理
    # print("cut:\n", baidu)
    work, time = main_han('title_list.py', bk360)
    bk360 = traversal(read_regex("regexpression.txt"), bk360)
    bk360["人物履历"]["工作经历"]["人物经历"] = work
    bk360["人物履历"]["工作经历"]["任职经历"] = time
    bk360["院士名"] = name
    bk360["百科名"] = "360百科"
    print("360:\n", bk360)
    return (baidu, sougou, hudong, bk360)
    # #获取院士文件夹下所有的文件，进行分词
    # text_list = []
    # for root, dirs, files in os.walk('./院士信息'):#默认为广度优先，root为当前目录，
    #     #dirs为当前目录下的目录，files为当前目录下的文件。
    #     # print(root,files)
    #     if files:
    #         for name in files:
    #             text_list.append(os.path.join(root, name))
    # #对每一个文件进行分词
    # for txt in text_list:
    #     print(txt)
    #     dirpath = op.dirname(txt)#获取txt的路径
    #     dirpath = dirpath.replace('院士信息', '分词')
    #     if not op.exists(dirpath):#创建分词文件夹
    #         os.mkdir(dirpath)
    #     txtname = op.basename(txt)#获取最底层的名字（文件名）
    #     save_path = op.join(dirpath, txtname) #替换文件夹，将二者结合成新的路径
    #     text_cut = words_cut(txt)#分词
    #     save_cut(text_cut, save_path)#保存
    # print("一共对%s个文件进行了分词。" % (len(text_list)))

    # cutdir('./院士信息', '院士信息', '分词')
    # extractdir('./分词', '分词', '简历')

# #   #获取所有已经分词的文件    
#     text_list = []
#     for root, dirs, files in os.walk('./分词'):#默认为广度优先
#         if files:
#             for name in files:
#                 text_list.append(os.path.join(root, name))
#     #读取正则表达式
#     filename='regexpression.txt'
#     dict_ = read_regex(filename)
#     #信息抽取
#     for txt in text_list:
#         print(txt)
#         dirpath = op.dirname(txt)#获取路径
#         dirpath = dirpath.replace('分词', '简历')
#         if not op.exists(dirpath):#创建简历文件夹
#             os.mkdir(dirpath)
#         txtname = op.basename(txt)#获取最底层的名字（文件名）
#         save_path = op.join(dirpath, txtname) #将二者结合成新的路径
#         lines = read_academician(txt)
#         dict_jiben = traversal(dict_, lines)
#         work, time = main_han('title_list.py', txt)
#         dict_jiben["人物履历"]["工作经历"]["人物经历"] = work
#         dict_jiben["人物履历"]["工作经历"]["任职经历"] = time
#         save_dict(dict_jiben,save_path)
#     print("一共抽取了%s个文件。" % (len(text_list)))

if __name__ == '__main__':
    main()
