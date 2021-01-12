# Author Atticus_lv
# -*- coding =utf-8 -*-
# @Time : 2020/9/8 11:16
# version: 2.0

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from time import sleep
from random import uniform

import os
import shutil
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('mylogger')
logger.setLevel(20)

TW = f"{round(uniform(36.5, 37.0), 1)}"


def mutiUser(basepath='./users/'):
    files = get_files_from_dir(basepath)
    for f in files:
        student = UserInfo_2(path=f)
        # print(student.username, student.password)
        try:
            f = 每日报平安(student.username, student.password)
            f.execute()
            logger.info(f'{student.username} 完成填报')
        except Exception as e:
            logger.warning(f'{student.username} 无法填报\n{e}\n')
            error_dir = os.path.join(basepath, 'error_user')
            if not os.path.exists(error_dir):
                os.makedirs(error_dir)
            shutil.move(os.path.join(basepath, f'{student.username}.txt'),
                        os.path.join(error_dir, f'{student.username}.txt'))


def get_files_from_dir(file_dir, type='.txt'):
    files = [os.path.join(root, file) for root, dirs, files in os.walk(file_dir) for file in files if
             os.path.splitext(file)[1] == type]

    return files


class UserInfo_2():
    def __init__(self, path):
        self.path = path
        self.name = self.get_name()
        self.username = self.name[:-4]
        self.password = self.read()

    def get_name(self):
        return os.path.basename(self.path)

    def read(self):
        logger.info(f"检测到用户:{self.username}...")
        try:
            with open(self.path, "r") as f:
                lines = f.readlines()
            return lines[0]
        except Exception:
            logger.warning(f'{self.username}密码读取错误')


def singleUser():
    student = UserInfo()
    if student.mode.startswith('0'):
        f = 每日报平安(student.username, student.password)
        f.execute()
    elif student.mode.startswith('1'):
        f = 晨午间体温(student.username, student.password)
        f.execute()
    else:
        print(student.mode)
        print(f"未输入正确运行模式")


class UserInfo():
    def __init__(self):
        username, password, mode = self.get_info()
        self.username = username
        self.password = password
        self.mode = mode

    @staticmethod
    def read(path="账号密码.txt"):
        print("检测账号密码文件中...")
        with open(path, "r") as f:
            lines = f.readlines()
        return lines[0], lines[1], lines[2]  # username password headless

    @staticmethod
    def write(path="账号密码.txt"):
        print("没有检测到账号密码文件\n请依次输入账号密码")
        username = input("账号")
        password = input("密码")
        mode = input('选择运行模式，每日报平安填0，晨午间提问填1')

        with open(path, "w") as f:
            f.write(f'{username}\n')
            f.write(f'{password}\n')
            f.write(f'{mode}\n')
        print('账号密码文件生成中...\n下次可直接登录')
        return username, password, mode

    @classmethod
    def get_info(self):
        try:
            return self.read()
        except:
            return self.write()


class Autoform():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self.get_driver()

    def get_driver(self):
        logger.info('检测浏览器驱动...')
        try:
            chrome_options = Options()
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('log-level=3')
            driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
            logger.info('驱动正常')
            return driver
        except:
            logger.error("目录文件夹下缺少驱动程序，无法使用"
                           "\n请检查浏览器驱动版本是否正确,本文件所附带驱动版本为 Chrome 87"
                           "\n下载正确版本：http://chromedriver.storage.googleapis.com/index.html")
            return None

    def finish(self):
        logger.info('程序结束')
        pass


class 每日报平安(Autoform):
    def execute(self):
        if self.driver:
            self.login()
            self.switch()
            if self.fill():
                self.upload()
            self.finish()

    def login(self):
        logger.info("寻找网页...")
        self.driver.get(
            "http://xgfx.bnuz.edu.cn/xsdtfw/sys/emapfunauth/pages/funauth-login.do?service=%2Fxsdtfw%2Fsys%2Femaphome%2Fportal%2Findex.do#/")
        self.driver.implicitly_wait(10)
        logger.info("登录中...")
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[
            0].send_keys(
            self.username)
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[
            1].send_keys(
            self.password)
        self.driver.find_element_by_xpath(
            '//button[@class="ivu-btn ivu-btn-primary ivu-btn-long ivu-btn-large"]').click()
        return True

    def switch(self):
        logger.info("网页跳转中，请勿移动鼠标...")
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element_by_xpath('//li[@title="疫情自查上报"]').click()
        self.driver.implicitly_wait(10)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def fill(self):
        logger.info("自动填写开始,移动鼠标可能导致填写失败...")
        try:
            tem = self.driver.find_element_by_xpath("//input[@name='TW']")
            tem.send_keys(TW)
            logger.info("体温填写完毕...")
        except:
            logger.info("您已填写完毕,无需再次填写...")
            self.driver.quit()
            return None

        try:
            # 下拉选项
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
                sleep(0.02)
            logger.info("下拉选项填写完成\n")
        except:
            logger.warning("中途移动鼠标导致错误，请重新启动本程序")
            self.driver.quit()
            return None

        return True

    def upload(self):
        logger.info('正在上传')
        try:
            self.driver.find_element_by_xpath('//*[@id="save"]').click()
            logger.info('上传完成')
            self.driver.quit()

        except Exception as ein:
            logger.warning(f"出现错误：{ein}")
            self.driver.quit()


class 晨午间体温(Autoform):
    def execute(self):
        if self.driver:
            self.login()
            if self.fill():
                self.upload()
            else:
                print('本时段已经填写完成')
            self.finish()

    def login(self):
        print("开始寻找网页")
        self.driver.get("http://xgfx.bnuz.edu.cn/xsdtfw/sys/swmxsyqxxsjapp/*default/index.do?THEME=indigo&EMAP_LANG=zh")
        self.driver.implicitly_wait(10)
        print("到达登录页面，开始填写用户数据")
        self.driver.find_element_by_xpath('//*[@id="page"]/div/div/div/div/button[2]').click()
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[
            0].send_keys(self.username)
        self.driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[
            1].send_keys(self.password)

        try:
            self.driver.find_element_by_xpath('//*[@id="emap-rsids-content"]/div/div[3]/div/div[3]/div/button').click()
        except:
            pass
        return True

    def fill(self):
        print("自动填写开始,移动鼠标可能导致填写失败")
        TW_input = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/a/div[2]/div[2]/input')
        TW_input.send_keys(TW)
        return True

    def upload(self):
        print("正在上传\n")
        try:
            self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[2]/button').click()
            print("上传完成\n")
            self.driver.quit()

        except Exception as e:
            print(f"出现错误：{e}")


if __name__ == '__main__':
    print("欢迎来到自动填报小助手")
    # singleUser()
    mutiUser()
