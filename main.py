#-*- coding =utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import os
from time import sleep


def main():
    if not os.path.exists("账户密码.txt"):
        username, password = pNoUser()
        wUserInfo(username,password)
        print('账号密码文件创建完成...\n开始检测浏览器驱动')
    else:
        username, password = rUserInfo()
        print('账号密码文件读取完成...\n开始检测浏览器驱动')

    try:
        print("自动填写开始，请勿移动鼠标")
        sleep(0.5)
        driver = login(username, password)
        try:
            switch(driver)
            fill_TW(driver)
            fill_dropbox(driver)
            upload(driver)
        except Exception as ein:
            print(f"出现错误：{ein}"
                  "\n你已填写完成？或是不小心移动了鼠标导致错误？")
        finally:
            print("\n5秒后退出程序")
            sleep(5)
            driver.quit()

    except Exception as e:
        print(f"出现错误：{e}"
              "\n请检测网络是否正常"
              "\n密码是否正确"
              "\n请检查浏览器驱动版本是否正确,本文件所附带驱动版本为 Chrome 84"
              "\n下载正确版本：http://chromedriver.storage.googleapis.com/index.html")

        print('\n程序将在10秒后关闭')
        sleep(10)


def pNoUser():
    print("没有检测到账号密码文件请输入\n")
    print("请依次输入账号密码\n")
    username = input("账号")
    password = input("密码")
    return username,password


def wUserInfo(username,password):
    print("start")
    info = open("账户密码.txt", "w")
    info.write(username)
    info.write("\n")
    info.write(password)
    info.close()
    print("finish")


def rUserInfo():
    f = open("账户密码.txt", "r")  # 打开文件 w为写入，没有则创建
    lines = f.readlines()  # readline 为一行 readlines为全部行，单独read为单个字符位
    username = lines[0]
    password = lines[1]
    f.close()  # 关闭文件'''
    return username,password


def login(username,password):
    driver = webdriver.Chrome('chromedriver.exe')
    print("驱动正常，开始寻找网页")
    driver.get("http://xgfx.bnuz.edu.cn/xsdtfw/sys/emapfunauth/pages/funauth-login.do?service=%2Fxsdtfw%2Fsys%2Femaphome%2Fportal%2Findex.do#/")
    driver.implicitly_wait(10)
    print("到达指定页面，开始填写用户数据")
    driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[0].send_keys(username)
    driver.find_elements_by_xpath('//input[@class="ivu-input ivu-input-large ivu-input-with-prefix"]')[1].send_keys(password)
    driver.find_element_by_xpath('//button[@class="ivu-btn ivu-btn-primary ivu-btn-long ivu-btn-large"]').click()

    return driver


def switch(driver):
    print("网页跳转中")
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath('//li[@title="疫情自查上报"]').click()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])


def fill_TW(driver):
    TW = driver.find_element_by_xpath("//input[@name='TW']")
    TW.send_keys('37')
    print("填写中")


def fill_dropbox(driver):
    print("...")
    var1 = 6
    var2 = 24
    action = ActionChains(driver)
    for i in range(0, 5):
        elements = [
            f"/html/body/main/article/section/div[2]/div[2]/div/div[2]/div[2]/div[{var1}]/div/div/div[2]/div/div/div[1]",
            f"/html/body/div[{var2}]/div/div/div/div[2]/div/div[3]"
        ]
        c = driver.find_element_by_xpath(elements[0]).click()
        action.click(on_element=c)
        c1 = driver.find_element_by_xpath(elements[1]).click()
        var1 += 2
        var2 += 2
        sleep(0.5)
    print("填写完成\n")


def upload(driver):
    print("正在上传\n")
    driver.find_element_by_xpath('//*[@id="save"]').click()
    print("上传完成\n")

if __name__ == '__main__':
    main()








