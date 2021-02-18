# "utf-8" 数据来源于天天基金
import requests
import time
import os

codes = ['006020', '005827', '320007',  ]  # 基金代码
num = ['1000', '1000', '1000', ]  # 持有份额
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
}


def ssyk(seconds: int):
    total, yk_total = 0, 0
    for code in codes:
        index_code = codes.index(code)
        url = "http://fundgz.1234567.com.cn/js/{}.js?".format(code)
        r = requests.get(url, headers=headers)
        # r.encoding = "UTF-8"
        # print(r.text)
        data_str = r.text.strip("jsonpgz(")  # 数据格式处理
        data_str = data_str.strip(");")  # 数据格式处理
        data = eval(data_str)  # 字符串转字典
        dwjz = float(data["dwjz"])  # 单位净值
        gsz = float(data["gsz"])  # 估算值
        yk_one = (gsz - dwjz) * float(num[index_code])  # 本基金当日盈亏=（估算值-单位净值）*份额
        total_one = dwjz * float(num[index_code])  # 本基金持有总额=单位净值*持有总份额
        print("持有{} {} 元，当日预估盈亏 {} 元。".format(data["name"], str('%.2f' % total_one), str('%.2f' % yk_one)))
        total = total + total_one
        yk_total = yk_total + yk_one
        total = total
    print("今日基金总持有 " + '%.2f' % total + ',' + " 今日预估总盈亏 " + '%.2f' % yk_total + "。")
    time.sleep(seconds)
    os.system("cls")


def main():
    try:
        sec = int(input("请输入刷新间隔（秒）:"))
    except ValueError:
        print("刷新间隔输入有误")
        input("按任意键退出！")
        return 0
    while True:
        ssyk(sec)


if __name__ == "__main__":
    main()
