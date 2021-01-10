### 自动填报 1.5版本

> **使用方法**

1. 点击本页面的 Code，下载ZIP 

2. 解压并打开 **`main.exe`** 文件（请勿删除`chromedriver.exe`文件）

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

选择 **main.exe**

![image-20200908121229475](img/image-20200908121229475.png)

点击确认完成定时任务。

然后就可以每天定时自动上报了

***

> 如果本项目对你有帮助，请我喝杯奶茶

<img src="img/img.jpg" alt="img" style="zoom: 80%;" />