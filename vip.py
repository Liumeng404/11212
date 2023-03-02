import time

from playwright.sync_api import Playwright, sync_playwright
import csv
import re
import math



def scrape_data(page):
    # 等待表格加载完成
    page.wait_for_selector('table.table')
    # 获取表格中所有的行
    rows = page.query_selector_all('table tbody tr')
    rows_list = [rows[i:i+10] for i in range(0, len(rows), 10)]
    return rows_list


def save_to_csv(rows_list):
    with open('data3.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['ID', '账户', '申请时间', '试用产品', '来源', '负责人', '状态', '变更时间', '来源URL', '页面标题', '操作'])
        # 循环遍历所有行，并将每个单元格写入csv文件
        for every_rows in rows_list:
            for row in every_rows:
                for each in row:
                    cols = each.query_selector_all('td')
                    data = [col.text_content() for col in cols]
                    writer.writerow(data)

def run(playwright: Playwright):
    # 初始化 Playwright 并启动一个新的 Chromium 浏览器实例
    browser = playwright.chromium.launch(headless=False, channel='chrome', slow_mo=50)
    page = browser.new_page()

    # 访问登录页面
    page.goto('https://adminvip.yaozh.com/login/index.html')

    # 等待用户名和密码输入框出现，并输入用户名和密码
    page.wait_for_selector("input[name='username']")
    page.fill("input[name='username']", 'liumeng')
    page.fill("input[name='password']", 'liumeng123')

    # 获取滑块
    # handle_box_locate = page.locator('.handler')
    #
    # #获取登录按钮
    # login_box_locate = page.locator('button.btn')
    #
    # print(handle_box_locate.bounding_box())
    #
    # print(login_box_locate.bounding_box())

    # 定位鼠标
    page.mouse.move(490, 416)

    # 按下鼠标
    page.mouse.down()

    # 移动鼠标
    page.mouse.move(800, 416)

    # 放起鼠标
    page.mouse.up()

    time.sleep(1)

    # 点击登录
    page.mouse.click(500, 465)

    # 等待1秒
    time.sleep(2)

    # 跳转到里面
    page.goto('https://adminvip.yaozh.com/user/viptrial.html?starttime=2023-03-01&endtime=2023-03-01')

    page.wait_for_selector('table')

    #获取共有多少页
    pages_content = page.query_selector('font').text_content()
    items = re.findall('(\d+)',pages_content)[0]
    pages = math.ceil(int(items) / 10)
    print(pages)

    rows_list = []

    #翻页转圈所有
    for each_page in range(1,pages):
        page.goto(f'https://adminvip.yaozh.com/user/viptrial.html?starttime=2023-03-01&endtime=2023-03-01&page={each_page}')
        rows_list.append(scrape_data(page))
        time.sleep(1)

    save_to_csv(rows_list)




    # 关闭浏览器
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
