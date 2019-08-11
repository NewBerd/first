# -*- coding:utf-8 -*-
import re
job_list = []
personal_experience = []
# work_experience = []  改成放到函数中不会出现检查警告


def process_personal_experience(personal_experience_list):
    work_experience = []
    edu_element = ['人物 经历', '社会 任职', '学位', '出生', '学习', '就读', '博士', '硕士', '本科']
    for exp in personal_experience_list:
        count = 0
        for element in edu_element:
            if element not in exp:
                count += 1
                # print('yes')
        if count == 9:
            work_experience.append(exp)
            # print(work_experience)
    return work_experience


# def read_file(filename1, filename2):
#     with open(filename1, 'r', encoding='utf-8') as jobs:
#         job_list = eval(jobs.read())
#     with open(filename2, 'r', encoding='utf-8') as f:
#         resume_txt = f.readlines()
#     return job_list, resume_txt



def process_work_experience(work_experience_list):
    global job_list
    # with open('title_list.py', 'r', encoding='utf-8') as jobs:
    #     job_list = eval(jobs.read())
    global time_unit_job_list
    time_unit_job_list = []
    for exp in work_experience_list:
        # 获取任职起始时间点
        # print(exp)
        begin_time_pre = re.findall(
            r'(\d*年|\d*年 \d*月|\d*年\d*月|\d*.\d*|\d*|\d*年 起|\d* 起|\d*年 \d*月 \d*日) (—|－|-|——|至|，).*?', exp)
        if begin_time_pre:
            begin_time = begin_time_pre[0][0]
        else:
            begin_time = []
        # print(begin_time)
        # 获取任职终止时间点
        end_time_pre = re.findall(r'.*(—|－|-|——|至) (\d*年 \d*月|\d*年|\d*.\d*|\d*)', exp)
        if end_time_pre:
            end_time = end_time_pre[0][1]
        else:
            end_time = ''
        job_out_list = []  # 该列表必须在循环里面，对每条工作经历文本单独处理
        job_txt1 = re.findall(r'.* (当选|担任|入选|任|任命 为|任命|成立|加入) (.*?) (,|、|，) (.*).*? (。|;|；)', exp)
        job_new_txt1 = []
        if job_txt1:
            for info in job_txt1[0]:
                if info not in ['成立', '加入', '担任', '当选', '入选', '任', '任命', '任命 为', ',', '、', '，', '。', ';', '；']:
                    # print(info)
                    job_new_txt1.append(info)
        # print(job_new_txt1)
        if job_new_txt1:
            for each in job_new_txt1:
                if each not in job_out_list:
                    # print(each)
                    job_out_list.append(each)
        # print(job_txt1)
        job_txt2 = re.findall(r'.* (当选|担任|入选|任|任命 为|任命|成立|加入) (.*?) (,|，|。|;|；)', exp)
        # print(job_txt2)
        job_new_txt2 = []
        if job_txt2:
            for info in job_txt2[0]:
                if info not in ['成立', '加入', '担任', '当选', '入选', '任', '任命', '任命 为', ',', '、', '，', '。', ';', '；']:
                    # print(info)
                    job_new_txt2.append(info)
        if job_new_txt2:
            for each in job_new_txt2:
                if each not in job_out_list:
                    # print(each)
                    job_out_list.append(each)
        job_txt3 = re.findall(r'.* 在 (.*?) 工作 (，|。|;|；) .* 担任(.*?) 。', exp)
        job_new_txt3 = []
        if job_txt3:
            for info in job_txt3[0]:
                if info not in ['成立', '加入', '担任', '当选', '入选', '任', '任命', '任命 为', ',', '、', '，', '。', ';', '；']:
                    # print(info)
                    job_new_txt3.append(info)
        if job_new_txt3:
            for each in job_new_txt3:
                if each not in job_out_list:
                    # print(each)
                    job_out_list.append(each)
        job_txt4 = re.findall(r'.* 加入 (.*?) (，|。|;|；) .* 担任 (.*?) 。', exp)
        job_new_txt4 = []
        if job_txt4:
            for info in job_txt4[0]:
                if info not in ['成立', '加入', '担任', '当选', '入选', '任', '任命', '任命 为', ',', '、', '，', '。', ';', '；']:
                    # print(info)
                    job_new_txt4.append(info)
        if job_new_txt4:
            for each in job_new_txt4:
                if each not in job_out_list:
                    # print(each)
                    job_out_list.append(each)
        # print(job_out_list)

        job_filter2_symbol_list = []
        for one in job_out_list:  # 对每一条任职信息都预处理一遍，过滤检查
            if '、' in one:  # 去除任职文本里的顿号
                job_filter2 = one.split('、')
                # print(job_filter2)
                for one_job in job_filter2:
                    one_job_ = one_job.strip()
                    if one_job_ not in job_filter2_symbol_list:
                        job_filter2_symbol_list.append(one_job_)
            else:
                if one.strip() not in job_filter2_symbol_list:
                    job_filter2_symbol_list.append(one.strip())
            # print(job_filter2_symbol_list)

        job_filter3_number_list = []
        for one_job in job_filter2_symbol_list:
            # 去除任职信息末尾的标注信息如:[7]
            # print(one_job)
            remove_number = re.findall(r'.* (\[ \d* \]).*', one_job)
            # print(remove_number)
            if remove_number:
                job_filter3_num = one_job.replace(remove_number[0], '')
                if job_filter3_num.strip() not in job_filter3_number_list:
                    job_filter3_number_list.append(job_filter3_num.strip())
            else:
                if one_job.strip() not in job_filter3_number_list:
                    job_filter3_number_list.append(one_job.strip())
        # print(job_filter3_number_list)

        job_filter4_years_list = []
        for one_ in job_filter3_number_list:
            # 去除任职信息末尾的任职年份区间，并更新任职时间如（ 2000年 — 2002年 ）
            # print(one_)
            # 更新准确的任职区间
            begin_time_pre = re.findall(
                r'(\d*年|\d*年 \d*月|\d*年\d*月|\d+.\d*|\d*|\d*年 起|\d* 起|\d*年 \d*月 \d*日) (—|－|-|——|至|，).*?', one_)
            if begin_time_pre:
                begin_time = begin_time_pre[0][0]
                # print(begin_time)
            else:
                begin_time_pre = re.findall(
                    r'(\d*年|\d*年 \d*月|\d*年\d*月|\d*.\d*|\d*|\d*年 起|\d* 起|\d*年 \d*月 \d*日) (—|－|-|——|至|，).*?', exp)
                if begin_time_pre:
                    begin_time = begin_time_pre[0][0]
                else:
                    begin_time = ''
            end_time_pre = re.findall(r'.*(—|－|-|——|至) (\d*年 \d*月|\d*年|\d*.\d*|\d*)', one_)
            if end_time_pre:
                end_time = end_time_pre[0][1]
                # print(end_time)
            else:
                end_time_pre = re.findall(r'.*(—|－|-|——|至) (\d*年 \d*月|\d*年|\d*.\d*|\d*)', exp)
                if end_time_pre:
                    end_time = end_time_pre[0][1]
                else:
                    end_time = ''
            remove1 = re.findall(r'.*(\（.*\d*年.* \）).*', one_)
            # print(remove1)
            if remove1:
                job_filter4_years = one_.replace(remove1[0], '')
                if job_filter4_years.strip() not in job_filter4_years_list:
                    # job_filter4_years_list.append(job_filter4_years.strip())
                    info = job_filter4_years.strip()
                else:
                    info = ''

            else:
                if one_ not in job_filter4_years_list:
                    job_filter4_years_list.append(one_.strip())
                    info = one_
                else:
                    info = ''
        # print(job_filter4_years_list)
# 弃用下面的循环，为了将类似‘教授级 高级 工程师（2000年—2002年）、主任（2002年—2006年）’
# 的信息上的任职年份起止时间点和特定的职称逐一对应上
        # for info in job_filter4_years_list:
            # job = []
            # institution = []
            if info:
                units = info.split(' ')
                # print(units)
                if len(units) >= 4:
                    unit_1 = units[-1]
                    unit_2 = units[-2]
                    unit_3 = units[-3]
                    unit_4 = units[-4]
                    unit_21 = unit_2 + ' ' + unit_1
                    unit_321 = unit_3 + ' ' + unit_2 + ' ' + unit_1
                    unit_4321 = unit_4 + ' ' + unit_3 + ' ' + unit_2 + ' ' + unit_1
                    if unit_4321 in job_list:
                        # print('职称_职位：{}'.format(unit_4321))
                        job = unit_4321
                        unit_institution = units[: -4]
                        institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                    elif unit_321 in job_list:
                        # print('职称_职位：{}'.format(unit_1))
                        job = unit_321
                        unit_institution = units[: -3]
                        institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                    elif unit_21 in job_list:
                        # print('职称_职位：{}'.format(unit_1))
                        job = unit_21
                        unit_institution = units[: -2]
                        institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                    else:
                        if unit_1 in job_list:
                            job = unit_1
                            unit_institution = units[: -1]
                            institution = ' '.join(unit_institution)
                        else:
                            job = ''
                            unit_institution = units
                            institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                elif len(units) == 3:
                    unit_1 = units[-1]
                    unit_2 = units[-2]
                    unit_3 = units[-3]
                    # print(unit_1, unit_2, unit_3)
                    unit_21 = unit_2 + ' ' + unit_1
                    unit_321 = unit_3 + ' ' + unit_2 + ' ' + unit_1
                    if unit_321 in job_list:
                        # print('职称_职位：{}'.format(unit_1))
                        job = unit_321
                        institution = ''
                        # print('所在单位_机构：{}'.format(institution))
                    elif unit_21 in job_list:
                        # print('职称_职位：{}'.format(unit_1))
                        job = unit_21
                        unit_institution = units[: -2]
                        institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                    else:
                        if unit_1 in job_list:
                            job = unit_1
                            institution = ''
                        else:
                            job = ''
                            unit_institution = units
                            institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                elif len(units) == 2:
                    unit_1 = units[-1]
                    unit_2 = units[-2]
                    # print(unit_1, unit_2)
                    unit_21 = unit_2 + ' ' + unit_1
                    if unit_21 in job_list:
                        # print('职称_职位：{}'.format(unit_1))
                        job = unit_21
                        institution = ''
                        # print('所在单位_机构：{}'.format(institution))
                    else:
                        if unit_1 in job_list:
                            job = unit_1
                            unit_institution = units[: -1]
                            institution = ' '.join(unit_institution)
                        else:
                            job = ''
                            unit_institution = units
                            institution = ' '.join(unit_institution)
                        # print('所在单位_机构：{}'.format(institution))
                else:
                    unit_1 = units[-1]
                    if unit_1 in job_list:
                        job = unit_1
                        institution = ''
                    else:
                        job = ''
                        unit_institution = units
                        institution = ' '.join(unit_institution)
                # print("{"+"\'起始时间\':\'{}\',\'终止时间\':\'{}\',\'所在单位\':\'{}\',\'职称\':\'{}\'".format(begin_time, end_time, institution, job)+"}")
                time_unit_job = str("{"+"\'起始时间\':\'{}\',\'终止时间\':\'{}\',\'所在单位\':\'{}\',\'职称\':\'{}\'".format(begin_time, end_time, institution, job)+"}")
                time_unit_job_list.append(time_unit_job)
    return time_unit_job_list


def main_han(title_file, resume_txt):
    global job_list
    personal_experience=[]
    time_unit_job_list=[]

    # work_experience =[]
    # global resume_txt
    # 读入简历文件和任职列表
    # job_list, resume_txt = read_file('D:/JupyterNoteBook/精准简历/Extract_job_infos/title_list.py', filename)
    # job_list, resume_txt = read_file(title_file, info_file)
    with open(title_file, 'r', encoding='utf-8') as jobs:
        job_list = eval(jobs.read())
    # print(__file__)
    flag_store = False
    for line in resume_txt:
        if line == '人物 经历\n':
            # (开始使用字典遍历的标志，将职称内容读到job_list中）
            flag_store = True     # (开始使用字典遍历的标志，将职称内容读到job_list中）

        if flag_store:
            personal_experience.append(line)

        if line == '社会 任职\n':
            # (结束字典遍历的标志，表示职称内容已经全部读完到job_list中)
            flag_store = False
    # print(personal_experience)
    # 处理人物经历，获取工作经历
    work_experience = process_personal_experience(personal_experience)
    # 处理工作经历，获取任职多信息列表
    time_unit_job_list = process_work_experience(work_experience)
    # print(time_unit_job_list)
    return personal_experience, time_unit_job_list
    personal_experience=[]
    time_unit_job_list=[]

if __name__ == '__main__':
    print('starting')
    txt = ['基本 信息\n', '中文名 : 方滨兴\n', '外文 名 : BinxingFang\n', '国籍 : 中国\n', '民族 : 汉族\n', '出生地 : 黑龙江省 哈尔滨市\n', '出生日期 : 1960 年 07 月 17 日\n', '职业 : 科研 工作者\n', '毕业 院校 : 哈尔滨工业大学\n', '主要 成就 : 2005 年 当选 为 中国工程院 院士\n', '代表作品 : 《 论 网络 空间主权 》 、 《 在线 社交 网络分析 》\n', '性别 : 男\n', '政治面貌 : 中国共产党 党员\n', '原籍 : 江西省 上饶市 万年县\n', '人物 经历\n', '1960 年 7 月 17 日 ， 方滨 兴出 生于 黑龙江省 哈尔滨市 ， 原籍 江西省 上饶市 万年县 。\n', '1978 年 3 月 ， 方滨兴 进入 哈尔滨工业大学 计算机 与 应用 专业 学习 [ 6 ] 。\n', '1982 年 1 月 ， 方滨兴 从 哈尔滨工业大学 毕业 ， 获得 学士学位 ， 并 考上 清华大学 计算机 组织 与 系统结构 专业 研究生 。\n', '1984 年 10 月 ， 方滨兴 获得 硕士学位 后 回到 哈尔滨工业大学 计算机系 工作 ， 先后 担任 助教 、 讲师 、 副教授 、 教授 （ 1992 年 晋升 ） 、 博士生 导师 （ 1995 年 晋升 ） 。\n', '1986 年 2 月 ， 方滨兴 在 哈尔滨工业大学 就读 在职 博士 研究生 （ 1989 年 9 月 毕业 ） 。\n', '1990 年 4 月 ， 方滨兴 进入 国防科学技术大学 计算机科学 与 技术 博士后 流动站 在职 研究 学习 （ 至 1993 年 10 月 ） ， 师从 计算机 专家 胡守仁 教授 。\n', '1993 年 7 月 ， 方滨兴 担任 哈尔滨工业大学 计算机系 计算机系统 结构 教研室 副 主任 、 主任 （ 至 1997 年 5 月 ） 。\n', '1997 年 6 月 ， 方滨兴 担任 哈尔滨工业大学 计算机 与 电气 工程学院 副 院长 （ 至 1999 年 6 月 ） 。\n', '1998 年 8 月 ， 方滨兴 担任 哈尔滨工业大学 网络 中心 主任 （ 至 1999 年 6 月 ） 。\n', '1999 年 6 月 ， 方滨兴 加入 中国共产党 。 7 月 在 国家 计算机网络 应急 技术 处理 协调 中心 工作 ， 先后 担任 副 总工 （ 1999 年 — 2000 年 ） 、 总工程师 、 副 主任 、 教授级 高级 工程师 （ 2000 年 — 2002 年 ） 、 主任 （ 2002 年 — 2006 年 ） 。\n', '2003 年 4 月 ， 方滨兴 担任 信息产业部 互联网 应急 处理 协调 办公室 主任 （ 至 2008 年 1 月 ） ， 同年 在 中央党校 地厅级 干部 进修班 第 41 期 脱产学习 半年 。\n', '2004 年 ， 方滨兴 入选 “ 新世纪 百千万 人才 工程 国家级 人选 ” 。\n', '2005 年 ， 方滨兴 当选 中国工程院 院士 。\n', '2006 年 ， 方滨兴 被 任命 为 国家 计算机网络 与 信息安全 管理中心 名誉 主任 。\n', '2007 年 12 月 ， 方滨兴 担任 北京邮电大学 校长 （ 至 2013 年 6 月 ） [ 7 ] 。\n', '2013 年 6 月 ， 方滨 兴称 因 身体 原因 ， 不再 连任 北邮 校长 职务 [ 8 ] 。\n', '2014 年 11 月 19 日 ， 方滨兴 在 世界 互联网 大会 做 题为 《 物 联网 搜索 技术 》 的 演讲 [ 9 ] 。\n', '2016 年 3 月 25 日 ， 中国 网络空间 安全 协会 在 北京 举行 成立 大会 ， 方滨兴 当选 为 中国 网络空间 安全 协会 理事长 [ 4 ] 。 8 月 ， 担任 哈尔滨工业大学 （ 深圳 ） 计算机科学 与 技术 学院 教授 、 首席 学术 顾问 [ 10 ] 。\n', '2017 年 7 月 ， 方滨兴 团队 30 多人 整体 加入 广州大学 ， 成立 广州大学 网络空间 先进 技术 研究院 [ 11 ] ， 担任 名誉 院长 。\n', '社会 任职\n', '中国 通信 标准化 协会理事 、 网络 与 信息安全 技术 委员会 （ TC8 ） 主席 ，\n', '专家 咨询 委员会 委员 、 技术 管理 委员会 委员\n', '2002 年 起 信息产业部 通信 科学技术委员会 常务委员\n', '2003 年 起 中国 通信 标准化 协会理事 、 网络 与 信息安全 技术 委员会 （ TC8 ） 主席 ， 专家 咨询 委员会 委员 、 技术 管理 委员会 委员\n', '2003 年 起 财政部 “ 金财 工程 ” 专家 咨询 委员会 委员\n', '2004 年 起 中国 下一代 互联网 示范 工程 （ CNGI ） 项目 专家 委员会 委员\n', '2004 年 起 中国 互联网 协会 副理事长 、 网络 与 信息安全 工作 委员会 主任\n', '2004 年 起 国家 计算机网络 与 信息安全 管理中心 科学技术委员会 主任\n', '2004 年 起 解放军总后勤部 信息化 专家 咨询 委员会 委员\n', '2005 年 起 国家 信息安全 产品认证 管理 委员会 委员\n', '2005 年 起 中国 通信 学会 会士 、 常务理事 、 通信安全 技术 委员会 主任 ， 学术 工作 委员会 委员\n', '2005 年 起 中国 网络通信 集团公司 技术 委员会 委员\n', '2005 年 起 清华大学 计算机系 兼职 教授\n', '2005 年 起 全国人大 信息化 系统 改造 和 建设工程 专家 咨询 顾问 组成员\n', '2005 年 起 国家 863 计划 “ 十一五 ” 信息技术 领域专家 委员会 委员\n', '2006 年 起 哈尔滨工业大学 教授 、 博士生 导师 、 哈尔滨工业大学 国家 计算机 内容 安全 重点 实验室 主任\n', '2006 年 起 国家 信息化 专家 咨询 委员会 委员 ， 网络 与 信息安全 专业 委员会 副 主任\n', '2006 年 起 上海市 互联网 宣传 管理 技术咨询 专家\n', '2006 年 起 北京市 信息化 专家 咨询 委员会 委员\n', '2006 年 起 国家 应急 管理 专家 组成员\n', '2007 年 起 公安部 信息安全 特聘 专家\n', '2007 年 起 “ 新世纪 百千万 人才 工程 国家级 人选 ” 评审 委员会 委员\n', '2007 年 起 北京市 公安交通 管理局 专家 顾问团 成员\n', '2007 年 起 中国科学院 计算所 客座 研究员 、 博士生 导师 、 信息安全 首席 科学家\n', '2007 年 起 国防科学技术大学 特聘 教授 、 博士生 导师\n', '2007 年 起 《 通信 学报 》 委员会 主任\n', '2007 年 起 国家自然科学基金 可信 软件 重大 专项 专家组 副组长\n', '2008 年 起 中国计算机学会 副理事长 、 计算机 安全 专业 委员会 主任 [ 12 ]\n', '2008 年 至 2013 年 中华人民共和国 第十一届 全国人民代表大会 代表 [ 18 ]\n', '2016 年 8 月 哈尔滨工业大学 （ 深圳 ） 计算机 学院 首席 学术 顾问\n', '2016 年 12 月 中国 中文信息 学会 第八届 理事会 理事长 [ 19 ]\n', '中国 电子 信息产业 集团 首席 科学家\n', '信息内容 安全 技术 国家 工程 实验室 主任\n', '可信 分布式计算 与 服务 教育部 重点 实验室 （ 北京邮电大学 ） 主任 [ 14 ]\n', '中国 云 安全 与 新兴 技术 安全 创新 联盟 理事长\n', '教育部 网络空间 安全 学科 评议组 召集人\n', '国家 八六三计划 信息安全 主题 组 专家\n', '国家 发展 改革 委 信息安全 专家 咨询 组成员\n', '主要 成就\n', '科研 综述\n', '方滨兴 的 研究 领域 主要 是 网络 与 信息安全 的 理论 与 技术 ， 侧重点 在于 信息安全 体系 框架 的 研究 、 网络协议 分析 技术 、 IPv6 技术 、 网络 应急 处理 技术 、 系统 灾备 技术 、 入侵 检测 技术 、 honey - net 技术 、 计算机病毒 技术 、 信息 捕获 与 分析 技术 、 高效 文字 匹配 算法 研究 、 网络 健壮性 研究 、 网格 计算 及其 安全 技术 [ 12 ] 。\n', '1989 年 方滨兴 开始 研究 计算机病毒 防御 技术 ， 并于 1992 年 出版 《 计算机病毒 及其 防范 》 专著 ， 20 世纪 90 年代 末 从事 计算机 安全事件 入侵 检测 方面 的 研究 工作 。 1999 年 提出 建设 国家 信息安全 基础设施 的 理念 ， 并 组织 建设 了 相关 系统 ， 为 保障 国家 信息安全 工作 奠定 了 坚实 的 技术 基础 [ 5 ] 。\n', '学术 论著\n', '截至 2017 年 3 月 ， 方滨兴 在 中国 国内外 核心 学术期刊 、 会议 上 发表 论文 400 余篇 ， 出版 著作 3 部 [ 10 ] 。\n', '承担 项目\n', '截至 2017 年 12 月 ， 方滨兴 先后 担任 信息安全 关键技术 “ 973 ” 项目 （ 2007 年 ） 、 社交 网络分析 “ 973 ” 项目 首席 科学家 [ 13 ] 。\n', '科研成果 奖励\n', '截至 2017 年 3 月 ， 方滨兴 作为 第一 完成 人 ， 先后 获得 国家 科技进步 一 、 二等奖 4 项 ， 部级 科技 进步奖 10 余项 ， 省 、 市 青年 科技奖 3 次 [ 10 ] 。\n', '教育 理念\n', '方滨兴 认为 ： 网络空间 安全 人才培养 存在 三个 特殊性 ： 一是 自身 网络安全 的 特殊性 ； 二是 人才 特殊性 ； 三是 网络空间 安全 人才培养 的 特殊性 [ 15 ] 。\n', '指导 学生\n', '截至 2017 年 3 月 ， 方滨兴 先后 培养 硕士 与 博士生 百余名 [ 10 ] 。\n', '中组部 、 中宣部 、 中央 政法委 、\n', '公安部 、 民政部 、 人事部 等 联合\n', '出版日期 - 名称 - 作者 - 出版社 -\n', '2017.09 - 《 论 网络 空间主权 》 - 方滨 兴著 - 北京 ： 科学出版社 -\n', '2014.11 - 《 在线 社交 网络分析 》 - 方滨 兴著 - 北京 ： 电子 工业 出版社 -\n', '2010.12 - 《 网 和 天下 三网 融合 理论 、 实验 与 信息安全 》 - 曾剑秋 ， 方滨兴 编著 - 北京 ： 北京邮电大学 出版社 -\n', '1992.09 - 《 计算机病毒 及其 对策 》 - 方滨兴 等 编著 - 哈尔滨 ： 黑龙江 科学技术 出版社 -\n', '1980 - 《 ECLIPSEMV / 8000 超级 小型机 产品 介绍 》 - 方滨 兴译 - 苏州 电子计算机 厂 情报 厂 -\n', '2007 年 至 2011 年 - 信息安全 理论 及 若干 关键技术 - 国家 973 项目 （ 2007CB311100 ） -\n', '2010 年 至 2012 年 - 非常规 突发事件 中 网络 舆情 作用 机制 与 相关 技术 研究 - 国家自然科学基金 重大 研究 计划 培育 项目 （ 90924029 ） -\n', '2010 年 至 2013 年 - Web 搜索 与 挖掘 的 新 理论 和 新 方法 — 支持 舆情 监控 的 Web 搜索 与 挖掘 的 理论 与 方法 研究 - 国家自然科学基金 重点 研究 计划 项目 （ 60933005 ） -\n', '2008 年 至 2010 年 - 网络 环境 下 特定 信息 获取 与 处理 技术 - 国防科技 创新 团队 项目 -\n', '2009 年 至 2011 年 - 下一代 互联网 舆情 管理系统 应用 示范 - 国家 发改委 CNGI 下一代 互联网 应用 示范 项目 -\n', '2006 年 至 2010 年 - 大规模 网络 入侵 定位 与 容忍 - 总装 预研 项目 [ 14 ] -\n', '1995 年 - 支持 存储器 无 冲突 访问 的 互联网络 开关 门阵列 芯片 的 研制 - 部级 科学 进步 二等奖 ， 第二 -\n', '1995 年 - 多 机系统 的 性能 评价 的 研究 - 部级 科学 进步 二等奖 ， 第二 -\n', '1996 年 - 支持 存储器 无 冲突 访问 的 互连 开关 设计 理论 及 方法 - 部级 科学 进步 三等奖 ， 第一 -\n', '1996 年 - ABC - 90 阵列 计算机 综合 模拟器 - 部级 科学 进步 三等奖 ， 第一 -\n', '2001 年 - 计算机病毒 及其 预防 技术 - 国防 科学技术 三等奖 ， 排名 第一 -\n', '2002 年 - 国家 信息安全 管理系统 - 国家 科学技术 进步 一等奖 ， 排名 第一 -\n', '2002 年 - 大 范围 宽带 网络 动态 处置 系统 - 国防 科学技术 二等奖 ， 排名 第二 -\n', '2004 年 - 大规模 网络 信息 获取 系统 - 国家 科学技术 进步 二等奖 ， 排名 第一 -\n', '2004 年 - 国家 信息安全 展略 研究 - 国家 发展 改革 委 机关 优秀成果 三等奖 -\n', '2005 年 - 搜索引擎 安全 管理系统 - 中国 通信 学会 科学技术 二等奖 ， 排名 第二 -\n', '2007 年 - 国家 通信 数据安全 管理系统 - 国家 科学技术 进步 二等奖 ， 排名 第一 -\n', '2015 年 - 在线 社交 网络分析 关键技术 及 系统 - 国家级 二等奖 -\n', '2018 年 - 大规模 网络安全 态势 分析 关键技术 及 系统 YHSAS - 国家 科学技术 进步奖 二等奖 -\n', '时间 - 荣誉 / 表彰 - 授予 单位 / 组织 -\n', '2001 年 - “ 在 信息产业部 重点 工程 中 做出 突出贡献 特等奖 先进个人 ” 称号 - 信息产业部 -\n', '2001 年 - “ 先进个人 ” 称号 - 中组部 、 中宣部 、 中央 政法委 、 公安部 、 民政部 、 人事部 等 联合 -\n', '2001 年 - 国务院 政府 特殊津贴 专家 - 中华人民共和国国务院 -\n', '2002 年 - 全国 “ 杰出 专业 技术 人才 ” 荣誉称号 - 中组部 、 中宣部 、 人事部 、 科技部 联合 -\n', '2005 年 - 中国工程院 院士 [ 5 ] - 中国工程院 -\n', '2006 年 8 月 - 信息产业 科技 创新 先进 工作者 - 信息产业部 -\n', '2006 年度 - 中国 信息安全 保障 突出 贡献奖 - 《 计算机 世界 》 -\n', '2007 年 - 何梁 何利 基金 科学 与 技术 进步奖 [ 16 ] - 何梁 何利 基金会 -\n', '2014 年 - 中国 互联网 年度人物 特别 贡献奖 [ 17 ] - 人民网 、 新华网 、 中国 网络 电视台 等 -\n', '2018 年 9 月 3 日 ， 为 培养 更 多 优秀 的 网络安全 人才 ， 广州大学 网络空间 先进 技术 研究院 专门 成立 了 以方 滨兴 名字 命名 的 “ 方滨 兴班 ” （ 简称 方班 ） ， 主要 围绕 几个 方向 开展 人才培养 ， 分别 是 网络安全 研究 、 物 联网 及 安全 研究 、 大 数据 及 安全 研究 、 先进 计算技术 研究 [ 21 - 22 ] 。\n', '方滨兴 在 信息安全 理论 及 若干 关键技术 领域 获得 了 卓越 学术 成就 ， 做出 了 重要 贡献 [ 17 ] 。 （ 人民网 评 ）\n', '方滨兴 先后 提出 了 国家 信息安全 基础设施 建设 思想 、 信息安全 属性 可 计算 理论 ， 在 网络 与 信息安全 领域 做出 了 突出贡献 [ 20 ] 。 （ 广州大学 评 ）\n']
    with open("info.txt", "w", encoding="utf-8") as f:
        f.writelines(txt)
    print(main_han('title_list.py', txt))
    print('done')


