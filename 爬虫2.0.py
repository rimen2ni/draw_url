import requests
import threading
from queue import Queue
from lxml import etree


link_queue = Queue()
DOWNLOADNUM = 50
#get 网页的函数
def feach(url):
    r = requests.get(url)
    return r.text.replace('\t','')

#解析每所大学地址
def prase (html):
    global link_queue
    sele = etree.HTML(html)
    links = sele.xpath('//*[@id="content"]/table/tbody/tr/td[2]/a/@href')
    for link in links:
        if not link.startswith('http://'):
            link = 'http://qianmu.iguye.com/%s' % link
        link_queue.put(link)

#解析爬虫每所大学的详细信息
def prrase_new(html):
    sele = etree.HTML(html)
    tables = sele.xpath('//*[@id="wikiContent"]/div[1]/table/tbody')
    #如果 tables为Flase则返回
    if  not tables:
        return
    tables = tables[0]
    keys = tables.xpath('./tr/td[1]//text()')
    values = tables.xpath('./tr/td[2]')
    #join 把文字中存在空格的链接起来
    value = [''.join(value.xpath('.//text()')) for value in values]
    info = dict(zip(keys, value))
    print(info)


def download():
    while True:
        link = link_queue.get()
        if link ==None:
            break
        print(link)
        prrase_new(feach(link))
        link_queue.task_done()
        print('剩下%s任务'%link_queue.qsize())




if __name__ == '__main__':
    url = 'http://qianmu.iguye.com/2018USNEWS%E4%B8%96%E7%95%8C%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D'
    prase(feach(url))
    for i in range(DOWNLOADNUM):
        t = threading.Thread(target=download)
        t.start()
    link_queue.join()
    for i in range(DOWNLOADNUM):
        link_queue.put(None)



