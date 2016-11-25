# -*- coding: utf-8 -*-
"""
Created on Sat Jan 02 09:39:55 2016
Python 2.7
@description: download papers in arxiv (CV/CG/CL)
@author: chongyang
"""

import requests
from lxml import etree
import os

# proxies = {
#    'http': 'socks5://user:pass@host:port',
#    'https': 'socks5://user:pass@host:port'
# }



def getHtml(url):
    html = requests.get(url).content
    selector = etree.HTML(html)
    return selector


def getContent(htm, xpathStr):
    selector = htm
    content = selector.xpath(xpathStr) 
    return content


# download images of each group
def getDownPdf(cons, title, folder, save_path):
    fn = '%s' % title
    # pa = os.path.dirname(__file__) + '/' + 'arxiv' + '/%s' % folder
    pa = os.path.abspath(os.path.join(save_path, folder))
    print("path:", pa)
    # check and create folder
    if not os.path.exists(pa):
        os.mkdir(pa)
    fl = (pa + '\%s.pdf' % fn.rstrip())
    print fl

    '''
    r = requests.get(cons)
    with open(fl, "wb") as code:
        print(len(r.content))
        code.write(r.content)


    r = requests.get(cons, stream=True)
    with open(fl, 'wb') as f:
        for chunk in r.iter_content(chunk_size=512 * 1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush()
    '''
	r = requests.get(cons, stream=True, timeout=None)
    # r = requests.get(cons, stream=True, proxies=proxies, timeout=None)  # with proxies
    f = open(fl, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    f.close()


if __name__ == '__main__':
    save_path = 'E://nlp//Paper-arxiv'
    # CV,CG,CL
    url = ['http://arxiv.org/list/cs.CV/recent',
            'http://arxiv.org/list/cs.GR/recent',
            'https://arxiv.org/list/cs.CL/recent',
            'https://arxiv.org/list/cs.CL/pastweek?show=1000']  # download all CL papers from last week


    htm = getHtml(url[3])
    xp_date = '//*[@id="dlpage"]/h3/text()'  
    cons_date = getContent(htm, xp_date) 
    print(cons_date)
    for n in range(0,len(cons_date)):
        xp1 = '//dl[' + str(n+1) + ']//*[@class="list-identifier"]//a[2]//@href' 
        xp2 = '//dl[' + str(n+1) + ']//*[@class="list-title mathjax"]/text()'

        cons1 = getContent(htm, xp1)  # get pdfs' href
        cons2 = getContent(htm, xp2)  # get papers' title
        print(cons1, cons2, cons_date[n])

        folder = cons_date[n].split(', ') 
        # judge the path exists or not
        if os.path.exists(save_path + '/' + 'arxiv' + '/%s' % folder[1]):
            print folder[1] + '  is  exist!'

        print folder[1] + ': having %s' % len(cons1) + '  files'
        print 'pdfs are downloading...'
        for indx in range(0, len(cons1)):
            href = 'http://arxiv.org' + cons1[indx]
            # print href
            title = cons2[2 * indx + 1]
            title = title.replace(':', ' ')
            title = title.replace('?', ' ')
            print '%s.' % (1 + indx) + ' ' + href + ' ' + title
            # print folder[1]
            getDownPdf(href, title, str(folder[1]).replace(' ', '_'), save_path)
