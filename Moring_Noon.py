#Author Atticus_lv
#-*- coding =utf-8 -*-
#@Time : 2020/9/8 11:16

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from time import sleep
from random import uniform

url = "http://xgfx.bnuz.edu.cn/xsdtfw/sys/swmxsyqxxsjapp/*default/index.do?THEME=indigo&EMAP_LANG=zh"
TW = f"{round(uniform(36.5,37.0),1)}"


def main():
    student = UserInfo()
    username,password = student.get()
    driver = getdriver()

    if driver:
        web = autoform(username,password,driver)
        if web.login():
            empty = web.autoform()
            if empty:
                web.upload()
            else:
                print("本时段已经填写完毕")
    else:
        print('\n程序将在10秒后关闭')
        sleep(10)


def getdriver():
    try:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('log-level=3')
        print("驱动正常")
        print("静默运行模式...")
        driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)

        return driver
    except:
        print("目录文件夹下缺少驱动程序，无法使用"
              "\n请检查浏览器驱动版本是否正确,本文件所附带驱动版本为 Chrome 85"
              "\n下载正确版本：http://chromedriver.storage.googleapis.com/index.html")
        return None


class UserInfo(object):

    @staticmethod
    def read():
        print("检测账号密码文件中...")
        f = open("账户密码.txt", "r")  # 打开文件 w为写入，没有则创建
        lines = f.readlines()  # readline 为一行 readlines为全部行，单独read为单个字符位
        username = lines[0]
        password = lines[1]
        f.close()  # 关闭文件'''
        return username, password

    @staticmethod
    def write():
        print("没有检测到账号密码文件")
        print("请依次输入账号密码")
        username = input("账号")
        password = input("密码")
        info = open("账户密码.txt", "w")
        info.write(username)
        info.write("\n")
        info.write(password)
        info.close()
        print('账号密码文件生成中...\n下次可直接登录')
        return username, password

    @classmethod
    def get(self):
        try:
            username, password = self.read()
            print("读取文件中...")
            return username, password
        except:
            username, password = self.write()
            return username, password
        finally:
            print('开始检测浏览器驱动')

class autoform(object):
    def __init__(self,username,password,driver):
        self.username = username
        self.password = password
        self.driver = driver

    def login(self):
        print("开始寻找网页")
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        print("到达指定页面，开始填写用户数据")
        self.driver.find_element_by_xpath('//*[@id="page"]/div/div/div/div/button[2]').click()
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[0].send_keys(self.username)
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[1].send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="emap-rsids-content"]/div/div[3]/div/div[3]/div/button').click()
        return True


    def autoform(self):
        print("自动填写开始,移动鼠标可能导致填写失败")
        TW_input = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/a/div[2]/div[2]/input')
        TW_input.send_keys(TW)
        return True

    def upload(self):
        print("正在上传\n")
        try:
            self.driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/div[2]/button').click()
            print("上传完成\n"
                  "\n5秒后退出程序")
            sleep(5)
            self.driver.quit()

        except Exception as ein:
            print(f"出现错误：{ein}"
                  "\n移动了鼠标导致错误")

if __name__ == '__main__':
    print("欢迎来到晨午自动填报小助手")
    main()