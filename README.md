# LetalkRollCall

## 软件介绍
一个简单的py脚本来连接手机并在获取到乐桃的签到信息时进行签到
> 基于uiautomator2，由pyinstaller打包而成

### 重要提示
- 代码未经过正式的测试，不保证效果！


## 下载
- 从release页下载最新版本或者直接下载源码补齐依赖后运行

## 关于release中下载的文件说明
- 文件为压缩包请解压后运行目录中的bat文件
- 为了加快程序打开速度，在程序打包时没有合成一个文件

## 弊病
- 电脑只能连接一个adb设备（因为直接采用了 uiautomator2.connect()）

## 源码运行提示
- 推荐python版本为3.9
- 需要安装uiautomator2，requests和pyaudio
### win环境下打开cmd：
```
pip install uiautomator2
pip install requests
pip install pyaudio
```
- 如果pyaudio安装报错请尝试去官网下载 在此提供一个 [镜像站](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
### macos环境在终端中执行：
```
pip3 install uiautomator2
pip3 install requests
brew install portaudio
pip3 install pyaudio
```

## win环境下的使用方式

### 在此之前
- 下载[adb工具包](https://developer.android.google.cn/studio/releases/platform-tools)并将其中所有文件拖入C:\Windows中或者添加到环境变量
- 注：请解压压缩包并将其中的所有文件拖入（包括adb.exe等）

### 连接虚拟机（较推荐）

#### mumu模拟器
1. 启动模拟器
2. 打开cmd输入 ```adb connect 127.0.0.1:7555```
3. 不出意外的话会显示：
```
C:\Users\Bhscer>adb connect 127.0.0.1:7555
connected to 127.0.0.1:7555
```
4. 返回打开已经打包好的程序或者源码即可运行

### 连接真机
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

## macos环境下的使用方式
### 由于手头没有macos系统无法进行测试，在此大概罗列方法
0.  安装adb环境和python3.9环境并补齐依赖
- 推荐使用HomeBrew来安装adb环境和python3.9环境
- HomeBrew安装方法自行百度，安装后执行
```
brew install python@3.9
brew cask install android-platform-tools
```
- 补齐依赖所需代码见[上文](https://github.com/Bhscer/LetalkRollCall/blob/main/README.md#macos%E7%8E%AF%E5%A2%83%E5%9C%A8%E7%BB%88%E7%AB%AF%E4%B8%AD%E6%89%A7%E8%A1%8C)
1.  连接模拟器/手机
- mumu模拟器可尝试终端执行以下命令：
```adb kill-server && adb server && adb shell```
2.  打开源码运行
