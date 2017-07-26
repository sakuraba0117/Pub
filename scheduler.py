# -*- coding:utf-8 -*-

#メモ書き：月ごとに31日分の格納先を持つデータベースを作成し、
#日にちをクリックするとその日のスケジュールのタイトルとスケジュール追加ボタンを表示。
#   画面:左上に戻るボタン、真ん中にリスト、右下にスケジュール追加 とか
#タイトルをクリックすると、スケジュール詳細を表示
#   左上に戻るボタン
#月ごとの遷移はサンプルプログラムそのままで問題なかった。

#カレンダー→指定日の予定一覧
#   渡す値は年と月と日。データベースにアクセスし、
#   年と月と日が一致するデータがあればデータベース側からタイトルとそのデータのIDを受け取る。そしてタイトルを上から表示。
#   タイトルがある領域を押された場合は、そのデータのIDを渡し値として予定詳細を表示
#   戻るボタンを押された際は、年と月と日を渡し値としてmycalender.createcalendar(年、月)
#   スケジュール追加ボタンが押された際は、年、月、日のデータを渡し値としてスケジュール追加画面へ移行。

#指定日の予定一覧→スケジュール追加画面
#   渡し値は年と月と日。タイトル、時間、場所、コメントのテキスト記入画面を追加。
#   記入後(少なくともタイトルが空でない状態)に完了ボタンが押されたら、データベースに内容を追加して予定一覧へ戻る
#   単に戻るボタンが押された場合は、記入内容すべてを空にして予定一覧に戻る。
#       上記の二行、いずれも渡し値は年と月と日

#指定日の予定→予定詳細
#   渡す値は、選択されたデータのID。そのデータのIDをもとに、年、月、日、該当データの時間、場所、コメントを受け取る。
#   受け取ったデータをもとに画面にそれらを上から表示。
#   戻るボタンを押された際は年、月、日のデータから該当する日の予定一覧を表示。

#必要データまとめ →データとなる要素：年 integer,月 integer,日 integer,タイトル varchar,時間 varchar,場所 varchar,コメント varchar, 年のところ、デフォルトはその年
#port_list.db内に"calender"テーブル作成。上記の順番通りにデータが入っているので、こちらをデータ参照


#------------------------------------------しんちょーく
#0717 もろもろ操作するっぽい関数を作成。
#特定の予定詳細表示は多分これで動くが、コンパイルエラーが出たら面倒なのでコメントアウト。
#ざっくり考察：d_buttonの引数にmonthとdayを設定。ボタンが押されたら、self.destroyしてday_schedule(year,month,day)したら
#   その日の予定が画面に出るはず→daylist_sampleで年月日指定してデータを呼び出すことができた
#   そちらを参照


import tkinter as tk
import datetime
import sqlite3

#日をボタンで選択した際の処理関数

#def detail_one(year,month,day,title,time,place,comment):
#    def back_button():
#        root.destroy()
#        day_schedule(year,month,day)
#    root = tk.Tk()
#    root.title("予定詳細")
#    frame = tk.Frame(root,bd=2,relief="ridge")
#    frame.pack(fill="x")
#    button = tk.Button(frame,text="戻る",command=back_button)
#    button.pack()

#    frame1=tk.Frame(root,pady=10)
#    frame1.pack()
#    label=tk.Label(frame1,text="タイトル")
#    label.pack(side="left")
#    label1=tk.Label(frame1,text=title,background='white')
#    label1.pack(side="left")

#    frame2=tk.Frame(root,pady=10)
#    frame2.pack()
#    label2=tk.Label(frame2,text="時間")
#    label2.pack(side="left")
#    label3=tk.Label(frame2,text=time,background='white')
#    label3.pack(side="left")

#    frame3=tk.Frame(root,pady=10)
#    frame3.pack()
#    label4=tk.Label(frame3,text="場所")
#    label4.pack(side="left")
#    label5=tk.Label(frame3,text=place,background='white')
#    label5.pack(side="left")

#    frame4=tk.Frame(root,pady=10)
#    frame4.pack()
#    label6=tk.Label(frame4,text="メモ書き")
#    label6.pack(side="left")
#    frame5=tk.Frame(root,pady=5)
#    frame5.pack()
#    label7=tk.Label(frame5,text=comment,background='white',wrap=tk.WORD)
#    label7.pack(side="left")
    

def day_schedule(year,month,day):
    def back_button():
        root.destroy()
    def append_item():
        root.destroy()
    def item_selected(number):
        sql = "SELECT * from schedule where rowid=%d"
        conn.execute(sql,number)
        data=c.fetchall()
        root.destroy()
    root=tk.Tk()
    root.title("%d年%d月%d日 予定一覧"% (year,month,day))

    c=sqlite3.connect("post_test.db")
    conn= c.cursor()
    conn.execute("SELECT title,time from schedule where year = %d AND month = %d AND day = %d"%(year,month,day))
    data = conn.fetchall();

    #frame=tk.Frame(root,bd=2,relief="ridge")
    #frame.pack()
    button=tk.Button(root,text="戻る",command=back_button)
    button.pack(anchor="nw")
    
    frame1 = tk.Frame(root,pady=10)
    frame1.pack(anchor=tk.N)
    listbox = tk.Listbox(frame1)
    listbox.pack(side="top")
    listbox.bind("<Double-Button-1>",)
    #データ数のくくりは、dataの長さの半分。それぞれセットにしてリストボックスへ出力
    print(len(data))
    for i in range(0,(len(data))):
        words = data[i]
        listbox.insert(tk.END, words)

    frame2 = tk.Frame(root,pady=10)
    frame2.pack(anchor=tk.S)
    button = tk.Button(frame2,text="予定追加",command=append_item)
    button.pack(side="right")
        
        
        

# カレンダーを作成するフレームクラス
class mycalendar(tk.Frame):
    def __init__(self,master=None,cnf={},**kw):
        "初期化メソッド"
        import datetime
        tk.Frame.__init__(self,master,cnf,**kw)
        
        # 現在の日付を取得
        now = datetime.datetime.now()
        # 現在の年と月を属性に追加
        self.year = now.year
        self.month = now.month

        # frame_top部分の作成
        frame_top = tk.Frame(self)
        frame_top.pack(pady=5)
        self.previous_month = tk.Label(frame_top, text = "<", font = ("",14))
        self.previous_month.bind("<1>",self.change_month)
        self.previous_month.pack(side = "left", padx = 10)
        self.current_year = tk.Label(frame_top, text = self.year, font = ("",18))
        self.current_year.pack(side = "left")
        self.current_month = tk.Label(frame_top, text = self.month, font = ("",18))
        self.current_month.pack(side = "left")
        self.next_month = tk.Label(frame_top, text = ">", font = ("",14))
        self.next_month.bind("<1>",self.change_month)
        self.next_month.pack(side = "left", padx = 10)

        # frame_week部分の作成
        frame_week = tk.Frame(self)
        frame_week.pack()
        button_mon = d_button(frame_week, text = "Mon")
        button_mon.grid(column=0,row=0)
        button_tue = d_button(frame_week, text = "Tue")
        button_tue.grid(column=1,row=0)
        button_wed = d_button(frame_week, text = "Wed")
        button_wed.grid(column=2,row=0)
        button_thu = d_button(frame_week, text = "Thu")
        button_thu.grid(column=3,row=0)
        button_fri = d_button(frame_week, text = "Fri")
        button_fri.grid(column=4,row=0)
        button_sta = d_button(frame_week, text = "Sat", fg = "blue")
        button_sta.grid(column=5,row=0)
        button_san = d_button(frame_week, text = "San", fg = "red")
        button_san.grid(column=6,row=0)

        # frame_calendar部分の作成
        self.frame_calendar = tk.Frame(self)
        self.frame_calendar.pack()

        # 日付部分を作成するメソッドの呼び出し
        self.create_calendar(self.year,self.month)

    def create_calendar(self,year,month):
        "指定した年(year),月(month)のカレンダーウィジェットを作成する"
        
        
        # calendarモジュールのインスタンスを作成
        import calendar
        #前に書かれていた要素の削除
        try:
                for key,item in self.day.items():
                    item.destroy()
        except:
            pass
        cal = calendar.Calendar()
        # 指定した年月のカレンダーをリストで返す
        days = cal.monthdayscalendar(year,month)

        # 日付ボタンを格納する変数をdict型で作成
        self.day = {}
        # for文を用いて、日付ボタンを生成
        for i in range(0,42):
            c = i - (7 * int(i/7))
            r = int(i/7)
            try:
                # 日付が0でなかったら、ボタン作成 cが曜日、rが週目
                if days[r][c] != 0:#祝日判定→あかんこれn週目の月曜日とかの判別できてへん… 月毎にn回目の月曜日を判定すればよい？
                    if (((self.month==1 and days[r][c]==1)or(self.month==1 and c==0 and r==1)or
                         (self.month==2 and days[r][c]==11)or(self.month==3 and days[r][c]==21)or
                         (self.month==4 and days[r][c]==29)or(self.month==5 and (days[r][c]==3 or days[r][c]==4 or days[r][c]==5))or
                         (self.month==7 and c==0 and r==3)or(self.month==8 and days[r][c]==11)or(self.month==9 and c==0 and r==3)or
                         (self.month==9 and days[r][c]==23)or(self.month==10 and r==2 and c==0)or(self.month==11 and days[r][c]==3)or
                         (self.month==11 and days[r][c]==23)or(self.month==12 and days[r][c]==23))and c!=5 and c!=6):
                        self.day[i] = d_button(self.frame_calendar,text = days[r][c],fg="red")
                        self.day[i].grid(column=c,row=r)
                    else:
                        self.day[i] = d_button(self.frame_calendar,text = days[r][c])
                        self.day[i].grid(column=c,row=r)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break

    def change_month(self,event):
        if event.widget["text"]=="<":
            self.month-=1
        else:
            self.month+=1
        if(self.month==0):
            self.year-=1
            self.month=12
        elif self.month==13:
            self.year+=1
            self.month=1
        self.current_year["text"]=self.year
        self.current_month["text"]=self.month
        self.create_calendar(self.year,self.month)

# デフォルトのボタンクラス
class d_button(tk.Button):
    def __init__(self,master=None,cnf={},**kw):
        tk.Button.__init__(self,master,cnf,**kw)
        self.configure(font=("",14),height=2, width=4, relief="flat")
            
# ルートフレームの定義      
root = tk.Tk()
root.title("Calendar App")
mycal = mycalendar(root)
mycal.pack()
root.mainloop()
