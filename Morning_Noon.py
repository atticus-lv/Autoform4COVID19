# Author Atticus_lv
# -*- coding =utf-8 -*-
# @Time : 2020/9/8 11:16

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from time import sleep
from random import uniform

url = "http://xgfx.bnuz.edu.cn/xsdtfw/sys/swmxsyqxxsjapp/*default/index.do?THEME=indigo&EMAP_LANG=zh"
TW = f"{round(uniform(36.5, 37.0), 1)}"


def main():
    student = UserInfo()
    username, password, headless = student.get()
    driver = InitDriver(headless)

    if driver:
        web = AutoForm(username, password, driver)
        if web.login():
            try:
                empty = web.fill_tem()
                if empty:
                    web.upload()
            except:
                print("本时段已经填写完毕")

    else:
        print('\n程序将在10秒后关闭')
        sleep(10)


def InitDriver(headless):
    try:
        chrome_options = Options()
        if headless == 1:
            chrome_options.add_argument('--headless')
            print("使用静默运行模式...")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
        print("驱动正常")
        return driver
    except:
        print("目录文件夹下缺少驱动程序，无法使用"
              "\n请检查浏览器驱动版本是否正确,本文件所附带驱动版本为 Chrome 85"
              "\n下载正确版本：http://chromedriver.storage.googleapis.com/index.html")
        return None


class UserInfo():

    @staticmethod
    def read():
        print("检测账号密码文件中...")
        with open("账号密码.txt", "r") as f:
            lines = f.readlines()
        return lines[0], lines[1], lines[2]  # username password headless

    @staticmethod
    def write():
        print("没有检测到账号密码文件\n请依次输入账号密码")
        username = input("账号")
        password = input("密码")
        headless = input('是否选择静默运行模式，是填1，否填0')

        with open("账号密码.txt", "w") as f:
            f.write(f'{username}\n')
            f.write(f'{password}\n')
            f.write(f'{headless}\n')
        print('账号密码文件生成中...\n下次可直接登录')
        return username, password, headless

    @classmethod
    def get(self):
        try:
            return self.read()
        except:
            return self.write()
        finally:
            print('开始检测浏览器驱动')


class AutoForm():
    def __init__(self, username, password, driver):
        self.username = username
        self.password = password
        self.driver = driver

    def login(self):
        print("开始寻找网页")
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        print("到达登录页面，开始填写用户数据")
        self.driver.find_element_by_xpath('//*[@id="page"]/div/div/div/div/button[2]').click()
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[
            0].send_keys(self.username)
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[
            1].send_keys(self.password)

        try:self.driver.find_element_by_xpath('//*[@id="emap-rsids-content"]/div/div[3]/div/div[3]/div/button').click()
        except:pass
        return True

    def fill_tem(self):
        print("自动填写开始,移动鼠标可能导致填写失败")
        TW_input = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/a/div[2]/div[2]/input')
        TW_input.send_keys(TW)
        return True

    def upload(self):
        print("正在上传\n")
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[2]/button').click()
            print("上传完成\n"
                  "\n5秒后退出程序")
            sleep(5)
            self.driver.quit()

        except Exception as e:
            print(f"出现错误：{e}")


if __name__ == '__main__':
    print("欢迎来到晨午自动填报小助手")
    main()
