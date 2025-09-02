import datetime as dt
import time
import csv
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import platform

def get_japanese_font():
    available = set(tkFont.families())

    candidates = [
        # Windows
        "Yu Gothic UI", "Yu Gothic", "Meiryo", "MS PGothic", "MS UI Gothic",
        # macOS
        "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Hiragino Kaku Gothic Pro",
        # Linux
        "Noto Sans CJK JP", "Noto Sans JP", "IPAGothic", "VL Gothic", "TakaoGothic",
    ]
    for name in candidates:
        if name in available:
            return name
        
    return "TkDefaultFont"

def early():
    #初期データ入力(休暇は次を参照:https://www.kanazawa-it.ac.jp/about_kit/yatsukaho.html)
    #日付データ
    dt_now = dt.datetime.now()
    week = dt_now.weekday()#月:0,火:1,水:2,木:3,金:4,土:5,日:6
    year, month, day = dt_now.year, dt_now.month, dt_now.day

    #夏季休暇
    SmmS, SmdS = 8, 4   #夏季休暇始まり月, 日
    SmmF, SmdF = 9, 12  #夏季休暇終わり月, 日
    #春季休暇
    SpmS, SpdS = 3, 2   #春季休暇始まり月, 日
    SpmF, SpdF = 3, 31  #春季休暇終わり月, 日
    #祝日及びその他運休日(dayを変更)
    month4_7 = (month == 4 and day == 29) or (month == 5 and 3 <= day <= 6) or (month == 6 and day == 1) or (month == 7 and 19 <= day <= 21)
    month8_9 = (month == 8 and (day == 2 or 7 <= day <= 17 or day == 23 or day == 30)) or (month == 9 and (13 <= day <= 15 or 21 <= day <= 23))
    month10_12 = (month == 10 and (day == 13 or 18 <= day <= 19)) or (month == 11 and (day == 3 or day == 24)) or (month == 12 and 27 <= day <= 31)
    month1_3 = (month == 1 and (1 <= day <= 6 or day == 12)) or (month == 2 and (day == 11 or day == 23)) and (month == 3 and day == 20)
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
    def __init__(self, info, place, window_position=None):
        self.root = tk.Tk()
        # 日本語フォントの設定
        font_family = get_japanese_font()
        print(f"使用フォント: {font_family}")
        self.root.title("Bus Time")
        
        # スタイルの設定
        self.style = ttk.Style()
        self.style.configure('TLabel', font=(font_family, 10))
        self.style.configure('TCombobox', font=(font_family, 10))
        
        # デフォルトフォントの設定
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family=font_family, size=10)
        
        # ウィンドウ位置の設定
        if window_position:
            self.root.geometry(f"400x300+{window_position[0]}+{window_position[1]}")
        else:
            self.root.geometry("400x300")
            # 中央に配置
            self.root.update_idletasks()
            x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
            y = (self.root.winfo_screenheight() // 2) - (300 // 2)
            self.root.geometry(f"400x300+{x}+{y}")
        
        # ウィジェットの辞書を初期化
        self.widgets = {}
        
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 今日の日付表示
        ttk.Label(main_frame, text="今日は:", font=(font_family, 10)).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.widgets["-TODAY-"] = ttk.Label(main_frame, text="", font=(font_family, 10))
        self.widgets["-TODAY-"].grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # 現在時刻表示
        ttk.Label(main_frame, text="現在時刻:", font=(font_family, 10)).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.widgets["-CLOCK-"] = ttk.Label(main_frame, text="", font=(font_family, 10))
        self.widgets["-CLOCK-"].grid(row=1, column=1, sticky=tk.W, pady=2)
        
        if info == "本日は運休です" or info == "本日の運航は終了しました":
            # 運休情報表示
            self.widgets["-info-"] = ttk.Label(main_frame, text=info, foreground="red", font=(font_family, 10))
            self.widgets["-info-"].grid(row=2, column=0, columnspan=2, pady=10)
            self.root.geometry("400x150")
        elif place == '23号館→65号館' or place == '65号館→23号館':
            # ルート選択
            ttk.Label(main_frame, text="ルート:", font=(font_family, 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
            self.widgets["-PULL-"] = ttk.Combobox(main_frame, values=['23号館→65号館', '65号館→23号館'], 
                                                 state="readonly", width=25, font=(font_family, 10))
            self.widgets["-PULL-"].set(place)
            self.widgets["-PULL-"].grid(row=2, column=1, sticky=tk.W, pady=2)
            self.widgets["-PULL-"].bind('<<ComboboxSelected>>', self.on_route_change)
            
            # バス情報表示
            ttk.Label(main_frame, text="次のバスの時間は:", font=(font_family, 10)).grid(row=3, column=0, sticky=tk.W, pady=2)
            self.widgets["-BUS_DEPA_TIME-"] = ttk.Label(main_frame, text="", font=(font_family, 10))
            self.widgets["-BUS_DEPA_TIME-"].grid(row=3, column=1, sticky=tk.W, pady=2)
            
            ttk.Label(main_frame, text="到着予定時刻は:", font=(font_family, 10)).grid(row=4, column=0, sticky=tk.W, pady=2)
            self.widgets["-BUS_ARR_TIME-"] = ttk.Label(main_frame, text="", font=(font_family, 10))
            self.widgets["-BUS_ARR_TIME-"].grid(row=4, column=1, sticky=tk.W, pady=2)
            
            ttk.Label(main_frame, text="次のバスの時間まで:", font=(font_family, 10)).grid(row=5, column=0, sticky=tk.W, pady=2)
            self.widgets["-NEXT_TIME-"] = ttk.Label(main_frame, text="", foreground="blue", font=(font_family, 10))
            self.widgets["-NEXT_TIME-"].grid(row=5, column=1, sticky=tk.W, pady=2)
            
            self.root.geometry("400x250")
        else:
            # 初期状態（ルート選択のみ）
            ttk.Label(main_frame, text="ルート:", font=(font_family, 10)).grid(row=2, column=0, sticky=tk.W, pady=2)
            self.widgets["-PULL-"] = ttk.Combobox(main_frame, values=['23号館→65号館', '65号館→23号館'], 
                                                 state="readonly", width=25, font=(font_family, 10))
            self.widgets["-PULL-"].set('選択してください')
            self.widgets["-PULL-"].grid(row=2, column=1, sticky=tk.W, pady=2)
            self.widgets["-PULL-"].bind('<<ComboboxSelected>>', self.on_route_change)
            
            self.root.geometry("400x150")
    
    def on_route_change(self, event=None):
        """ルート変更時のイベントハンドラー"""
        pass  # メインループで処理

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
class BusTimeApp:
    def __init__(self):
        self.next_time = ""
        self.year, self.month, self.day, self.bus23to65, self.bus65to23, self.info = early()
        self.place = ""
        self.window_position = None  # ウィンドウ位置を保存
        self.gui = GUI(self.info, self.place, self.window_position)
        self.bus_Sche_time = ""
        self.info_layout_1, self.info_layout_2, self.early_layout = 0, 0, 0
        self.last_hour = -1
        self.last_minute = -1
        self.last_second = -1
        
        # 初期更新
        self.update_display()
        
        # 1秒ごとに更新
        self.gui.root.after(1000, self.update_loop)
        
        # ウィンドウクローズ時の処理
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def update_loop(self):
        """メインループの代わり"""
        hour, minute, second, time_now = time_getter()
        
        # 日付が変わった場合の処理
        if hour == 0 and minute == 0 and second == 0 and self.last_hour != 0:
            # 現在のウィンドウ位置を保存
            self.window_position = (self.gui.root.winfo_x(), self.gui.root.winfo_y())
            self.year, self.month, self.day, self.bus23to65, self.bus65to23, self.info = early()
            self.gui.root.destroy()
            self.gui = GUI(self.info, self.place, self.window_position)
            self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.info_layout_1, self.info_layout_2, self.early_layout = 0, 0, 0
        
        self.last_hour, self.last_minute, self.last_second = hour, minute, second
        
        # 表示更新
        self.update_display()
        
        # 次の更新をスケジュール
        self.gui.root.after(1000, self.update_loop)
    
    def update_display(self):
        """表示の更新"""
        hour, minute, second, time_now = time_getter()
        today = f'{self.year}年{self.month}月{self.day}日'
        
        # 基本情報の更新
        self.gui.widgets["-TODAY-"].config(text=today)
        self.gui.widgets["-CLOCK-"].config(text=time_now)
        
        # ルート選択の処理
        if "-PULL-" in self.gui.widgets:
            current_place = self.gui.widgets["-PULL-"].get()
            if current_place != self.place and current_place in ['23号館→65号館', '65号館→23号館']:
                # 現在のウィンドウ位置を保存
                self.window_position = (self.gui.root.winfo_x(), self.gui.root.winfo_y())
                self.place = current_place
                if self.place == '23号館→65号館':
                    self.bus_Sche_time = self.bus23to65
                else:
                    self.bus_Sche_time = self.bus65to23
                self.early_layout = 0
                # レイアウトを更新
                self.gui.root.destroy()
                self.gui = GUI(self.info, self.place, self.window_position)
                self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                self.early_layout = 1
        
        # バス時刻の計算と表示
        if self.bus_Sche_time:
            self.next_time, bus_depa_time, bus_arr_time, self.info = next_bus_time(
                self.bus_Sche_time, hour, minute, second, self.info)
            
            if self.info == "本日は運休です":
                if self.info_layout_1 != 1:
                    # 現在のウィンドウ位置を保存
                    self.window_position = (self.gui.root.winfo_x(), self.gui.root.winfo_y())
                    self.gui.root.destroy()
                    self.gui = GUI(self.info, self.place, self.window_position)
                    self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                    self.info_layout_1 = 1
                if "-info-" in self.gui.widgets:
                    self.gui.widgets["-info-"].config(text=self.info)
            elif self.info == "本日の運航は終了しました":
                if self.info_layout_2 != 1:
                    # 現在のウィンドウ位置を保存
                    self.window_position = (self.gui.root.winfo_x(), self.gui.root.winfo_y())
                    self.gui.root.destroy()
                    self.gui = GUI(self.info, self.place, self.window_position)
                    self.gui.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                    self.info_layout_2 = 1
                if "-info-" in self.gui.widgets:
                    self.gui.widgets["-info-"].config(text=self.info)
            elif self.early_layout != 0:
                self.info_layout_1 = 0
                self.info_layout_2 = 0
                if "-BUS_DEPA_TIME-" in self.gui.widgets:
                    self.gui.widgets["-BUS_DEPA_TIME-"].config(text=bus_depa_time)
                if "-BUS_ARR_TIME-" in self.gui.widgets:
                    self.gui.widgets["-BUS_ARR_TIME-"].config(text=bus_arr_time)
                if "-NEXT_TIME-" in self.gui.widgets:
                    self.gui.widgets["-NEXT_TIME-"].config(text=self.next_time)
    
    def on_closing(self):
        """ウィンドウクローズ時の処理"""
        self.gui.root.destroy()
    
    def run(self):
        """アプリケーションの実行"""
        self.gui.root.mainloop()

def main():
    app = BusTimeApp()
    app.run()

if __name__ == '__main__':
    main()