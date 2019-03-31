#-*-coding:utf8-*-
##############  将爬取信息进行处理，处理为可以进行分析的数据
##############  by k 2019/3/31
import re
import spider_web


# 简单的数据处理，公司性质间用/分割并且删除括号内的东西，工作地址统一到市
def change(line):
    line = line.split('\t')

    for i in range(0,len(line)):
        line[i] = spider_web.filter(line[i])

    company = line[0]
    company_type = line[1]
    work_place = line[2]
    salary = line[3]
    job_name = line[4]
    job_description = line[5]

    company_type = company_type.replace(',', '/')
    company_type = re.sub('\(.*?\)', '', company_type)
    work_place = work_place.split('-')[0]

    line_process = company+'\t'+company_type+'\t'+work_place+'\t'+salary+'\t'+job_name + '\t'+job_description+'\n'
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
