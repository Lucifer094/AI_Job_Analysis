# -*- coding:utf-8 -*-
import urllib
import re,codecs
import time,random
import requests
from lxml import html
from urllib import parse

# 整个爬虫所需的headers
headers={'Host':'search.51job.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}


# 得到搜索指定页面上的所有链接
def get_link(key, page):
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,' + key + ',2,' + str(page) + '.html'
    r = requests.get(url, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r.encoding = 'gbk'
    reg = re.compile(r'class="t1 ">.*? <a target="_blank" title=".*?" href="(.*?)".*? <span class="t2">', re.S)
    link_all = re.findall(reg, r.text)
    return link_all


# 删去句子中不需要的信息
def delete_useless(sentence):
    sentence = str(sentence).replace(' ', '')
    sentence = str(sentence).replace('\t', '').replace(r'\t', '')
    sentence = str(sentence).replace('\r', '').replace(r'\r', '')
    sentence = str(sentence).replace('\n', '').replace(r'\n', '')
    sentence = str(sentence).replace(r'&nbsp', '').replace(r'&amphellip', '')
    sentence = str(sentence).replace(r"'", "").replace(r';', '').replace(r"'", "")
    sentence = str(sentence).replace(r'(', '').replace(r')', '')
    sentence = str(sentence).replace(r'<p>', '').replace(r'</p>', '')
    sentence = str(sentence).replace(r'<P>', '').replace(r'</P>', '')
    sentence = str(sentence).replace(r'<b>', '').replace(r'</b>', '')
    sentence = str(sentence).replace(r'<div>', '').replace(r'</div>', '')
    sentence = str(sentence).replace(r'<strong>', '').replace(r'</strong>', '')
    sentence = str(sentence).replace(r'<ol>', '').replace(r'</ol>', '')
    sentence = str(sentence).replace(r'<li>', '').replace(r'</li>', '')
    sentence = str(sentence).replace(r'<ul>', '').replace(r'</ul>', '')
    sentence = str(sentence).replace(r'<br>', '')
    sentence = str(sentence).replace(r'<span>', '').replace(r'</span>', '')
    sentence = str(sentence).replace(r'<SPAN>', '').replace(r'</SPAN>', '')
    sentence = str(sentence).replace(r'[', '').replace(r']', '')
    sentence = str(sentence).replace(' ', '')
    if sentence == '':
        sentence = '无'
    return sentence


# 页面上搜索有用信息并存储
def get_data(link, file):
    r1 = requests.get(link, headers, timeout=10)
    s = requests.session()
    s.keep_alive = False
    r1.encoding = 'gbk'
    t1 = html.fromstring(r1.text)
    try:
        # 搜索需要的部分信息
        company = t1.xpath('//p[@class="cname"]/a/text()')[0]
        job = t1.xpath('//div[@class="tHeader tHjob"]//h1/text()')[0]
        education = t1.xpath('//p[@class="msg ltype"]/text()')[2]
        boon = t1.xpath('//div[@class="t1"]//span/text()')
        salary = t1.xpath('//div[@class="tHeader tHjob"]//strong/text()')[0]
        # companytype = t1.xpath('//p[@class="msg ltype"]/text()')[3]
        # workyear = t1.xpath('//p[@class="msg ltype"]/text()')[1]
        area = t1.xpath('//p[@class="msg ltype"]/text()')[0]
        describe = re.findall(re.compile(r'<div class="bmsg job_msg inbox">(.*?)'
                                         r'(职责要求|职位要求|任职要求|职位要求|岗位要求|任职资格|任职条件|能力要求)', re.S), r1.text)
        require = re.findall(re.compile(r'<div class="bmsg job_msg inbox">.*?'
                                        r'(职责要求|职位要求|任职要求|职位要求|岗位要求|任职资格|任职条件|能力要求)'
                                        r'(.*?)<div class="mt10">', re.S), r1.text)

        # 删去句子中不需要的信息
        company = delete_useless(str(company))
        job = delete_useless(str(job))
        education = delete_useless(str(education))
        boon = delete_useless(str(boon))
        salary = delete_useless(str(salary))
        area = delete_useless(str(area))
        describe = delete_useless(str(describe))
        require = delete_useless(str(require))

        # 存储筛选结果
        print(company)
        try:
            item = company + '\t' + job + '\t' + education + '\t' + boon + '\t' + salary + '\t' + area + '\t' + describe\
                + '\t' + require + '\t' + link + '\n'
            file.write(item)
        except Exception as e:
            print(e)
            return None
    except:
        print('页面搜索出错！')


if __name__ == '__main__':
    # 数据存储位置
    store_path = '51job.txt'
    file = open(store_path, 'w', encoding='utf-8')

    # 搜索关键字
    key = '人工智能'
    key = parse.quote(parse.quote(key))
    for page in range(1, 100):
        print('正在爬取第{}页信息'.format(page))
        try:
            link_all = get_link(key, page)
            for link in link_all:
                get_data(link, file)
        except:
            continue
            print('搜索页面爬取出现问题！')

    file.close()
