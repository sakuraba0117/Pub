#0717 サンプルで作った関数
#年・月・日データからその日の分で登録されている予定のタイトルを呼び出す。
#引数を、カレンダー本体のyear,month＋押された日のボタンを参照してやれば予定一覧出力はできる。
#back_buttonが押されたら、年＋月を参照して再度calendarを生成すればよさげ
#listboxの要素はダブルクリックで反応してくれているので、その後の処理を見出す

#main関数内部でmainloopを行っていると、関数内部でroot.destroyしても画面が閉じない様子。
#classを用いたオブジェクト指向は、ひとまずの実装が終わり次第整備したい。


import tkinter as tk
import datetime
import sqlite3


#詳細表示
def plan_detail(days,title,time,place,memo):
    def back_button():
        root.destroy()
        mycalender()
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
def plan_adding():
    today = datetime.datetime.now()
    def registrate():
        c=sqlite3.connect("post_test.db")
        conn=c.cursor()
        year = entry_y.get()
        if(year==''):
            year = str(today.year)
        month = entry_m.get()
        if(month==''):
            month = str(today.month)
        day = entry_d.get()
        if(day==''):
            day = str(today.day)
        title = entry_n.get()
        time = entry_tm.get()
        place = entry_p.get()
        memo = entry_m.get()
        root.destroy()
        conn.execute("insert into schedule values(?,?,?,?,?,?,?)",(int(year),int(month),int(day),title,time,place,memo))
        c.commit()
        c.close()
        print("登録完了")
        mycalender()
    def back_button():
        root.destroy()
        mycalender()
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

#immediately内部の処理を応用すれば、指定された予定の詳細表示ができる。
#printで出力しているテキストは出力内容確認用。テキストをそのまま引数にすれば、詳細表示で用いるインタフェースに流用できる。
def mycalender(year,month,day):

    def back_button():
        root.destroy()
    def append_list():
        root.destroy()
        plan_adding()
        
    def immediately(e):
        w = e.widget
        index = int (w.curselection()[0])
        value = w.get(index)
        print('You selected item %d : %s' % (index,value))

        c=sqlite3.connect("post_test.db")
        conn= c.cursor()
        conn.execute("SELECT * from schedule where rowid = %d"%value[2])
        detail = conn.fetchall()
        d=('予定日：'+ str(detail[0][0]) + '/' + str(detail[0][1]) + '/' + str(detail[0][2]))
        tit=('タイトル：'+ detail[0][3])
        tim=('時間：'+detail[0][4])
        pla=('場所：'+detail[0][5])
        mem=('メモ書き：\n'+detail[0][6])
        #↓rowidの取得
        #print(value[2])
        root.destroy()
        plan_detail(d,tit,tim,pla,mem)

    
    #↓予定一覧表示。
    date = datetime.datetime.now()
    print(date.year)
    root=tk.Tk()
    root.title("%d年%d月%d日現在 登録済予定一覧"% (date.year,date.month,date.day))

    c=sqlite3.connect("post_test.db")
    conn= c.cursor()
    #conn.execute("SELECT title,time,rowid from schedule")
    conn.execute("SELECT title,time from schedule where year = %d AND month = %d AND day = %d"%(year,month,day))
    data = conn.fetchall();

    button=tk.Button(root,text="戻る",command=back_button)
    button.pack(anchor="nw")
       
    frame1 = tk.Frame(root,pady=10)
    frame1.pack(anchor=tk.N)
    listbox = tk.Listbox(frame1,selectmode='BROWSE')
    listbox.pack(side="top")

    #fetchallでデータベースから受け取ったデータをリストボックスへ格納
    print(len(data))
    for i in range(0,(len(data))):
        words = data[i]
        listbox.insert(tk.END,words)
    item = map(int,listbox.curselection())
    listbox.bind('<<ListboxSelect>>',immediately)

    frame2 = tk.Frame(root,pady=10)
    frame2.pack(anchor=tk.S)
    button = tk.Button(frame2,text="予定追加",command=append_list)
    button.pack(side="right")
    root.mainloop()

# カレンダーを作成する関数
def monthcalendar(year,month,day):
    def p_day(day):
        print(day)

    #現状だと7月→8月→8月→…6月と、おかしなことになっている。参照する値を調整すればどうにかなりそう。
    def change_month(year,month):
        if(month==0):
            year-=1
            month=12
        elif month==13:
            year+=1
            month=1
        root.current_year.set(year)
        current_month.text.set(month)
        create_calendar(year,month)
    def create_calendar(year,month):
        "指定した年(year),月(month)のカレンダーウィジェットを作成する"
        # calendarモジュールのインスタンスを作成
        import calendar
        #前に書かれていた要素の削除
        try:
                for key,item in day.items():
                    item.destroy()
        except:
            pass
        cal = calendar.Calendar()
        # 指定した年月のカレンダーをリストで返す
        days = cal.monthdayscalendar(year,month)

        # 日付ボタンを格納する変数をdict型で作成
        day = {}
        # for文を用いて、日付ボタンを生成
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
                        day[i] = tk.Button(frame_calendar,font=("",14),height=2, width=4, relief="flat",text = days[r][c],fg="red")
                        day[i].grid(column=c,row=r)
                    else:
                        day[i] = tk.Button(frame_calendar,font=("",14),height=2, width=4, relief="flat",text = days[r][c])
                        day[i].grid(column=c,row=r)
            except:
                """
                月によっては、i=41まで日付がないため、日付がないiのエラー回避が必要
                """
                break
            
    root=tk.Tk()

    # frame_top部分の作成
    frame_top = tk.Frame()
    frame_top.pack(pady=5)
    previous_month = tk.Label(frame_top, text = "<", font = ("",14))
    previous_month.bind("<1>",change_month(year,month-1))
    previous_month.pack(side = "left", padx = 10)
    current_year = tk.Label(frame_top, text = year, font = ("",18))
    current_year.pack(side = "left")
    current_month = tk.Label(frame_top, text = month, font = ("",18))
    current_month.pack(side = "left")
    next_month = tk.Label(frame_top, text = ">", font = ("",14))
    next_month.bind("<1>",change_month(year,month+1))
    next_month.pack(side = "left", padx = 10)

    # frame_week部分の作成
    frame_week = tk.Frame()
    frame_week.pack()
    button_mon = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "Mon")
    button_mon.grid(column=0,row=0)
    button_tue = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "Tue")
    button_tue.grid(column=1,row=0)
    button_wed = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "Wed")
    button_wed.grid(column=2,row=0)
    button_thu = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "Thu")
    button_thu.grid(column=3,row=0)
    button_fri = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "Fri")
    button_fri.grid(column=4,row=0)
    button_sta = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "Sat", fg = "blue")
    button_sta.grid(column=5,row=0)
    button_san = tk.Label(frame_week,font=("",14),height=2, width=4, relief="flat", text = "San", fg = "red")
    button_san.grid(column=6,row=0)
    
    # frame_calendar部分の作成
    frame_calendar = tk.Frame()
    frame_calendar.pack()

    # 日付部分を作成するメソッドの呼び出し
    create_calendar(year,month)

    root.mainloop()
    

today = datetime.datetime.now()
#mycalender(today.year,today.month,today.day)
monthcalendar(today.year,today.month,today.day)
