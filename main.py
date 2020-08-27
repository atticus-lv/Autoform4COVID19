#-*- coding =utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from time import sleep


def main():
    student = UserInfo()
    username,password = student.get()
    driver = getdriver()

    if driver:
        web = autoform(username,password,driver)
        if web.login():
            web.switch()
            empty = web.autoform()

            if empty:
                web.upload()
    else:
        print('\n程序将在10秒后关闭')
        sleep(10)


def getdriver():
    try:

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('log-level=3')
        print("驱动正常")
        print("静默运行模式...")
        driver = webdriver.Chrome('chromedriver.exe',options=chrome_options)

        return driver
    except:
        print("目录文件夹下缺少驱动程序，无法使用"
              "\n请检查浏览器驱动版本是否正确,本文件所附带驱动版本为 Chrome 84"
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
        self.driver.get(
            "http://xgfx.bnuz.edu.cn/xsdtfw/sys/emapfunauth/pages/funauth-login.do?service=%2Fxsdtfw%2Fsys%2Femaphome%2Fportal%2Findex.do#/")
        self.driver.implicitly_wait(10)
        print("到达指定页面，开始填写用户数据")
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[0].send_keys(
            self.username)
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[1].send_keys(
            self.password)
        self.driver.find_element_by_xpath('//button[@class="ivu-btn ivu-btn-primary ivu-btn-long ivu-btn-large"]').click()
        return True


    def switch(self):
        print("网页跳转中，请勿移动鼠标")
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element_by_xpath('//li[@title="疫情自查上报"]').click()
        self.driver.implicitly_wait(10)
        self.driver.switch_to.window(self.driver.window_handles[1])


    def autoform(self):
        print("自动填写开始,移动鼠标可能导致填写失败")
        try:
            TW = self.driver.find_element_by_xpath("//input[@name='TW']")
            TW.send_keys('36.7')
            print("体温填写完毕")
        except:
            print("您已填写完毕,无需再次填写")
            return None

        try:
            #下拉选项
            var1 = 6
            var2 = 24
            action = ActionChains(self.driver)
            for i in range(0, 5):
                elements = [
                    f"/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[{var1}]/div/div/div[2]/div/div/div[1]",
                    f"/html/body/div[{var2}]/div/div/div/div[2]/div/div[3]"
                ]
                c = self.driver.find_element_by_xpath(elements[0]).click()
                action.click(on_element=c)
                c1 = self.driver.find_element_by_xpath(elements[1]).click()
                var1 += 2
                var2 += 2
                sleep(0.1)
            print("下来选项填写完成\n")
        except:
            print("中途移动鼠标导致错误，请重新启动本程序")
            return None

        return True

    def upload(self):
        print("正在上传\n")
        try:
            self.driver.find_element_by_xpath('//*[@id="save"]').click()
            print("上传完成\n"
                  "\n5秒后退出程序")
            sleep(5)
            self.driver.quit()

        except Exception as ein:
            print(f"出现错误：{ein}"
                  "\n移动了鼠标导致错误")


if __name__ == '__main__':
    main()
