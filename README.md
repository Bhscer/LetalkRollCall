# LetalkRollCall

## 软件介绍
一个简单的py脚本来连接手机并在获取到乐桃签到信息时进行签到
> 基于uiautomator2，由pyinstaller打包而成

### 重要提示
- 代码未经过正式的测试，不保证效果！


## 下载
- 从release页下载最新版本或者直接下载源码补齐依赖后运行


## 弊病
- 电脑只能连接一个adb设备（因为直接采用了 uiautomator2.connect()）

## 各种连接方式

### 在此之前
- 下载[adb工具包](https://developer.android.google.cn/studio/releases/platform-tools)并将其中所有文件拖入C:\Windows中或者添加到环境变量
- 注：请解压压缩包并将其中的所有文件拖入（包括adb.exe等）

### 连接虚拟机（较推荐）

#### mumu模拟器（win版）
1. 启动模拟器
2. 打开cmd输入 ```adb connect 127.0.0.1:7555```
3. 不出意外的话会显示：
```
C:\Users\Bhscer>adb connect 127.0.0.1:7555
connected to 127.0.0.1:7555
```
4. 返回打开已经打包好的程序或者源码即可运行

#### 连接真机
1.  打开usb调试
- 可以百度搜索 品牌+打开usb调试
- MIUI新版本需要在调试页将三个选项全部允许
- 此步可以通过百度学习得到，在此不展开叙述
2.  打开cmd输入 ```adb devices``` 查看设备是否连接
3.  不出意外的话会显示：
```
C:\Users\Bhscer>adb devices
List of devices attached
33xxxxx(手机序号不用管） device
```
4.  如果后面跟着的是device说明连接已经正常
5.  返回打开已经打包好的程序或者源码即可运行
