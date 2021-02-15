import uiautomator2, time, random, requests, json
import subprocess

# letalk_app_name = "com.bhscer.letalkdemo"
letalk_app_name = "com.strong.letalk"

is_inletalk = True
is_rollcall_flag = True

on_debug = True
on_debug = not on_debug

if on_debug:
    letalk_app_name = "com.bhscer.letalkdemo"
else:
    letalk_app_name = "com.strong.letalk"
# print(letalk_app_name)
order = 'adb devices'  # 获取连接设备

pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)

adb_d = str(pi.stdout.read(), encoding="utf8")


# print(adb_d)


def check_if_rollcall_success():
    try:
        rollcall_result = d(resourceId=letalk_app_name + ":id/tv_result").get_text()
        if "成功" in rollcall_result:
            print(" > 签到成功")
            if on_debug:
                ss = random.randint(0, 1)
                if ss == 0:
                    d(resourceId=letalk_app_name + ":id/show_add").click()
                elif ss == 1:
                    d(resourceId=letalk_app_name + ":id/show_subtract").click()
        else:
            print(" > 疑似自动签到失败，请前往手动签到！\n > 正确答案是%i" % rollcall_true_ans)
    except:
        print(" > 疑似自动签到失败，请前往手动签到！\n > 正确答案是%i" % rollcall_true_ans)


if len(adb_d) <= 28:
    input("手机未连接请关闭软件连接后重试")
    exit()
else:

    adb_status = (adb_d[28 + adb_d[28:].index("	") + 1:]).replace("\r\n", "")
    # print(adb_status)

    if adb_status != "device":
        print("手机连接失败 可能是手机已锁屏或未授权或者连接了多台设备")
    else:
        try:
            d = uiautomator2.connect()
        except:
            input("手机未连接请关闭软件连接后重试")
            exit()

        d.settings['wait_timeout'] = 1

        if not on_debug:
            try:
                r = requests.get("https://bhscer.github.io/letalkrollcall_py/files/app_info.json")
                with open("app_info.json", "wb") as code:
                    code.write(r.content)
            except:
                input("与服务器沟通失败，按回车后退出")
                exit()

            with open("app_info.json", 'r', encoding="UTF-8") as f:
                a = json.load(f)
        else:
            with open("letalkrollcall_py//files//app_info.json", 'r', encoding="UTF-8") as f:
                a = json.load(f)

        if a['avliable'] == 0:
            print(a['close_message'])
            input("")

        else:
            print("服务器端验证成功...")
            while True:
                if d.info['currentPackageName'] == letalk_app_name:
                    is_inletalk = True
                    try:
                        rollcall_title = d(resourceId=letalk_app_name + ":id/tv_content").get_text()
                        print("\n- " + time.strftime("%H:%M:%S ", time.localtime()) + "检测到签到")
                        is_rollcall_flag = True
                        if rollcall_title[-2:] == "=?" and len(rollcall_title) == 5:
                            rollcall_ans_result1 = int(d(resourceId=letalk_app_name + ":id/tv_result_first").get_text())
                            rollcall_ans_result2 = int(
                                d(resourceId=letalk_app_name + ":id/tv_result_second").get_text())
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
                    except:
                        if is_rollcall_flag:
                            print("当前未签到")
                        is_rollcall_flag = False
                else:
                    if is_inletalk:
                        print("当前不在乐课！")
                    is_inletalk = False

                time.sleep(0.5)
