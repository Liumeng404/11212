import time

from playwright.sync_api import Playwright, sync_playwright
from time import sleep
# from lxml import etree


def run(playwright: Playwright) -> None:
    # 初始化 Playwright 并启动一个新的 Chromium 浏览器实例
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 访问登录页面
    page.goto('https://adminvip.yaozh.com/login/index.html')


    #获取滑块背景
    bg_box_locate = page.locator('.drag_bg')

    #获取滑块
    handle_box_locate = page.locator('.handler handler_bg')

    #背景位置信息
    bg_box = bg_box_locate.bounding_box()

    #获取滑块位置信息
    handle_box = handle_box_locate.bounding_box()

    #计算滑块中心的坐标
    x = bg_box["x"] + handle_box["x"] + handle_box["width"] / 2
    y = bg_box["y"] + handle_box["y"] + handle_box["height"] / 2


    #移动滑块
    handle_box_locate.drag_to(x=x+260, y=y, timeout=1000)

    # 等待用户名和密码输入框出现，并输入用户名和密码
    page.wait_for_selector("input[name='username']")
    page.fill("input[name='username']", 'liumeng')
    page.fill("input[name='password']", 'liumeng123')

    # 等待登录成功并跳转到目标页面
    page.wait_for_selector('#wrapper')
    page.goto('https://adminvip.yaozh.com/user/viptrial.html')


    time.sleep(1000)

    # 等待表格元素加载并提取 HTML 内容
    page.wait_for_selector('#table')
    table_html = page.inner_html('#table')

    # 使用 lxml 库解析 HTML 并提取表格数据
    table = etree.HTML(table_html).xpath('//table')[0]
    for row in table.xpath('.//tr'):
        row_data = [cell.text.strip() for cell in row.xpath('.//td')]
        print(row_data)

    # 关闭浏览器
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
