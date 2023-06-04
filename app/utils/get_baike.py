# -*- coding: utf-8 -*-
# FileName: 爬取百度百科.py
# Time : 2023/5/4 22:13
# Author: zzy
from lxml import etree

import requests


def get_baike(keyword):
    url = rf'https://baike.baidu.com/item/{keyword}?fromModule=lemma_search-box'

    resp = requests.get(url)

    html = resp.text
    selector = etree.HTML(html)

    para_element = selector.xpath("//div[@class='para MARK_MODULE'][1]")
    if para_element:
        # 找到第一个符合条件的 div 元素，并将其中的所有文本拼接在一起
        text_list = para_element[0].xpath(".//text()")
        text = "".join(text_list)
        return text
    else:
        return "未找到"


if __name__ == '__main__':
    print(get_baike('番茄叶斑病'))
