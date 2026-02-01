import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import random
import time
import numpy as np
import sqlite3_users


class Aplication(ttk.Frame):
    def __init__(self, master=None):
        super().__init__()
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.click_close)
        sqlite3_users.open_file()
        self.login()

    def create_app(self):
        self.create_variable()
        self.create_wigets()
        self.create_menu()
        self.constant_credit()

    # ログインシステム
    def login(self):
        self.window_login = tk.Toplevel()
        self.window_login.geometry("300x100")
        self.window_login.protocol("WM_DELETE_WINDOW", self.check_number)
        self.window_login.resizable(False, False)
        self.window_login.title("ログイン")
        label = tk.Label(self.window_login, text="学生番号：", font=("", 14))
        self.id_entry = tk.Entry(self.window_login, font=("", 14), width=10)
        self.id_entry.focus()
        button = tk.Button(
            self.window_login, text="ログイン", font=("", 14), command=self.check_number
        )
        self.id_entry.bind("<Return>", self.check_number)
        label.grid(row=0, column=0)
        self.id_entry.grid(row=0, column=1)
        button.grid(row=0, column=2)
        self.window_login.grab_current()
        self.window_login.grab_set()

    def check_number(self, event=None):
        if len(self.id_entry.get()) == 5:
            self.id = self.id_entry.get()
            self.window_login.destroy()
            self.master.title(f"Credit Clicker {self.id}")
            self.data = sqlite3_users.read_user(self.id)
            self.create_app()
        else:
            label = tk.Label(
                self.window_login,
                text="正しい学生番号を入力してください",
                font=("", 12),
                fg="RED",
            )
            label.grid(row=1, column=0, columnspan=3)

    def create_variable(self):
        # 各施設の名前
        self.store_name = (
            "USBメモリ",
            "関数電卓",
            "オシロスコープ",
            "ノートパソコン",
            "定期試験",
            "TOEIC",
            "インターンシップ",
            "卒業研究",
            "ノーベル賞",
            "タイムマシン",
        )
        # 各施設の所持数(初期値=0)
        self.store_num = np.array(
            [self.data[f"store_{i}"] for i in range(10)], dtype=np.int64
        )
        # 各施設の購入価格(初期値),+1ごとに1.15倍
        self.store_cost = (
            np.array(
                [
                    15,
                    100,
                    400,
                    2500,
                    12000,
                    55000,
                    250000,
                    1777777,
                    133333333,
                    44000000000,
                ]
            )
            * 1.15**self.store_num
        )
        # 各施設のランク(初期値=0)
        self.item_power = np.array(
            [self.data[f"store_level_{i}"] for i in range(10)], dtype=np.int64
        )
        # 各施設の強化アイテム
        self.item_power_list = np.array([1, 2, 40, 8000])
        self.item_cost_1 = np.array(
            [
                150,
                1000,
                4000,
                25000,
                120000,
                550000,
                2500000,
                17777770,
                1333333330,
                440000000000,
            ],
            dtype=np.int64,
        )
        self.item_cost_2 = np.array(
            [
                15000,
                100000,
                400000,
                2500000,
                12000000,
                55000000,
                250000000,
                1777777000,
                133333333000,
                2500000000000,
            ],
            dtype=np.int64,
        )
        self.item_cost_3 = np.array(
            [
                15000000,
                100000000,
                400000000,
                2500000000,
                12000000000,
                55000000000,
                250000000000,
                800000000000,
                4000000000000,
                10000000000000,
            ],
            dtype=np.int64,
        )

        self.rein = self.data["reincarnation"]
        self.rein_power = 1.2**self.rein

        # 各施設のCps
        self.store_cps = (
            np.array([0.1, 0.5, 2, 10, 40, 100, 400, 6666, 200000, 1200000])
            * self.rein_power
        )
        # 各施設の情報
        self.str_store_info = [
            tk.StringVar(
                value=f"{self.store_name[i]} ×{int(self.store_num[i]):,}\nCps {self.store_cps[i]*self.item_power_list[self.item_power[i]]: ,.1f}\n\\{int(self.store_cost[i]): ,}"
            )
            for i in range(10)
        ]

        # マウスクリック強化
        self.mouse_cost = np.array([1, 5000, 500000, 50000000, 5000000000])
        self.mouse_cpc = np.array([0, 1, 20, 400, 10000, 1000000])
        self.mouse_level = self.data["click_level"]
        self.num_cps = (
            sum(self.store_cps * self.store_num * self.item_power_list[self.item_power])
            * self.rein_power
        )
        self.str_cps = tk.StringVar(value=f"{self.num_cps:,.1f} Cps")
        if int(time.time() - self.data["lastdate"]) > 60 * 60 * 12:
            self.add_credit = self.num_cps * 60 * 60 * 12 * 0.5
        else:
            self.add_credit = (
                self.num_cps * int(time.time() - self.data["lastdate"]) * 0.5
            )
        self.num_credit = int(self.data["num_credit"]) + self.add_credit
        self.str_credit = tk.StringVar(value=f"{self.num_credit: ,.1f}" + " 単位")
        self.num_cpc = self.mouse_cpc[self.mouse_level] * self.rein_power
        self.num_click_count = tk.IntVar(value=self.data["click_count"])
        self.fevertime = False
        self.click_effect = 0
        if self.num_credit >= 10000 * 100**self.rein:
            self.reinable = True
        else:
            self.reinable = False
        if self.add_credit:
            info = tk.messagebox.showinfo(
                "単位取得",
                f"放置している間に\n{self.add_credit: ,.1f} 単位を取得しました",
            )

    def create_wigets(self):
        self.win_width = int(self.master.winfo_screenwidth() / 5)
        self.win_height = int(self.master.winfo_screenheight())
        self.frame_left = tk.Frame(
            self.master,
            bd=2,
            relief="groove",
            width=self.win_width * 2,
            height=self.win_height,
        )
        self.frame_right = tk.Frame(
            self.master,
            bd=2,
            relief="groove",
            width=self.win_width * 3,
            height=self.win_height,
        )
        self.frame_left.grid(row=0, column=0)
        self.frame_right.grid(row=0, column=1)
        self.frame_left.propagate(False)
        self.frame_right.propagate(False)
        self.create_frame_left()
        self.create_frame_right()

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        menu1 = tk.Menu(self.menu)
        self.menu.add_cascade(label="アカウント", menu=menu1)
        menu1.add_command(label="ログアウト", command=self.logout)
        menu1.add_command(label="データ削除", command=self.delete)

    def create_frame_left(self):
        self.canvas_left = tk.Canvas(
            self.frame_left, width=self.win_width * 2, height=self.win_height
        )
        self.canvas_left.pack()
        self.image_credit = tk.PhotoImage(file="image\\creditpan.png")
        self.image_credit_clicked = tk.PhotoImage(file="image\\creditpan_clicked.png")
        self.button_click = self.canvas_left.create_image(
            30, 130, image=self.image_credit, anchor="nw", tag="img_credit"
        )

        self.canvas_left.tag_bind("img_credit", "<Button-1>", self.click_credit)
        self.master.bind("<space>", self.click_credit)
        self.text_cps = self.canvas_left.create_text(
            220, 105, text=self.str_cps.get(), tag="text_cps", font=("", 25)
        )
        self.text_credit = self.canvas_left.create_text(
            220, 60, text=self.str_credit.get(), tag="text_credit", font=("", 28)
        )
        style_click_count = ttk.Style()
        style_click_count.configure("CC.TProgressbar")
        self.click_count = ttk.Progressbar(
            self.canvas_left,
            orient="horizontal",
            variable=self.num_click_count,
            maximum=100,
            mode="determinate",
            length=390,
        )
        self.image_report = tk.PhotoImage(file="image\\report.png").subsample(2, 2)
        self.button_fever = tk.Button(
            self.canvas_left,
            text="提出",
            image=self.image_report,
            compound="top",
            command=self.change_fever,
            state=tk.DISABLED,
            font=("Times", 18),
            padx=5,
            relief="groove",
            cursor="hand2",
        )
        if self.num_click_count.get() >= 100:
            self.button_fever["state"] = tk.NORMAL
        self.button_rein = tk.Button(
            self.canvas_left,
            text="留年可能!!",
            font=("", 24),
            state=tk.NORMAL,
            fg="RED",
            relief="raised",
            bd=5,
            command=self.reincarnation,
        )
        if self.reinable:
            self.button_rein.place(x=165, y=548)
        self.master.bind("<Return>", self.change_fever)
        self.click_count.place(x=10, y=0)
        self.button_fever.place(x=415, y=0)
        self.button_mouse = [0] * 5
        self.image_mouse = [0] * 5
        for i in range(5):
            self.image_mouse[i] = tk.PhotoImage(file=f"image\\mouse_{i}.png")
            self.button_mouse[i] = tk.Button(
                self.canvas_left,
                text=f"クリックレベル{i+1}\n\\{self.mouse_cost[i]:,}",
                command=partial(self.buy_mouse, i),
                width=90,
                image=self.image_mouse[i],
                compound="top",
                state=tk.DISABLED,
                font=("", 10),
                cursor="hand2",
            )
            self.button_mouse[i].place(x=i * 101, y=615)
            if self.mouse_level > i:
                self.button_mouse[i]["relief"] = "solid"
                self.button_mouse[i]["state"] = tk.DISABLED

    def create_frame_right(self):
        self.frame_store = []
        self.button_store = []
        self.frame_item = []
        self.label_store = []
        self.text_store = []
        self.image_store = []
        self.button_item_1 = [0] * 10
        self.button_item_2 = [0] * 10
        self.button_item_3 = [0] * 10
        self.scrollbar_right = ScrollableFrame(master=self.frame_right)
        style_store = ttk.Style()
        style_store.configure("BF.TLabel", font=(None, 24))
        style_frame = ttk.Style()
        style_frame.configure("BF.TFrame", background="WHITE")
        for i in range(10):
            self.frame_store.append(
                ttk.Frame(
                    self.scrollbar_right.frame,
                    style="BF.TFrame",
                    relief="groove",
                    width=500,
                    height=100,
                )
            )
            self.frame_store[i].grid_propagate(True)
            self.frame_store[i].grid(row=i, column=0)
            self.image_store.append(tk.PhotoImage(file=f"image\store_{i}.png"))
            self.button_store.append(
                tk.Button(
                    self.frame_store[i],
                    textvariable=self.str_store_info[i],
                    text=self.str_store_info[i].get(),
                    font=("", 17),
                    command=partial(self.buy_store, i),
                    cursor="hand2",
                    relief="groove",
                )
            )
            self.button_store[i].configure(
                image=self.image_store[i], compound="left", width=380
            )
            self.button_store[i].grid(row=0, column=0, padx=3, pady=3)
            self.button_item_1[i] = tk.Button(
                self.frame_store[i],
                command=partial(self.buy_item, i, 1),
                width=14,
                height=6,
                state=tk.DISABLED,
                text=f"{self.store_name[i]} Lv.1\n必要：1\n\\{self.item_cost_1[i]:,}",
                cursor="hand2",
            )
            self.button_item_2[i] = tk.Button(
                self.frame_store[i],
                command=partial(self.buy_item, i, 2),
                width=14,
                height=6,
                state=tk.DISABLED,
                text=f"{self.store_name[i]} Lv.2\n必要：20\n\\{self.item_cost_2[i]:,}",
                cursor="hand2",
            )
            self.button_item_3[i] = tk.Button(
                self.frame_store[i],
                command=partial(self.buy_item, i, 3),
                width=14,
                height=6,
                state=tk.DISABLED,
                text=f"{self.store_name[i]} Lv.3\n必要：100\n\\{self.item_cost_3[i]:,}",
                cursor="hand2",
            )
            self.button_item_1[i].propagate(False)
            self.button_item_1[i].propagate(False)
            self.button_item_1[i].propagate(False)
            self.button_item_1[i].grid(row=0, column=i + 1, padx=3, pady=3)
            self.button_item_2[i].grid(row=0, column=i + 2, padx=3, pady=3)
            self.button_item_3[i].grid(row=0, column=i + 3, padx=3, pady=3)
            if self.item_power[i] >= 1:
                self.button_item_1[i]["relief"] = "solid"
                self.button_item_1[i]["state"] = tk.DISABLED
            if self.item_power[i] >= 2:
                self.button_item_2[i]["relief"] = "solid"
                self.button_item_2[i]["state"] = tk.DISABLED
            if self.item_power[i] >= 3:
                self.button_item_3[i]["relief"] = "solid"
                self.button_item_3[i]["state"] = tk.DISABLED

        self.scrollbar_right.canvas.create_window(
            (0, 0), window=self.scrollbar_right.frame, anchor="nw"
        )
        self.is_buyable()

    # 単位パンをクリックしたときに呼び出す
    # クリックで増える単位の数だけ所持単位に加算
    # is_variableの呼び出し
    def click_credit(self, event=None):
        def resize():
            self.canvas_left.itemconfigure(self.button_click, image=self.image_credit)

        def delete_text(x):
            self.canvas_left.delete(f"plus_credit{x}")

        if self.fevertime:
            self.num_credit = self.num_credit + (self.num_cpc) * 3
        else:
            self.num_credit = self.num_credit + self.num_cpc
            self.num_click_count.set(self.num_click_count.get() + 1)
            if self.num_click_count.get() >= 100:
                self.num_click_count.set(100)
                self.button_fever["state"] = tk.NORMAL

        self.str_credit.set(f"{self.num_credit: ,.1f}" + " 単位")
        self.canvas_left.create_text(
            random.randint(50, 410),
            random.randint(150, 550),
            text=f"単位 +{self.num_cpc:,.1f}",
            tag=f"plus_credit{self.click_effect}",
            font=("", 20),
        )
        self.canvas_left.itemconfigure(
            self.button_click, image=self.image_credit_clicked
        )
        self.canvas_left.tag_bind(
            f"plus_credit{self.click_effect}", "<Button-1>", self.click_credit
        )
        self.canvas_left.after(50, resize)
        self.canvas_left.after(1000, partial(delete_text, self.click_effect))
        self.click_effect += 1

    def buy_mouse(self, i):
        self.num_credit -= self.mouse_cost[i]
        self.mouse_level = i + 1
        self.num_cpc = self.mouse_cpc[self.mouse_level]
        self.button_mouse[i]["relief"] = "solid"
        self.button_mouse[i]["state"] = tk.DISABLED

    # ストアで購入した際の処理
    # 購入に必要な値段を1.15倍する(整数に直す)
    def buy_store(self, i):
        self.store_num[i] += 1
        self.num_credit -= self.store_cost[i]
        self.store_cost[i] *= 1.15
        self.str_store_info[i].set(
            f"{self.store_name[i]} ×{int(self.store_num[i]):,}\nCps {self.store_cps[i]*self.item_power_list[self.item_power[i]]: ,.1f}\n\\{int(self.store_cost[i]): ,}"
        )
        # self.num_cps = self.num_cps + self.store_cps[i]
        self.set_cps()

    def buy_item(self, i, num):
        self.item_power[i] = num
        # self.store_cps[i] = self.store_cps[i] * self.item_power_list[self.item_power[i]]
        if num == 1:
            self.num_credit -= self.item_cost_1[i]
            self.button_item_1[i]["relief"] = "solid"
            self.button_item_1[i]["state"] = tk.DISABLED
        if num == 2:
            self.num_credit -= self.item_cost_2[i]
            self.button_item_2[i]["relief"] = "solid"
            self.button_item_2[i]["state"] = tk.DISABLED
        if num == 3:
            self.num_credit -= self.item_cost_3[i]
            self.button_item_3[i]["relief"] = "solid"
            self.button_item_3[i]["state"] = tk.DISABLED
        self.set_cps()
        self.str_store_info[i].set(
            f"{self.store_name[i]} ×{int(self.store_num[i]):,}\nCps {self.store_cps[i]*self.item_power_list[self.item_power[i]]: ,.1f}\n\\{int(self.store_cost[i]): ,}"
        )

    def set_cps(self):
        self.num_cps = np.sum(
            self.store_cps * self.store_num * self.item_power_list[self.item_power]
        )
        self.str_cps.set(f"{self.num_cps: ,.1f} Cps")
        self.canvas_left.itemconfigure("text_cps", text=self.str_cps.get())

    def set_credit(self):
        self.str_credit.set(f"{self.num_credit: ,.1f} 単位")
        self.canvas_left.itemconfigure("text_credit", text=self.str_credit.get())

    # 0.1秒ごとに合計Cpsの1/10を足す
    def constant_credit(self):
        if self.fevertime:
            self.num_click_count.set(self.num_click_count.get() - 1)
            self.num_credit = self.num_credit + (self.num_cps / 10) * 3
            if self.num_click_count.get() <= 0:
                self.fevertime = False
        else:
            self.num_credit = self.num_credit + self.num_cps / 10
        self.set_credit()
        self.is_buyable()
        self.func_constant = self.master.after(90, self.constant_credit)

    def change_fever(self, event=None):
        if not self.fevertime and self.num_click_count.get() >= 100:
            self.fevertime = True
        self.button_fever["state"] = tk.DISABLED

    # ストア・アイテム・単位クリックの際に呼び出す
    # 所持単位と比べて買えるかどうかの判断
    def is_buyable(self):
        for i in range(10):
            if self.num_credit >= self.store_cost[i]:
                self.button_store[i]["state"] = tk.NORMAL
            else:
                self.button_store[i]["state"] = tk.DISABLED

            if (
                self.num_credit >= self.item_cost_1[i]
                and self.item_power[i] == 0
                and self.store_num[i] >= 1
            ):
                self.button_item_1[i]["state"] = tk.NORMAL
            else:
                self.button_item_1[i]["state"] = tk.DISABLED
            if (
                self.num_credit >= self.item_cost_2[i]
                and self.item_power[i] == 1
                and self.store_num[i] >= 20
            ):
                self.button_item_2[i]["state"] = tk.NORMAL
            else:
                self.button_item_2[i]["state"] = tk.DISABLED
            if (
                self.num_credit >= self.item_cost_3[i]
                and self.item_power[i] == 2
                and self.store_num[i] >= 100
            ):
                self.button_item_3[i]["state"] = tk.NORMAL
            else:
                self.button_item_3[i]["state"] = tk.DISABLED

            if i < 5:
                if self.num_credit >= self.mouse_cost[i] and self.mouse_level == i:
                    self.button_mouse[i]["state"] = tk.NORMAL
                else:
                    self.button_mouse[i]["state"] = tk.DISABLED
            if self.num_credit >= 10000 * 100**self.rein and not self.reinable:
                self.button_rein.place(x=165, y=550)

    def click_close(self):
        exit_yesno = tk.messagebox.askquestion(
            "アプリケーションの終了", "単位クリッカーを終了しますか？"
        )
        if exit_yesno == "yes":
            self.save()
            self.master.destroy()

    def save(self):
        self.master.after_cancel(self.func_constant)
        sqlite3_users.save_user(
            id=self.id,
            credit=self.num_credit,
            stores=list(map(int, self.store_num)),
            store_level=list(map(int, self.item_power)),
            click_level=self.mouse_level,
            click_count=self.num_click_count.get(),
            lastdate=int(time.time()),
            rein=self.rein,
        )
        sqlite3_users.close_file()

    def delete(self):
        delete_yesno = tk.messagebox.askquestion(
            title="アカウント削除",
            message="アカウントを削除しますか？\n※再ログインしてもデータは復元されません",
            icon="error",
        )
        if delete_yesno == "yes":
            self.master.after_cancel(self.func_constant)
            sqlite3_users.delete_user(self.id)
            sqlite3_users.close_file()
            self.master.destroy()
            main()

    def logout(self):
        logout_yesno = tk.messagebox.askquestion(
            "ログアウト", "ログアウトしますか？\n※再ログインすればデータは復元されます"
        )
        if logout_yesno == "yes":
            self.master.after_cancel(self.func_constant)
            self.save()
            self.master.destroy()
            main()

    def reincarnation(self):
        rein_yesno = tk.messagebox.askquestion(
            title="留年確認",
            message="""留年しますか？\n※留年すると所持単位、アイテムは全て初期化され、\n　次回以降の獲得単位数がすべて1.2倍になります。""",
            icon="error",
        )
        if rein_yesno == "yes":
            sqlite3_users.save_user(
                id=self.id,
                credit=1,
                stores=[0] * 10,
                store_level=[0] * 10,
                click_level=0,
                click_count=0,
                lastdate=int(time.time()),
                rein=self.rein + 1,
            )
            self.master.after_cancel(self.func_constant)
            sqlite3_users.close_file()
            self.master.destroy()
            main()


class ScrollableFrame(ttk.Frame):
    def __init__(self, master=None):
        self.master = master
        self.canvas = tk.Canvas(self.master)
        self.frame = tk.Frame(self.canvas)
        scrollbar = ttk.Scrollbar(
            self.canvas, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.canvas.configure(scrollregion=(0, 0, 0, 1220))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(expand=True, fill=tk.BOTH)


def main():
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("classic")
    root.state("zoomed")
    app = Aplication(root)
    app.mainloop()


if __name__ == "__main__":
    main()
