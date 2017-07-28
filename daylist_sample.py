#0717 サンプルで作った関数
#年・月・日データからその日の分で登録されている予定のタイトルを呼び出す。
#引数を、カレンダー本体のyear,month＋押された日のボタンを参照してやれば予定一覧出力はできる。
#back_buttonが押されたら、年＋月を参照して再度calendarを生成すればよさげ
#listboxの要素はダブルクリックで反応してくれているので、その後の処理を見出す

#0728 クラス実装を投げ捨てて関数だけでどうにかしようとしたやつ
#月ごとのカレンダーの部分を追加実装。動きに不備なし

#0728翌月、前月への切り替え以外は実装したもの

#0728 nonlocalを用いて、翌月・前月への切り替えを実装。
#前の月のアイテム削除ができていないので要修正

import tkinter as tk
import datetime
import sqlite3
import calendar

day = 0

def immediately(li):
    print(li.curselection())

def prnt(txt):
    print(txt)

#予定詳細
def plan_detail(year,month,days):
    def back_button():
        root.destroy()
        day_schedule(year,month,days)
    def quit_button():
        root.destroy()
    root=tk.Tk()
    root.title(title + "予定詳細")
    button=tk.Button(root,text="戻る",command=back_button)
    button.pack(anchor="nw")
    label1 = tk.Label(root,text=days,background='white')
    label1.pack()
    label5 = tk.Label(root,text=title,background='white',pady=10)
    label5.pack()
    label2 = tk.Label(root,text=time,background='white',pady=10)
    label2.pack()
    label3 = tk.Label(root,text=place,background='white',pady=10)
    label3.pack()
    label4 = tk.Label(root,text=memo,background='white',pady=10)
    label4.pack()

#予定追加
def plan_adding(year,month,day):
    today = datetime.datetime.now()
    def registrate():
        c=sqlite3.connect("post_test.db")
        conn=c.cursor()
        e_year = entry_y.get()
        if(e_year==''):
            e_year = str(today.year)
        e_month = entry_m.get()
        if(e_month==''):
            e_month = str(today.month)
        e_day = entry_d.get()
        if(e_day==''):
            e_day = str(today.day)
        title = entry_n.get()
        time = entry_tm.get()
        place = entry_p.get()
        memo = entry_m.get()
        root.destroy()
        conn.execute("insert into schedule values(?,?,?,?,?,?,?)",(int(e_year),int(e_month),int(e_day),title,time,place,memo))
        c.commit()
        c.close()
        print("登録完了")
        day_schedule(year,month,day)
    def back_button():
        root.destroy()
        day_schedule(year,month,day)
    root=tk.Tk()
    root.title("予定追加")
    button=tk.Button(root,text="戻る",command=back_button)
    button.pack(anchor="nw")
    frame=tk.Frame(root,pady=5)
    frame.pack()
    label1=tk.Label(frame,text="年")
    label1.pack(side="left")
    entry_y=tk.Entry(frame,justify="left",width=10)
    entry_y.pack(side="left")
    frame1=tk.Frame(root,pady=5)
    frame1.pack()
    label2=tk.Label(frame1,text="月")
    label2.pack(side="left")
    entry_m=tk.Entry(frame1,justify="left",width=10)
    entry_m.pack(side="left")
    frame2=tk.Frame(root,pady=5)
    frame2.pack()
    label3=tk.Label(frame2,text="日")
    label3.pack(side="left")
    entry_d=tk.Entry(frame2,justify="left",width=10)
    entry_d.pack(side="left")
    frame3=tk.Frame(root,pady=5)
    frame3.pack()
    label4=tk.Label(frame3,text="タイトル")
    label4.pack(side="left")
    entry_n=tk.Entry(frame3,justify="left",width=15)
    entry_n.pack(side="left")
    frame4=tk.Frame(root,pady=5)
    frame4.pack()
    label5=tk.Label(frame4,text="時間")
    label5.pack(side="left")
    entry_tm=tk.Entry(frame4,justify="left",width=15)
    entry_tm.pack(side="left")
    frame5=tk.Frame(root,pady=5)
    frame5.pack()
    label6=tk.Label(frame5,text="場所")
    label6.pack(side="left")
    entry_p=tk.Entry(frame5,justify="left",width=15)
    entry_p.pack(side="left")
    frame7=tk.Frame(root,pady=5)
    frame7.pack()
    label7=tk.Label(frame7,text="メモ")
    label7.pack(side="left")
    frame8=tk.Frame(root)
    frame8.pack()
    entry_p=tk.Entry(frame8,justify="left",width=30)
    entry_p.pack(side="left")
    frame6=tk.Frame(root,pady=5)
    frame6.pack()
    button_reg = tk.Button(frame6,text="登録",command=registrate)
    button_reg.pack()

def month_calendar(year=datetime.datetime.now().year,month=datetime.datetime.now().month):
    def pre_month(event):
        nonlocal year
        nonlocal month
        month = month - 1
        if(month==0):
            year=year-1
            month=12
        current_year["text"]=year
        current_month["text"]=month
        create_calendar(year,month)

    def n_month(event):
        nonlocal year
        nonlocal month
        month=month+1
        if(month==13):
            year=year+1
            month=1
        current_year["text"]=year
        current_month["text"]=month
        create_calendar(year,month)

    
    def dcall(event):
        day = event.widget["text"]
        print(day)
        root.destroy()
        day_schedule(year,month,day)
    def create_calendar(year,month):
        try:
            for key,item in day.items():
                item.destroy()
        except:
            pass
        cal=calendar.Calendar()
        days=cal.monthdayscalendar(year,month)
        day={}
        for i in range(0,42):
            c = i - (7 * int(i/7))
            r = int(i/7)
            try:
                # 日付が0でなかったら、ボタン作成 cが曜日、rが週目
                if days[r][c] != 0:#祝日判定→あかんこれn週目の月曜日とかの判別できてへん… 月毎にn回目の月曜日を判定すればよい？
                    if (((month==1 and days[r][c]==1)or(month==1 and c==0 and r==1)or
                         (month==2 and days[r][c]==11)or(month==3 and days[r][c]==21)or
                         (month==4 and days[r][c]==29)or(month==5 and (days[r][c]==3 or days[r][c]==4 or days[r][c]==5))or
                         (month==7 and c==0 and r==3)or(month==8 and days[r][c]==11)or(month==9 and c==0 and r==3)or
                         (month==9 and days[r][c]==23)or(month==10 and r==2 and c==0)or(month==11 and days[r][c]==3)or
                         (month==11 and days[r][c]==23)or(month==12 and days[r][c]==23))and c!=5 and c!=6):
                        day[i] = tk.Button(frame_calendar,font=("",14),height=2,width=4,relief="flat",text = days[r][c],fg="red")
                        day[i].bind("<1>",dcall)
                        day[i].grid(column=c,row=r)
                    else:
                        day[i] = tk.Button(frame_calendar,font=("",14),height=2,width=4,relief="flat",text = days[r][c],command=dcall)
                        day[i].bind("<1>",dcall)
                        day[i].grid(column=c,row=r)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break
    root=tk.Tk()
    root.title("%d年%d月 カレンダー"%(year,month))
    frame_top=tk.Frame(root)
    frame_top.pack(pady=5)
    previous_month=tk.Label(frame_top,text="<",font=("",14))
    previous_month.bind("<1>",pre_month)
    previous_month.pack(side="left",padx=10)
    current_year=tk.Label(frame_top,text=year,font=("",18))
    current_year.pack(side="left")
    current_month=tk.Label(frame_top,text=month,font=("",18))
    current_month.pack(side="left")
    next_month=tk.Label(frame_top,text=">",font=("",14))
    next_month.bind("<1>",n_month)
    next_month.pack(side="left",padx=10)

    frame_week=tk.Frame(root)
    frame_week.pack()
    button_mon = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat",text = "Mon")
    button_mon.grid(column=0,row=0)
    button_tue = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat",text = "Tue")
    button_tue.grid(column=1,row=0)
    button_wed = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat",text = "Wed")
    button_wed.grid(column=2,row=0)
    button_thu = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "Thu")
    button_thu.grid(column=3,row=0)
    button_fri = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "Fri")
    button_fri.grid(column=4,row=0)
    button_sta = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "Sat", fg = "blue")
    button_sta.grid(column=5,row=0)
    button_san = tk.Button(frame_week,font=("",14),height=2,width=4,relief="flat", text = "San", fg = "red")
    button_san.grid(column=6,row=0)

    frame_calendar=tk.Frame(root)
    frame_calendar.pack()
    create_calendar(year,month)

def day_schedule(year,month,day):
    def back_button():
        root.destroy()
        month_calendar(year,month)
    def append_item():
        root.destroy()
        plan_adding(year,month,day)
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

    button=tk.Button(root,text="戻る",command=back_button)
    button.pack(anchor="nw")
    
    frame1 = tk.Frame(root,pady=10)
    frame1.pack(anchor=tk.N)
    listbox = tk.Listbox(frame1,selectmode='BROWSE')
    listbox.pack(side="top")
    
    #データ数のくくりは、dataの長さの半分。それぞれセットにしてリストボックスへ出力
    print(len(data))
    for i in range(0,(len(data))):
        words = data[i]
        listbox.insert(tk.END,words)
    item = map(int,listbox.curselection())
    listbox.bind('<<ListboxSelect>>',immediately(listbox))

    frame2 = tk.Frame(root,pady=10)
    frame2.pack(anchor=tk.S)
    button = tk.Button(frame2,text="予定追加",command=append_item)
    button.pack(side="right")
    root.mainloop()

date = datetime.datetime.now()
print(date.year)
month_calendar()
