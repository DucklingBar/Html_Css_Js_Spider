# -*- coding:utf-8 -*-
# Author: Geekerichan
# @Time :2024-12-16
import re
import requests
import os

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    response = requests.get(url, timeout=10, headers=headers)
    response.encoding = 'utf8'
    return response.text

def get_pic(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    pic_response = requests.get(url, timeout=10, headers=headers)
    return pic_response.content

def save_file(chdir_path, filename, content):
    file_path = os.path.join(chdir_path, filename)
    if filename[-4:] in ['.jpg', '.png', 'webp', '.jpeg', '.gif', '.bmp']:
        with open(file_path, "wb") as f:
            f.write(content)
            print('写入{}成功'.format(filename))
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            print('写入{}成功'.format(filename))

def scarpy_web(url, web_name):
    local_path = os.getcwd()
    if not os.path.exists(web_name):
        os.makedirs(os.path.join(web_name, 'images'))
        os.makedirs(os.path.join(web_name, 'css'))
        os.makedirs(os.path.join(web_name, 'js'))

    content = get_html(url)
    filename = web_name + '.html'
    chdir_path = os.path.join(local_path, web_name)

    save_file(chdir_path, filename, content)

    # save css file
    patterns = ['<link href="(.*?)"', '<link rel="stylesheet" href="(.*?)"', '<link type="text/css" rel="stylesheet" href="(.*?)"']
    for pattern in patterns:
        result = re.compile(pattern, re.S).findall(content)
        for link in result:
            if link.startswith('http'):
                css_url = link
            else:
                css_url = url + '/' + link.lstrip('/')
            try:
                response = get_html(css_url)
                css_filename = re.search('.*/(.*?).css', link).group(1) + '.css'
                save_file(chdir_path, 'css/' + css_filename, response)
            except Exception as e:
                print('css文件下载失败，原因:', e)

    # save js file
    patterns = ['<script src="(.*?)"', '<script type="text/javascript" src="(.*?)"']
    for pattern in patterns:
        list = re.compile(pattern, re.S).findall(content)
        for i in list:
            if i.startswith('http'):
                js_url = i
            else:
                js_url = url + '/' + i.lstrip('/')
            try:
                response = get_html(js_url)
                js_filename = re.search('.*/(.*?).js', i).group(1) + '.js'
                save_file(chdir_path, 'js/' + js_filename, response)
            except Exception as e:
                print('js文件下载失败，原因:', e)

    # save pic file
    patterns = ['<img src="(.*?)"', '<img.*?src="(.*?)"']
    for pattern in patterns:
        pic_list = re.compile(pattern, re.S).findall(content)
        for i in pic_list:
            if i.startswith('http'):
                pic_url = i
            else:
                pic_url = url + '/' + i.lstrip('/')
            try:
                pic = get_pic(pic_url)
                pic_filename = re.search('.*/(.*?).(jpg|webp|png|jpeg|gif|bmp)', i).group(1) + '.' + re.search('.*/(.*?).(jpg|webp|png|jpeg|gif|bmp)', i).group(2)
                save_file(chdir_path, 'images/' + pic_filename, pic)
            except Exception as e:
                print('图片下载失败，原因:', e)

if __name__ == '__main__':
    url = input('输入你想要爬取的网页:')
    web_name = input('输入匹配的页面title:')
    scarpy_web(url=url, web_name=web_name)