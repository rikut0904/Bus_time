import datetime as dt
import time
import csv
import PySimpleGUI as sg
#GUIデザイン
#sg.theme("Dark")
sg.theme("LightPurple")
def early():
    #初期データ入力(休暇は次を参照:https://www.kanazawa-it.ac.jp/about_kit/yatsukaho.html)
    #現在のバージョン:v2j   024
    #日付データ
    dt_now = dt.datetime.now()
    week = dt_now.weekday()#月:0,火:1,水:2,木:3,金:4,土:5,日:6
    year, month, day = dt_now.year, dt_now.month, dt_now.day

    #夏季休暇
    SmmS, SmdS = 8, 5   #夏季休暇始まり月, 日
    SmmF, SmdF = 9, 13  #夏季休暇終わり月, 日
    #春季休暇
    SpmS, SpdS = 3, 1   #春季休暇始まり月, 日
    SpmF, SpdF = 3, 31  #春季休暇終わり月, 日
    #祝日及びその他運休日(dayを変更)
    month4_7 = (month == 4 and day == 29) or (month == 5 and 3 <= day <= 6) or (month == 6 and day == 1) or (month == 7 and 13 <= day <= 15)
    month8_9 = (month == 8 and (day == 3 or 8 <= day <= 18 or day == 24 or day == 31)) or (month == 9 and (14 <= day <= 16 or 22 <= day <= 23))
    month10_12 = (month == 10 and (day == 14 or 19 <= day <= 20)) or (month == 11 and (3 <= day <= 4 or day == 23)) or (month == 12 and 27 <= day <= 31)
    month1_3 = (month == 1 and (1 <= day <= 6 or day == 13)) or (month == 2 and (day == 11 or 23 <= day <= 24)) and (month == 3 and day == 20)
    # print(week)
    #バス時刻表
    if not(month4_7 or month8_9 or month10_12 or month1_3):
        if 0 <= week <= 4:
            if (month == SmmS and day >= SmdS) or (month == SmmF and day <= SmdF) or (month == SpmS and day >= SpdS) or (month == SpmF and day <= SpdF):#夏季・春季休暇
                with open('vac_mon-fri_23to65.csv','r') as input_sheet23to65:
                    bus23to65 = [row for row in csv.reader(input_sheet23to65)]
                with open('vac_mon-fri_65to23.csv','r') as input_sheet65to23:
                    bus65to23 = [row for row in csv.reader(input_sheet65to23)]
                info = ""
            else:
                with open('normal_mon-fri_23to65.csv','r') as input_sheet23to65:
                    bus23to65 = [row for row in csv.reader(input_sheet23to65)]
                with open('normal_mon-fri_65to23.csv','r') as input_sheet65to23:
                    bus65to23 = [row for row in csv.reader(input_sheet65to23)]
                info = ""
        elif week == 5:
            if (month == SmmS and day >= SmdS) or (month == SmmF and day <= SmdF) or (month == SpmS and day >= SpdS) or (month == SpmF and day <= SpdF):#夏季・春季休暇
                with open('vac_sat_23to65.csv','r') as input_sheet23to65:
                    bus23to65 = [row for row in csv.reader(input_sheet23to65)]
                with open('vac_sat_65to23.csv','r') as input_sheet65to23:
                    bus65to23 = [row for row in csv.reader(input_sheet65to23)]
                info = ""
            else:
                with open('normal_sat_23to65.csv','r') as input_sheet23to65:
                    bus23to65 = [row for row in csv.reader(input_sheet23to65)]
                with open('normal_sat_65to23.csv','r') as input_sheet65to23:
                    bus65to23 = [row for row in csv.reader(input_sheet65to23)]
                info = ""
        else:
            bus23to65 = []
            bus65to23 = []
            info = "本日は運休です"
    else:
        bus23to65 = ""
        bus65to23 = ""
        info = "本日は運休です"
    # print(bus23to65)
    # print(bus65to23)
    # print(f"info={info}")
    return (year, month, day, bus23to65, bus65to23, info)

#GUI設定
class GUI():
    def __init__(self, info, place):
        if info == "本日は運休です" or info == "本日の運航は終了しました":
            layout = [[sg.T("今日は:"),sg.T("", key="-TODAY-")], # type: ignore
                [sg.T("現在時刻:"),sg.T("", key="-CLOCK-")], # type: ignore
                [sg.T("",key="-info-")]]
            layout_size = (250,100)
        elif place == '23号館→65号館' or place == '65号館→23号館':
            layout = [[sg.T("今日は:"),sg.T("", key="-TODAY-"), ], # type: ignore
                    [sg.T("現在時刻:"),sg.T("", key="-CLOCK-")], # type: ignore
                    [sg.Combo(['23号館→65号館', '65号館→23号館'], default_value = place, size =(30,1), 
                                key = "-PULL-", enable_events=True)],
                    [sg.T("次のバスの時間は:"),sg.T("",key="-BUS_DEPA_TIME-")],
                    [sg.T("到着予定時刻は:"),sg.T("",key="-BUS_ARR_TIME-")],
                    [sg.T("次のバスの時間まで:")],
                    [sg.T("",key="-NEXT_TIME-")]]
            layout_size = (300,230)
        else:
            layout = [[sg.T("今日は:"),sg.T("", key="-TODAY-")], # type: ignore
                    [sg.T("現在時刻:"),sg.T("", key="-CLOCK-")], # type: ignore
                    [sg.Combo(['23号館→65号館', '65号館→23号館'], default_value = '選択してください', size =(30,1), 
                                key = "-PULL-", enable_events=True)]]
            layout_size = (320,150)
        self.window = sg.Window("八束穂キャンパスバス", layout,
                        font = (None,15), finalize = True, size = layout_size)

#現在時刻取得
def time_getter():
    time.sleep(1)
    dt_now = dt.datetime.now()
    hour, minute, second = dt_now.hour, dt_now.minute, dt_now.second
    time_now = f'{hour}時{minute}分{second}秒'
    return (hour, minute, second, time_now)

#次回バス時間までの計算
def next_bus_time(bus_Sche_time, hour, minute, second, info):
    #次回バス時間の判定
    time_Sche_num = len(bus_Sche_time)
    next_time = ""
    bus_depa_time = ""
    bus_arr_time = ""
    i = 0
    if info == "":
        while i < time_Sche_num:
            #出発時刻
            #print(bus_Sche_time)
            Sche_depa_hour = bus_Sche_time[i][0]
            Sche_depa_min = bus_Sche_time[i][1]
            if int(Sche_depa_hour) > hour or (int(Sche_depa_hour) == hour and int(Sche_depa_min) >= minute):
                #到着予定時刻
                Sche_arr_hour = bus_Sche_time[i][2]
                Sche_arr_min = bus_Sche_time[i][3]
                #カウントダウン計算
                hour_sec_now = hour * 60 * 60
                minute_sec_now = minute * 60
                all_sec_now = hour_sec_now + minute_sec_now + second
                hour_sec_bus = int(Sche_depa_hour) * 60 * 60
                minute_sec_bus =int(Sche_depa_min) * 60
                all_sec_bus = hour_sec_bus + minute_sec_bus + 0
                all_sec = all_sec_bus - all_sec_now
                next_hour = (all_sec // 60) // 60
                next_min = all_sec // 60 - (next_hour * 60)
                next_sec = all_sec - (next_min * 60) - (next_hour * 60 * 60)
                #GUI表示
                next_time = f'{next_hour}時間{next_min}分{next_sec}秒'
                bus_depa_time = f'{Sche_depa_hour}時{Sche_depa_min}分'
                bus_arr_time = f'{Sche_arr_hour}時{Sche_arr_min}分'
                break
            i += 1
        if time_Sche_num == 0:
            info = ""
        elif time_Sche_num == i:
            info = "本日の運航は終了しました"
    elif info == "本日の運航は終了しました":
        if time_Sche_num > i:
            info = ""
    return (next_time, bus_depa_time, bus_arr_time, info)

#mainループ
def main():
    next_time = ""
    year, month, day, bus23to65, bus65to23, info = early()
    place = ""
    gui = GUI(info, place)
    win = gui.window
    bus_Sche_time = ""
    info_layout_1 , info_layout_2 , early_layout = 0, 0, 0
    while True:
        hour, minute, second, time_now = time_getter()
        #年,月,日の取得
        if hour == 0 and minute == 0 and second == 0:
            year, month, day, bus23to65, bus65to23, info = early()
            win.close()
            gui = GUI(info, place)
            win = gui.window
        today = f'{year}年{month}月{day}日'
        print(today)
        print(time_now)
        # print(bus23to65)
        # print(bus65to23)
        eve, val = win.read(timeout=0.1)
        if eve == sg.WINDOW_CLOSED:
            break
        elif eve == "-PULL-":
            place = val["-PULL-"]
            if place == '23号館→65号館':
                bus_Sche_time = bus23to65
            else:
                bus_Sche_time = bus65to23
            next_time, bus_depa_time, bus_arr_time, info = next_bus_time(bus_Sche_time, hour, minute, second, info)
            while early_layout != 1:
                win.close()
                gui = GUI(info, place)
                win = gui.window
                early_layout += 1
        # print(bus_Sche_time)
        next_time, bus_depa_time, bus_arr_time, info = next_bus_time(bus_Sche_time, hour, minute, second, info)
        # print(f"info={info}")
        win["-TODAY-"].update(today)
        win["-CLOCK-"].update(time_now)
        if info == "本日は運休です":
            while info_layout_1 != 1:
                win.close()
                gui = GUI(info, place)
                win = gui.window
                info_layout_1 += 1
            win["-info-"].update(info)
        elif info == "本日の運航は終了しました":
            while info_layout_2 != 1:
                win.close()
                gui = GUI(info, place)
                win = gui.window
                info_layout_2 += 1
            win["-info-"].update(info)
        elif early_layout != 0:
            info_layout_1 = 0
            info_layout_2 = 0
            win["-BUS_DEPA_TIME-"].update(bus_depa_time)
            win["-BUS_ARR_TIME-"].update(bus_arr_time)
            win["-NEXT_TIME-"].update(next_time)

if __name__ == '__main__':
    main()