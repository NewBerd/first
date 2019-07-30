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


def read_file(filename1, filename2):
    with open(filename1, 'r', encoding='utf-8') as jobs:
        job_list = eval(jobs.read())
    with open(filename2, 'r', encoding='utf-8') as f:
        resume_txt = f.readlines()
    return job_list, resume_txt


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


def main_han(title_file, info_file):
    global job_list
    personal_experience=[]
    time_unit_job_list=[]

    # work_experience =[]
    # global resume_txt
    # 读入简历文件和任职列表
    # job_list, resume_txt = read_file('D:/JupyterNoteBook/精准简历/Extract_job_infos/title_list.py', filename)
    job_list, resume_txt = read_file(title_file, info_file)
    # print(__file__)
    flag_store = False
    for line in resume_txt:
        if line == '人物 经历 ：\n':
            # (开始使用字典遍历的标志，将职称内容读到job_list中）
            flag_store = True     # (开始使用字典遍历的标志，将职称内容读到job_list中）

        if flag_store:
            personal_experience.append(line)

        if line == '社会 任职 ：\n':
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
    print(main_han('title_list.py', '..\\分词\\方滨兴\\方滨兴_百度百科.txt'))
    print('done')


