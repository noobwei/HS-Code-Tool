import requests
from bs4 import BeautifulSoup
import pandas as pd
from hs2class import query_class
# 定义查询函数
def query_hs_code(item_name):
    # 构建查询URL
    url = f"https://www.hsbianma.com/Search?keywords={item_name}"
    hs_codes = []  # 用于存放所有匹配的HS编码

    try:
        # 发送HTTP GET请求
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找查询结果
            results = soup.find_all(class_="result")
            if results:
                for result in results:
                    # 提取查询值
                    hs_code = result.find('a').text.strip()
                    hs_codes.append(hs_code)
                return hs_codes
            else:
                return ["未找到匹配的HS编码。"]
        else:
            return ["请求失败。"]
    except requests.RequestException as e:
        return [f"发生错误：{str(e)}"]


df = pd.read_excel('test.xlsx', header=None)

# 新建两列用于存放HS编码和所属目录
df['HS编码'] = ''
df['所属目录'] = ''

# 遍历每一行，查询并填充HS编码和所属目录
for index, row in df.iterrows():
    item_name = row[0]  # 根据实际列索引获取商品名称
    hs_codes = query_hs_code(item_name)
    if hs_codes:
        for hs_code in hs_codes:
            try:
                filtered_info = query_class(hs_code)
                if filtered_info:
                    df.at[index, 'HS编码'] += f'{hs_code}\n'
                    df.at[index, '所属目录'] += f'{filtered_info}\n'
            except IndexError:
                continue
    else:
        df.at[index, 'HS编码'] = "未找到匹配的HS编码。"  # 若没有编码，填写提示信息

# 保存结果到新的Excel文件
df.to_excel('output.xlsx', index=False)