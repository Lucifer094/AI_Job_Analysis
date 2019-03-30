#-*-coding:utf8-*-
##############  普通爬取51job网页招聘信息
##############  by k 2019/3/30
import requests
from lxml import etree


# 简单破解反爬虫机制，使用headers模拟浏览器
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/73.0.3683.86 Safari/537.36'
}


# 得到指定搜索页面上所有的链接信息，以供搜索招聘的具体信息
def get_link(key_word, page):
    url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,' + key_word + ',2,' + str(page) + '.html'
    html = requests.get(url, headers=headers)
    html_xpath = etree.HTML(html.text)  # 获取网页中的所有信息并转化成xpath
    link_all = html_xpath.xpath('//*[@id="resultList"]/div/p/span/a/@href')
    return link_all


# 将无关的符号进行替换删除
def filter(data):
    result = data.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
    return result


# 获取链接中的有用信息并储存
def get_data(link, file_store):
    html = requests.get(link, headers=headers)
    html_xpath = etree.HTML(html.text)  # 获取网页中的所有信息并转化成xpath
    try:
        company = html_xpath.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[1]/a[1]/@title')
        company_type = html_xpath.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[3]/@title')
        work_place = html_xpath.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')[0]
        work_place = filter(work_place)
        job_name = html_xpath.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/h1/@title')
        job_description = html_xpath.xpath('/html/body/div[3]/div[2]/div[3]/div[1]')[0]
        job_description = job_description.xpath('string(.)')
        job_description = filter(job_description)
        try:
            item = str(company[0])+'\t'+str(company_type[0])+'\t'+str(work_place)+'\t'+str(job_name[0]) +\
                   '\t'+str(job_description)+'\n'
            file_store.write(item)
        except Exception as e:
            print(e)
            return None
    except:
        print('{}链接页面搜索出错'.format(link))


if __name__ == '__main__':
    store_path = '51job.txt'  # 存储位置
    file_store = open(store_path, 'w', encoding='utf-8')    # 结果存储文件
    page_all = 100
    key_word = "人工智能"   # 搜索设定关键字和页数
    for page in range(1, page_all):
        print('正在爬取第{}页链接信息'.format(page))
        try:
            link_all = get_link(key_word, page)
            for link in link_all:
                get_data(link, file_store)
        except:
            print('第{}页链接信息爬取失败'.format(page))
            continue
    file_store.close()
