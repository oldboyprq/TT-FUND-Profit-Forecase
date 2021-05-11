import requests
import json
import time
import os
from rich.console import Console
from rich.table import Table


def get_local_info():
    # 输入信息处理..txt保存数据
    demo_info = "320007:1000,005827:1000,006020:1000"
    print("请输入持有基金代码及份额")
    print("输入格式: 基金代码1:份额1,基金代码2:份额2,基金代码3:份额3...")
    print("输入示例: {}".format(demo_info))
    fund_info = input("请输入（无输入则用保存数据）:")
    if not fund_info:
        try:
            with open('fund.txt', 'r') as f:
                fund_info = f.read()
                f.close()
        except FileNotFoundError as e:
            print("当前无保存数据,使用demo数据")
            fund_info = demo_info
    if input("输入任意字符保存,直接回车不保存"):
        with open('fund.txt', 'w') as f:
            f.write(fund_info)
            f.close()
    fund_num = dict()  # 基金代码:份额
    for info in fund_info.split(","):
        index = info.index(":")
        key = info[:index]
        value = float(info[index + 1:])
        fund_num[key] = value
    return fund_num


def get_internet_info(infos: dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75",
    }
    fund_today = list()  # 所有基金的当日涨跌情况
    for fund in infos.keys():  # 基金代码
        url = "https://fundgz.1234567.com.cn/js/{}.js?".format(fund)
        r = requests.get(url, headers=headers)
        internet_infos = json.loads(r.text[r.text.index("(") + 1:-2])
        fund_today.append(internet_infos)
    return fund_today


def show_info(nums: dict, today: list, sec: int):
    while True:
        fund_yk = list()
        fund_total = list()
        table = Table(title="基金当日收益预估")
        table.add_column("基金代码", style='blue', justify='center')
        table.add_column("基金名称", justify="center")
        table.add_column("{}净值".format(today[0]['jzrq']), justify="center")
        table.add_column("{}估值".format(today[0]['gztime']), justify="center")
        table.add_column("涨跌情况", justify="center")
        table.add_column("持有份额", justify="center", style="Purple")
        table.add_column("当日预估盈亏", justify="center")
        table.add_column("持有总额", justify="center")
        table.add_column("刷新时间", justify="center", style="yellow")
        for fund_today in today:  # fundcode":"320007","name":"璇哄畨鎴愰暱娣峰悎","jzrq":"2021-05-10","dwjz":"1.5430",
            # "gsz":"1.5258","gszzl":"-1.12","gztime":"2021-05-11 10:57"
            money_yk = nums[fund_today['fundcode']] * (float(fund_today['gsz'])-float(fund_today['dwjz']))
            fund_yk.append(money_yk)
            money_total = nums[fund_today['fundcode']] * float(fund_today['gsz'])
            fund_total.append(money_total)
            if float(fund_today['gszzl']) < 0:
                table.add_row(fund_today['fundcode'],
                              fund_today['name'],
                              fund_today['dwjz'],
                              '[green]'+ fund_today['gsz'] + '[/green]',
                              '[green]' + fund_today['gszzl'] + '%' + '[/green]',
                              str(nums[fund_today['fundcode']]),
                              '[green]' + str('%.2f' % money_yk) + '[/green]',
                              str('%.2f' % money_total),
                              fund_today['gztime'])
            else:
                table.add_row(fund_today['fundcode'],
                              fund_today['name'],
                              fund_today['dwjz'],
                              '[red]' + fund_today['gsz'] + '[/red]',
                              '[red]' + '+' + fund_today['gszzl'] + '%' + '[/red]',
                              str(nums[fund_today['fundcode']]),
                              '[red]' + '+' + str('%.2f' % money_yk) + '[/red]',
                              str('%.2f' % money_total),
                              fund_today['gztime'])
        if sum(fund_yk) > 0:
            table.add_row('---', '---', '---', '---', '---', '---',
                          '[red]' + '+' + str('%.2f' % sum(fund_yk)) + '[/red]',
                          str('%.2f' % sum(fund_total)), '---', )
        else:
            table.add_row('---', '---', '---', '---', '---', '---',
                          '[green]' + str('%.2f' % sum(fund_yk)) + '[/green]',
                          str('%.2f' % sum(fund_total)), '---', )
        console = Console()
        console.print(table, justify="center")
        print("按CTRL+C退出")
        time.sleep(sec)
        os.system("cls")


def main():
    sec = int(input("请输入刷新时间(秒):"))
    a = get_local_info()
    b = get_internet_info(a)
    show_info(a, b, sec)


if __name__ == '__main__':
    main()
