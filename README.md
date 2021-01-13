### 自动填报 1.5版本

> **使用方法**

1. 点击本页面的 Code，下载ZIP 

2. 解压并打开 **`自动填报.exe`** 文件（请勿删除`chromedriver.exe`文件）

> **连接学校WIFI时无法进入网站，会导致程序报错**

第一次使用需按照提示输入用户信息，随后会保存为`账号密码.txt`

其中，第三行为输入0为每日报平安，1为晨午间体温

```
18180xxxxx 
password
0 
```

若提示找不到驱动或出现奇怪的报错，确保你使用的是最新的谷歌浏览器(87版本)

使用其他版本的，请按提示下载对应驱动，[或点击这里](http://chromedriver.storage.googleapis.com/index.html)

替换`chromedriver.exe`，并重新启动程序



#### Windows 用户定时任务

搜索栏搜索

![image-20200908120326549](img/image-20200908120326549.png)

创建任务 *可以在常规当中更改任务名字*

![image-20200908120424584](img/image-20200908120424584.png)

因为第一次运行会生成一个实例，用于记录账户密码，所以建议触发时间可以先选一个比较接近的，运行完第一次后再将时间改回来

![image-20200908120648812](img/image-20200908120648812.png)

选择 **自动填报.exe**

![image-20200908121229475](img/image-20200908121229475.png)

点击确认完成定时任务。

然后就可以每天定时自动上报了



> 多人版本使用方法...

配置python环境：

1. 安装  https://www.python.org/downloads/
2. 添加 python 到环境变量中（如果第一步勾选了path选项可忽略，若无请百度）
3. 搜索 cmd ，弹出黑窗后输入 `python`，若弹出版本信息则整明配置成功
4. 打开新的cmd 输入 `pip install selenium` ，等待安装完成，关闭黑窗

配置用户：

1. 解压后的文件夹路径为 E:\某个文件夹\Autoform4COVID19
2. 在里面新建文件夹并命名为 users
3. 在user里面添加以用户名为名称的txt文件，第一行输入密码(若密码错误则该用户在运行后会被移动到‘错误用户’文件夹内)

定时任务设置

1. 任意地方新建txt文件，并在里面输入相关信息

    其中，E: 以及 cd E:\某个文件夹\Autoform4COVID19 是你解压下载文件的盘和具体位置

    ```shell
    @echo off  
    E:  
    cd E:\pythondemo\Autoform4COVID19
    start python main.py
    exit
    ```

2. 重命名后缀.txt 为 .bat

3. 按上面图文配置定时任务 最后选择.bat文件而不是exe文件



***

> 如果本项目对你有帮助，请我喝杯奶茶

<img src="img/img.jpg" alt="img" style="zoom: 80%;" />
