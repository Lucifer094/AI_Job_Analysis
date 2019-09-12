#-*-coding:utf8-*-
##############  将爬取信息进行处理，处理为可以进行分析的数据
##############  by k 2019/4/2
import re
import spider_web

mounth_int = {'天': 365, '月': 12, '年': 1}
money_int = {'万': 10000, '千': 1000, '百': 100, '十': 10, '元': 1}


# 工资统一为元/年
def str2int(salary):
    try:
        salary = salary.split('/')
        month_num = mounth_int.get(salary[1])   # 提取月份数量
        money_num = money_int.get(salary[0][len(salary[0])-1])  # 提取单位
        salary[0] = salary[0][:-1]
        salary = salary[0].split('-')
        base_num = 0    # 工资的数目
        for num in salary:
            base_num = base_num + float(num)
        base_num = base_num / len(salary)   # 求平均值
        salary = base_num * money_num * month_num
        salary = int(salary)
    except:
        return None
    return salary


# 简单的数据处理，公司性质间用/分割并且删除括号内的东西，工作地址统一到市，工资统一为元/年
def change(line):
    line = line.split('\t')

    for i in range(0,len(line)):
        line[i] = spider_web.filter(line[i])

    company = line[0]
    company_type = line[1]
    work_place = line[2]
    work_experience = line[3]
    education = line[4]
    salary = line[5]
    job_name = line[6]
    job_description = line[7]

    company_type = company_type.replace(',', '/')
    company_type = re.sub('\(.*?\)', '', company_type)  # 公司性质间用/分割并且删除括号内的东西
    work_place = work_place.split('-')[0]   # 工作地址统一到市
    try:
        salary = str(str2int(salary))
    except:
        return None

    line_process = company+'\t'+company_type+'\t'+work_place+'\t'+work_experience +\
                   '\t'+education+'\t'+salary+'\t'+job_name + '\t'+job_description+'\n'
    return line_process


if __name__ == '__main__':
    data_path = 'data/original/51job.txt'
    store_path = 'data/process/51job.txt'
    file_read = open(data_path, 'r', encoding='utf-8')
    file_write = open(store_path, 'w', encoding='utf-8')
    for line in file_read:
        line_process = change(line)
        file_write.write(line_process)
    file_read.close()
    file_write.close()
