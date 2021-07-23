#-*- coding:UTF-8 -*-
import json
import time
import pdfkit

import requests

base_url = 'https://mp.weixin.qq.com/mp/profile_ext'


# 这些信息不能抄我的，要用你自己的才有效
headers = {
    'Connection': 'keep - alive',
    'Accept': '* / *',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030073)',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI5NzA5MDEzNg==&scene=124&uin=MTQzMTY3OTAyNA%3D%3D&key=e996497b9d3f5e80bcbddd81db63fc1ee00930ded07f6393640035fdbf715988126b5d0e73e4a64ab9ccf0a77ae7af8e5aa736396b42e759decd12af028533f9d58b492e2071e6aa3461440d9fbf1804f4df2ce302ba51e3b496ca81e48230231e2c49ec184da6c6b576aea100fc81a1c7addd7e71770e93c17fd5559baf79eb&devicetype=Windows+10+x64&version=63030073&lang=zh_CN&a8scene=7&pass_ticket=lbGf%2BuV1yrvMFdctTw1F2xrr%2BhpGM8jE0PQqxE6xbIN5%2BgcbmUluopaBYqJML60I&fontgear=3',
    'Accept-Encoding': 'br, gzip, deflate'
}

cookies = {
    'devicetype': 'iOS12.2',
    'lang': 'zh_CN',
    'pass_ticket': 'lbGfuV1yrvMFdctTw1F2xrrhpGM8jE0PQqxE6xbIN5gcbmUluopaBYqJML60I',
    'version': '1700042b',
    'wap_sid2': 'CLDg1qoFEooBeV9ITTBDc3YybDd2WkRfZlFxOV9YNHpnOXJZVVlvbng1MVQwVEkxYWR6ellmR01ZeVVLMHhpLVNJT1pnUEtPb0t2QzE4dnFYZWJDX2hHRGh4RkVXYmFVUzhBejRqVTQybHVsemROcUhfNjFNa2ZBUzJLNHV6SlQ4WXNYMkoyMVJDTGkwQVNBQUF+MJbF6IcGOA1AlU4=',
    'wxuin': '3340537333'
}



def get_params(offset):
    params = {
        'action': 'getmsg',
        '__biz': 'MzI5NzA5MDEzNg==',
        'f': 'json',
        'offset': '{}'.format(offset),
        'count': '10',
        'is_ok': '1',
        'scene': '126',
        'uin': '777',
        'key': '777',
        'pass_ticket': 'lbGf+uV1yrvMFdctTw1F2xrr+hpGM8jE0PQqxE6xbIN5+gcbmUluopaBYqJML60I',
        'appmsg_token': '1123_evjsSMODWkDKDXmleBsFBq8tJc6drW-w3rTPmg~~',
        'x5': '0',
        'f': 'json',
    }

    return params


def get_list_data(offset):
    res = requests.get(base_url, headers=headers, params=get_params(offset), cookies=cookies)
    data = json.loads(res.text)
    can_msg_continue = data['can_msg_continue']
    next_offset = data['next_offset']

    general_msg_list = data['general_msg_list']
    list_data = json.loads(general_msg_list)['list']

    for data in list_data:
        try:
            if data['app_msg_ext_info']['copyright_stat'] == 11:
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                content_url = msg_info['content_url']
                # 自己定义存储路径
                #pdfkit.from_url(content_url, '/home/wistbean/wechat_article/'+title+'.pdf')
                print('获取到原创文章：%s ： %s' % (title, content_url))
        except:
            print('不是图文')

    if can_msg_continue == 1:
        time.sleep(1)
        get_list_data(next_offset)


if __name__ == '__main__':
    get_list_data(0)
