import requests
from bs4 import BeautifulSoup
import re

def query_class(HSCode):
    # 发起网络请求获取网页内容
    url = f'https://hsciq.com/HSCN/Code/{HSCode}'
    response = requests.get(url)
    html_code = response.content

    # 解析HTML代码
    soup = BeautifulSoup(html_code, 'html.parser')

    # 提取信息
    rows = soup.find_all('tr')
    result = []
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 2:
            code = tds[0].text.strip()
            description = tds[1].text.strip()
            result.append((code, description))

    # 输出递进式信息
    progressive_info = '->'.join([f'{code} {description}' for code, description in result])
    # print(progressive_info)
    filtered_info = re.findall(r'(第\d+章[\s\S]*)', progressive_info)[0]

    return(filtered_info)

