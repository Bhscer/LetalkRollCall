import json
import random
import requests
import subprocess
import time
import uiautomator2
import wave
import pyaudio
import sys
import webbrowser
import os

# letalk_app_name = "com.bhscer.letalkdemo"

v_code = 3
letalk_app_name = "com.strong.letalk"

adb_dir = os.path.split(os.path.abspath(__file__))[0] + "//adb//"
is_inletalk = True
is_rollcall_flag = True

on_debug = True
on_debug = not on_debug

if on_debug:
    letalk_app_name = "com.bhscer.letalkdemo"
else:
    letalk_app_name = "com.strong.letalk"


# print(letalk_app_name)


# print(adb_d)

def play():
    CHUNK = 1024
    wf = wave.open("res//warn.wav", 'rb')
    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    # read data
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    # stop stream (4)
    stream.stop_stream()
    stream.close()
    # close PyAudio (5)
    p.terminate()


def check_if_rollcall_success():
    try:
        rollcall_result = d(resourceId=letalk_app_name + ":id/tv_result").get_text()
        if "成功" in rollcall_result:
            print(" > 签到成功")
            if on_debug:
                ss = random.randint(0, 1)
                #play()
                if ss == 0:
                    d(resourceId=letalk_app_name + ":id/show_add").click()
                elif ss == 1:
                    d(resourceId=letalk_app_name + ":id/show_subtract").click()
        else:
            play()
            print(" > 疑似自动签到失败，请前往手动签到！\n > 正确答案是%i" % rollcall_true_ans)
    except:
        play()
        print(" > 疑似自动签到失败，请前往手动签到！\n > 正确答案是%i" % rollcall_true_ans)


print("- 乐课自动签到工具\n > v1.01(3) by Bhscer\n > Github:https://github.com/Bhscer/LetalkRollCall\n\n- 开始连接服务器...")

if not on_debug:

    connect_t = 0
    while connect_t < 5:
        try:
            proxies = {'http': None, 'https': None}
            r = requests.get("https://bhscer.github.io/letalkrollcall_py/files/app_info.json", proxies=proxies)
            with open("app_info.json", "wb") as code:
                code.write(r.content)
            connect_t = 6
        except Exception as e:
            connect_t += 1
            print(" > 连接失败 正在重试 %i/5" % connect_t)

            if connect_t == 5:
                print(" > 与服务器沟通失败\n > 出现此类问题请尝试\n"
                      "    0.多次重新打开（解决大部分问题）\n"
                      "    1.关闭代理/vpn\n    "
                      "2.检查电脑是否能连接到Github\n错误代码为：\n" + repr(e))
                input("\n - 按回车后退出")
                sys.exit()

    with open("app_info.json", 'r', encoding="UTF-8") as f:
        a = json.load(f)
else:
    with open("app_info.json", 'r', encoding="UTF-8") as f:
        a = json.load(f)

if a['avliable'] == 0:
    print(a['close_message'])
    input("")

else:
    print(" > 服务器端验证成功...\n")

    if a['newest_v_code'] > v_code:
        print("- 签到工具已有更新 以下是更新日志：")
        print(a['update_msg'])
        if input("- 输入1并按下回车前往更新 不更新请直接回车: ") == "1":
            webbrowser.open(a['update_url'])
            sys.exit(0)
        else:
            print(" > 您选择了本次跳过更新\n")

    print("- 是否使用内建的adb?\n - windows正常用户默认请按回车")
    if input(" - macOS用户请输入 1 并按下回车： ") == "1":
        adb_dir = ""
        print(" - 已经修改为使用环境变量中的adb\n")
    else:
        print(" > 选择了使用内建的adb\n")


    print("- 请选择你的连接方式\n - mumu模拟器（win）输入 1 并按下回车")
    if input(" - 其他方式请在连接好后直接按下回车: ") == "1":
        order_mumu = adb_dir + 'adb connect 127.0.0.1:7555'  # 获取连接设备

        pi_mumu = subprocess.Popen(order_mumu, shell=True, stdout=subprocess.PIPE)

        adb_d_mumu = str(pi_mumu.stdout.read(), encoding="ansi")

        # print(adb_d_mumu)

        if "connected to 127.0.0.1:7555" in adb_d_mumu or "already connected to 127.0.0.1:7555" in adb_d_mumu:
            print(" > 连接mumu模拟器成功")
        else:
            print(" > 连接mumu模拟器失败")
            input(" - 按回车后退出")
            sys.exit(0)
    else:
        print(" > 你选择了通过其他方式连接")
    order = adb_dir + 'adb devices'  # 获取连接设备

    pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)

    adb_d = str(pi.stdout.read(), encoding="ansi")

    print("\n- 正在通过adb devices确定连接的设备...")
    if len(adb_d) <= 28:
        print(" > 手机未连接请关闭软件连接后重试\n > 如果手机确实已连接请百度 品牌+usb调试")
        input(" - 按回车键退出")
        sys.exit(0)
    else:

        adb_status = (adb_d[28 + adb_d[28:].index("	") + 1:]).replace("\r\n", "")
        # print(adb_status)

        if adb_status != "device":
            print(" > 手机连接失败 可能是手机已锁屏或未授权或者连接了多台设备\n下一行开始为adb返回结果\n" + adb_d)
            input(" - 按回车键退出")
            sys.exit(0)
        else:
            try:
                d = uiautomator2.connect()
            except Exception as e:
                print(" > 手机连接失败 错误为：\n" + repr(e))
                input(" - 按回车键退出")
                sys.exit(0)

            d.settings['wait_timeout'] = 1
            print(" > 手机连接成功 开始签到检测\n > 当前检测的包名为 " + letalk_app_name + "\n")
            while True:
                if d.info['currentPackageName'] == letalk_app_name:
                    is_inletalk = True
                    """tmp = time.time()
                    print(d.xpath(letalk_app_name + ":id/tv_result_first").wait(timeout=0.5))
                    print(time.time()-tmp)"""
                    """if d.xpath(letalk_app_name + ":id/tv_result_first").wait(timeout=1) != None and \
                            d.xpath(letalk_app_name + ":id/tv_result_first").wait(timeout=1) != None:
                        print("0")"""
                    try:
                        rollcall_ans_result1 = int(d(resourceId=letalk_app_name + ":id/tv_result_first").get_text())
                        rollcall_ans_result2 = int(d(resourceId=letalk_app_name + ":id/tv_result_second").get_text())
                    except:
                        if is_rollcall_flag or on_debug:
                            print("- 当前未签到")
                        is_rollcall_flag = False
                    else:
                        is_rollcall_flag = True

                    if is_rollcall_flag:
                        rollcall_title = d(resourceId=letalk_app_name + ":id/tv_content").get_text()
                        print("\n- " + time.strftime("%H:%M:%S ", time.localtime()) + "检测到签到")
                        is_rollcall_flag = True
                        if rollcall_title[-2:] == "=?" and len(rollcall_title) == 5:
                            '''rollcall_ans_result1 = int(d(resourceId=letalk_app_name + ":id/tv_result_first").get_text())
                            rollcall_ans_result2 = int(
                                d(resourceId=letalk_app_name + ":id/tv_result_second").get_text())'''
                            if rollcall_title[1] == "+":
                                rollcall_title_num1 = int(rollcall_title[0])
                                rollcall_title_num2 = int(rollcall_title[2])
                                rollcall_true_ans = rollcall_title_num1 + rollcall_title_num2
                                print(" > %i + %i = %i" % (rollcall_title_num1, rollcall_title_num2, rollcall_true_ans))
                                if rollcall_true_ans == rollcall_ans_result1:
                                    d(resourceId=letalk_app_name + ":id/tv_result_first").click()
                                    time.sleep(0.2)
                                    check_if_rollcall_success()
                                elif rollcall_true_ans == rollcall_ans_result2:
                                    d(resourceId=letalk_app_name + ":id/tv_result_second").click()
                                    time.sleep(0.2)
                                    check_if_rollcall_success()
                                else:
                                    print(" > 自动签到失败，请前往手动签到！")

                            elif rollcall_title[1] == "-":
                                rollcall_title_num1 = int(rollcall_title[0])
                                rollcall_title_num2 = int(rollcall_title[2])
                                rollcall_true_ans = rollcall_title_num1 - rollcall_title_num2
                                print(" > %i - %i = %i" % (rollcall_title_num1, rollcall_title_num2, rollcall_true_ans))
                                if rollcall_true_ans == rollcall_ans_result1:
                                    d(resourceId=letalk_app_name + ":id/tv_result_first").click()
                                    time.sleep(0.2)
                                    check_if_rollcall_success()
                                elif rollcall_true_ans == rollcall_ans_result2:
                                    d(resourceId=letalk_app_name + ":id/tv_result_second").click()
                                    time.sleep(0.2)
                                    check_if_rollcall_success()
                            else:
                                print(" > 签到失败！")
                            print("")

                else:
                    if is_inletalk:
                        print("- 当前不在乐课")
                    is_inletalk = False
                    is_rollcall_flag = True

                time.sleep(0.5)
