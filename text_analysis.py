#-*-coding:utf8-*-
##############  招聘信息内容文本分词处理，招聘地区、公司类型、学历、工作经验、工资、职位信息词语计数
##############  by k 2019/4/18
import os
import jieba
import re

CURRENT_PATH = os.path.dirname(__file__)


# 分析工作描述中需要的知识点
def knowledge_analyse():
    data_path = CURRENT_PATH + r'/data/process/need.txt'
    store_path = CURRENT_PATH + r'/data/process/need_words.txt'
    dictionary_path = CURRENT_PATH + r'/stop_words.txt'
    # 自定义词典载入
    jieba.load_userdict(dictionary_path)
    # 自定义正则表达式中删去无意义的标点符号以及数字和字母
    no_means = u'[a-zA-Z0-9’!"：；)(#$%&\'（）*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    file_read = open(data_path, 'r', encoding='utf-8')
    file_store = open(store_path, 'w', encoding='utf-8')
    texts = file_read.readlines()
    for text in texts:
        # text = text.split('\t')
        # text = text[7]
        words = jieba.cut(text)
        for word in words:
            word = re.sub(no_means, '', word)
            if word == '':
                continue
            elif word == ' ':
                continue
            elif word == '\n':
                continue
            else:
                word = word + '\n'
                file_store.write(word)
    file_read.close()
    file_store.close()


# 公司类型词语分割
def company(data_path, store_path):
    file_read = open(data_path, 'r', encoding='utf-8')
    file_store = open(store_path, 'w', encoding='utf-8')
    texts = file_read.readlines()
    for text in texts:
        text = text.replace('\n', '')
        datas = text.split('/')
        for data in datas:
            data = data.replace('\ufeff', '').replace('\n', '')
            file_store.write(data+'\n')
    file_read.close()
    file_store.close()


# 词语计数器
def word_count(data_path, store_path):
    # 计数所有词语数目
    file_read = open(data_path, 'r', encoding='utf-8')
    file_store = open(store_path, 'w', encoding='utf-8')
    texts = file_read.readlines()
    words = list(set(texts))    # 去重复后的所有词语
    print(len(words))
    print(len(texts))
    for word in words:
        number = texts.count(word)
        word = word.replace('\n', '')
        write_data = str(word) + '\t' + str(number) + '\n'
        file_store.write(write_data)
    file_read.close()
    file_store.close()


if __name__ == '__main__':
    # # 职位信息词语计数
    # # 分析工作描述中需要的知识点
    # # knowledge_analyse()
    # # 分割词语计数
    # data_path = CURRENT_PATH + r'/data/process/need_words.txt'
    # store_path = CURRENT_PATH + r'/data/process/need_number.txt'
    # word_count(data_path, store_path)

    # # 招聘地区计数
    # data_path = CURRENT_PATH + r'/data/process/area.txt'
    # store_path = CURRENT_PATH + r'/data/process/area_number.txt'
    # word_count(data_path, store_path)

    # # 公司类型计数
    # data_path = CURRENT_PATH + r'/data/process/company_type_original.txt'
    # store_path = CURRENT_PATH + r'/data/process/company_type.txt'
    # company(data_path, store_path)
    # data_path = CURRENT_PATH + r'/data/process/company_type.txt'
    # store_path = CURRENT_PATH + r'/data/process/company_type_number.txt'
    # word_count(data_path, store_path)

    # # 学历计数
    # data_path = CURRENT_PATH + r'/data/process/education.txt'
    # store_path = CURRENT_PATH + r'/data/process/education_number.txt'
    # word_count(data_path, store_path)

    # # 工作经验计数
    # data_path = CURRENT_PATH + r'/data/process/experience.txt'
    # store_path = CURRENT_PATH + r'/data/process/experience_number.txt'
    # word_count(data_path, store_path)

    # 工资计数
    data_path = CURRENT_PATH + r'/data/process/money.txt'
    store_path = CURRENT_PATH + r'/data/process/money_number.txt'
    word_count(data_path, store_path)

